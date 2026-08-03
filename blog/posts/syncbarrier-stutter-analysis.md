# SyncBarrier 卡顿问题

## 1. 问题背景

业务代码在子线程调用：

```java
imageView.setImageDrawable(drawable);
```

这属于跨线程访问 View。Android 的 View 体系不是线程安全的，正常情况下只能由创建 View 层级的线程（通常是主线程）修改。

但在 Android 11 中，如果窗口开启了硬件加速，这类调用可能不会立即抛出 `CalledFromWrongThreadException`。错误线程可能继续进入 `ViewRootImpl.scheduleTraversals()`；在并发时序下，有机会重复插入 SyncBarrier 并遗留一个无法删除的屏障，最终阻塞主线程同步消息，造成卡顿或 ANR。

> 没有抛出线程异常不代表允许在子线程更新 UI，也不代表该操作是线程安全的。

## 2. Android 11 的 invalidate 调用入口

`ImageView.setImageDrawable()` 更新 Drawable 后会触发 `invalidate()`。主要调用链为：

```text
ImageView.setImageDrawable()
  → View.invalidate()
  → View.invalidateInternal()
  → mParent.invalidateChild(this, damage)
  → ViewGroup.invalidateChild()
```

`View.invalidateInternal()` 中的关键代码：

```java
final AttachInfo ai = mAttachInfo;
final ViewParent p = mParent;
if (p != null && ai != null && l < r && t < b) {
    final Rect damage = ai.mTmpInvalRect;
    damage.set(l, t, r, b);
    p.invalidateChild(this, damage);
}
```

软硬件加速的传播分支发生在 `ViewGroup.invalidateChild()` 中。

## 3. 硬件加速与非硬件加速分支

Android 11 的关键判断：

```java
public final void invalidateChild(View child, final Rect dirty) {
    final AttachInfo attachInfo = mAttachInfo;
    if (attachInfo != null && attachInfo.mHardwareAccelerated) {
        // HW accelerated fast path
        onDescendantInvalidated(child, child);
        return;
    }

    // 非硬件加速路径：逐级传递 dirty Rect
    ViewParent parent = this;
    if (attachInfo != null) {
        do {
            // 计算 dirty Rect、坐标变换和裁剪等
            parent = parent.invalidateChildInParent(location, dirty);
        } while (parent != null);
    }
}
```

两条路径可以概括为：

```text
ViewGroup.invalidateChild()
  │
  ├─ attachInfo.mHardwareAccelerated == true
  │    → ViewGroup.onDescendantInvalidated()
  │    → 各级 ViewGroup 向父节点传播
  │    → ViewRootImpl.onDescendantInvalidated()
  │
  └─ attachInfo.mHardwareAccelerated == false
       → ViewGroup.invalidateChildInParent()
       → 逐级计算和传递 dirty Rect
       → ViewRootImpl.invalidateChildInParent()
```

### 3.1 硬件加速路径

`ViewGroup.onDescendantInvalidated()` 是忽略 dirty Rect 的硬件加速快速路径。各级 `ViewGroup` 最终通过以下代码传播到 `ViewRootImpl`：

```java
if (mParent != null) {
    mParent.onDescendantInvalidated(this, target);
}
```

Android 11 的 `ViewRootImpl.onDescendantInvalidated()`：

```java
@Override
public void onDescendantInvalidated(
        @NonNull View child, @NonNull View descendant) {
    // TODO: Re-enable after camera is fixed or consider targetSdk checking this
    // checkThread();
    if ((descendant.mPrivateFlags & PFLAG_DRAW_ANIMATION) != 0) {
        mIsAnimating = true;
    }
    invalidate();
}
```

