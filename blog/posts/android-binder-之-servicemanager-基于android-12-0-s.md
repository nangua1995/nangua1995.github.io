> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/03/27/android-binder-%e4%b9%8b-servicemanager-%e5%9f%ba%e4%ba%8eandroid-12-0-s/)

<h3 class="wp-block-heading" id="Binder%20%E5%8E%9F%E7%90%86%E6%95%B4%E7%90%86%EF%BC%9A">Binder 原理整理：</h3>



<p>因为Linux中的进程的用户空间是不共享的，内核空间是共享的，所以IPC通信是两个用户空间（APP 进程）通过共享的内核空间（Binder驱动）进行数据交互。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="595" height="391" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-32.png" alt="" class="wp-image-414" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-32.png 595w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-32-300x197.png 300w" sizes="(max-width: 595px) 100vw, 595px" /></figure>



<p>Binder 整体框架：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="899" height="492" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-33.png" alt="" class="wp-image-415" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-33.png 899w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-33-300x164.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-33-768x420.png 768w" sizes="(max-width: 899px) 100vw, 899px" /></figure>



<p>Binder 通信框架：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="803" height="511" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-34.png" alt="" class="wp-image-416" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-34.png 803w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-34-300x191.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-34-768x489.png 768w" sizes="(max-width: 803px) 100vw, 803px" /></figure>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="805" height="559" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-35.png" alt="" class="wp-image-417" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-35.png 805w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-35-300x208.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-35-768x533.png 768w" sizes="(max-width: 805px) 100vw, 805px" /></figure>



<h2 class="wp-block-heading" id="ServiceManager%20%EF%BC%9A">ServiceManager ：</h2>



<h3 class="wp-block-heading" id="ServiceManager%20%E5%8F%AF%E6%89%A7%E8%A1%8C%E6%96%87%E4%BB%B6%E7%9A%84%E7%94%9F%E6%88%90%EF%BC%9A"><a></a>ServiceManager 可执行文件的生成：</h3>



<p>ServiceManager 在android系统中是一个可执行文件，位于/system/bin/servicemanager下面</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="548" height="598" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-36.png" alt="" class="wp-image-418" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-36.png 548w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-36-275x300.png 275w" sizes="(max-width: 548px) 100vw, 548px" /></figure>



<p>Servicemanager 是在init.rc中启动的</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="398" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-37-1024x398.png" alt="" class="wp-image-419" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-37-1024x398.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-37-300x117.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-37-768x299.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-37.png 1276w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="768" height="506" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-38.png" alt="" class="wp-image-420" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-38.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-38-300x198.png 300w" sizes="(max-width: 768px) 100vw, 768px" /></figure>



<p>在android 10.0.0.R47 及以前 servicemanager是由以下目录结构编译生成的，</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="888" height="413" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-39.png" alt="" class="wp-image-421" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-39.png 888w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-39-300x140.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-39-768x357.png 768w" sizes="(max-width: 888px) 100vw, 888px" /></figure>



<p>在android 10.0.0.R47 及以前 控制编译的相关bp文件：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="700" height="573" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-40.png" alt="" class="wp-image-422" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-40.png 700w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-40-300x246.png 300w" sizes="(max-width: 700px) 100vw, 700px" /></figure>



<p>在android 11.0.0_r21后面原先的service_manager.c变成了ServiceManager.cpp，binder.c变成了main.cpp，同时添加了Access.cpp和Access.h,bctest 变成了 test_sm。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="874" height="513" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-41.png" alt="" class="wp-image-423" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-41.png 874w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-41-300x176.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-41-768x451.png 768w" sizes="(max-width: 874px) 100vw, 874px" /></figure>



<p>Android 11.0.0_r21 以后的bp如图，先是将ServiceManager.cpp和Access.cpp一起生成了servicemanager_defaults,然后通过servicemanager_defaults编译生成可运行的servicemanager。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="865" height="801" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-42.png" alt="" class="wp-image-424" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-42.png 865w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-42-300x278.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-42-768x711.png 768w" sizes="(max-width: 865px) 100vw, 865px" /></figure>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="682" height="368" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-43.png" alt="" class="wp-image-425" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-43.png 682w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-43-300x162.png 300w" sizes="(max-width: 682px) 100vw, 682px" /></figure>



<p>再简单看下目前android 12中的代码目录结构和 android 13的代码结构：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="882" height="507" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-44.png" alt="" class="wp-image-426" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-44.png 882w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-44-300x172.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-44-768x441.png 768w" sizes="(max-width: 882px) 100vw, 882px" /></figure>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="978" height="564" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-45.png" alt="" class="wp-image-427" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-45.png 978w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-45-300x173.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-45-768x443.png 768w" sizes="(max-width: 978px) 100vw, 978px" /></figure>



<p>Android T（13.0）中添加了servicemanager.microdroid.rc 和servicemanager.recovery.rc 两个rc文件。<br>ServiceManager的代码分析：<br>总入口：</p>



<p>Android S 中将android 10.0.0.R47 及以前 在service_manager.c中的 main 方法提取到了main.cpp中。main.cpp中除了main 方法外还额外有ClientCallbackCallback和BinderCallback两个callback.</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="637" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-48-1024x637.png" alt="" class="wp-image-430" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-48-1024x637.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-48-300x187.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-48-768x478.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-48.png 1332w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<pre class="wp-block-code"><code>int main(int argc, char** argv) {    
    if (argc &gt; 2) {
        LOG(FATAL) &lt;&lt; "usage: " &lt;&lt; argv&#91;0] &lt;&lt; " &#91;binder driver]";
    }
 
    const char* driver = argc == 2 ? argv&#91;1] : "/dev/binder";//第二个参数可以缺省
 
    sp&lt;ProcessState&gt; ps = ProcessState::initWithDriver(driver);//打开binder驱动
    ps-&gt;setThreadPoolMaxThreadCount(0);
    ps-&gt;setCallRestriction(ProcessState::CallRestriction::FATAL_IF_NOT_ONEWAY);
 
   // 实例化ServiceManager
    sp&lt;ServiceManager&gt; manager = sp&lt;ServiceManager&gt;::make(std::make_unique&lt;Access&gt;());
    // 将自身注册到ServiceManager当中
    if (!manager-&gt;addService("manager", manager, false /*allowIsolated*/, IServiceManager::DUMP_FLAG_PRIORITY_DEFAULT).isOk()) {
        LOG(ERROR) &lt;&lt; "Could not self register servicemanager";
    }
 
    // 将ServiceManager设置给IPCThreadState的全局变量
    IPCThreadState::self()-&gt;setTheContextObject(manager);
    ps-&gt;becomeContextManager();//注册成为binder服务的大管家
 
    // 准备Looper
    sp&lt;Looper&gt; looper = Looper::prepare(false /*allowNonCallbacks*/);
 
    //给Looper设置callback 
    BinderCallback::setupTo(looper);
    ClientCallbackCallback::setupTo(looper, manager);
    //进入无限循环，处理client端发来的请求
    while(true) {
        looper-&gt;pollAll(-1);
    }
 
    // should not be reachedreturn EXIT_FAILURE;
}</code></pre>



