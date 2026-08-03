# 一次 Android 黑屏问题排查：从应用返回到 InputDispatcher 崩溃

> 本文来自一次车载 Android 系统问题排查。项目名称、应用名称、窗口名称、设备信息、人员信息、内部地址、时间与坐标等均已脱敏或泛化。

## 现象：一次普通返回，为何会黑屏十秒？

问题最初看起来很像应用缺陷：用户从底部快捷栏打开一个系统面板，点击返回后，屏幕突然变黑，约十秒后又回到桌面。

如果只盯着前台应用，很容易把排查方向放在 Activity 生命周期、窗口动画或 Surface 提交上。但日志显示，黑屏期间并不是某个应用窗口没有绘制，而是 Android Framework 发生了软重启。`zygote` 仍然存活，`system_server` 的进程号却发生了变化。

这解释了两个关键现象：

- 屏幕会短暂变黑，因为系统服务和系统界面需要重新拉起；
- 十秒左右可以自行恢复，因为这不是整机重启。

## 第一步：先给“黑屏”定性

DropBox 中的 native crash 记录把范围迅速缩小到了输入系统。脱敏后的核心信息如下：

```text
pid: <system_server_pid>, tid: <input_thread_tid>
name: InputDispatcher  >>> system_server <<<
signal 6 (SIGABRT)

Abort message:
addPointers - overlap with incoming pointers ...
dispatchMode=OUTSIDE
```

调用栈集中在：

```text
InputDispatcher::addPointerWindowTargetLocked(...)
InputDispatcher::findTouchedWindowTargetsLocked(...)
InputDispatcher::dispatchMotionLocked(...)
```

崩溃前还有一条更直接的线索：

```text
DispatchMode doesn't match!
existing mode=OUTSIDE, new mode=HOVER_EXIT
```

至此可以得出第一个结论：所谓“返回后黑屏”只是表象，真正的问题是 `InputDispatcher` 遇到不一致的输入目标状态后主动触发了 fatal check，导致 `system_server` 退出。

为了排除偶发内存破坏，我们又对另一份独立现场做了交叉检查。两次崩溃的线程、abort message 和关键调用栈一致，说明它们来自同一条稳定的逻辑路径。

## 第二步：理解 OUTSIDE 与 HOVER_EXIT 为什么会相遇

Android 会为一次输入事件计算一个或多个 `InputTarget`。在这个案例中，底部快捷栏窗口具备 `WATCH_OUTSIDE_TOUCH` 能力，因此用户点击其他窗口时，它也可能收到一个 `OUTSIDE` 事件。

问题发生前，这个快捷栏窗口还保留着一个鼠标 hover pointer。当同一设备随后产生一次落在快捷栏之外的 `DOWN` 时，Dispatcher 依次做了两件事：

1. 因为窗口监听外部触摸，为它建立 `OUTSIDE` target，并加入 pointer 0；
2. 因为旧 hover 状态需要结束，又为同一窗口计算出 `HOVER_EXIT` target，同样携带 pointer 0。

理想情况下，这两种 dispatch mode 应当使用两个独立 target。但相关逻辑只处理了一种顺序：已有 target 是 `HOVER_EXIT` 时，强制新建 target；反过来，已有 target 是 `OUTSIDE`、新 target 才是 `HOVER_EXIT` 时，却继续复用已有对象。

问题逻辑可以简化为：

```cpp
// 只覆盖了一个方向
if (it != inputTargets.end() &&
    it->dispatchMode == DispatchMode::HOVER_EXIT) {
    it = inputTargets.end();
}
```

于是，新来的 pointer 0 被再次添加到已有的 `OUTSIDE` target。集合重叠检查失败，`LOG(FATAL)` 最终把整个 `system_server` 打掉。

完整链路如下：