![Android 11 中被注释的 checkThread](https://zhinengzuocang.cn/static/uploads/syncbarrier-android11-checkthread.png)

由于这里没有执行 `checkThread()`，子线程可能继续执行：

```text
ViewRootImpl.invalidate()
  → ViewRootImpl.scheduleTraversals()
  → MessageQueue.postSyncBarrier()
```

### 3.2 非硬件加速路径

非硬件加速时，通过 `invalidateChildInParent()` 逐级计算并传递 dirty Rect，最终进入：

```java
ViewRootImpl.invalidateChildInParent()
```

该方法开头会执行：

```java
@Override
public ViewParent invalidateChildInParent(int[] location, Rect dirty) {
    checkThread();
    // ...
}
```

因此，子线程从这条路径更新 View 时，通常会抛出 `CalledFromWrongThreadException`。

### 3.3 软件 Layer 不等于关闭窗口硬件加速

以下设置：

```java
view.setLayerType(View.LAYER_TYPE_SOFTWARE, null);
```

只是让某个 View 使用软件 Layer，不代表整个 Window 关闭了硬件加速。决定上述两条 invalidate 传播路径的是：

```java
attachInfo.mHardwareAccelerated
```

## 4. SyncBarrier 遗留的形成过程

Android 11 的 `scheduleTraversals()` 关键代码：

```java
void scheduleTraversals() {
    if (!mTraversalScheduled) {
        mTraversalScheduled = true;
        mTraversalBarrier = mHandler.getLooper()
                .getQueue().postSyncBarrier();
        mChoreographer.postCallback(
                Choreographer.CALLBACK_TRAVERSAL,
                mTraversalRunnable, null);
        notifyRendererOfFramePending();
        pokeDrawLockIfNeeded();
    }
}
```

`mTraversalScheduled` 和 `mTraversalBarrier` 按照 View 单线程模型设计，没有用于保护多线程调用的同步机制。若两个错误线程并发进入，可能出现以下时序：

```text
线程 A：读取 mTraversalScheduled == false
线程 B：读取 mTraversalScheduled == false

线程 A：mTraversalScheduled = true
线程 B：mTraversalScheduled = true

线程 A：postSyncBarrier() → token 1
线程 B：postSyncBarrier() → token 2

mTraversalBarrier 最终只能保存其中一个 token
```

随后 Choreographer 收到 Vsync，开始执行 traversal callback。`doTraversal()` 会在 `performTraversals()` 之前删除当前记录的屏障：

```java
void doTraversal() {
    if (mTraversalScheduled) {
        mTraversalScheduled = false;
        mHandler.getLooper().getQueue()
                .removeSyncBarrier(mTraversalBarrier);
        performTraversals();
    }
}
```

第一次 callback 只能删除 `mTraversalBarrier` 当前保存的一个 token，并将 `mTraversalScheduled` 设置为 `false`。另一个 callback 再执行时，由于条件不成立，不会尝试删除另一个屏障。因此可能留下一个失去 token 引用的 SyncBarrier。

## 5. 遗留 SyncBarrier 的影响

MessageQueue 遇到 SyncBarrier 后：

- 屏障之后的同步消息不能被取出执行；
- 异步消息仍然可以越过屏障；
- 大量普通 Handler 消息可能长期得不到处理；
- 应用可能表现为点击无响应、页面不跳转、生命周期或业务任务不执行，最终出现 ANR。

因此不能简单描述成“主线程不再执行任何 Message”。更准确的说法是：

> 遗留的 SyncBarrier 会长期阻塞其后的同步消息，而异步消息仍可能被执行。

## 6. 其他线程安全风险

即使没有触发重复 SyncBarrier，子线程调用 `setImageDrawable()` 仍然不安全：

### 6.1 View 状态位竞态

`View.invalidateInternal()` 会修改 `mPrivateFlags`：

```java
mPrivateFlags |= PFLAG_DIRTY;
```

这是读—修改—写操作。多个线程并发修改时，可能产生逻辑上的更新丢失或状态不一致。

### 6.2 dirty Rect 并发访问

`ViewRootImpl.invalidate()` 会修改：

```java
mDirty.set(0, 0, mWidth, mHeight);
```

错误线程可能与 UI 线程的 traversal/draw 流程并发访问同一个 `Rect`。`Rect` 没有相应的线程同步保证，可能造成脏区状态不一致。

这里不应描述为“主线程的 RenderThread 直接读取 `mDirty`”。主线程和 RenderThread 是不同线程，`mDirty` 主要参与 UI 线程的 ViewRoot traversal/draw 流程。

### 6.3 ImageView 和 Drawable 状态竞态

`setImageDrawable()` 不仅触发 invalidate，还会更新 `ImageView` 持有的 Drawable、Drawable callback、尺寸及相关状态。这些对象同样按照 View 单线程模型使用，可能与主线程测量、布局或绘制并发。

## 7. checkThread 的版本历史

| 时间/版本 | `onDescendantInvalidated()` 中的线程检查情况 |
|---|---|
| Android 7.1 及以前 | 还没有这条 `onDescendantInvalidated()` 快速失效链路 |
| Android 8.0 | 引入该方法；最初就没有 `checkThread()` |
| Android 9 | 仍没有 `checkThread()` |
| 2019-03-29，Android 10 开发期 | 提交 `78704efc`，补上 `checkThread()` |
| 2019-04-01，Android 10 开发期 | 提交 `52efe835`，因 Camera 问题临时注释 |
| Android 10～14 正式版 | 保持注释状态 |
| 2024-04-11，Android 15 开发期 | 提交 `c683d2a`，通过 feature flag 加回 |
| Android 15 正式版 | 存在 `checkThread()`，是否执行受 `enable_invalidate_check_thread` flag 控制 |

Android 15 的实现为：

```java
@Override
public void onDescendantInvalidated(
        @NonNull View child, @NonNull View descendant) {
    if (sToolkitEnableInvalidateCheckThreadFlagValue) {
        checkThread();
    }
    if ((descendant.mPrivateFlags & PFLAG_DRAW_ANIMATION) != 0) {
        mIsAnimating = true;
    }
    invalidate();
}
```

![Android 15 通过 flag 恢复 checkThread](https://zhinengzuocang.cn/static/uploads/syncbarrier-android15-checkthread.jpg)

需要区分两个概念：

- Android 8、9：方法中从未加入过 `checkThread()`，不能称为“被注释”；
- Android 10 开发期：先短暂加入，随后明确因 Camera 问题注释，并一直保留到 Android 14。

## 8. 最终结论

1. Android 11 硬件加速窗口通过 `onDescendantInvalidated()` 传播 invalidate，该入口没有执行 `checkThread()`，所以某些子线程 UI 操作不会立即抛出线程异常。
2. 非硬件加速路径最终进入 `ViewRootImpl.invalidateChildInParent()`，其中存在 `checkThread()`，通常会直接抛出异常。
3. 没有线程异常不代表子线程操作 View 是安全或受支持的。
4. 多线程并发进入 `scheduleTraversals()` 时，可能重复插入 SyncBarrier，而只保存一个 token，最终遗留屏障并长期阻塞同步消息。
5. Android 15 通过 feature flag 在 `onDescendantInvalidated()` 中重新加入线程检查。
6. 业务修复应保证所有 View 和 Drawable 状态更新切换到主线程；不要依赖 Android 11 中缺失的线程检查。

建议写法：

```java
imageView.post(() -> imageView.setImageDrawable(drawable));
```

或者在协程中明确切换到主线程：

```kotlin
withContext(Dispatchers.Main) {
    imageView.setImageDrawable(drawable)
}
```

## 9. AOSP 参考

- [Android 11 View.java](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-11.0.0_r1/core/java/android/view/View.java)
- [Android 11 ViewGroup.java](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-11.0.0_r1/core/java/android/view/ViewGroup.java)
- [Android 11 ViewRootImpl.java](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-11.0.0_r1/core/java/android/view/ViewRootImpl.java)
- [Android 8 引入 onDescendantInvalidated](https://android.googlesource.com/platform/frameworks/base/+/9de95db)
- [Android 10 开发期补上 checkThread](https://android.googlesource.com/platform/frameworks/base/+/78704efc3a0f18fb9518bd3cca8e04e1e6d38882)
- [Android 10 开发期临时关闭 checkThread](https://android.googlesource.com/platform/frameworks/base/+/52efe835f19187c26f201af645e450af073261fe)
- [Android 15 开发期通过 flag 加回 checkThread](https://android.googlesource.com/platform/frameworks/base/+/c683d2aea4e10a6b91c00160c99da12b1286067e)
- [enable_invalidate_check_thread flag 定义](https://android.googlesource.com/platform/frameworks/base/+/897c0e136b4d99b8fd393683688b826340f43103/core/java/android/view/flags/view_flags.aconfig)
