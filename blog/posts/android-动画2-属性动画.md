> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/03/20/android-%e5%8a%a8%e7%94%bb2-%e5%b1%9e%e6%80%a7%e5%8a%a8%e7%94%bb/)

<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="728" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-1024x728.png" alt="" class="wp-image-321" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-1024x728.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-300x213.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-768x546.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image.png 1320w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<h1 class="wp-block-heading">属性动画</h1>



<p></p>



<h2 class="wp-block-heading">属性动画与视图动画的区别</h2>



<p>帧动画 和 视图动画 都只能对 View 对象添加动画效果，而且只能对公开对象属性添加效果，比如可以对 view 的缩放和旋转添加动画，但是不能操作背景颜色。</p>



<p>视图动画系统的另一个缺点是它只会在绘制视图的位置进行修改，而不会修改实际的视图本身。例如，如果您为某个按钮添加了动画效果，使其可以在屏幕上移动，该按钮会正确绘制，但能够点击按钮的实际位置并不会更改，必须通过实现自己的逻辑来处理此事件。</p>



<p>有了属性动画系统，您就可以完全摆脱这些束缚，还可以为任何对象（视图和非视图）的任何属性添加动画效果，并且实际修改的是对象本身。属性动画系统在执行动画方面也更为强健。概括地讲，您可以为要添加动画效果的属性（例如颜色、位置或大小）分配 Animator，还可以定义动画的各个方面，例如多个 Animator 的插值和同步。</p>



<p>不过，视图动画系统的设置需要的时间较短，需要编写的代码也较少。如果视图动画可以完成您需要执行的所有操作，或者现有代码已按照您需要的方式运行，则无需使用属性动画系统。在某些用例中，也可以针对不同的情况同时使用这两种动画系统。</p>



<blockquote class="wp-block-quote">
<p>如果是view 的平移、缩放等常规操作，通过View动画是完全可以实现的。</p>
</blockquote>



<h2 class="wp-block-heading">动画本质</h2>



<p>在了解属性动画之前，看一下动画本质</p>



<p>动画实际上是改变 View 在某一时间点的样式属性<br>比如在 10 时，view 坐标是10px，在 20s 时是 20px，就有向右移动的视觉</p>



<p>实际上通过一个线程每个一段时间通过调用 view.setX(index ++) 值也能产生动画效果，这就是属性动画的原理。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="568" height="166" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-3.png" alt="" class="wp-image-324" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-3.png 568w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-3-300x88.png 300w" sizes="(max-width: 568px) 100vw, 568px" /></figure>



<p>动画是一个比较复杂的流程，需要考虑的因素比较多，在开发层面肯定不能直接调用view.setX()。</p>



<h2 class="wp-block-heading">属性动画的工作方式</h2>



<ul>
<li>计算属性值</li>



<li>设置目标对象的属性值（应用产生动画效果）</li>
</ul>



<h3 class="wp-block-heading">属性值的计算</h3>



<p>前面的例子简单的描述了 40ms 内 从在 0-40之间的属性值变化</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="723" height="240" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-1.png" alt="" class="wp-image-322" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-1.png 723w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-1-300x100.png 300w" sizes="(max-width: 723px) 100vw, 723px" /></figure>



<p>如何计算动画</p>



<p>我们总说插值器和估值器，他们到底是怎么转化成属性的变化的？</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="200" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-2-1024x200.png" alt="" class="wp-image-323" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-2-1024x200.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-2-300x59.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-2-768x150.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-2.png 1254w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p><strong>1. 计算已完成动画 fraction</strong><br>执行一个动画，会指定目标对象属性的开始值、结束值以及持续时间。在动画 start 后，会得到一个 elapsed fraction 表示当前动画已完成的百分比，范围是 0~1，表示 0%~100%。</p>



<p><strong>2. 计算插值（动画变化率）</strong><br>之前的已经介绍过，插值器，用来改变动画的变化速率的，在计算 elapsed fraction 之后，会根据当前设置的 TimeInterpolator 计算出一个 interpolation value。</p>



