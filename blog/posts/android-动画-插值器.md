> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/03/20/android-%e5%8a%a8%e7%94%bb-%e6%8f%92%e5%80%bc%e5%99%a8/)

<p>参考：https://www.jianshu.com/p/2e5c6326371b</p>



<p><a href="https://links.jianshu.com/go?to=http%3A%2F%2Finloop.github.io%2Finterpolator%2F" target="_blank" rel="noreferrer noopener">http://inloop.github.io/interpolator/</a>&nbsp;特别好的工具，能够直观的看到各种插值器的效果</p>



<h2 class="wp-block-heading">基本使用</h2>



<p>在之前的文章中有提到，插值器定义了动画变化的速率</p>



<p>在 xml 中，使用 <code>android:interpolator</code> 来定义，而在类中的使用也很简单，new 一个对象设置进去就可以了<em></em></p>



<pre class="wp-block-code"><code>animation.setInterpolator(new AccelerateInterpolator());
</code></pre>



<p>那么这个插值器是怎么实现动画速率变化的呢，都有哪些插值器呢，总结一下。</p>



<h2 class="wp-block-heading">简介</h2>



<p>Interpolator 插值器定义了动画变化的速率，使得动画效果能够匀速、加速、减速的变化。</p>



<p>一个动画定义需要定义起始帧和结束帧，中间帧是由系统计算补齐的，如何做补齐计算就是由插值器完成的。</p>



<p><code>Interpolater</code> 继承于 TimeInterpolator，而 <code>TimeInterpolater</code>是一个接口，里面只有一个方法 <code>getInterpolation()</code><em></em></p>



<pre class="wp-block-code"><code>public interface TimeInterpolator {

    /**
     * Maps a value representing the elapsed fraction of an animation to a value that represents
     * the interpolated fraction. This interpolated value is then multiplied by the change in
     * value of an animation to derive the animated value at the current elapsed animation time.
     *
     * @param input A value between 0 and 1.0 indicating our current point
     *        in the animation where 0 represents the start and 1.0 represents
     *        the end
     * @return The interpolation value. This value can be more than 1.0 for
     *         interpolators which overshoot their targets, or less than 0 for
     *         interpolators that undershoot their targets.
     */
    float getInterpolation(float input);
}
</code></pre>



<p>这个插值器就像一个坐标转换的工具，将动画的值分布在时间轴上，<code>getInterpolation()</code> 的入参是个 0 ~ 1，对应着时间的索引，是坐标的 X 轴，返回的就是 X 轴上的时刻对应的动画插值，也就是 Y 轴。</p>



<h2 class="wp-block-heading">Android 的 API 支持的插值器</h2>



<figure class="wp-block-table"><table><thead><tr><th>插值器</th><th>效果</th></tr></thead><tbody><tr><td>LinearInterpolator</td><td>线性插值器：匀速变化</td></tr><tr><td>AccelerateInterpolator</td><td>加速插值器：加速，先慢后快</td></tr><tr><td>DecelerateInterpolator</td><td>减速差值：减速，先快后慢</td></tr><tr><td>AccelerateDecelerateInterpolator</td><td>开始慢，然后加速，最后减速</td></tr><tr><td>AnticipateInterpolator</td><td>这个效果有点像射箭，往回拉一下，在加速射出去</td></tr><tr><td>OvershootInterpolator</td><td>这个效果和上面是相反的，就像从 A 跑到 B 跑过了 又回来了</td></tr><tr><td>AnticipateOvershootInterpolator</td><td>这个是前两个的结合，前面收了一下，结尾过了一下， 中间加速</td></tr><tr><td>BounceInterpolator</td><td>弹跳插值器：像一个自由落下的皮球，碰到了地面，弹几下</td></tr><tr><td>CycleInterpolator</td><td>周期插值器：以起始点为中心，数值加减变化</td></tr></tbody></table></figure>



<h3 class="wp-block-heading">1. LinearInterpolator 线性插值器</h3>



<ul>
<li>类名： <em>LinearInterpolator</em></li>



<li>资源ID： @android:anim/linear_interpolator</li>



<li>XML标记： linearInterpolator</li>



<li>公式： <img decoding="async" src="https://math.jianshu.com/math?formula=y%20%3D%20t" alt="y = t"></li>



<li>构造函数： <code>public LinearInterpolator()</code></li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-7.png" alt="" class="wp-image-331" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-7.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-7-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<h3 class="wp-block-heading">2. Accelerate Interpolator 加速插值器</h3>



<ul>
<li>类名：<em>AcceleraeInterpolator</em></li>



<li>资源ID： @android:anim/accelerate_interpolator</li>



<li>XML标记：accelerateInterpolator</li>



<li>公式： <img decoding="async" src="https://math.jianshu.com/math?formula=y%20%3D%20t%5E%7B2f%7D" alt="y = t^{2f}"></li>