<p>下图为android 10.0.0.R47 及以前 在service_manager.c中的 main 方法（因为页面截图空间限制没有截全 可以自行查看 http://aospxref.com/android-10.0.0_r47/xref/frameworks/native/cmds/servicemanager/service_manager.c#382），相关代码讲解可以参考http://gityuan.com/2015/11/07/binder-start-sm/</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="822" height="915" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-49.png" alt="" class="wp-image-431" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-49.png 822w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-49-270x300.png 270w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-49-768x855.png 768w" sizes="(max-width: 822px) 100vw, 822px" /></figure>



<p>其中main方法中主要干了四件事：</p>



<p>1）初始化binder驱动</p>



<p>2）将自身以“manager” 注册到servicemanager中</p>



<p>3）注册成为binder服务的大管家</p>



<p>4) 给Looper设置callback,进入无限循环，处理client端发来的请求</p>



<p>这里面着重讲后三个代码块</p>



<p>1）第一个代码块中，android 10.0.0.R47 之前是通过binder_open 直接操作binder驱动，没有借助libbinder，Android 11.0.0_r21 以后是通过initWithDriver 对于binder进行操作的，在编译servicemanager的时候，添加了libbinder的库依赖进去。</p>



<p>2）第二个代码块，将自身以“manager” 注册到servicemanager中：</p>



<pre class="wp-block-code"><code>Status ServiceManager::addService(const std::string&amp; name, const sp&lt;IBinder&gt;&amp; binder, bool allowIsolated, int32_t dumpPriority) {    
    auto ctx = mAccess-&gt;getCallingContext();//获取到调用的Context
 
    // apps cannot add services  （AID_APP =10000）
    if (multiuser_get_app_id(ctx.uid) &gt;= AID_APP) {
        return Status::fromExceptionCode(Status::EX_SECURITY);
    }
 
    if (!mAccess-&gt;canAdd(ctx, name)) {
        return Status::fromExceptionCode(Status::EX_SECURITY);
    }
 
    if (binder == nullptr) {
        return Status::fromExceptionCode(Status::EX_ILLEGAL_ARGUMENT);
    }
 
    if (!isValidServiceName(name)) {
        LOG(ERROR) &lt;&lt; "Invalid service name: " &lt;&lt; name;
        return Status::fromExceptionCode(Status::EX_ILLEGAL_ARGUMENT);
    }
 
#ifndef VENDORSERVICEMANAGER
     if (!meetsDeclarationRequirements(binder, name)) {
        // already logged
        return Status::fromExceptionCode(Status::EX_ILLEGAL_ARGUMENT);
    }
#endif  // !VENDORSERVICEMANAGER
       // implicitly unlinked when the binder is removed     
     if (binder-&gt;remoteBinder() != nullptr &amp;&amp;
        binder-&gt;linkToDeath(sp&lt;ServiceManager&gt;::fromExisting(this)) != OK) {
        LOG(ERROR) &lt;&lt; "Could not linkToDeath when adding " &lt;&lt; name;
        return Status::fromExceptionCode(Status::EX_ILLEGAL_STATE);
    }
     //以上代码多是异常情况处理 
 
    // Overwrite the old service if it exists
    //将service的相关信息写入到 servicemanager的 map中
    mNameToService&#91;name] = Service {
        .binder = binder,
        .allowIsolated = allowIsolated,
        .dumpPriority = dumpPriority,
        .debugPid = ctx.debugPid,
    };
 
    auto it = mNameToRegistrationCallback.find(name);
    if (it != mNameToRegistrationCallback.end()) {
        for (const sp&lt;IServiceCallback&gt;&amp; cb : it-&gt;second) {
            mNameToService&#91;name].guaranteeClient = true;
            // permission checked in registerForNotifications
            cb-&gt;onRegistration(name, binder);
        }
    }
 
    return Status::ok();
}</code></pre>



<p>上面的addService 涉及到 Binder的报错类型枚举类：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="989" height="795" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-50.png" alt="" class="wp-image-432" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-50.png 989w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-50-300x241.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-50-768x617.png 768w" sizes="(max-width: 989px) 100vw, 989px" /></figure>



<p>servicemanager中维护注册服务的map：</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="626" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-53-1024x626.png" alt="" class="wp-image-436" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-53-1024x626.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-53-300x183.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-53-768x470.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-53.png 1125w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>分解看service类和ServiceMap:</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="504" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-54-1024x504.png" alt="" class="wp-image-437" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-54-1024x504.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-54-300x148.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-54-768x378.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-54.png 1075w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="509" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-55-1024x509.png" alt="" class="wp-image-438" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-55-1024x509.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-55-300x149.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-55-768x382.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-55.png 1125w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>这里可以看到servicemanager是用map维护注册的服务的，android 10.0.0.R47 及以前是通过链表进行维护的。这里面猜测数据结构的变化是随着手机代码的内存增大和性能指标的增强，链表省空间但是查询较慢的特性已经不能满足需求，于是改用了查询更快的 map进行存储。下图是 android 10.0.0.R47 的注册方法：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="971" height="882" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-56.png" alt="" class="wp-image-439" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-56.png 971w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-56-300x273.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-56-768x698.png 768w" sizes="(max-width: 971px) 100vw, 971px" /></figure>



<p>3）第三个代码块，servicemanager 成为binder服务的大管家。此处通过ioctl往binder驱动发了#define BINDER_SET_CONTEXT_MGR_EXT _IOW(&#8216;b&#8217;, 13, struct flat_binder_object) 的命令，如果不好用则按照android 10.0.0.R47的方式发 #define BINDER_SET_CONTEXT_MGR _IOW(&#8216;b&#8217;, 7, __s32)。后续流程的拆解欢迎大家帮忙补充下。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="1012" height="715" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-57.png" alt="" class="wp-image-440" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-57.png 1012w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-57-300x212.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-57-768x543.png 768w" sizes="(max-width: 1012px) 100vw, 1012px" /></figure>



