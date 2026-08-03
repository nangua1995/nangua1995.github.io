> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/03/20/android-animation-animator-%e6%ba%90%e7%a0%81%e5%88%86%e6%9e%90/)

<p><strong>Animation</strong>（<strong>android.view.animation.Animation</strong>）对象 我们使用的时候，一般是用这样的形式：View.startAnimation(a);</p>



<p>那么就来看看View中的<strong>startAnimation()</strong>方法。</p>



<p>1.<strong>View.startAnimation(Animation)</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="405" height="120" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-17.png" alt="" class="wp-image-346" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-17.png 405w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-17-300x89.png 300w" sizes="(max-width: 405px) 100vw, 405px" /></figure>



<p>先是调用<strong>View.setAnimation(Animation)</strong>方法给自己设置一个Animation对象，这个对象是View类中的一个名为<strong>mCurrentAnimation</strong>的成员变量。</p>



<p>然后它调用<strong>invalidate()</strong>来重绘自己。</p>



<p>我想，既然setAnimation()了，那么它要用的时候，肯定要getAnimation()，找到这个方法在哪里调用就好了。于是通过搜索，在<strong>View.draw(Canvas, ViewGroup, long)</strong>方法中发现了它的调用，代码片段如下：</p>



<p>2.<strong>View.draw(Canvas, ViewGroup, long)</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="607" height="450" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-18.png" alt="" class="wp-image-347" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-18.png 607w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-18-300x222.png 300w" sizes="(max-width: 607px) 100vw, 607px" /></figure>



<p><span style="color: rgb(17, 17, 17); font-family: cursive; font-size: 16px; white-space-collapse: collapse; background-color: var(--ast-global-color-5); font-weight: inherit;">其中调用了</span><strong style="color: rgb(17, 17, 17); font-family: cursive; font-size: 16px; white-space-collapse: collapse; background-color: var(--ast-global-color-5); margin: 0px; padding: 0px;">View.drawAnimation()</strong><span style="color: rgb(17, 17, 17); font-family: cursive; font-size: 16px; white-space-collapse: collapse; background-color: var(--ast-global-color-5); font-weight: inherit;">方法。</span><p style="margin: 10px auto; padding: 0px; font-family: cursive; font-size: 16px; color: rgb(17, 17, 17); white-space-collapse: collapse;"> 3.<strong style="margin: 0px; padding: 0px;">View.drawAnimation(ViewGroup, long, Animation, boolean)</strong>代码片段如下：</p></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="620" height="420" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-19.png" alt="" class="wp-image-348" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-19.png 620w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-19-300x203.png 300w" sizes="(max-width: 620px) 100vw, 620px" /></figure>



<p>其中调用了<strong>Animation.getTransformation()</strong>方法。</p>



<p>4.<strong>Animation.getTransformation(long, Transformation, float)</strong></p>



<p>该方法直接调用了两个参数<strong>Animation.getTransformation()</strong>方法。</p>



<p>5.<strong>Animation.getTransformation(long, Transformation)</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="617" height="608" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-20.png" alt="" class="wp-image-349" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-20.png 617w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-20-300x296.png 300w" sizes="(max-width: 617px) 100vw, 617px" /></figure>



<p>该方法先将参数currentTime处理成一个float表示当前动画进度，比如说，一个2000ms的动画，已经执行了1000ms了，那么进度就是0.5或者说50%。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="578" height="62" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-21.png" alt="" class="wp-image-350" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-21.png 578w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-21-300x32.png 300w" sizes="(max-width: 578px) 100vw, 578px" /></figure>



<p>然后将进度值传入插值器（Interpolator）得到新的进度值，前者是均匀的，随着时间是一个直线的线性关系，而通过插值器计算后得到的是一个曲线的关系。</p>



<p>然后将新的进度值和Transformation对象传入<strong>applyTranformation()</strong>方法中。</p>



<p>6.<strong>Animation.applyTransformation(float, Transformation)</strong></p>



<p>Animation的applyTransformation()方法是空实现，具体实现它的是Animation的四个子类，而该方法正是真正的处理动画变化的过程。分别看下四个子类的applyTransformation()的实现。</p>



<p><strong>ScaleAnimation</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="544" height="330" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-22.png" alt="" class="wp-image-351" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-22.png 544w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-22-300x182.png 300w" sizes="(max-width: 544px) 100vw, 544px" /></figure>



<p><strong>AlphaAnimation</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="548" height="100" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-23.png" alt="" class="wp-image-352" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-23.png 548w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-23-300x55.png 300w" sizes="(max-width: 548px) 100vw, 548px" /></figure>



<p><strong>RotateAnimation</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="554" height="194" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-24.png" alt="" class="wp-image-353" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-24.png 554w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-24-300x105.png 300w" sizes="(max-width: 554px) 100vw, 554px" /></figure>



<p><strong>TranslateAnimation</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="545" height="216" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-25.png" alt="" class="wp-image-354" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-25.png 545w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-25-300x119.png 300w" sizes="(max-width: 545px) 100vw, 545px" /></figure>



<p>可见<strong>applyTransformation()</strong>方法就是动画<strong>具体的实现</strong>，系统会以一个比较高的频率来调用这个方法，一般情况下60FPS，是一个非常流畅的画面了，也就是16ms，这个和<strong>Choreographer（android.view.Choreographer）</strong>类的原理有关。</p>