```text
快捷栏窗口保留 mouse hover 状态
        ↓
同一注入设备在其他窗口产生 DOWN
        ↓
WATCH_OUTSIDE_TOUCH 创建 OUTSIDE target {pointer 0}
        ↓
清理旧 hover 又创建 HOVER_EXIT target {pointer 0}
        ↓
两个 mode 被错误合并到同一个 target
        ↓
addPointers 检测到 pointer 重叠并触发 FATAL
        ↓
system_server 退出，Framework 软重启，屏幕短暂变黑
```

## 第三步：hover 到底从哪里来？

最初只有崩溃现场，没有 hover 的产生记录。当时存在几种合理假设：触摸驱动释放 slot 不完整、InputReader 把触摸误判为 hover、Dispatcher 残留旧状态，或者某个进程主动注入了鼠标事件。

这类问题不能依靠猜测收敛。我们在输入注入入口、hover target 计算和 `TouchState` 更新位置增加了仅用于定位的结构化日志，记录以下字段：

- 调用进程和权限身份；
- action、source、deviceId 与 pointerId；
- 是否为注入事件；
- hover 写入和清理的目标窗口；
- target 已有 mode 与新 mode。

第二次现场给出了完整证据链。脱敏后的日志如下：

```text
[inject-hover-caller]
action=ACTION_HOVER_MOVE
caller=<screen_mirroring_service>
source=SOURCE_MOUSE
deviceId=<injected_device>
isInjected=true

[hover-source]
window=<bottom_shortcut_window>
pointerId=0

[target-mode-mismatch]
existingMode=OUTSIDE
newMode=HOVER_EXIT
```

调用进程最终对应到开发环境中的屏幕投送工具。PC 鼠标在镜像画面上移动时，工具通过 Android 输入注入接口发送标准的 `ACTION_HOVER_MOVE`；光标经过屏幕底部区域后，快捷栏窗口获得了 hover 状态。稍后，业务页面关闭流程又向下层窗口补发了一次合成点击。两类事件使用了相同的注入设备标识和 pointerId，于是满足了前述冲突条件。

这里要特别区分“触发器”和“根因”：

- 屏幕投送工具制造了稳定的 hover 前置状态，是触发器；
- 页面中的合成点击补齐了触发条件；
- Dispatcher 无法安全处理同一窗口同时需要 `OUTSIDE` 与 `HOVER_EXIT` 的合法组合，才是导致系统进程崩溃的根因。

简单禁用投送工具可以降低复现概率，却不能保证其他鼠标、触控板或输入注入服务不会触发同类问题。

## 修复：让 HOVER_EXIT 的隔离逻辑保持对称

最小修复是补全现有分支：无论已有 target 是 `HOVER_EXIT`，还是新加入的 mode 是 `HOVER_EXIT`，都不要复用同一个 target。

```cpp
if (it != inputTargets.end() &&
    (it->dispatchMode == DispatchMode::HOVER_EXIT ||
     dispatchMode == DispatchMode::HOVER_EXIT)) {
    it = inputTargets.end();
}
```

这个修改没有改变事件命中规则，也没有吞掉任何输入，只是确保不同 dispatch mode 使用独立的 `InputTarget`，与原有设计意图一致。

可以按以下层次处理：

1. **框架层根治**：补全 target 隔离条件，避免状态组合演变成进程级 fatal；
2. **工具侧规避**：使用 scrcpy 投屏时增加 `--no-mouse-hover`，禁止转发“没有按键动作的鼠标移动”事件，从源头避免这条 hover 触发路径；
3. **应用侧收敛**：检查合成点击和可触摸区域是否确有必要，避免窗口动画期间扩大输入竞争面。

后两项是降低触发概率的防御措施，不能替代框架层修复。

scrcpy 可以直接这样启动：

```bash
scrcpy --no-mouse-hover
```

Windows 快捷方式本质上也是执行命令，因此可以直接给 `scrcpy.exe` 追加启动参数。具体做法如下：

1. 找到投屏软件的 Windows 快捷方式，右键选择“属性”；
2. 打开“快捷方式”页签，找到“目标”输入框；
3. 在原有目标路径末尾添加一个空格，再追加 `--no-mouse-hover`；
4. 保存设置，关闭并重新启动投屏软件。