<p><strong>3. 计算属性值</strong><br>当插值计算完成后，ValueAnimator 会根据插值分数调用合适的 TypeEvaluator 去计算运动中的属性值。<br>其实就是时间与属性的映射关系。也可以自定义估值器让这个关系更加丰富和灵活。</p>



<p>比如：1000ms 内 0-100变化 如果是线性的、属性为整数时 time = fraction， value = start + t*（end &#8211; start）（ValueAnimator.ofInt &#8212; IntEvalutaor）</p>



<figure class="wp-block-table"><table><thead><tr><th>elapsed fraction</th><th>0</th><th>0.2</th><th>0.5</th><th>0.7</th><th>1</th></tr></thead><tbody><tr><td>time = fraction</td><td>0</td><td>0.2</td><td>0.5</td><td>0.7</td><td>1</td></tr><tr><td>value =x0 + t * (x1 &#8211; x0)</td><td>0</td><td>20</td><td>50</td><td>70</td><td>100</td></tr></tbody></table></figure>



<p>使用插值器 time = f^2</p>



<figure class="wp-block-table"><table><thead><tr><th>elapsed fraction</th><th>0</th><th>0.2</th><th>0.5</th><th>0.7</th><th>1</th></tr></thead><tbody><tr><td>time = f^2</td><td>0</td><td>0.04</td><td>0.25</td><td>0.49</td><td>1</td></tr><tr><td>value =x0 + t * (x1 &#8211; x0)</td><td>0</td><td>4</td><td>25</td><td>49</td><td>100</td></tr></tbody></table></figure>



<p>使用估值器 float value = (x0 + t * (x1 &#8211; x0))/2</p>



<figure class="wp-block-table"><table><thead><tr><th>elapsed fraction</th><th>0</th><th>0.2</th><th>0.5</th><th>0.7</th><th>1</th></tr></thead><tbody><tr><td>time = f^2</td><td>0</td><td>0.04</td><td>0.25</td><td>0.49</td><td>1</td></tr><tr><td>value</td><td>0</td><td>2</td><td>12.5</td><td>24.5</td><td>50</td></tr></tbody></table></figure>



<h3 class="wp-block-heading">设置属性值</h3>



<p>可以为 ValueAnimator 对象添加 AnimatorUpdateListener，通过实现 <code>onAnimationUpdate</code> 方法更新目标 View 的属性值，当前属性值通过 <code>ValueAnimator#getAnimatedValue()</code>获取。</p>



<h2 class="wp-block-heading">估值器 Evaluators</h2>



<p>定义如何通过起始和结束值计算属性值，可得出某一个时刻具体的值。</p>



<p>API 提供了几种 Evaluators</p>



<ul>
<li>IntEvaluator：计算 int 值</li>



<li>FloatEvaluator：计算 float 值</li>



<li>ArgbEvaluator：计算 color（十六进制）属性值</li>



<li>PointFEvaluator：计算 Point<br>TypeEvaluator 是一个可以自定义计算属性值的接口，上面的的集中 API 内部的Evaluators 也是实现 TypeEvaluator，如果 API 内部不满足也可以自定义类型和计算方式</li>
</ul>



<p><em></em></p>



<pre class="wp-block-code"><code>public interface TypeEvaluator&lt;T&gt; {

    /**
     * This function returns the result of linearly interpolating the start and end values, with
     * &lt;code&gt;fraction&lt;/code&gt; representing the proportion between the start and end values. The
     * calculation is a simple parametric calculation: &lt;code&gt;result = x0 + t * (x1 - x0)&lt;/code&gt;,
     * where &lt;code&gt;x0&lt;/code&gt; is &lt;code&gt;startValue&lt;/code&gt;, &lt;code&gt;x1&lt;/code&gt; is &lt;code&gt;endValue&lt;/code&gt;,
     * and &lt;code&gt;t&lt;/code&gt; is &lt;code&gt;fraction&lt;/code&gt;.
     *
     * @param fraction   The fraction from the starting to the ending values
     * @param startValue The start value.
     * @param endValue   The end value.
     * @return A linear interpolation between the start and end values, given the
     *         &lt;code&gt;fraction&lt;/code&gt; parameter.
     */
    public T evaluate(float fraction, T startValue, T endValue);
}
</code></pre>



<p>这个接口只有一个方法 <code>evaluate()</code>，比如，<em></em></p>



<pre class="wp-block-code"><code>class BulletEvaluator implements TypeEvaluator&lt;PointF&gt; {

    int degree;// 变化角度

    /**
     * 与 ↑ 夹角
     *
     * @param degree
     */
    public BulletEvaluator(int degree) {
        super();
        this.degree = degree;
    }

    @Override
    public PointF evaluate(float fraction, PointF startValue, PointF endValue) {
        double rad = degree * Math.PI / 180;
        PointF pointf = new PointF();
        pointf.y = (endValue.y - startValue.y) * fraction + startValue.y;
        pointf.x = (float) (Math.abs(((endValue.y - startValue.y) * fraction)* Math.tan(rad)) + startValue.x);
        return pointf;
    }
}
</code></pre>



<p>使用这个估值器<em></em></p>



<pre class="wp-block-code"><code> ValueAnimator valueAnimator = ValueAnimator.ofObject(new BulletEvaluator(DEGREE), mPointFs&#91;0], mPointFs&#91;1]);
</code></pre>



<h2 class="wp-block-heading">相关 API Animator</h2>



<p>视图动画 使用的类都在 <code>android.view.animation</code> 包 下<br>而属性动画系统的API 在 <code>android.animation</code> 包下<br></p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="407" height="185" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-4.png" alt="" class="wp-image-325" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-4.png 407w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-4-300x136.png 300w" sizes="(max-width: 407px) 100vw, 407px" /></figure>



<h3 class="wp-block-heading">ValueAnimator</h3>



<p><em></em></p>



<pre class="wp-block-code"><code>ValueAnimator animation = ValueAnimator.ofFloat(0f, 100f);
animation.setDuration(1000);
animation.start();
</code></pre>



<p>当 <code>start()</code> 方法运行时，<code>ValueAnimator</code> 会开始计算 1000ms 时长内 0 和 100 之间的值。可以为 <code>ValueAnimator</code> 对象添加 <code>AnimatorUpdateListener</code>来使用变化的值，如以下代码所示：<em></em></p>



<pre class="wp-block-code"><code>animation.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
  @Override
  public void onAnimationUpdate(ValueAnimator updatedAnimation) {
    // You can use the animated value in a property that uses the
    // same type as the animation. In this case, you can use the
    // float value in the translationX property.
  float animatedValue = (float)updatedAnimation.getAnimatedValue();
  textView.setTranslationX(animatedValue);
  }
});
</code></pre>



<p>在 <code>onAnimationUpdate()</code> 方法中，可以使用更新后的动画值，使用在某个视图的属性中。比如实例就实现了右移的效果。</p>



<p>API 提供了几个方法来获取 ValueAnimator 对象（红色区域）。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="960" height="488" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-5.png" alt="" class="wp-image-326" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-5.png 960w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-5-300x153.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-5-768x390.png 768w" sizes="(max-width: 960px) 100vw, 960px" /></figure>



<p>除了 <code>ofFloat()</code>，<code>ofInt()</code> 和<code>ofArgb()</code>（可以做颜色渐变）都可以获取 ValueAnimator 对象，使用方法与<code>ofFloat()</code> 一样的。这里的的入参是对应类型的可变长参数。</p>



<p>这里还有个<code>ofObject()</code> ，它的入参除了 Object 数组，还有一个 TypeEvaluator 类型的入参。TypeEvaluator 是估值器，我们可以自定义动画效果，通过执行以下操作来指定要添加动画效果的自定义类型：<em></em></p>



<pre class="wp-block-code"><code>ValueAnimator animation = ValueAnimator.ofObject(new MyTypeEvaluator(), startPropertyValue, endPropertyValue);
animation.setDuration(1000);
animation.start();
</code></pre>



<p><code>ofProertyValuesHolder()</code> 见下文关键帧的使用</p>



<p>valueAnimator 是通过监听，使用数值 value 对 view 进行属性改变，达到动画效果。为了更便于使用，API 提供了一个 ObjectAnimator</p>



<h3 class="wp-block-heading">ObjectAnimator</h3>



<p>ObjectAnimator 是 ValueAnimator 的子类，允许指定目标对象和该对象的一个属性，这个类会根据计算得到的新值自动更新属性。</p>



<p>因为继承了 ValueAnimator，因此完全可以像ValueAnimator 那样调用。你看下 ObjectAnimator 的工厂方法中，重载了一些方法，比起常用的 <code>ofxxx()</code>，多了一些入参。</p>



<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" width="445" height="503" src="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-6.png" alt="" class="wp-image-327" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-6.png 445w, https://zhinengzuocang.cn/wp-content/uploads/2024/03/image-6-265x300.png 265w" sizes="(max-width: 445px) 100vw, 445px" /></figure>



<p>下面的写法等同于上面的示例，表示对 view 的 translationX 属性，在 1000ms 内从向右移动100px，使用更方便，不需要通过监听。<em></em></p>



<pre class="wp-block-code"><code>ObjectAnimator animation = ObjectAnimator.ofFloat(view, "translationX", 0f, 100f);
animation.setDuration(1000);
animation.start();
</code></pre>



<blockquote class="wp-block-quote">
<p>ObjectAnimator 的自动更新功能 ， 依赖于属性身上的<code>setter</code> 和 <code>getter</code> 方法 ， 所以要使 ObjectAnimator 正确更新属性，需要注意一下几点：<br><strong>（言简意赅：就注意要有 setter 和 getter， 细节见下文）</strong></p>



<ul>
<li>要添加动画效果的对象属性 <strong>必须具有 <code>set&lt;PropertyName&gt;()</code> 形式的 setter 函数</strong>（采用驼峰式大小写形式）。由于 ObjectAnimator 会在动画过程中自动更新属性，它必须能够使用此 <code>setter</code> 方法访问该属性。例如，如果属性名称为 <code>foo</code>，则需要使用 <code>setFoo()</code> 方法。如果此 <code>setter</code> 方法不存在，可以考虑如下方式：
<ul>
<li>如果有权限，可添加 setter 方法到类中。</li>



<li>使用可以更改的封装容器类，让该封装容器使用有效的 setter 方法接收值并将其转发给原始对象。</li>



<li>改用 ValueAnimator。</li>
</ul>
</li>



<li>如果在 ObjectAnimator 的一个工厂方法中仅为 values&#8230; 参数指定了一个值，则系统会假定它是动画的结束值。因此，要添加动画效果的对象属性必须具有用于获取动画起始值的 <code>getter</code> 函数。getter 函数必须采用 <code>get&lt;PropertyName&gt;()</code> 形式。例如，如果属性名称为 <code>foo</code>，则需要使用 <code>getFoo()</code> 方法。</li>



<li>要添加动画效果的属性的 getter（如果需要）和 <code>setter</code> 方法的操作对象必须与您为 ObjectAnimator 指定的起始值和结束值的类型相同。例如，如果构建以下 ObjectAnimator，则必须具有 <code>targetObject.setPropName(float)</code> 和 <code>targetObject.getPropName(float)</code> :<br><code>ObjectAnimator.ofFloat(targetObject, "propName", 1f)</code></li>



<li>根据要添加动画效果的属性或对象，可能需要对视图调用 <code>invalidate()</code> 方法，以强制屏幕使用添加动画效果之后的值重新绘制自身。可以在 <code>onAnimationUpdate()</code> 回调中执行此操作。例如，如果为可绘制对象的颜色属性添加动画效果，则仅当该对象重新绘制自身时，屏幕才会刷新。视图的所有属性 setter（如 setAlpha() 和 setTranslationX()）都会使视图失效，因此，在使用新值调用这些方法时，无需使视图失效。</li>
</ul>
</blockquote>



<h3 class="wp-block-heading">AnimatorSet</h3>



<p>使用 AnimatorSet 用来编排多个动画<br>在一些场景，需要根据一个动画开始或结束的时间来播放另一个动画。通过相关 API，可以将动画捆绑到一个 AnimatorSet 中，来指定是同时播放动画、按顺序播放还是在指定的延迟时间后播放。也可以相互嵌套 AnimatorSet 对象。</p>



<p>以下代码段通过以下方式播放相应的 Animator 对象：</p>



<p>播放 bounceAnim。<br>同时播放 squashAnim1、squashAnim2、stretchAnim1 和 stretchAnim2。<br>播放 bounceBackAnim。<br>播放 fadeAnim。<em></em></p>



<pre class="wp-block-code"><code>    AnimatorSet bouncer = new AnimatorSet();
    bouncer.play(bounceAnim).before(squashAnim1);
    bouncer.play(squashAnim1).with(squashAnim2);
    bouncer.play(squashAnim1).with(stretchAnim1);
    bouncer.play(squashAnim1).with(stretchAnim2);
    bouncer.play(bounceBackAnim).after(stretchAnim2);
    ValueAnimator fadeAnim = ObjectAnimator.ofFloat(newBall, "alpha", 1f, 0f);
    fadeAnim.setDuration(250);
    AnimatorSet animatorSet = new AnimatorSet();
    animatorSet.play(bouncer).before(fadeAnim);
    animatorSet.start();
</code></pre>



<h3 class="wp-block-heading">关键帧 Keyframe</h3>



<p><em>Keyframe</em> 对象由 time-value 的键值对组成，用于在动画的特定时间定义特定的状态。每个关键帧还可以用自己的插值器，控制前一帧和当前帧的时间间隔间内的动画。</p>



<p>如果想指定某一特定时间的特定状态，那么简单的使用ObjectAnimator 就不能满足了ObjectAnimator.ofInt(&#8230;.) 类似的工厂方法，无法指定特定的时间点的状态。</p>



<p>要实例化 <em>Keyframe</em> 对象</p>



<ul>
<li>使用它的任一工厂方法（ofInt()、ofFloat() 或 ofObject()）来获取类型合适的 keyframe。</li>



<li>通过调用 <code>ofKeyframe()</code> 方法获取 <em>PropertyValuesHolder</em> 对象。获取对象后，您可以通过传入 <em>PropertyValuesHolder</em> 对象以及要添加动画效果的对象来获取 Animator。以下代码段演示了如何做到这一点： <em>PropertyValuesHolder</em> 属性持有者，相关属性值的操作以及属性的setter，getter方法的创建，属性值以 Keyframe来承载，最终由KeyframeSet 统一处理</li>
</ul>



<p><em></em></p>



<pre class="wp-block-code"><code>Keyframe kf0 = Keyframe.ofFloat(0f, 0f);
Keyframe kf1 = Keyframe.ofFloat(.5f, 360f);
Keyframe kf2 = Keyframe.ofFloat(1f, 0f);
PropertyValuesHolder pvhRotation = PropertyValuesHolder.ofKeyframe("rotation", kf0, kf1, kf2);
ObjectAnimator rotationAnim = ObjectAnimator.ofPropertyValuesHolder(target, pvhRotation);
    rotationAnim.setDuration(5000);
</code></pre>



<p>每个 KeyFrame 的 Interpolator</p>



<p>每个 KeyFrame 其实也有个 Interpolator 。如果没有设置，默认是线性的。之前为 Animator 设置的<br>Interpolator 是整个动画的，而系统允许你为每一 KeyFrame 的单独定义 Interpolator ，系统这样做的目的是允许你在某一个 keyFrame 做特殊的处理，也就是整体上是按照你的插值函数来计算，但是，如果希望某个或某些 KeyFrame 会有不同的动画表现，那么你可以为这个 keyFrame 设置 Interpolator 。<br>因此，Keyframe的定制性更高，你如果想精确控制某一个时间点的动画值及其运动规律，你可以自己创建特定的 Keyframe</p>



<h3 class="wp-block-heading">ViewPropertyAnimator</h3>



<p>为方便为某一个View的 多个属性添加并行动画，使用 ViewPropertyAnimator 对象就可以完成。</p>



<p>比如：view 的 x 和 y 同时变化，使用 ObjectAnimator + AnimatorSet 这样处理<em></em></p>



<pre class="wp-block-code"><code>ObjectAnimator animX = ObjectAnimator.ofFloat(myView, "x", 50f);
ObjectAnimator animY = ObjectAnimator.ofFloat(myView, "y", 100f);
AnimatorSet animSetXY = new AnimatorSet();
animSetXY.playTogether(animX, animY);
animSetXY.start();
</code></pre>



<p>使用 ObjectAnimator + PropertyValuesHolder<em></em></p>



<pre class="wp-block-code"><code>PropertyValuesHolder pvhX = PropertyValuesHolder.ofFloat("x", 50f);
PropertyValuesHolder pvhY = PropertyValuesHolder.ofFloat("y", 100f);
ObjectAnimator.ofPropertyValuesHolder(myView, pvhX, pvyY).start();
</code></pre>



<p>而使用 ViewPropertyAnimator 只需一行代码<em></em></p>



<pre class="wp-block-code"><code>myView.animate().x(50f).y(100f); // myView.animate() 直接返回一个ViewPropertyAnimator对象
</code></pre>



<h2 class="wp-block-heading">动画监听器</h2>



<p>可以使用下述监听器来监听动画播放期间的重要事件</p>



<h3 class="wp-block-heading">Animator.AnimatorListener</h3>



<ul>
<li>onAnimationStart() &#8211; 在动画开始播放时调用。</li>



<li>onAnimationEnd() &#8211; 在动画结束播放时调用。</li>



<li>onAnimationRepeat() &#8211; 在动画重复播放时调用。</li>



<li>onAnimationCancel() &#8211; 在动画取消播放时调用。取消的动画也会调用 onAnimationEnd()，无论它们以何种方式结束。</li>
</ul>



<h3 class="wp-block-heading">ValueAnimator.AnimatorUpdateListener</h3>



<p><code>onAnimationUpdate()</code> &#8211; 对动画的每一帧调用。监听此事件即可使用 <em>ValueAnimator</em> 在动画播放期间生成的计算值。要使用该值，请查询传递到事件中的 ValueAnimator 对象，以使用 <code>getAnimatedValue()</code>方法获取当前添加动画效果之后的值。<strong>如果使用了 ValueAnimator ，则必须实现此监听器</strong>。</p>



<p>根据您要添加动画效果的属性或对象，您可能需要对视图调用 invalidate()，以强制屏幕上的相应区域使用添加动画效果之后的新值重新绘制自身。例如，如果为可绘制对象的颜色属性添加动画效果，则仅当该对象重新绘制自身时，屏幕才会刷新。视图的所有属性 setter（如 setAlpha() 和 setTranslationX()）都会使视图失效，因此，在使用新值调用这些方法时，您无需使视图失效。</p>



<p>不一定需要实现 <em>Animator.AnimatorListener</em> 接口的所有方法，可以使用 <strong>AnimatorListenerAdapter</strong> 类，而非实现接口。<code>AnimatorListenerAdapter</code> 类提供了方法的空实现，可供替换。</p>



<p>例如，以下代码段可仅为 <code>onAnimationEnd()</code> 回调创建 <em>AnimatorListenerAdapter</em>：<em></em></p>



<pre class="wp-block-code"><code>ValueAnimator fadeAnim = ObjectAnimator.ofFloat(newBall, "alpha", 1f, 0f);
fadeAnim.setDuration(250);
fadeAnim.addListener(new AnimatorListenerAdapter() {
    public void onAnimationEnd(Animator animation) {
        balls.remove(((ObjectAnimator)animation).getTarget());
    }
}
</code></pre>



<h2 class="wp-block-heading">在XML中声明属性动画</h2>



<p>属性动画系统支持使用 XML 声明属性动画。通过在 XML 中定义动画，可以轻松地在多个 Activity 中重复使用，而且也更容易编辑。</p>



<p>为了将使用新属性动画 API 的动画文件与使用旧版视图动画框架的动画文件区分开来，从 Android 3.1 开始，属性动画的 XML 文件需要保存到 <code>res/animator/</code> 目录中。</p>



<p>属性动画支持的 Tag 有:</p>



<ul>
<li>ValueAnimator &#8211; &lt;animator&gt;</li>



<li>ObjectAnimator &#8211; &lt;objectAnimator&gt;</li>



<li>AnimatorSet &#8211; &lt;set&gt;<br>以下示例依次播放两组对象动画，其中第一个嵌套集会同时播放两个对象动画：</li>
</ul>



<p><em></em></p>



<pre class="wp-block-code"><code>&lt;set android:ordering="sequentially"&gt;
    &lt;set&gt;
        &lt;objectAnimator
            android:propertyName="x"
            android:duration="500"
            android:valueTo="400"
            android:valueType="intType"/&gt;
        &lt;objectAnimator
            android:propertyName="y"
            android:duration="500"
            android:valueTo="300"
            android:valueType="intType"/&gt;
    &lt;/set&gt;
    &lt;objectAnimator
        android:propertyName="alpha"
        android:duration="500"
        android:valueTo="1f"/&gt;
&lt;/set&gt;
</code></pre>



<p>java 代码中 使用 <code>AnimatorInflater.loadAnimator</code> 获取 AnimatorSet 对象，调用 setTarget() 设置一个目标对象，使用 start 运行即可<em></em></p>



<pre class="wp-block-code"><code>AnimatorSet set = (AnimatorSet) AnimatorInflater.loadAnimator(myContext, R.animator.property_animator);
set.setTarget(myObject);
set.start();
</code></pre>



<p>标签编译后的资源对象分别为 ValueAnimator , ObjectAnimator , or AnimatorSet</p>



<p>XML文件的根元素必须为 &lt;set&gt; , &lt;objectAnimator&gt; , or &lt;valueAnimator&gt; 之一。也可以在一个 set 中组织不同的动画，包含其它 &lt;set&gt; 元素，也就是说，可以嵌套<em></em></p>



<pre class="wp-block-code"><code>&lt;set 
android:ordering=&#91;"together" | "sequentially"]&gt;  &lt;!-- 启动方式是先后顺序还是有同时（default）的--&gt;
    
&lt;!--propertyName 属性名--&gt;
&lt;objectAnimator 
    android:propertyName="string" 
    android:duration="int" 
    android:valueFrom="float | int | color" 
    android:valueTo="float | int | color" 
    android:startOffset="int" 
    android:repeatCount="int" 
    android:repeatMode=&#91;"repeat" | "reverse"] 
    android:valueType=&#91;"intType" | "floatType"]/&gt; 
&lt;animator 
    android:duration="int" 
    android:valueFrom="float | int | color" 
    android:valueTo="float | int | color" 
    android:startOffset="int" 
    android:repeatCount="int" 
    android:repeatMode=&#91;"repeat" | "reverse"] 
    android:valueType=&#91;"intType" | "floatType"]/&gt; 
&lt;set&gt; 
... 
&lt;/set&gt; 
&lt;/set&gt;  
</code></pre>



<ul>
<li>objectAnimator 元素没有暴露 target 属性，因此不能够在<br>XML中执行一个动画，必须通过调用 loadAnimator() 填充你的XML动画资源，并且调用 setTarget() 应<br>用到拥有这个属性的目标对象上</li>
</ul>



<p>还可以在 XML 中声明 ValueAnimator<em></em></p>



<pre class="wp-block-code"><code>&lt;animator xmlns:android="http://schemas.android.com/apk/res/android"
    android:duration="1000"
    android:valueType="floatType"
    android:valueFrom="0f"
    android:valueTo="-100f" /&gt;
</code></pre>



<p>要使用代码中的上一个 ValueAnimator，扩充为 ValueAnimator 对象、添加 AnimatorUpdateListener、更新属性，如下面的代码所示：<em></em></p>



<pre class="wp-block-code"><code>ValueAnimator xmlAnimator = (ValueAnimator) AnimatorInflater.loadAnimator(this,R.animator.animator);
xmlAnimator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
    @Override
    public void onAnimationUpdate(ValueAnimator updatedAnimation) {
        float animatedValue =(float)updatedAnimation.getAnimatedValue();
            textView.setTranslationX(animatedValue);
        }
});
xmlAnimator.start();</code></pre>
