> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/03/27/android-binder-%e7%ba%bf%e7%a8%8b%e6%b1%a0%e5%92%8c%e7%ba%bf%e7%a8%8b%e6%b1%a0%e5%b7%a5%e4%bd%9c%e6%b5%81%e7%a8%8b/)

<p>简介：</p>



<p>每一个进程都有且只有一个processState（单例模式）来描述当前进程在binder通信时binder的状态。且都有一个默认的binder主线程Pool thread来跟底层Binder Driver进行通信，这个线程的主体是一个IPCThreadState对象。关系如下：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="819" height="466" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-1.png" alt="" class="wp-image-367" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-1.png 819w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-1-300x171.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-1-768x437.png 768w" sizes="(max-width: 819px) 100vw, 819px" /></figure>



<p>Pool Thread的类在ProcessState.cpp中：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="497" height="533" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-2.png" alt="" class="wp-image-368" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-2.png 497w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-2-280x300.png 280w" sizes="(max-width: 497px) 100vw, 497px" /></figure>



<h3 class="wp-block-heading"><strong>Binder 线程池的启动代码走读：</strong></h3>



<p>binder线程池的启动是通过调用ProcessState.cpp 的startThreadPool()实现的，主要做了两件事：1.设置了线程池的启动状态 2.调用了spawnPooledThread方法，传入参数为TRUE</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="491" height="301" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-3.png" alt="" class="wp-image-369" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-3.png 491w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-3-300x184.png 300w" sizes="(max-width: 491px) 100vw, 491px" /></figure>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="713" height="311" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-4.png" alt="" class="wp-image-370" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-4.png 713w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-4-300x131.png 300w" sizes="(max-width: 713px) 100vw, 713px" /></figure>



<p>1.创建binder线程名</p>



<p>2.创建线程并开启线程。结合上面PoolThread的类看，创建后会执行到threadLoop方法，并传入参数true 调用IPCThreadState的joinThreadPool方法如下：</p>



<pre class="wp-block-code"><code>void IPCThreadState::joinThreadPool(bool isMain)
{
    LOG_THREADPOOL("**** THREAD %p (PID %d) IS JOINING THE THREAD POOL\n", (void*)pthread_self(), getpid());
//isMain ==TRUE 代表主线程，isMain ==FALSE 代表普通的binder线程
//主线程 BC_ENTER_LOOPER 发送给binder_driver后，binder_driver会确定能否启动线程
//普通binder线程 BC_REGISTER_LOOPER 发送给binder_driver后，binder_driver会确定能否启动线程
    mOut.writeInt32(isMain ? BC_ENTER_LOOPER : BC_REGISTER_LOOPER);
 
    mIsLooper = true;
    status_t result;
    do {
        processPendingDerefs();
        // now get the next command to be processed, waiting if necessary
        result = getAndExecuteCommand();
 
        if (result &lt; NO_ERROR &amp;&amp; result != TIMED_OUT &amp;&amp; result != -ECONNREFUSED &amp;&amp; result != -EBADF) {
            LOG_ALWAYS_FATAL("getAndExecuteCommand(fd=%d) returned unexpected error %d, aborting",
                  mProcess->mDriverFD, result);
        }
 
        // Let this thread exit the thread pool if it is no longer
        // needed and it is not the main process thread.
        if(result == TIMED_OUT &amp;&amp; !isMain) {
            break;
        }
    } while (result != -ECONNREFUSED &amp;&amp; result != -EBADF);
 
    LOG_THREADPOOL("**** THREAD %p (PID %d) IS LEAVING THE THREAD POOL err=%d\n",
        (void*)pthread_self(), getpid(), result);
 
    mOut.writeInt32(BC_EXIT_LOOPER);
    mIsLooper = false;
    talkWithDriver(false);
}</code></pre>



<p>主线程是在启动binder线程池的时候被创建的，其他线程是binder Driver发送BR_SPAWN_LOOPER 来通知进程创建的。</p>



<p>发送BR_SPAWN_LOOPER的条件如下：</p>



<pre class="wp-block-code"><code>当前进程已经没有可以请求的线程，并且也没有已经ready可用的线程了
当前进程已经开始请求的线程小于最大线程数（每个进程包含主线程一个，其他线程的限额是15个）
当前线程状态不能是BINDER_LOOPER_STATE_REGISTERED,也不能是BINDER_LOOPER_STATE_ENTERED.这两个状态代表此线程的状态已经启动了。不能重复启动</code></pre>



<p>{其中BR_SPAWN_LOOPER 是在BINDER_WORK_TRANSACTION的cmd中被发送出来的，而BINDER_WORK_TRANSACTION是在client发送BC_TRANSACTION或者发送BC_REPLY的时候被调用的</p>



<p>BC_TRANSACTION或发送BC_REPLY 对应两种情景：</p>



<p>BC_TRANSACTION : client进程向 binderDriver发送IPC调用请求的时候</p>



<p>BC_REPLY : server进程收到了binderDriver的IPC调用请求，请求执行完毕后发送返回值时候}<br>线程池的工作过程：</p>



<p>线程池工作中主要涉及ProcessState，Pool Thread, IPCThreadState 和BpBinder。ProcessState和Pool Thread 、IPCThreadState 都是以单例模式设计的。每个进程中只有一个。</p>



<p>ProcessState 负责创建并管理BpBinder以及Pool Thread，PoolThread的核心是IPCThreadState，这个类里面有两个Parcel对象，分别负责存储从BinderDriver读出来的数据和要往BinderDriver中写入的数据。我们一般使用的各种Manager继承自BpBinder，当我们需要通过IPC调用到server的接口时，会通过BpBinder的transact方法将数据写入到mOut中，然后IPCThreadState 又会通过talkwithDriver将数据发给binderDriver。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="808" height="463" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-5.png" alt="" class="wp-image-371" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-5.png 808w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-5-300x172.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-5-768x440.png 768w" sizes="(max-width: 808px) 100vw, 808px" /></figure>



<p><br>Binder通信模型流程图：</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="669" height="511" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-6.png" alt="" class="wp-image-372" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-6.png 669w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/图片-6-300x229.png 300w" sizes="(max-width: 669px) 100vw, 669px" /></figure>