<li>构造函数： <code>public AccelerateInterpolator(float factor)</code>
<ul>
<li>factor（android:factor）加速度参数，默认 1，f 越大，起始速度越慢，但是速度越来越快</li>
</ul>
</li>
</ul>



<p></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-8.png" alt="" class="wp-image-332" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-8.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-8-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<h3 class="wp-block-heading">3. Decelerate Interpolator 减速插值</h3>



<ul>
<li>类名： <em>DecelerateInterpolator</em></li>



<li>资源ID： @android:anim/decelerate_interpolator</li>



<li>XML标记： decelerateInterpolator</li>



<li>公式：：<img decoding="async" src="https://math.jianshu.com/math?formula=y%3D1-(1-t)%5E%7B2f%7D" alt="y=1-(1-t)^{2f}"></li>



<li>构造函数： <code>public DecelerateInterpolator(float factor)</code>
<ul>
<li>factor（android:factor）加速度参数，f 越大，起始速度越快，但是速度越来越慢</li>
</ul>
</li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-9.png" alt="" class="wp-image-333" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-9.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-9-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<h3 class="wp-block-heading">4. Accelerate Decelerate Interpolator 先加速后减速</h3>



<ul>
<li>类名： <em>AccelerateDecelerateInterpolator</em></li>



<li>资源ID：@android:anim/accelerate_decelerate_interpolator</li>



<li>XML 标记：accelerateDecelerateInterpolator</li>



<li>公式：<img decoding="async" src="https://math.jianshu.com/math?formula=y%3Dcos((t%2B1)%CF%80)%2F2%20%2B%200.5" alt="y=cos((t+1)π)/2 + 0.5"></li>



<li>构造函数：<code>public AccelerateDecelerateInterpolator()</code></li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-10.png" alt="" class="wp-image-334" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-10.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-10-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<p></p>



<h3 class="wp-block-heading">5. Anticipate Interpolator</h3>



<ul>
<li>类名： <em>AnticipateInterpolator</em></li>



<li>资源ID： @android:anim/anticipate_interpolator</li>



<li>XML标记： anticipateInterpolator</li>



<li>公式： <img decoding="async" src="https://math.jianshu.com/math?formula=y%3D(T%2B1)t%5E3%E2%80%93Tt%5E2" alt="y=(T+1)t^3–Tt^2"></li>



<li>构造函数： <code>public AnticipateInterpolator(float tension)</code>
<ul>
<li>tension（android:tension） 张力值, 默认为2，T越大，初始的偏移越大，而且速度越快</li>
</ul>
</li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-11.png" alt="" class="wp-image-335" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-11.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-11-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<h3 class="wp-block-heading">6. Overshoot Interpolator</h3>



<ul>
<li>类名： <em>OvershootInterpolator</em></li>



<li>资源ID： @android:anim/overshoot_interpolator</li>



<li>XML标记： overshootInterpolator</li>



<li>公式： <img decoding="async" src="https://math.jianshu.com/math?formula=y%3D(T%2B1)t%5E3%2BTt%5E2%20%2B1" alt="y=(T+1)t^3+Tt^2 +1"></li>



<li>构造函数： <code>public OvershootInterpolator (float tension)</code>
<ul>
<li>tesion (android:tension) 张力值，默认为2，T越大，结束时的偏移越大，而且速度越快</li>
</ul>
</li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-12.png" alt="" class="wp-image-336" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-12.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-12-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<p><br></p>



<h3 class="wp-block-heading">7. Anticipate Overshoot Interpolator</h3>



<ul>
<li>类名： <em>AnticipateOvershootInterpolator</em></li>



<li>资源ID： @android:anim/anticipate_overshoot_interpolator</li>



<li>XML标记： anticipateOvershootInterpolator</li>



<li>公式：<br><img decoding="async" src="https://math.jianshu.com/math?formula=y%20%3D%20%5Cbegin%7Bcases%7D%200.5((T%2B1)(2t)%5E3-T(2t)%5E2)%2C%20%26%20%5Ctext%7Bt%20%3C%200.5%7D%20%5C%5C%5B2ex%5D%200.5((T%2B1)(2t-2)%5E3%2BT(2t-2)%5E2)%2B1%2C%20%26%20%5Ctext%7Bt%20%E2%89%A5%200.5%7D%20%5Cend%7Bcases%7D" alt="y = \begin{cases} 0.5((T+1)(2t)^3-T(2t)^2), &amp; \text{t < 0.5} \\[2ex] 0.5((T+1)(2t-2)^3+T(2t-2)^2)+1, &amp; \text{t ≥ 0.5} \end{cases}"></li>



<li>构造函数：
<ul>
<li><code>public AnticipateOvershootInterpolator(float tension)</code></li>



<li><code>public AnticipateOvershootInterpolator(float tension, float extraTension)</code>
<ul>
<li>tension(android:tension) 张力值，默认为2，张力越大，起始和结束时的偏移越大，而且速度越快</li>



