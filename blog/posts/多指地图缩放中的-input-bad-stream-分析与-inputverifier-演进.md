# 多指地图缩放中的 Input Bad Stream 分析与 InputVerifier 演进

## 一、问题现象

在地图页面进行双指缩小时，偶发出现如下错误：

```text
Bad stream: Received ACTION_UP but no pointers are currently down
```

表现为地图缩放中断，后续触摸事件无法正常继续分发。问题发生在真实双指操作过程中，并非单指操作。

压测过程中还出现过另一类日志：

```text
There are currently 2 touching pointers, but the incoming POINTER_DOWN event has 2
```

这表示当前输入序列重复发送了 `POINTER_DOWN`。它与“收到没有对应按下状态的 `ACTION_UP`”属于不同问题，不能混为一谈。

## 二、事件处理链路

```text
驱动
  ↓
InputReader：读取并组装原始事件
  ↓
InputDispatcher：选择窗口并发送事件
  ↓
OutboundQueue / WaitQueue
  ↓
InputChannel socket
  ↓
应用主线程 Looper
  ↓
应用消费事件并返回处理结果
```

`InputVerifier` 位于 framework 向应用发布事件的路径上，用于检查触摸流的状态一致性，例如 pointer 是否重复按下、抬起是否有对应按下、连续事件中的 pointer 集合是否一致等。

## 三、日志分析

### 3.1 原始问题中的异常事件

脱敏后的典型日志如下：

```text
XXX InputTransport: Bad stream: XXX
    Received ACTION_UP but no pointers are currently down for device DeviceId(XXX)
```

这条日志的含义是：InputTransport 在校验发送给目标连接的事件流时，发现当前 verifier 中没有处于按下状态的 pointer，但收到了 `ACTION_UP`。它描述的是“发送流的状态不一致”，并不直接说明事件一定由驱动错误生成。

分析这条日志时，需要同时查看异常前后的事件序列：

```text
... ACTION_DOWN
... POINTER_DOWN
... MOVE
... WOULD_BLOCK / outbound retry
... ACTION_UP
```

如果 `ACTION_UP` 之前的 `DOWN` 或 `POINTER_DOWN` 没有成功发送，或者 verifier 已经因失败重试提前更新状态，就可能出现 framework 侧认为“当前没有 pointer 按下”的情况。

### 3.2 `UnwantedInteractionBlocker` 日志

脱敏后的相关日志形式为：

```text
XXX UnwantedInteractionBlocker: enqueueOutboundMotionLocked: tag=XXX
```

该日志说明运动事件进入了 outbound 处理路径，通常需要和以下信息一起看：

- 事件的 action 和 pointer 数量；
- 事件序号或 eventId；
- 目标窗口/连接是否仍然有效；
- `sendMessage()` 的返回值；
- 是否随后出现 outbound retry、`WOULD_BLOCK` 或 `ACTION_CANCEL`。

单独出现 `enqueueOutboundMotionLocked` 不能判断事件异常，也不能证明驱动重复上报。只有当它和发送失败、队列重试以及 verifier 状态异常在同一时间窗口内出现时，才支持“应用消费不及时导致发送路径积压”的判断。

### 3.3 `WOULD_BLOCK` 日志

脱敏后可按如下形式整理：

```text
XXX InputTransport: sendMessage failed, status=-2147483639 (WOULD_BLOCK)
XXX InputDispatcher: retry outbound event, seq=XXX, eventId=XXX
```

`WOULD_BLOCK` 表示非阻塞 socket 当前暂时不可写。它通常与应用主线程未及时读取 InputChannel、发送缓冲区积压有关。该错误是暂时性的，框架会保留事件并在后续重新尝试发送。

重点不是单独统计 `WOULD_BLOCK`，而是确认：

1. 发送失败时 verifier 是否已经更新；
2. 同一事件重试成功时 verifier 是否再次更新；
3. 重试期间是否插入了取消、抬起或新的多指事件。

### 3.4 驱动、Reader 与 Framework 时间点

日志中的时间戳可能来自不同层级，不能直接按打印顺序判断事件产生顺序。建议对同一事件建立如下记录：

```text
driver_time=XXX
reader_time=XXX
dispatcher_enqueue_time=XXX
send_time=XXX
app_receive_time=XXX
seq=XXX eventId=XXX action=XXX pointerCount=XXX
```

如果 `driver_time` 中存在对应 `UP`，说明 framework 至少不是该 `UP` 的唯一来源；如果驱动没有该事件，而 Reader 或 Dispatcher 出现，则应进一步检查 Reader 转换、取消补发和重试逻辑。

