> 原文发布于主站：[查看原文](https://zhinengzuocang.cn/2024/10/22/gradle-%e6%9c%ac%e5%9c%b0%e9%85%8d%e7%bd%ae%e8%a6%81%e6%94%be%e5%9c%a8%e5%93%aa%e4%b8%aa%e8%b7%af%e5%be%84%e4%b8%8b-%e6%9d%a5%e8%87%aa%e7%ae%80%e4%b9%a6-evenzhu/)

<p>因为梯子问题，有些时候会出现gradle下载不下来的问题，可以通过将gradle的压缩包下载下来然后放在对应路径下的方式解决。如下步骤：</p>



<p>1.导入你的项目（会卡在下载gradle，但是会在本地生成一些文件，本地配置关键就是要找到生成文件的位置）：</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="606" src="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-38-1024x606.png" alt="" class="wp-image-796" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-38-1024x606.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-38-300x178.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-38-768x455.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-38.png 1500w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>2.找到你的Gradle自动生成的网络Gradle下载文件路径：</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="289" src="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-39-1024x289.png" alt="" class="wp-image-797" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-39-1024x289.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-39-300x85.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-39-768x217.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-39.png 1500w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>3.去下载Gradle3.3版本（或者你项目中配置的Gradle对应版本——取决于你dists下面的gradle版本，我的是gradle-3.3），网站 https://services.gradle.org/distributions/</p>



<p>4.把你刚才下载好的gradle-xx-all/bin.zip放到刚才生成的那个“乱码”路径下,不需要解压zip：</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="259" src="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-40-1024x259.png" alt="" class="wp-image-798" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-40-1024x259.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-40-300x76.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-40-768x194.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-40.png 1500w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>5.重新导入你的项目，搞定：</p>



<p>6.如果你没有成功，那么说明你dists下的gradle版本和你项目中的gradle版本不一致，怎么办：</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="400" src="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-43-1024x400.png" alt="" class="wp-image-801" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-43-1024x400.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-43-300x117.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-43-768x300.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-43.png 1500w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="284" src="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-42-1024x284.png" alt="" class="wp-image-800" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-42-1024x284.png 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-42-300x83.png 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-42-768x213.png 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/image-42.png 1458w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>



<p>另外需要关注工程设置中配置的gradle本地位置：比如下面，就需要将下载下来的文件放在对应路径下的wrapper-dists-乱码路径下而不是上面的home目录下</p>



<figure class="wp-block-image size-large"><img decoding="async" loading="lazy" width="1024" height="577" src="https://zhinengzuocang.cn/wp-content/uploads/2024/10/img_v3_02ft_70c614bb-9787-48b5-90d1-f0e372aed32g-1024x577.jpg" alt="" class="wp-image-803" srcset="https://zhinengzuocang.cn/wp-content/uploads/2024/10/img_v3_02ft_70c614bb-9787-48b5-90d1-f0e372aed32g-1024x577.jpg 1024w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/img_v3_02ft_70c614bb-9787-48b5-90d1-f0e372aed32g-300x169.jpg 300w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/img_v3_02ft_70c614bb-9787-48b5-90d1-f0e372aed32g-768x433.jpg 768w, https://zhinengzuocang.cn/wp-content/uploads/2024/10/img_v3_02ft_70c614bb-9787-48b5-90d1-f0e372aed32g.jpg 1291w" sizes="(max-width: 1024px) 100vw, 1024px" /></figure>
