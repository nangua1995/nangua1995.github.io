# 双指同时点击为何会弹出两个确认框

- **复现**：应用商店 → 「我的」页 → 一只手两根手指几乎同时按下两行不同的「卸载」按钮
- **现象**：屏幕上同时出现两个「确认卸载」弹窗
- 本文仅保留经脱敏的机制分析；原始视频、日志、设备及应用标识均不公开。

---

## 一、结论先行

**根因在应用自身的 Dialog 管理。**

- 弹窗由一个预装应用自身创建；包名、路径、进程号和内部实现标识均已脱敏。
- 根因：Android `ViewGroup.splitMotionEvents=true` 默认开启，导致两指落在两行不同的「卸载」按钮时，两个 itemView 各触发一次 `OnClickListener.onClick`，各自 `DialogFragment.show(fm, "UninstallDialog")`，而应用的 Dialog 管理器未按 tag 去重。

---

## 二、日志证据链

### 2.1 两个同 tag DialogFragment 相隔 128 ms 上屏

```
<time>  AppDialog onAttach:true                              ← 弹窗①
<time>  AppDialogManager: register application
<time>  moveTo CREATED  tag=UninstallDialog                  ← 弹窗①
<time>  moveTo RESUMED                                       ← 弹窗① 可见

<time + 128ms>  AppDialog onAttach:true                      ← 弹窗②
<time + 128ms>  AppDialogManager: register application
<time + 128ms>  moveTo CREATED  tag=UninstallDialog          ← 弹窗②，同 tag
<time + 128ms>  moveTo RESUMED                               ← 弹窗② 可见
```

两个 `UninstallDialog` 同处 `RESUMED` 状态，且都在同一个主线程、同一个 `FragmentManager`、同一个 tag。应用的 Dialog 管理器只按应用维度注册，不做 tag 级互斥。

## 三、核心机制：`splitMotionEvents`（重点）

> **这一节是理解为什么会「触发两次」的关键。** 双弹窗的根本触发点不在业务代码，而在 Android 触摸分派模型。

### 3.1 多指事件序列

两指同一屏时，InputDispatcher 派下来的原始事件：

```
finger1 落下 → ACTION_DOWN         (pointerId=0)
finger2 落下 → ACTION_POINTER_DOWN (pointerId=1)
finger1 抬起 → ACTION_POINTER_UP   (pointerId=0)
finger2 抬起 → ACTION_UP           (pointerId=1)
```

### 3.2 `ViewGroup.dispatchTouchEvent` 的规则

从 API 11（Android 3.0）起，`ViewGroup#setMotionEventSplittingEnabled` **默认为 true**。规则：

| 事件 | 行为 |
|------|------|
| `ACTION_DOWN` | 做命中测试，把 pointer 交给命中的子 View，记录到 `mFirstTouchTarget` 链表 |
| `ACTION_POINTER_DOWN` | **再做一次命中测试**。若命中另一个子 View，把新 pointer 加进另一条 target；对那个子 View 而言，事件被 `MotionEvent.split()` **改写为 `ACTION_DOWN`**（只含它这条 pointer），让它以为自己刚被首次按下 |
| `ACTION_POINTER_UP` / `ACTION_UP` | 各自派回自己的 target，target 独立完成 DOWN→UP，各触发一次 `performClick()` |

**关键结论**：两条 target 独立走完完整手势，`OnClickListener.onClick(v)` 被调**两次**，各来自不同的 itemView。

### 3.3 视觉化对照

```
                  RecyclerView (splitMotionEvents=true, 默认)
                  ┌──────────────────────────────────────┐
       finger1 →  │  ┌── item A ─────────┐               │
                  │  │  ...  [卸载按钮] ← onClick 弹窗①   │
                  │  └──────────────────┘                │
                  │                                       │
       finger2 →  │  ┌── item B ─────────┐               │
                  │  │  ...  [卸载按钮] ← onClick 弹窗②   │
                  │  └──────────────────┘                │
                  └──────────────────────────────────────┘

     两个 onClick 都在同一个 UI 线程顺序执行，View 层看到的却是两条独立手势。
```

### 3.4 「不是双指是两次单点」这个误解