## 四、原因分析

### 4.1 应用主线程卡顿是重要触发条件

地图缩放期间，应用主线程可能同时执行地图引擎计算、布局、绘制或其他耗时任务，导致应用不能及时从 InputChannel 读取事件。

主线程卡顿不会凭空生成一个 `ACTION_UP`，但会导致：

- 事件消费延迟，应用侧 pointer 状态更新滞后；
- framework 侧发送队列和 socket 缓冲区积压；
- 非阻塞发送返回暂时不可写，后续进入重试；
- framework、驱动和应用日志中的时间点出现偏移；
- 应用恢复处理时，看到的事件状态可能已经与 framework 当前状态不同。

因此，主线程阻塞更适合被定义为异常输入流的触发和放大条件，而不是唯一事件来源。

### 4.2 `WOULD_BLOCK` 与重试

错误码 `-2147483639` 对应 `WOULD_BLOCK`，表示非阻塞发送暂时无法继续写入，通常意味着 socket 发送缓冲区当前不可写。它不等于事件已经丢失，也不能单独证明驱动产生了错误事件。

如果发送失败后从 `OutboundQueue` 重试，而 verifier 在发送成功前就更新状态，则同一个逻辑事件可能在失败尝试和成功重试中重复推进 verifier 状态，导致 verifier 看到的状态与真实发送流不一致。

### 4.3 `UnwantedInteractionBlocker` 的含义

`UnwantedInteractionBlocker: enqueueOutboundMotionLocked` 表明运动事件进入了 outbound 相关处理路径。该日志本身不能证明事件异常，也不能直接证明事件来自驱动重复上报。需要结合事件序号、action、pointer 数量和发送返回值进行判断。

### 4.4 是否为驱动多报了一个 `UP`

目前不能仅凭 framework 的 Bad stream 日志认定驱动多上报了 `UP`。应按同一事件序号或时间窗口对齐：

| 层级 | 关键数据 |
| --- | --- |
| 驱动 | 原始 type/code/value、硬件时间戳 |
| InputReader | 读取时间、转换后的 action、pointer 状态 |
| Dispatcher | 入队、发送、重试、取消时间 |
| InputChannel | `sendMessage()` 返回值及错误码 |
| 应用 | 收到事件时间、主线程开始/结束处理时间 |

如果原始驱动事件中不存在对应 `UP`，但 Reader 或 Dispatcher 之后出现，应继续检查 framework 的取消、补发和重试逻辑；如果驱动原始记录已经包含该事件，则不能归因于 framework 重复生成。

## 五、修复方案

### 5.1 Google InputVerifier 源码问题分析（截至 2024-09-23）

在 Google upstream 截至 2024-09-23 的 InputTransport/InputPublisher 实现中，motion event 的发布路径存在一个时序问题：事件在调用 `sendMessage()` 之前就执行了 InputVerifier 校验并推进内部 pointer 状态。

简化后的旧流程如下：

```text
InputPublisher::publishMotionEvent()
  → InputVerifier::processMovement()
  → InputChannel::sendMessage()
```

正常发送时该顺序没有明显问题。但当应用主线程处理不及时、socket 缓冲区暂时不可写时，`sendMessage()` 可能返回 `WOULD_BLOCK`。此时事件并没有真正发送到应用侧，verifier 却已经记录了该事件的状态。

随后 Dispatcher 从 outbound queue 重试同一个事件，又会重新经过发布路径。如果 verifier 再次处理该事件，就可能出现以下不一致：

- `DOWN` 或 `POINTER_DOWN` 被重复计入；
- verifier 中记录的 active pointer 数量与实际已发送事件不一致；
- 后续 `UP` 被判断为“没有对应按下状态”；
- 合法的重试被误报为 `Bad stream`。

因此，截至该时间点的源码实现存在“发送结果”和“verifier 状态更新”不同步的问题。它不意味着每次 `WOULD_BLOCK` 都会触发 Bad stream，也不意味着必然导致 system_server 重启，但在多指事件密集、应用主线程卡顿和发送重试同时出现时，会显著放大异常概率。

该问题的关键是：InputVerifier 应验证最终成功发布给应用的事件，而不是验证每一次可能失败的发送尝试。

### 5.2 调整 verifier 更新时机

将处理流程调整为：

```text
构造事件
  → 调用 sendMessage()
  → 发送成功
  → 更新 InputVerifier 状态
```

发送因 `WOULD_BLOCK` 失败时，不推进 verifier 状态；从 outbound 队列重试并真正发送成功后，再更新状态。这样可以避免同一逻辑事件因发送重试被 verifier 重复处理。