<li>extraTension(android:extraTension)额外张力值，默认为1.5。</li>



<li>公式中 <code>T</code> 的值为 <img decoding="async" src="https://math.jianshu.com/math?formula=tension%20*%20extraTension" alt="tension * extraTension"></li>
</ul>
</li>
</ul>
</li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-13.png" alt="" class="wp-image-337" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-13.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-13-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<h3 class="wp-block-heading">8. Bounce Interpolator 弹跳插值器</h3>



<ul>
<li>类名： <em>BounceInterpolator</em></li>



<li>资源ID： @android:anim/bounce_interpolator</li>



<li>XML标记：bounceInterpolator</li>



<li>公式：<br><img decoding="async" src="https://math.jianshu.com/math?formula=y%20%3D%5Cbegin%7Bcases%7D%208(1.226t)%5E2%2C%20%26%20%5Ctext%7Bt%20%3C%200.3535%7D%20%5C%5C%5B2ex%5D%208(1.226t-0.54719)%5E2%20%2B%200.7%2C%20%26%20%5Ctext%7B%200.3535%E2%89%A4t%3C0.7408%7D%5C%5C%5B2ex%5D%208(1.226t-0.8526)%5E2%20%2B%200.9%2C%20%26%20%5Ctext%7B%200.7408%E2%89%A4t%3C0.9644%7D%5C%5C%5B2ex%5D%208(1.226t-1.0435)%5E2%20%2B%200.95%2C%20%26%20%5Ctext%7Bt%20%E2%89%A50.9644%7D%5C%5C%5B2ex%5D%20%5Cend%7Bcases%7D" alt="y =\begin{cases} 8(1.226t)^2, &amp; \text{t < 0.3535} \\[2ex] 8(1.226t-0.54719)^2 + 0.7, &amp; \text{ 0.3535≤t<0.7408}\\[2ex] 8(1.226t-0.8526)^2 + 0.9, &amp; \text{ 0.7408≤t<0.9644}\\[2ex] 8(1.226t-1.0435)^2 + 0.95, &amp; \text{t ≥0.9644}\\[2ex] \end{cases}"></li>



<li>构造参数 <code>public BounceInterpolator()</code></li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-14.png" alt="" class="wp-image-338" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-14.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-14-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<h3 class="wp-block-heading">9. Cycle Interpolator 周期插值器</h3>



<ul>
<li>类名：<em>CycleInterpolator</em></li>



<li>资源ID：@android:anim/cycle_interpolator</li>



<li>XML标记：cycleInterpolator</li>



<li>公式： <img decoding="async" src="https://math.jianshu.com/math?formula=y%3Dsin(2%CF%80%C3%97c%C3%97t)" alt="y=sin(2π×c×t)"></li>



<li>构造参数 <code>public CycleInterpolator(float cycles)</code>
<ul>
<li>cycles (android:cycles) 周期值，默认为 1，标识执行的次数</li>
</ul>
</li>
</ul>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="640" height="480" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-15.png" alt="" class="wp-image-339" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-15.png 640w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-15-300x225.png 300w" sizes="(max-width: 640px) 100vw, 640px" /></figure>



<p>以上的插值器都是 API 自带的，可直接使用，如果是在 java /kotlin 类中使用，好像更明确，可以直接设置插值器的参数。xml 中也是可以的，只不过要先自定义一个 插值器的 xml，比如：</p>



<p>在 <code>res/anim</code> 创建一个 accelerate_interpolator_2.xml<em></em></p>



<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;accelerateInterpolator xmlns:android="http://schemas.android.com/apk/res/android"
    android:factor="2"&gt;
&lt;/accelerateInterpolator&gt;
</code></pre>



<p>xml 使用时<em></em></p>



<pre class="wp-block-code"><code>android:interpolator="@anim/accelerate_interpolator_2" 
</code></pre>



<p>我们重写的这个加速插值器在代码中也是可以使用的<em></em></p>



<pre class="wp-block-code"><code>animation.setInterpolator(AnimationUtils.loadInterpolator(this,R.anim.accelerate_interpolator_2));
</code></pre>



<h2 class="wp-block-heading">自定义插值器</h2>



<p>前面提到的都是 Android 中配置好的可用的插值器，如果这些都无法满足设计效果的时候，也可以自定义插值器。只要继承 <em>Interpolator</em> 实现 getInterpolation() 即可<em></em></p>



<pre class="wp-block-code"><code>public class MyInterpolator implements Interpolator {
    public MyInterpolator() {}
    public float getInterpolation(float t) 
      return t * t * (3 - 2 * t);
    }
}</code></pre>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="427" height="421" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-16.png" alt="" class="wp-image-340" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-16.png 427w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-16-300x296.png 300w" sizes="(max-width: 427px) 100vw, 427px" /></figure>



<p></p>