例如，修改前为：

```text
C:\tools\scrcpy\scrcpy.exe
```

修改后为：

```text
C:\tools\scrcpy\scrcpy.exe --no-mouse-hover
```

如果可执行文件路径包含空格，应保留路径两侧的引号，并把参数写在引号外：

```text
"C:\Program Files\scrcpy\scrcpy.exe" --no-mouse-hover
```

该参数只阻止 mouse hover（没有点击时的鼠标移动）转发，正常点击控制仍可保留。scrcpy 当前命令行帮助中也对这一选项做了相同定义；较老版本如果提示参数未知，应升级到支持该选项的版本，或根据实际使用场景选择 `--mouse=uhid` 等输入模式。参数能力可在 [scrcpy 官方命令行源码](https://github.com/Genymobile/scrcpy/blob/master/app/src/cli.c) 中核对。

## 如何验证修复

复现不应继续依赖人工“碰运气”。可以构造一个最小输入序列：

1. 向底部窗口注入 `HOVER_ENTER` 或 `HOVER_MOVE`，建立 hover 状态；
2. 短暂等待后，以同一注入设备在窗口外注入 `DOWN`；
3. 检查 `system_server` 是否存活、进程号是否变化，并过滤 mismatch、pointer overlap 与 native crash；
4. 如果系统未崩溃，补发 `UP`，保证测试自身不留下脏状态。

修复后的成功标准至少包括：

- `system_server` 不退出，界面无黑屏；
- 不再出现 `DispatchMode doesn't match` 和 `addPointers overlap`；
- `OUTSIDE` 与 `HOVER_EXIT` 都能按预期分发；
- 正常鼠标 hover enter/move/exit 不受影响；
- 普通触摸、外部触摸监听、多指输入、窗口切换和取消事件通过回归。

需要如实说明的是：现有归档材料包含修复前的两次一致崩溃、专项定位日志、最小复现程序和修复方案，但没有包含一份明确的修复后回归结果。因此，本文把以上内容称为“验证方案”，不把它包装成已经完成的验证结论。

## 这次排查带来的几个经验

### 1. “黑屏”不是根因描述

先区分应用无画面、Surface 异常、SystemUI 重启、`system_server` 重启和整机重启，后续排查空间会立刻缩小。进程号变化、DropBox、tombstone 和启动时序通常比肉眼现象更可靠。

### 2. Fatal 前的 error 往往比崩溃栈更接近逻辑错误

调用栈只能说明 pointer 在哪里重叠；紧邻崩溃的 mode mismatch 日志则解释了为什么会重叠。排查时应围绕 fatal 前后建立事件时间线，而不是只看最后一帧。

### 3. 用“状态组合”设计复现

这个问题的关键不是点击某个具体应用，而是同时满足三个条件：旧 hover、`WATCH_OUTSIDE_TOUCH`、同设备的新 `DOWN`。把业务操作翻译成状态条件后，才能得到稳定、可自动化的最小复现。

### 4. 诊断日志要能推翻假设

早期怀疑底层触摸释放异常是合理的，但专项日志显示 hover 来自注入进程，就应及时放弃旧假设。好的诊断日志不仅支持某个猜测，还应能区分 InputReader 生成、Dispatcher 残留和外部注入等竞争解释。

### 5. 不要把触发工具当成根因

一个开发工具触发了边界条件，不代表禁用工具就完成了修复。系统级组件面对可接受的输入状态时，不应因为内部 target 组织方式而让核心进程崩溃。

## 结语

这次问题从“某页面返回后黑屏”一路追到了输入分发器内部：一个残留 hover 与一次外部触摸通知相遇，又撞上了不对称的 target 隔离逻辑。真正有效的排查路径，是先用系统证据重新定义现象，再用事件时间线还原状态，最后用最小输入序列验证代码级假设。

对于 Android 系统问题，界面往往只是最后倒下的那块多米诺骨牌。越早找到第一块，越少会在错误的模块里消耗时间。