<p>&nbsp;4）第四个代码块，给Looper设置callback，进入无限循环，处理client端发来的请求  </p>



<p><div class="main_father clearfix d-flex justify-content-center"><div class="container clearfix" id="mainBox"><main><div class="blog-content-box"><article class="baidu_pl"><div id="article_content" class="article_content clearfix"><div id="content_views" class="htmledit_views"><p>给Looper 设置了BinderCallback 和 ClientCallbackCallback，两个callback 都是Loopercallback的子类</p></div></div></article></div></main></div></div></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="991" height="714" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-58.png" alt="" class="wp-image-441" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-58.png 991w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-58-300x216.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-58-768x553.png 768w" sizes="(max-width: 991px) 100vw, 991px" /></figure>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="862" height="624" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-59.png" alt="" class="wp-image-442" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-59.png 862w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-59-300x217.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-59-768x556.png 768w" sizes="(max-width: 862px) 100vw, 862px" /></figure>



<pre class="wp-block-code"><code>class BinderCallback : public LooperCallback {
public:
    static sp&lt;BinderCallback&gt; setupTo(const sp&lt;Looper&gt;&amp; looper) {   
       // 实例化BinderCallback     
       sp&lt;BinderCallback&gt; cb = sp&lt;BinderCallback&gt;::make();
 
        int binder_fd = -1;
        //通过IPCThreadState获取binder_fd，这里面的IPCThreadState待补充
        IPCThreadState::self()-&gt;setupPolling(&amp;binder_fd);
        LOG_ALWAYS_FATAL_IF(binder_fd &lt; 0, "Failed to setupPolling: %d", binder_fd);
        //添加监听目标
        int ret = looper-&gt;addFd(binder_fd,
                                Looper::POLL_CALLBACK,
                                Looper::EVENT_INPUT,
                                cb,
                                nullptr /*data*/);
        LOG_ALWAYS_FATAL_IF(ret != 1, "Failed to add binder FD to Looper");
 
        return cb;
    }
    int handleEvent(int /* fd */, int /* events */, void* /* data */) override {         //处理回调
        IPCThreadState::self()-&gt;handlePolledCommands();
        return 1;  // Continue receiving callbacks.
    }
};</code></pre>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="695" height="452" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-60.png" alt="" class="wp-image-443" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-60.png 695w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-60-300x195.png 300w" sizes="(max-width: 695px) 100vw, 695px" /></figure>



<p>Looper会监听ServiceManager 进程中打开的binder_fd，有消息上来了会调用handlePolledCommands处理。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="853" height="485" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-61.png" alt="" class="wp-image-444" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-61.png 853w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-61-300x171.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-61-768x437.png 768w" sizes="(max-width: 853px) 100vw, 853px" /></figure>



<p>核心是getAndExecuteCommand方法：</p>



<pre class="wp-block-code"><code>status_t IPCThreadState::getAndExecuteCommand(){
    status_t result;
    int32_t cmd;
 
    //从binder driver获取mIn数据
    result = talkWithDriver();
    if (result &gt;= NO_ERROR) {
        size_t IN = mIn.dataAvail();
        if (IN &lt; sizeof(int32_t)) return result;
        cmd = mIn.readInt32();
        IF_LOG_COMMANDS() {
            alog &lt;&lt; "Processing top-level Command: "
                 &lt;&lt; getReturnString(cmd) &lt;&lt; endl;
        }
 
        pthread_mutex_lock(&amp;mProcess-&gt;mThreadCountLock);
        mProcess-&gt;mExecutingThreadsCount++;
        if (mProcess-&gt;mExecutingThreadsCount &gt;= mProcess-&gt;mMaxThreads &amp;&amp;
                mProcess-&gt;mStarvationStartTimeMs == 0) {
            mProcess-&gt;mStarvationStartTimeMs = uptimeMillis();
        }
        pthread_mutex_unlock(&amp;mProcess-&gt;mThreadCountLock);
        // 解析出对应的cmd，执行cmd
        result = executeCommand(cmd);
 
        pthread_mutex_lock(&amp;mProcess-&gt;mThreadCountLock);
        mProcess-&gt;mExecutingThreadsCount--;
        if (mProcess-&gt;mExecutingThreadsCount &lt; mProcess-&gt;mMaxThreads &amp;&amp;
                mProcess-&gt;mStarvationStartTimeMs != 0) {
            int64_t starvationTimeMs = uptimeMillis() - mProcess-&gt;mStarvationStartTimeMs;
            if (starvationTimeMs &gt; 100) {
                ALOGE("binder thread pool (%zu threads) starved for %" PRId64 " ms",
                      mProcess-&gt;mMaxThreads, starvationTimeMs);
            }
            mProcess-&gt;mStarvationStartTimeMs = 0;
        }
 
        // Cond broadcast can be expensive, so don't send it every time a binder// call is processed. b/168806193
        if (mProcess-&gt;mWaitingForThreads &gt; 0) {
            pthread_cond_broadcast(&amp;mProcess-&gt;mThreadCountDecrement);
        }
        pthread_mutex_unlock(&amp;mProcess-&gt;mThreadCountLock);
    }
    return result;
}</code></pre>