- **物理上是不是同时不重要**。两指差 0 ms 到 200 ms，走的是同一条 `splitMotionEvents` 分派路径，结果都一样。日志里的 128 ms 只是人手落地的物理微差，不是「一根一根按」。
- **两指落在同一个 Button 上不会重复**。同一个 View 的第二个 pointer 只会加入已有 target，`performClick()` 仅在 primary pointer 抬起时执行一次。所以单测同一个按钮怎么按都只弹一次；换到列表里跨行就中招。

### 3.5 一句话记忆

> `splitMotionEvents=true` = **允许一个 ViewGroup 同时把不同手指派给不同子 View**。列表 / 按钮组 / Toolbar 这类容器只要没关，就都存在「多指并发触发不同点击」的风险。

---

## 四、因果链

1. 用户两指落在**两行不同**的「卸载」按钮。
2. `RecyclerView`（默认 `splitMotionEvents=true`）把两个 pointer 分派给两个 itemView。
3. 两个 itemView 的 `OnClickListener.onClick` 各执行一次。
4. 各自 `DialogFragment.show(fm, "UninstallDialog")` 但**不查 tag 是否已存在**。
5. 应用的 Dialog 管理器只按应用维度注册，不做 tag 级互斥。
6. 两个 `UninstallDialog` 同时上屏。

---

## 五、修复方向

改动必须落在 **目标应用自身**。

按有效性和成本排序：

### 5.1 [根治] 关掉列表的 splitMotionEvents

给「我的」页里承载卸载按钮的列表根容器（`RecyclerView` / `ListView` / `LinearLayout` 都行）加：

```xml
<androidx.recyclerview.widget.RecyclerView
    android:id="@+id/my_app_list"
    android:splitMotionEvents="false"
    ... />
```

或者代码里：

```java
recyclerView.setMotionEventSplittingEnabled(false);
```

效果：任意时刻只有一个 pointer 能在这个容器里点子 View，从触摸源头消掉双击。**顺手挡住同类的其他多指并发 bug**（打开、更新、详情、评分等按钮）。

### 5.2 [兜底] 弹窗 tag 去重

`show()` 前查一下：

```java
if (fragmentManager.findFragmentByTag("UninstallDialog") != null) {
    return;  // 已有相同 dialog，忽略后来者
}
uninstallDialog.show(fragmentManager, "UninstallDialog");
```

或者把这条逻辑收敛到应用的 Dialog 管理器，按 `(applicationId, tag)` 二元组做互斥，一次改动全应用生效。

### 5.3 [兜底] 按钮点击防抖

```java
uninstallButton.setOnClickListener(v -> {
    v.setEnabled(false);           // 立即禁用，防止并发点击
    v.postDelayed(() -> v.setEnabled(true), 500);
    showUninstallDialog(pkg);
});
```

或用 `SystemClock.elapsedRealtime()` 判两次点击门限（≥ 500 ms）。

### 5.4 三条的组合关系

- **5.1** 从触摸层拦，最省事、副作用最大范围可控；
- **5.2** 从 Dialog 层拦，专治「同弹窗被多次 show」；
- **5.3** 从 View 事件层拦，专治「按钮被快速多次点」。

**建议 5.1 + 5.2 都做**：5.1 干掉同一列表内的并发点击，5.2 兜底跨来源（例如通知栏、遥控器）触发的重复 show。5.3 可选。

### 5.5 无法直接修改应用时的兜底

若只能维护目标应用的补丁分支：

- 在 Dialog 管理器注册逻辑里加：「若同 tag 已注册，直接 return，不 attach 新 fragment」。
- 或者在打包脚本里对 `activity_my_page.xml` 之类布局文件后处理，把根容器塞一个 `android:splitMotionEvents="false"`。

---

## 六、附：验证要点

改动后回归时至少验证：

1. 同一列表两行按钮双指同点 → 只弹一个卸载框（针对 5.1 / 5.2）
2. 同一行按钮双指同点 → 只弹一个（本来就应该，回归即可）
3. 快速双击同一「卸载」按钮 → 只弹一个（针对 5.3）
4. 单指正常单点 → 行为不变
5. 列表里其他按钮（打开、更新）双指同点 → 也不再并发触发（5.1 的顺带收益）
6. 通知栏 / 语音助手 / 遥控器 触发的卸载入口 → tag 去重仍然生效（5.2 的作用范围）
