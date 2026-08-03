> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/03/27/android%e5%90%84%e4%b8%aa%e7%89%88%e6%9c%ac%e5%af%b9%e9%80%9a%e7%9f%a5notification%e7%9a%84%e5%8f%98%e6%9b%b4%e4%b8%8e%e9%80%82%e9%85%8d/)

<p><code><strong>1. Android 4.1（API 级别 16）</strong></code></p>



<p>引入了展开式通知模板（称为通知样式），可以提供较大的通知内容区域来显示信息。用户可以使用单指向上/向下滑动的手势来展开通知。</p>



<h3 class="wp-block-heading">2. Android 5.0（API 级别 21）</h3>



<p>引入了锁定屏幕和浮动通知。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="900" height="506" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-88.png" alt="" class="wp-image-482" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-88.png 900w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-88-300x169.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-88-768x432.png 768w" sizes="(max-width: 900px) 100vw, 900px" /></figure>



<p>允许用户将手机设为勿扰模式，并配置允许哪些通知在设备处于“仅限优先”模式时打扰他们。</p>



<p>添加了设置是否在锁定屏幕上显示通知的方法，并指定通知文本的“公开”版本。</p>



<p>添加了 setPriority() 方法，告知系统通知的干扰程度。例如，将优先级设置为“高”会使通知以浮动通知的形式显示。</p>



<p>为 Android Wear（现称为 Wear OS）设备添加了通知堆栈支持。使用 setGroup()将通知放入堆栈。在 Android 7.0（API 级别 24）之前，平板电脑或手机不支持通知堆栈（之后称为组或软件包）。</p>



<p>3.Android 7.0（API 级别 24）</p>



<p>调整了通知模板的样式，以强调主打图片和头像。</p>



<p>添加了三个通知模板：一个用于即时通讯应用，另外两个用于使用可展开功能和其他系统装饰来装饰自定义内容视图。从 Android 7.0（API 级别 24）开始，Android 提供了专用于消息内容的通知样式模板。使用 NotificationCompat.MessagingStyle 类，您可以更改在通知中显示的多个标签，包括会话标题、其他消息和通知的内容视图。</p>



<p>添加了对通知组的手持设备（例如手机和平板电脑）的支持。使用与 Android 5.0（API 级别 21）中引入的 Android Wear（现称为 Wear OS）通知堆栈相同的 API。从 Android 7.0（API 级别 24）开始，您可以在一个组中显示相关通知。例如，如果您的应用针对收到的电子邮件显示通知，请将有关新电子邮件的所有通知放入同一个群组中，以便它们收起来。在 Android 7.0（API 级别 24）及更高版本中，如果您的应用发送了 4 条或更多通知，并且未指定组键或组摘要，系统可能会自动将这些通知分为一组。</p>



<p>允许用户使用内嵌回复功能在通知内回复。用户可以输入文本，系统会将文本路由到通知的父级应用。 Android 7.0（API 级别 24）中引入的直接回复操作可让用户直接在通知中输入文本。然后，文本会在不打开 activity 的情况下传递给您的应用。例如，您可以使用直接回复操作，让用户能够在通知中回复短信或更新任务列表。</p>



<h4 class="wp-block-heading"><strong>4. Android 8.0（API 级别 26）</strong></h4>



<p>将各个通知放入特定渠道。</p>



<p>允许用户按渠道关闭通知，而不是关闭来自某个应用的所有通知。</p>



<p>让具有活动通知的应用在主屏幕或启动器屏幕上的应用图标上方显示通知标志。</p>



<p>允许用户暂停抽屉式通知栏中的通知。您可以为通知设置自动超时时间</p>



<p>通过此设置，您可以设置通知的背景颜色。</p>



<p>将一些与通知行为相关的 API 从 Notification移至 NotificationChannel。例如，对于 Android 8.0 及更高版本，请使用 NotificationChannel.setImportance() 而非 NotificationCompat.Builder.setPriority()。</p>



<p></p>



<p><strong>5. Android 13(API 级别 33)</strong></p>



<p>添加了新的运行时权限 POST_NOTIFICATIONS。为了让您的应用能够发送非豁免通知，用户必须向您的应用授予此权限。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="861" height="531" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-89.png" alt="" class="wp-image-483" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-89.png 861w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-89-300x185.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-89-768x474.png 768w" sizes="(max-width: 861px) 100vw, 861px" /></figure>



<p><strong>6. Android 14(API </strong><strong>级别 </strong><strong>34)</strong></p>



<p>仅限提供通话和闹钟的应用使用全屏 intent 通知。使用 NotificationManager.canUseFullScreenIntent API 检查您的应用是否具有权限。否则，您的应用可以使用 ACTION_MANAGE_APP_USE_FULL_SCREEN_INTENT启动设置页面，在该页面中，用户可以授予权限。</p>



<p>即使设置了 Notification.FLAG_ONGOING_EVENT 标志，也允许用户关闭通知操作来更改用户体验不可关闭通知的方式。如果已设置 Notification.FLAG_ONGOING_EVENT 标志或设备政策控制器 (DPC) 和企业支持软件包，则这不适用于 CallStyle 通知。当手机处于锁定状态或用户选择全部清除时，此规则也不适用。</p>



<p></p>



<p><strong>7. Android 15(API 级别 35)</strong></p>



<p>而从 Android 15 开始，通知冷却主要是用来限制同一来源的连续通知，用户可以选择将其应用于所有通知或仅限于对话通知。</p>



<p>同一来源的连续通知会让通知音量逐渐降低，不过目前预览版看，重复通知并不会完全静音，而是通过音量变化提醒来自同一来源。</p>



<p>“通知冷却” 目前在预览版里存在一个“未知的“冷却计时器，也就是”冷却“会在一段时间后重置，一旦重置就会恢复原本音量，暂时没看到自定义”冷却计时器“的支持</p>