<pre class="wp-block-code"><code>status_t IPCThreadState::executeCommand(int32_t cmd){
    BBinder* obj;
    RefBase::weakref_type* refs;
    status_t result = NO_ERROR;
 
    switch ((uint32_t)cmd) {
    case BR_ERROR:
        result = mIn.readInt32();
        break;
 
    case BR_OK:
        break;
 
    case BR_ACQUIRE:
        refs = (RefBase::weakref_type*)mIn.readPointer();
        obj = (BBinder*)mIn.readPointer();
        ALOG_ASSERT(refs-&gt;refBase() == obj,
                   "BR_ACQUIRE: object %p does not match cookie %p (expected %p)",
                   refs, obj, refs-&gt;refBase());
        obj-&gt;incStrong(mProcess.get());
        IF_LOG_REMOTEREFS() {
            LOG_REMOTEREFS("BR_ACQUIRE from driver on %p", obj);
            obj-&gt;printRefs();
        }
        mOut.writeInt32(BC_ACQUIRE_DONE);
        mOut.writePointer((uintptr_t)refs);
        mOut.writePointer((uintptr_t)obj);
        break;
 
    case BR_RELEASE:
        refs = (RefBase::weakref_type*)mIn.readPointer();
        obj = (BBinder*)mIn.readPointer();
        ALOG_ASSERT(refs-&gt;refBase() == obj,
                   "BR_RELEASE: object %p does not match cookie %p (expected %p)",
                   refs, obj, refs-&gt;refBase());
        IF_LOG_REMOTEREFS() {
            LOG_REMOTEREFS("BR_RELEASE from driver on %p", obj);
            obj-&gt;printRefs();
        }
        mPendingStrongDerefs.push(obj);
        break;
 
    case BR_INCREFS:
        refs = (RefBase::weakref_type*)mIn.readPointer();
        obj = (BBinder*)mIn.readPointer();
        refs-&gt;incWeak(mProcess.get());
        mOut.writeInt32(BC_INCREFS_DONE);
        mOut.writePointer((uintptr_t)refs);
        mOut.writePointer((uintptr_t)obj);
        break;
 
    case BR_DECREFS:
        refs = (RefBase::weakref_type*)mIn.readPointer();
        obj = (BBinder*)mIn.readPointer();
        // NOTE: This assertion is not valid, because the object may no// longer exist (thus the (BBinder*)cast above resulting in a different// memory address).//ALOG_ASSERT(refs-&gt;refBase() == obj,//           "BR_DECREFS: object %p does not match cookie %p (expected %p)",//           refs, obj, refs-&gt;refBase());
        mPendingWeakDerefs.push(refs);
        break;
 
    case BR_ATTEMPT_ACQUIRE:
        refs = (RefBase::weakref_type*)mIn.readPointer();
        obj = (BBinder*)mIn.readPointer();
 
        {
            const bool success = refs-&gt;attemptIncStrong(mProcess.get());
            ALOG_ASSERT(success &amp;&amp; refs-&gt;refBase() == obj,
                       "BR_ATTEMPT_ACQUIRE: object %p does not match cookie %p (expected %p)",
                       refs, obj, refs-&gt;refBase());
 
            mOut.writeInt32(BC_ACQUIRE_RESULT);
            mOut.writeInt32((int32_t)success);
        }
        break;
 
    case BR_TRANSACTION_SEC_CTX:
    case BR_TRANSACTION:
        {
            //读取mIn中的数据到一个binder_transaction_data中
            binder_transaction_data_secctx tr_secctx;
            binder_transaction_data&amp; tr = tr_secctx.transaction_data;
 
            if (cmd == (int) BR_TRANSACTION_SEC_CTX) {
                result = mIn.read(&amp;tr_secctx, sizeof(tr_secctx));
            } else {
                result = mIn.read(&amp;tr, sizeof(tr));
                tr_secctx.secctx = 0;
            }
 
            ALOG_ASSERT(result == NO_ERROR,
                "Not enough command data for brTRANSACTION");
            if (result != NO_ERROR) break;
 
            Parcel buffer;
            buffer.ipcSetDataReference(
                reinterpret_cast&lt;const uint8_t*&gt;(tr.data.ptr.buffer),
                tr.data_size,
                reinterpret_cast&lt;const binder_size_t*&gt;(tr.data.ptr.offsets),
                tr.offsets_size/sizeof(binder_size_t), freeBuffer);
 
            const void* origServingStackPointer = mServingStackPointer;
            mServingStackPointer = &amp;origServingStackPointer; // anything on the stackconst pid_t origPid = mCallingPid;
            const char* origSid = mCallingSid;
            const uid_t origUid = mCallingUid;
            const int32_t origStrictModePolicy = mStrictModePolicy;
            const int32_t origTransactionBinderFlags = mLastTransactionBinderFlags;
            const int32_t origWorkSource = mWorkSource;
            const bool origPropagateWorkSet = mPropagateWorkSource;
            // Calling work source will be set by Parcel#enforceInterface. Parcel#enforceInterface// is only guaranteed to be called for AIDL-generated stubs so we reset the work source// here to never propagate it.
            clearCallingWorkSource();
            clearPropagateWorkSource();
 
            mCallingPid = tr.sender_pid;
            mCallingSid = reinterpret_cast&lt;const char*&gt;(tr_secctx.secctx);
            mCallingUid = tr.sender_euid;
            mLastTransactionBinderFlags = tr.flags;
 
            // ALOGI("&gt;&gt;&gt;&gt; TRANSACT from pid %d sid %s uid %d\n", mCallingPid,//    (mCallingSid ? mCallingSid : "&lt;N/A&gt;"), mCallingUid);
 
            Parcel reply;
            status_t error;
            IF_LOG_TRANSACTIONS() {
                TextOutput::Bundle _b(alog);
                alog &lt;&lt; "BR_TRANSACTION thr " &lt;&lt; (void*)pthread_self()
                    &lt;&lt; " / obj " &lt;&lt; tr.target.ptr &lt;&lt; " / code "
                    &lt;&lt; TypeCode(tr.code) &lt;&lt; ": " &lt;&lt; indent &lt;&lt; buffer
                    &lt;&lt; dedent &lt;&lt; endl
                    &lt;&lt; "Data addr = "
                    &lt;&lt; reinterpret_cast&lt;const uint8_t*&gt;(tr.data.ptr.buffer)
                    &lt;&lt; ", offsets addr="
                    &lt;&lt; reinterpret_cast&lt;const size_t*&gt;(tr.data.ptr.offsets) &lt;&lt; endl;
            }
            if (tr.target.ptr) {
                // We only have a weak reference on the target object, so we must first try to// safely acquire a strong reference before doing anything else with it.if (reinterpret_cast&lt;RefBase::weakref_type*&gt;(
                        tr.target.ptr)-&gt;attemptIncStrong(this)) {
                    error = reinterpret_cast&lt;BBinder*&gt;(tr.cookie)-&gt;transact(tr.code, buffer,
                            &amp;reply, tr.flags);
                    reinterpret_cast&lt;BBinder*&gt;(tr.cookie)-&gt;decStrong(this);
                } else {
                    error = UNKNOWN_TRANSACTION;
                }
 
            } else {
                //调用BBinder的transact方法
                error = the_context_object-&gt;transact(tr.code, buffer, &amp;reply, tr.flags);
            }
            //打开该处log可以用来调试
            //ALOGI("&lt;&lt;&lt;&lt; TRANSACT from pid %d restore pid %d sid %s uid %d\n",//     mCallingPid, origPid, (origSid ? origSid : "&lt;N/A&gt;"), origUid);if ((tr.flags &amp; TF_ONE_WAY) == 0) {
                LOG_ONEWAY("Sending reply to %d!", mCallingPid);
                if (error &lt; NO_ERROR) reply.setError(error);
 
                constexpr uint32_t kForwardReplyFlags = TF_CLEAR_BUF;
                //将返回的结果重新发给binder
                sendReply(reply, (tr.flags &amp; kForwardReplyFlags));
            } else {
                if (error != OK) {
                    alog &lt;&lt; "oneway function results for code " &lt;&lt; tr.code
                         &lt;&lt; " on binder at "
                         &lt;&lt; reinterpret_cast&lt;void*&gt;(tr.target.ptr)
                         &lt;&lt; " will be dropped but finished with status "
                         &lt;&lt; statusToString(error);
 
                    // ideally we could log this even when error == OK, but it// causes too much logspam because some manually-written// interfaces have clients that call methods which always// write results, sometimes as oneway methods.if (reply.dataSize() != 0) {
                         alog &lt;&lt; " and reply parcel size " &lt;&lt; reply.dataSize();
                    }
 
                    alog &lt;&lt; endl;
                }
                LOG_ONEWAY("NOT sending reply to %d!", mCallingPid);
            }
 
            mServingStackPointer = origServingStackPointer;
            mCallingPid = origPid;
            mCallingSid = origSid;
            mCallingUid = origUid;
            mStrictModePolicy = origStrictModePolicy;
            mLastTransactionBinderFlags = origTransactionBinderFlags;
            mWorkSource = origWorkSource;
            mPropagateWorkSource = origPropagateWorkSet;
 
            IF_LOG_TRANSACTIONS() {
                TextOutput::Bundle _b(alog);
                alog &lt;&lt; "BC_REPLY thr " &lt;&lt; (void*)pthread_self() &lt;&lt; " / obj "
                    &lt;&lt; tr.target.ptr &lt;&lt; ": " &lt;&lt; indent &lt;&lt; reply &lt;&lt; dedent &lt;&lt; endl;
            }
 
        }
        break;
 
    case BR_DEAD_BINDER:
        {
            BpBinder *proxy = (BpBinder*)mIn.readPointer();
            proxy-&gt;sendObituary();
            mOut.writeInt32(BC_DEAD_BINDER_DONE);
            mOut.writePointer((uintptr_t)proxy);
        } break;
 
    case BR_CLEAR_DEATH_NOTIFICATION_DONE:
        {
            BpBinder *proxy = (BpBinder*)mIn.readPointer();
            proxy-&gt;getWeakRefs()-&gt;decWeak(proxy);
        } break;
 
    case BR_FINISHED:
        result = TIMED_OUT;
        break;
 
    case BR_NOOP:
        break;
 
    case BR_SPAWN_LOOPER:
        mProcess-&gt;spawnPooledThread(false);
        break;
 
    default:
        ALOGE("*** BAD COMMAND %d received from Binder driver\n", cmd);
        result = UNKNOWN_ERROR;
        break;
    }
 
    if (result != NO_ERROR) {
        mLastError = result;
    }
 
    return result;
}</code></pre>



