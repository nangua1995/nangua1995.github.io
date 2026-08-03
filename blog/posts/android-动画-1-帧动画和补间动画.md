> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/03/20/android-%e5%8a%a8%e7%94%bb-1-%e5%b8%a7%e5%8a%a8%e7%94%bb%e5%92%8c%e8%a1%a5%e9%97%b4%e5%8a%a8%e7%94%bb/)

<p>在移动开发中，动画可以丰富页面的 UI 效果，一个动画包含以下几个元素</p>



<ul>
<li>控件： 想实现动画的 View 等</li>



<li>时长：动画的时长</li>



<li>起始值，结束值：动画从开始和结束的值（比如移动，就是坐标值）</li>



<li>插值器：定义了动画变化的速率</li>
</ul>



<p>动画包含三大类型：帧动画（Frame），补间动画（Tween），属性动画（Property）</p>



<p></p>



<h2 class="wp-block-heading">帧动画 (Frame）</h2>



<p>顺序播放一组预先定义好的图。</p>



<ul>
<li>首先在 res/drawable/目录下定义xml，根节点为<code>animation-list</code>，设置动画播放的帧资源</li>



<li>使用 <code>AnimationDrawable</code> 加载定义好的资源</li>
</ul>



<p><em></em></p>



<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;animation-list xmlns:android="http://schemas.android.com/apk/res/android"
    android:oneshot="false" &gt;
    &lt;item android:drawable="@drawable/wifi1" android:duration="500"/&gt;
    &lt;item android:drawable="@drawable/wifi2" android:duration="500"/&gt;
    &lt;item android:drawable="@drawable/wifi3" android:duration="500"/&gt;
    &lt;item android:drawable="@drawable/wifi4" android:duration="500"/&gt;
    &lt;item android:drawable="@drawable/wifi5" android:duration="500"/&gt;
&lt;/animation-list&gt;</code></pre>



<blockquote class="wp-block-quote">
<ul>
<li><code>oneshot</code> 是否只展示一遍，设置为false会不停的循环播放动画</li>



<li>根标签下，通过<code>&lt;item&gt;</code>标签对动画中的每一个图片进行声明
<ul>
<li><code>drawable</code> 要播放的图片</li>



<li><code>duration</code> 展示该图片的时间长度</li>
</ul>
</li>
</ul>
</blockquote>



<p>使用<code>AnimationDrawable</code> 播放动画<em></em></p>



<pre class="wp-block-code"><code>view.setBackground(R.drawable.frame_animation);
AnimationDrawable animation = (AnimationDrawable)view.getBackground();
animation.start();</code></pre>



<h2 class="wp-block-heading">补间动画（Tween ）</h2>



<p>补间动画也称作 View 动画，只要定义 View，设置它开始和结束的位置，中间的 View 会由系统自动补齐，不需要准备每一帧动画。<br>View 动画主要支持四种效果：平移、缩放、旋转、透明度。实现这几种动画的类，都是 Animation 的子类。<br>使用这种动画可以通过在 xml 中实现，也可以在 类文件中定义。</p>



<h3 class="wp-block-heading">TranslateAnimation</h3>



<p>平移动画，对应标签为 <code>&lt;translate&gt;</code></p>



<ul>
<li>android:fromXDelta 起始 x 坐标</li>



<li>android:toXDelta 结束 x 坐标</li>



<li>android:fromYDelta 起始 y 坐标</li>



<li>android:toYDelta 结束 y 坐标</li>
</ul>



<blockquote class="wp-block-quote">
<p>数值的表示方式如下：<br>数字：如10，表示当前坐标位置<br>百分比：如10%，表示当前 View 的坐标 + View 控件长度 10%<br>百分数p：如10%p，表示当前View的坐标 + 父控件长度 50%</p>
</blockquote>



<p>范例：<em></em></p>



<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;translate xmlns:android="http://schemas.android.com/apk/res/android"
    android:duration="1000"
    android:interpolator="@android:anim/decelerate_interpolator"
    android:fromXDelta="0"
    android:fromYDelta="0"
    android:toXDelta="100"
    android:toYDelta="100"/&gt;
</code></pre>



<p>在 java / kotlin 中使用该文件<em></em></p>



<pre class="wp-block-code"><code>Animation animation = AnimationUtils.loadAnimation(this, R.anim.anim_translate);
view.startAnimation(animation);
</code></pre>



<blockquote class="wp-block-quote">
<p>其中 duration 是动画的时长，interpolator 是动画的插值器，来定义动画变化的速率，每一种动画都具有这两个属性，还有一些其他的公共属性可配置，可以慢慢尝试。</p>
</blockquote>



<p>类实现，等同于上面的配置（后面的几种动画实现方式是一样的）<em></em></p>



<pre class="wp-block-code"><code>// view 在 1s 间从(0, 0) 移动到 (100, 100)
TranslateAnimation animation = new TranslateAnimation(0, 0, 100, 100);
animation .setDuration(1000);
animation .setInterpolator(new DecelerateInterpolator());
view.startAnimation(animation);
</code></pre>



<ul>
<li>TranslateAnimation 还有一个重载的构造函数</li>
</ul>



<p><em></em></p>



<pre class="wp-block-code"><code>/**
 * @param fromXType 动画开始前的X坐标类型。取值范围为 ABSOLUTE（绝对位置）、RELATIVE_TO_SELF（以自身宽或高为参考）、RELATIVE_TO_PARENT（以父控件宽或高为参考）
 * @param fromXValue 动画开始前的X坐标值。当对应的 Type 为ABSOLUTE时，表示绝对位置；否则表示相对位置，1.0表示100%
 * @param toXType 动画结束后的 X 坐标类型
 * @param toXValue 动画结束后的 X 坐标值
 * @param fromYType 动画开始前的 Y 坐标类型
 * @param fromYValue 动画开始前的 Y 坐标值
 * @param toYType 动画结束后的 Y 坐标类型
 * @param toYValue 动画结束后的 Y 坐标值
*/
public TranslateAnimation(int fromXType, float fromXValue, int toXType, float toXValue,
            int fromYType, float fromYValue, int toYType, float toYValue)
</code></pre>



<h3 class="wp-block-heading">ScaleAnimation</h3>



<p>缩放动画，对应标签 <code>&lt;scale&gt;</code></p>



<ul>
<li>fromXScale、 fromYScale 起始缩放值</li>



<li>toXScale、toYScale 目标缩放值</li>



<li>pivotX、pivotY 缩放的中心位置</li>
</ul>



<p><em></em></p>



<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;scale xmlns:android="http://schemas.android.com/apk/res/android"
    android:duration="1000"
    android:fromXScale="1.0"
    android:fromYScale="1.0"
    android:pivotX="50%"
    android:pivotY="50%"
    android:toXScale="2.0"
    android:toYScale="2.0"/&gt;
</code></pre>



<ul>
<li>ScaleAnimation 有三个构造函数</li>
</ul>



<p><em></em></p>



<pre class="wp-block-code"><code>public ScaleAnimation(float fromX, float toX, float fromY, float toY) 

public ScaleAnimation(float fromX, float toX, float fromY, float toY,  float pivotX, float pivotY)

/**
 * @param fromX X坐标初始值
 * @param toX X坐标目标值
 * @param fromY Y坐标初始值
 * @param toY Y坐标目标值
 * @param pivotXType 缩放中心点的X坐标类型。取值范围有三种
 *        Animation.ABSOLUTE（绝对坐标）
 *        Animation.RELATIVE_TO_SELF（相对于自身View)
 *        Animation.RELATIVE_TO_PARENT（相对于父控件的坐标）
 * @param pivotXValue 缩放中心点的X坐标值当对应的 Type 为ABSOLUTE时，表示绝对位置；否则表示相对位置，1.0表示100%
 * @param pivotYType 缩放中心点的Y坐标类型
 * @param pivotYValue 缩放中心点的Y坐标
*/
public ScaleAnimation(float fromX, float toX, float fromY, float toY,  
                      int pivotXType, float pivotXValue, int pivotYType, float pivotYValue)
</code></pre>



<p><em></em></p>



<pre class="wp-block-code"><code>// 以view中心为缩放点，放大两倍
ScaleAnimation animation = new ScaleAnimation(
        1.0f, 2.0f, 1.0f, 2.0f,
        Animation.RELATIVE_TO_SELF, 0.5f, Animation.RELATIVE_TO_SELF, 0.5f
);
animation.setDuration(1000);
view.startAnimation(animation);
</code></pre>



<h3 class="wp-block-heading">RotateAnimation</h3>



<p>旋转动画，对应标签 <code>&lt;rotate&gt;</code></p>



<ul>
<li>fromDegree 旋转的起始角度</li>



<li>toDegree 旋转的结束角度</li>
</ul>



<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;rotate xmlns:android="http://schemas.android.com/apk/res/android"
      android:fromDegree="0"
      android:toDegree="90"
      android:pivotX = "50%"
      android:pivotY="50%"
      android:duration = "3000"
/&gt;
</code></pre>



<p><em></em></p>



<pre class="wp-block-code"><code>/**
 * @param fromDegrees 旋转的起始角度
 * @param toDegrees 旋转的结束角度
 * 默认旋转中心点为 （0, 0）
 */
public RotateAnimation(float fromDegrees, float toDegrees) 
 
public RotateAnimation(float fromDegrees, float toDegrees, float pivotX, float pivotY)
    
/**
 * @param fromDegrees 旋转的起始角度
 * @param toDegrees 旋转的结束角度
 * @param pivotXType 
 * @param pivotXValue
 * @param pivotYType
 * @param pivotYValue
 */
public RotateAnimation(float fromDegrees, float toDegrees, int pivotXType, float pivotXValue,
        int pivotYType, float pivotYValue) {
</code></pre>



<h3 class="wp-block-heading">AlphaAnimation</h3>



<p>透明度动画，对应标签<code>&lt;alpha&gt;</code><em></em></p>



<pre class="wp-block-code"><code>/**
 * @param fromAlpha 动画开始透明度 0~1
 * @param toAlpha 动画结束透明度
 */
public AlphaAnimation(float fromAlpha, float toAlpha) 
</code></pre>



<h3 class="wp-block-heading">AnimationSet</h3>



<p>AnimationSet 也继承于 Animation，可以同时处理多组动画，比如在平移的时候旋转等。</p>



<p>构造参数有一个参数，表示所添加的动画是否都共用一个插值器<em></em></p>



<pre class="wp-block-code"><code>/**
 * @param shareInterpolator 
 */
public AnimationSet(boolean shareInterpolator) {
</code></pre>



<p>常用的方法如下<em></em></p>



<pre class="wp-block-code"><code>// 添加动画
animationSet.addAnimation(new TranslateAnimation(0, 0, 100, 100));
// 设置插值器 默认 @android:anim/accelerate_decelerate_interpolator--&gt; android:interpolator="`@android:anim/linear_interpolator`"
animationSet.setInterpolator(new LinearInterpolator());
// 设置动画持续时长，默认 0 --&gt; android:duration="3000"
animationSet.setDuration(3000);
//设置动画结束之后是否保持动画的目标状态，默认 false --&gt; android:fillAfter="true"
animationSet.setFillAfter(true);
//设置动画结束之后是否保持动画开始时的状态，默认 ture --&gt; android:fillBefore="false"
animationSet.setFillBefore(false);
// 设置重复模式，RESTART(1) 顺序播放，REVERSE(2) 重复时逆向播放 android:repeatMode
animationSet.setRepeatMode(AnimationSet.REPEAT);
//设置重复次数，默认 0 --&gt; android:repeatCount=-1
animationSet.setRepeatCount(AnimationSet.INFINITE);
//设置动画延时时间，默认 0 --&gt; android:startOffset="2000"
animationSet.setStartOffset(2000);
//取消动画
animationSet.cancel();
//重置动画
animationSet.reset();
</code></pre>



<p>为 View 设置动画<em></em></p>



<pre class="wp-block-code"><code>//开始动画
view.startAnimation(animationSet);</code></pre>