### 5.3 增强诊断信息

建议记录以下信息：

- 事件序号、eventId、action、pointer 数量；
- 驱动、Reader、Dispatcher 和应用侧时间点；
- `sendMessage()` 返回值及 `WOULD_BLOCK` 次数；
- OutboundQueue、WaitQueue 的入队、出队和重试；
- verifier 失败时的 pointer 状态摘要。

日志应避免记录设备序列号、用户坐标、应用包名和内部路径等敏感信息。

## 六、InputVerifier 为什么会被引入

InputVerifier 的核心目的不是提升发送性能，而是在事件发给应用之前尽早发现不一致的触摸流，避免错误状态继续传播，典型检查包括：

- 重复 `DOWN`；
- 没有对应 `DOWN` 的 `UP`；
- `MOVE` 时 pointer 集合发生非法变化；
- `POINTER_DOWN` / `POINTER_UP` 状态错误；
- 多指触摸状态不一致。

早期实现发现异常后会直接报告严重错误。随着 Android 版本演进，校验范围、灰度开关、可观测性和异常恢复能力逐步增强，以降低异常输入流对系统稳定性的影响。

## 七、Google upstream 演进概览

| Android 阶段 | 提交 | 主要变化 |
| --- | --- | --- |
| Android 14 开发阶段，2023-02-22 | `92c8fd5ad1` / `f06b672b3e` | 首次引入 touch stream verifier，检查发往 InputChannel 的触摸流一致性 |
| Android 14，2023-06-14 | `5c02a71995` | 将 InputVerifier 迁移到 Rust |
| Android 14，2023-06-28 | `1160ecdfa2` | 增加 hover enter/move/exit 校验 |
| Android 14，2023-07-18 | `227a7f8fd9` | 将 flags 纳入事件一致性检查 |
| Android 14，2023-09-19 | `2d151ac3e2` | 限制 verifier 只检查 pointer 类型输入 |
| Android 15 前后，2023-08-23 | `96818960a7` | 增加事件校验 feature flag |
| Android 15，2024-10-16 | `72090cbd1c` | 将 publish 阶段的 verifier 更新移动到 `sendMessage()` 成功之后，避免 `WOULD_BLOCK` 重试导致重复更新 |
| Android 15/16，2025-01-17 | `fb477b1399`、`1e37d1e8bd`、`26640c9988` | 增加 button press/release 状态校验，期间经历测试问题和后续调整 |
| Android 16，2025-04-04 | `2042f272e8` | 增加 injection verifier 的 dumpsys input 输出，提升问题定位能力 |
| Android 17，2025-10-02 | `a2548f859d` | 增加 downTime 合法性校验 |
| Android 17，2025-10-16 | `bf29210a32` | 将 downTime 校验拆为独立 feature flag，便于灰度启用 |
| Android 17，2025-12-10 | `36fda36aea` | 支持 absolute mode captured touchpad 事件流校验 |
| Android 17，2026-02-03 | `f1179754c5` | 优化 display 移除/折叠场景下 verifier 的生命周期处理 |
| Android 17，2026-03-04 | `ffe2eae576` | 使用 `unique_ptr` 管理 InputPublisher 中的 InputChannel，明确对象所有权 |

其中，`72090cbd1c` 与本问题关系最直接：它修正了发送失败重试路径中的 verifier 更新时机。

## 八、验证方法

建议对原始版本和修复版本执行相同次数的双指缩放，并分别测试正常负载、应用主线程人为阻塞两种场景，统计：

- Bad stream 次数；
- `WOULD_BLOCK` 次数；
- outbound 重试次数；
- 重复 `POINTER_DOWN` 和异常 `ACTION_UP` 次数；
- `ACTION_CANCEL` 次数；
- 应用主线程 dispatch 延迟和丢帧情况。

最终需要确认三点：

1. 驱动原始事件与 framework 事件可以按序号或时间准确对应；
2. `WOULD_BLOCK` 重试不会重复推进 verifier 状态；
3. 修复后 Bad stream 下降，同时压测脚本自身不再生成非法 pointer 序列。

## 九、结论

该问题更可能是“多指缩放期间应用主线程处理不及时 + 非阻塞发送重试 + verifier 更新时机不合理”共同作用的结果。现有证据不能直接证明驱动多报了 `UP`，需要通过驱动原始事件与 framework 事件的跨层时序比对完成最终归因。

修复的关键是保证 verifier 只对真正成功发送给应用的事件更新状态，并通过完整的事件时序日志和正确的压测脚本验证修复效果。