<p>ClientCallbackCallback:</p>



<pre class="wp-block-code"><code>// LooperCallback for IClientCallbackclass ClientCallbackCallback : public LooperCallback {
public:
    static sp&lt;ClientCallbackCallback&gt; setupTo(const sp&lt;Looper&gt;&amp; looper, const sp&lt;ServiceManager&gt;&amp; manager) {       
     sp&lt;ClientCallbackCallback&gt; cb = sp&lt;ClientCallbackCallback&gt;::make(manager);
        //创建一个定时器描述符timerfd
        int fdTimer = timerfd_create(CLOCK_MONOTONIC, 0 /*flags*/);
        LOG_ALWAYS_FATAL_IF(fdTimer &lt; 0, "Failed to timerfd_create: fd: %d err: %d", fdTimer, errno);
 
        itimerspec timespec {
            .it_interval = {
                .tv_sec = 5,
                .tv_nsec = 0,
            },
            .it_value = {
                .tv_sec = 5,
                .tv_nsec = 0,
            },
        };
        //启动所有的定时器
        int timeRes = timerfd_settime(fdTimer, 0 /*flags*/, &amp;timespec, nullptr);
        LOG_ALWAYS_FATAL_IF(timeRes &lt; 0, "Failed to timerfd_settime: res: %d err: %d", timeRes, errno);
        //以时间为描述符注册到Looper中
        int addRes = looper-&gt;addFd(fdTimer,
                                   Looper::POLL_CALLBACK,
                                   Looper::EVENT_INPUT,
                                   cb,
                                   nullptr);
        LOG_ALWAYS_FATAL_IF(addRes != 1, "Failed to add client callback FD to Looper");
 
        return cb;
    }
    int handleEvent(int fd, int /*events*/, void* /*data*/) override {        uint64_t expirations;
        int ret = read(fd, &amp;expirations, sizeof(expirations));
        if (ret != sizeof(expirations)) {
            ALOGE("Read failed to callback FD: ret: %d err: %d", ret, errno);
        }
 
        mManager-&gt;handleClientCallbacks();
        return 1;  // Continue receiving callbacks.
    }
private:
    friend sp&lt;ClientCallbackCallback&gt;;
    ClientCallbackCallback(const sp&lt;ServiceManager&gt;&amp; manager) : mManager(manager) {}
    sp&lt;ServiceManager&gt; mManager;
};</code></pre>



<p>当looper接收到消息时候，调用servicemanager的 handleClientCallbacks进行处理。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="796" height="300" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-62.png" alt="" class="wp-image-445" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-62.png 796w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-62-300x113.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-62-768x289.png 768w" sizes="(max-width: 796px) 100vw, 796px" /></figure>



<p>主要调用handleServiceClientCallback进行处理：</p>



<pre class="wp-block-code"><code>ssize_t ServiceManager::handleServiceClientCallback(const std::string&amp; serviceName,                                                    bool isCalledOnInterval) {
    auto serviceIt = mNameToService.find(serviceName);
    if (serviceIt == mNameToService.end() || mNameToClientCallback.count(serviceName) &lt; 1) {
        return -1;
    }
 
    Service&amp; service = serviceIt-&gt;second;
    ssize_t count = service.getNodeStrongRefCount();
 
    // binder driver doesn't support this featureif (count == -1) return count;
 
    bool hasClients = count &gt; 1; // this process holds a strong countif (service.guaranteeClient) {
        // we have no record of this clientif (!service.hasClients &amp;&amp; !hasClients) {
            sendClientCallbackNotifications(serviceName, true);
        }
 
        // guarantee is temporary
        service.guaranteeClient = false;
    }
 
    // only send notifications if this was called via the interval checking workflowif (isCalledOnInterval) {
        if (hasClients &amp;&amp; !service.hasClients) {
            // client was retrieved in some other way
            sendClientCallbackNotifications(serviceName, true);
        }
 
        // there are no more clients, but the callback has not been called yetif (!hasClients &amp;&amp; service.hasClients) {
            sendClientCallbackNotifications(serviceName, false);
        }
    }
 
    return count;
}</code></pre>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="593" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-63-1024x593.png" alt="" class="wp-image-446" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-63-1024x593.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-63-300x174.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-63-768x445.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-63.png 1390w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>最后通过Looper.pollAll进入无限循环，如果Looper收到消息则触发callback。</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="450" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-64-1024x450.png" alt="" class="wp-image-447" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-64-1024x450.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-64-300x132.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-64-768x338.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-64.png 1126w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<h4 class="wp-block-heading" id="servicemanager%E7%9A%84%E4%B8%BB%E8%A6%81%E5%8A%9F%E8%83%BD%EF%BC%9A">servicemanager的主要功能：</h4>