<p>6.<strong>Choreographer.doFrame()</strong></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="427" height="67" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-26.png" alt="" class="wp-image-355" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-26.png 427w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-26-300x47.png 300w" sizes="(max-width: 427px) 100vw, 427px" /></figure>



<p>它调用了三次<strong>doCallbacks()</strong>方法，暂且不说这个方法是干什么的，但从它的第一个参数可以看到分别是<strong>输入（INPUT），动画（ANIMATION），遍历（TRAVERSAL）</strong>。</p>



<p>于是，我先是看了下这三个常量的意义。下图所示：</p>



<figure class="wp-block-image"><img decoding="async" src="https://images0.cnblogs.com/blog/491312/201411/101732206471957.png" alt=""/></figure>



<p>显然，注释是说：输入事件最先处理，然后处理动画，最后才处理view的布局和绘制。接下来我们看看<strong>Choreographer.doCallbacks()</strong>里面做了什么。</p>



<p>7.<strong>Choreographer.doCallbacks(int, long)</strong></p>



<figure class="wp-block-image"><img decoding="async" src="https://images0.cnblogs.com/blog/491312/201411/101735296316889.png" alt=""/></figure>



<p>这个方法的操作非常统一，有三种不同类型的操作（输入，动画，遍历），但在这里却看不见这些具体事件的痕迹，这里我们不得不分析一下<strong>mCallbackQueues</strong>这个成员变量了。</p>



<figure class="wp-block-image"><img decoding="async" src="https://images0.cnblogs.com/blog/491312/201411/101740206473314.png" alt=""/></figure>



<p>mCallbackQueues是一个<strong>CallbackQueue对象数组</strong>。而它的下标，其意义并不是指元素1，元素2，元素3……而是指<strong>类型</strong>，请看上面doCallbacks()的代码，<strong>参数callbackType</strong>传给了<strong>mCallbackQueues[callbackType]</strong>中，而callbackType是什么呢？</p>



<p>其实就是前面说到的三个常量，<strong>CALLBACK_INPUT</strong>,&nbsp;<strong>CALLBACK_ANIMATION</strong>,&nbsp;<strong>CALLBACK_TRAVERVAL</strong>。</p>



<p>那么只需要根据<strong>不同的callbackType</strong>，就可以从这个数组里面取出<strong>不同类型的CallbackQueue对象</strong>来。</p>



<p>那么<strong>CallbackQueue</strong>又是什么呢？</p>



<p><strong>CallbackQueue</strong>是<strong>Choreographer</strong>的一个内部类，其中我认为有两个很重要的方法，分别是：<strong>extractDueCallbacksLocked(long)</strong>和<strong>addCallbackLocked(long, Object, Object)</strong>。</p>



<p>先说<strong>addCallbackLocked(long, Object, Object)</strong>。</p>



<p>1.<strong>CallbackQueue.addCallbackLocked(long, Object, Object)</strong></p>



<figure class="wp-block-image"><img decoding="async" src="https://images0.cnblogs.com/blog/491312/201411/101747086785526.png" alt=""/></figure>



<p>首先它通过一个内部方法构建了一个CallbackRecord对象，然后后面的if判断和while循环，大致上是将参数中的对象链接在CallbackRecord的尾部。其实CallbackRecord就是一个链表结构的对象。</p>



<p>2.<strong>CallbackQueue.extractDueCallbacksLocked(long)</strong></p>



<figure class="wp-block-image"><img decoding="async" src="https://images0.cnblogs.com/blog/491312/201411/101752193197322.png" alt=""/></figure>



<p>这个方法是根据当前的时间，选出执行链表中与该时间最近的一个操作来处理，实际上，我们可以通俗的理解为“<strong>跳帧</strong>”。</p>



<p>想象一下，如果主线程运行的非常快速，非常流畅，每一步都能在10ms内准时运行到，那么我们的执行链表中的元素始终只有一个。</p>



<p>如果主线程中做了耗时操作，那么各种事件一直在往各自的链表中添加，但是当主线程有空来执行的时候，发现链表已经那么多积累的过期的事件了，那么就直接选择最后一个来执行，那么界面上看起来，就是卡顿了一下。</p>



<p></p>



<p>ObjectAnimator.start()方法实际上是辗转几次调用了ValueAnimator的start()方法，ValueAnimator.start()又调用了一个临时变量animationHandler.start()。</p>



<p>animationHandler实际上是一个Runnable，其中start()方法调用了scheduleAnimation()。</p>



<p>而这个方法：</p>



<figure class="wp-block-image"><img decoding="async" src="https://images0.cnblogs.com/blog/491312/201411/101948292256012.png" alt=""/></figure>



<p>调用了postCallback()方法。</p>



<p>将this（Runnable）post之后，实际上肯定就是要执行Runnable.run()方法</p>



<figure class="wp-block-image"><img decoding="async" src="https://images0.cnblogs.com/blog/491312/201411/101953096639502.png" alt=""/></figure>



<p>run()方法中又调用了doAnimationFrame()方法。这个方法具体的实现了动画的某一帧的过程，然后再次调用了scheduleAnimation()方法。</p>



<p>就相当于postDelayed(this, 16)这种方式了。</p>