<p>1）注册服务</p>



<p>其中注册服务主要是通过addService 方法实现的，在讲解总入口第二个代码块的时候已经做过拆解，不再赘余。</p>



<p>2）查询服务</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="267" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-65-1024x267.png" alt="" class="wp-image-448" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-65-1024x267.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-65-300x78.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-65-768x200.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-65.png 1143w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<pre class="wp-block-code"><code>sp ServiceManager::tryGetService(const std::string&amp; name, bool startIfNotFound) { auto ctx = mAccess->getCallingContext();
sp&lt;IBinder> out;
Service* service = nullptr;
if (auto it = mNameToService.find(name); it != mNameToService.end()) {
    service = &amp;(it->second);

    if (!service->allowIsolated) {
        uid_t appid = multiuser_get_app_id(ctx.uid);
        bool isIsolated = appid >= AID_ISOLATED_START &amp;&amp; appid &lt;= AID_ISOLATED_END;

        if (isIsolated) {
            return nullptr;
        }
    }
    //将map中的信息赋值
    out = service->binder;
}

if (!mAccess->canFind(ctx, name)) {
    return nullptr;
}

 //如果找不到对应的service，则尝试以AIDL的方式启动该service
if (!out &amp;&amp; startIfNotFound) {
    tryStartService(name);
}

if (out) {
    // Setting this guarantee each time we hand out a binder ensures that the client-checking
    // loop knows about the event even if the client immediately drops the service
    service->guaranteeClient = true;
}
return out;
}</code></pre>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="277" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-66-1024x277.png" alt="" class="wp-image-450" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-66-1024x277.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-66-300x81.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-66-768x208.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-66.png 1319w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>3）获取servicemanager</p>



<p>不论是注册服务或者查询服务，都需要先获得servicemanager的实例，servicemanager是通过defaultServiceManager 获取的，</p>



<pre class="wp-block-code"><code>&#91;&#91;clang::no_destroy]] static std::once_flag gSmOnce;
sp&lt;IServiceManager> defaultServiceManager(){
    std::call_once(gSmOnce, &#91;]() {
        //AidlServiceManager 就是IServiceManager
        sp&lt;AidlServiceManager> sm = nullptr;
        while (sm == nullptr) {
            sm = interface_cast&lt;AidlServiceManager>(ProcessState::self()->getContextObject(nullptr));
            if (sm == nullptr) {
                ALOGE("Waiting 1s on context object on %s.", ProcessState::self()->getDriverName().c_str());
                sleep(1);
            }
        }
 
        gDefaultServiceManager = sp&lt;ServiceManagerShim>::make(sm);
    });
 
    return gDefaultServiceManager;
}</code></pre>



<p>这里面的gSmOnce和call_once 从名字看是只调用一次的意思，这里先不求甚解。类比android 10.0之前是使用的单例模式，此处的功能应该是类似的。</p>



<p>如图，AidlServiceManager 就是IServiceManager。</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="258" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-67-1024x258.png" alt="" class="wp-image-451" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-67-1024x258.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-67-300x75.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-67-768x193.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-67.png 1053w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>这里与一般的单例模式不太一样，里面多了一层while循环，这是google在2013年1月Todd Poynor提交的修改。当尝试创建或获取ServiceManager时，ServiceManager可能尚未准备就绪，这时通过sleep 1秒后，循环尝试获取直到成功。gDefaultServiceManager的创建过程,可分解为以下3个步骤：</p>



<pre class="wp-block-code"><code>ProcessState::self()：用于获取ProcessState对象(也是单例模式)，每个进程有且只有一个ProcessState对象，存在则直接返回，不存在则创建;

getContextObject()： 用于获取BpBinder对象，对于handle=0的BpBinder对象，存在则直接返回，不存在才创建;

interface_cast&lt;AidlServiceManager&gt;()：用于获取BpServiceManager对象;</code></pre>



<p>分开讲三个流程：</p>



<p>1）ProcessState::self() 获取ProcessState对象</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="1016" height="322" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-68.png" alt="" class="wp-image-452" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-68.png 1016w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-68-300x95.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-68-768x243.png 768w" sizes="(max-width: 1016px) 100vw, 1016px" /></figure>



<pre class="wp-block-code"><code>sp&lt;ProcessState> ProcessState::init(const char *driver, bool requireDefault){
    &#91;&#91;clang::no_destroy]] static sp&lt;ProcessState> gProcess;
    &#91;&#91;clang::no_destroy]] static std::mutex gProcessMutex;
 
    if (driver == nullptr) {
        std::lock_guard&lt;std::mutex> l(gProcessMutex);
        return gProcess;
    }
 
    &#91;&#91;clang::no_destroy]] static std::once_flag gProcessOnce;
    std::call_once(gProcessOnce, &#91;&amp;](){
        if (access(driver, R_OK) == -1) {
            ALOGE("Binder driver %s is unavailable. Using /dev/binder instead.", driver);
            driver = "/dev/binder";
        }
 
        std::lock_guard&lt;std::mutex> l(gProcessMutex);
        //ProcessState调用构造方法进行初始化
        gProcess = sp&lt;ProcessState>::make(driver);
    });
 
    if (requireDefault) {
        // Detect if we are trying to initialize with a different driver, and// consider that an error. ProcessState will only be initialized once above.
        LOG_ALWAYS_FATAL_IF(gProcess->getDriverName() != driver,
                            "ProcessState was already initialized with %s,"" can't initialize with %s.",
                            gProcess->getDriverName().c_str(), driver);
    }
 
    return gProcess;
}</code></pre>



<pre class="wp-block-code"><code>ProcessState::ProcessState(const char *driver)    : mDriverName(String8(driver))
    , mDriverFD(open_driver(driver))//打开Binder驱动
    , mVMStart(MAP_FAILED)
    , mThreadCountLock(PTHREAD_MUTEX_INITIALIZER)
    , mThreadCountDecrement(PTHREAD_COND_INITIALIZER)
    , mExecutingThreadsCount(0)
    , mWaitingForThreads(0)
    , mMaxThreads(DEFAULT_MAX_BINDER_THREADS)
    , mStarvationStartTimeMs(0)
    , mThreadPoolStarted(false)
    , mThreadPoolSeq(1)
    , mCallRestriction(CallRestriction::NONE)
{
    if (mDriverFD >= 0) {
        // mmap the binder, providing a chunk of virtual address space to receive transactions. 
        //mmap binder驱动，提供一个虚拟内存空间地址用于收到事务
        //#define BINDER_VM_SIZE ((1 * 1024 * 1024) - sysconf(_SC_PAGE_SIZE) * 2)
        mVMStart = mmap(nullptr, BINDER_VM_SIZE, PROT_READ, MAP_PRIVATE | MAP_NORESERVE, mDriverFD, 0);
        if (mVMStart == MAP_FAILED) {
            // *sigh*
            ALOGE("Using %s failed: unable to mmap transaction memory.\n", mDriverName.c_str());
            close(mDriverFD);
            mDriverFD = -1;
            mDriverName.clear();
        }
    }
 
#ifdef __ANDROID__
    LOG_ALWAYS_FATAL_IF(mDriverFD &lt; 0, "Binder driver '%s' could not be opened.  Terminating.", driver);
#endif
}</code></pre>



<p>打开binder驱动代码块：</p>



<pre class="wp-block-code"><code>static int open_driver(const char *driver){
    // 打开/dev/binder设备，建立与内核的Binder驱动的交互通道
    int fd = open(driver, O_RDWR | O_CLOEXEC);
    if (fd >= 0) {
        int vers = 0;
        status_t result = ioctl(fd, BINDER_VERSION, &amp;vers);
        if (result == -1) {
            ALOGE("Binder ioctl to obtain version failed: %s", strerror(errno));
            close(fd);
            fd = -1;
        }
        if (result != 0 || vers != BINDER_CURRENT_PROTOCOL_VERSION) {
          ALOGE("Binder driver protocol(%d) does not match user space protocol(%d)! ioctl() return value: %d",
                vers, BINDER_CURRENT_PROTOCOL_VERSION, result);
            close(fd);
            fd = -1;
        }
        size_t maxThreads = DEFAULT_MAX_BINDER_THREADS;
        // 通过ioctl设置binder驱动，能支持的最大线程数
        //#define DEFAULT_MAX_BINDER_THREADS 15  默认是15个线程
        result = ioctl(fd, BINDER_SET_MAX_THREADS, &amp;maxThreads);
        if (result == -1) {
            ALOGE("Binder ioctl to set max threads failed: %s", strerror(errno));
        }
        uint32_t enable = DEFAULT_ENABLE_ONEWAY_SPAM_DETECTION;
        result = ioctl(fd, BINDER_ENABLE_ONEWAY_SPAM_DETECTION, &amp;enable);
        if (result == -1) {
            ALOGD("Binder ioctl to enable oneway spam detection failed: %s", strerror(errno));
        }
    } else {
        ALOGW("Opening '%s' failed: %s\n", driver, strerror(errno));
    }
    return fd;
}</code></pre>



<p>2）<code>getContextObject()</code>： 获取BpBinder对象</p>



<p>获取handle=0的IBinder</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="573" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-69-1024x573.png" alt="" class="wp-image-454" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-69-1024x573.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-69-300x168.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-69-768x430.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-69.png 1339w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<pre class="wp-block-code"><code>sp&lt;IBinder> ProcessState::getStrongProxyForHandle(int32_t handle){
    sp&lt;IBinder> result;
 
    AutoMutex _l(mLock);
    //查找handle对应的资源项
    handle_entry* e = lookupHandleLocked(handle);
 
    if (e != nullptr) {
        // We need to create a new BpBinder if there isn't currently one, OR we// are unable to acquire a weak reference on this current one.  The// attemptIncWeak() is safe because we know the BpBinder destructor will always// call expungeHandle(), which acquires the same lock we are holding now.// We need to do this because there is a race condition between someone// releasing a reference on this BpBinder, and a new reference on its handle// arriving from the driver.
        IBinder* b = e->binder;
        if (b == nullptr || !e->refs->attemptIncWeak(this)) {
            if (handle == 0) {
                // Special case for context manager...// The context manager is the only object for which we create// a BpBinder proxy without already holding a reference.// Perform a dummy transaction to ensure the context manager// is registered before we create the first local reference// to it (which will occur when creating the BpBinder).// If a local reference is created for the BpBinder when the// context manager is not present, the driver will fail to// provide a reference to the context manager, but the// driver API does not return status. Note that this is not race-free if the context manager// dies while this code runs. TODO: add a driver API to wait for context manager, or// stop special casing handle 0 for context manager and add// a driver API to get a handle to the context manager with// proper reference counting.
 
                IPCThreadState* ipc = IPCThreadState::self();
 
                CallRestriction originalCallRestriction = ipc->getCallRestriction();
                ipc->setCallRestriction(CallRestriction::NONE);
 
                Parcel data;
                status_t status = ipc->transact(
                        0, IBinder::PING_TRANSACTION, data, nullptr, 0);
                //通过ping操作测试binder是否准备就绪
                ipc->setCallRestriction(originalCallRestriction);
 
                if (status == DEAD_OBJECT)
                   return nullptr;
            }
            //当handle值所对应的IBinder不存在或弱引用无效时，则创建BpBinder对象
            sp&lt;BpBinder> b = BpBinder::create(handle);
            e->binder = b.get();
            if (b) e->refs = b->getWeakRefs();
            result = b;
        } else {
            // This little bit of nastyness is to allow us to add a primary// reference to the remote proxy when this team doesn't have one// but another team is sending the handle to us.
            result.force_set(b);
            e->refs->decWeak(this);
        }
    }
 
    return result;</code></pre>



<p>如果handle 为0的Ibinder存在且通过Ping 测试已经准备好了，则返回该Ibinder,当handle值所对应的IBinder不存在或弱引用无效时，则创建BpBinder对象。</p>



<pre class="wp-block-code"><code>ProcessState::handle_entry* ProcessState::lookupHandleLocked(int32_t handle){
    const size_t N=mHandleToObject.size();
    //当handle大于mHandleToObject的长度时，进入该分支
    if (N &lt;= (size_t)handle) {
        handle_entry e;
        e.binder = nullptr;
        e.refs = nullptr;
        //从mHandleToObject的第N个位置开始，插入(handle+1-N)个e到队列中
        status_t err = mHandleToObject.insertAt(e, N, handle+1-N);
        if (err &lt; NO_ERROR) return nullptr;
    }
    return &amp;mHandleToObject.editItemAt(handle);
}</code></pre>



<p>（下面模板函数部分文案出自GitYuan，非原创）根据handle值来查找对应的handle_entry,handle_entry是一个结构体，里面记录IBinder和weakref_type两个指针。当handle大于mHandleToObject的Vector长度时，则向该Vector中添加(handle+1-N)个handle_entry结构体，然后再返回handle向对应位置的handle_entry结构体指针。</p>



<p>当handle值所对应的IBinder不存在或弱引用无效时，创建BpBinder并延长对象的生命时间，创建BpBinder对象中会将handle相对应Binder的弱引用增加1：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="981" height="634" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-71.png" alt="" class="wp-image-456" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-71.png 981w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-71-300x194.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-71-768x496.png 768w" sizes="(max-width: 981px) 100vw, 981px" /></figure>



<p>&nbsp;3）<code>interface_cast&lt;</code><strong><code>AidlServiceManager</code></strong><code>&gt;()</code>：获取BpServiceManager对象</p>



<p>AidlServiceManager就是IServiceManager，所以主要拆解 interface_cast:</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="437" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-72-1024x437.png" alt="" class="wp-image-457" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-72-1024x437.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-72-300x128.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-72-768x328.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-72.png 1350w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>（interface_cast() 等价于 IServiceManager::asInterface(),asInterface是通过模板函数来定义的，</p>



<p>主要由以下两个部分构成：</p>



<p>① DECLARE_META_INTERFACE(IServiceManager)</p>



<p>② IMPLEMENT_META_INTERFACE(IServiceManager,&#8221;android.os.IServiceManager&#8221;)</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="571" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-73-1024x571.png" alt="" class="wp-image-458" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-73-1024x571.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-73-300x167.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-73-768x429.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-73.png 1206w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>对于IServiceManager来说只需要换INTERFACE=IServiceManager即可，</p>



<p>DECLARE_META_INTERFACE 过程主要是声明asInterface(),getInterfaceDescriptor()方法。</p>



<p>IMPLEMENT_META_INTERFACE 过程:</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="759" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-74-1024x759.png" alt="" class="wp-image-459" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-74-1024x759.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-74-300x222.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-74-768x569.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-74.png 1223w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>对于IServiceManager来说 INTERFACE=IServiceManager, NAME=”android.os.IServiceManager”，可以看到DECLARE_META_INTERFACE 中的IServiceManager::asInterface() 等价于 BpIServiceManager()::make（obj）。在这里，更确切地说应该是BpIServiceManager::make（BpBinder)。</p>



<p>BpIServiceManager/BpServiceManager 的构造暂时未找到，能力有限，模板函数并不是很熟悉，此处文大家可以参考GitYuan的博客http://gityuan.com/2015/11/08/binder-get-sm/ 先看下android 11.0之前的讲解。后续会补上android 12部分的拆解<br></p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="491" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-75-1024x491.png" alt="" class="wp-image-460" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-75-1024x491.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-75-300x144.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-75-768x368.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-75-1536x736.png 1536w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-75.png 1750w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>总结来看，defaultServiceManager 几近 等于BpIServiceManager::make（BpBinder)，这样就获得到了serviceManager的proxy，类似systemServer 中调用PackageManagerService的方法要拿到PackageManager 一样，后续就可以调用serviceManager中的addService和getService方法了。</p>



<p>从网上找到的 Android 11 之前的 启动流程图，可以先借助理解下，后面会更新最新的图示：<br></p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="712" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-76-1024x712.png" alt="" class="wp-image-461" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-76-1024x712.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-76-300x209.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-76-768x534.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-76.png 1040w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<h4 class="wp-block-heading" id="%C2%A0%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6%E6%A8%A1%E5%9D%97%EF%BC%9A">权限控制模块：</h4>



<p>Access 主要是通过Selinux来进行权限控制的</p>



<p>1）注册服务的时候的校验：</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="409" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-77-1024x409.png" alt="" class="wp-image-464" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-77-1024x409.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-77-300x120.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-77-768x307.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-77-1536x614.png 1536w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-77.png 1712w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="252" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-78-1024x252.png" alt="" class="wp-image-465" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-78-1024x252.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-78-300x74.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-78-768x189.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-78.png 1432w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="563" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-79-1024x563.png" alt="" class="wp-image-466" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-79-1024x563.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-79-300x165.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-79-768x422.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-79.png 1469w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>由于manager在service_contexts中注册了，所以这块Selinux可以顺利通过。</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="689" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-80-1024x689.png" alt="" class="wp-image-467" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-80-1024x689.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-80-300x202.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-80-768x517.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-80.png 1269w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>2）在查询服务的时候通过canFind对于权限进行校验。</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="706" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-81-1024x706.png" alt="" class="wp-image-468" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-81-1024x706.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-81-300x207.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-81-768x529.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-81.png 1284w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="246" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-82-1024x246.png" alt="" class="wp-image-469" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-82-1024x246.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-82-300x72.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-82-768x184.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-82.png 1026w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>最后和 addService一样也会通过actionAllowedFromLookup 进行校验。</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="474" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-83-1024x474.png" alt="" class="wp-image-470" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-83-1024x474.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-83-300x139.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-83-768x355.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-83.png 1459w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<h4 class="wp-block-heading" id="%E2%80%8B%E7%BC%96%E8%BE%91%C2%A0%E5%AF%B9%E5%A4%96%E6%8E%A5%E5%8F%A3%EF%BC%9A">&nbsp;对外接口：</h4>



<p>在android 11之前对外接口只有四个：</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="605" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-86-1024x605.png" alt="" class="wp-image-473" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-86-1024x605.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-86-300x177.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-86-768x454.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-86.png 1125w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="145" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-85-1024x145.png" alt="" class="wp-image-472" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-85-1024x145.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-85-300x43.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-85-768x109.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-85.png 1177w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>在android 12中扩充为14个： （这里将binderDied和handleClientCallbacks计算在内了）</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="593" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-87-1024x593.png" alt="" class="wp-image-474" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-87-1024x593.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-87-300x174.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-87-768x445.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-87.png 1523w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>
