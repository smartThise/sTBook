#import "../module/myutils.typ":*
#show:conf

#outline()

= 〇 机械运动
== 一、运动学的基础概念 #datetime(day:4,month:3,year:2026).display()
=== (1) Displacement, speed, acceleration, velocity
average speed: $ overline(s)= frac("total distance",Delta t)$

average velocity: $ overline(v)= frac(Delta x,Delta t)$

velocity: $v=lim_(Delta t -> 0) frac(Delta x,Delta t)= frac(\dx , \dt)$

acceleration: $a=lim_(Delta t ->0) frac(Delta v,Delta t)= frac(\dv , \dt)=frac(d^2x,\dt^2)$

$integral_(v_0)^v \dv=integral_(t_0)^t a(t)\dt => v=v_0 +integral_(t_0)^t a(t)\dt$

$integral_(x_0)^x \dx=integral_(t_0)^t v(t)\dt => a(x-x_0)=integral_(v_0)^v v(t)\dv =>v^2-v_0^2=2a(x-x_0)$

In 3D World,we can also say that-- 三个分量决定一切！导数也是三个导分量组成的！举个例子：$arrow(a)=frac(d^2 x,d t^2)arrow(i)+frac(d^2 y,d t^2)arrow(j)$

Something interesting: $|arrow(v)|=frac(\ds,\dt)$

==== 1. Free Fall & Throwing
$
  v_y=v_(0y) - \gt \
  Delta t=v_(0y)/g \
  y=1/2 \gt^2=v_(0y)^2 / (2g)\
  "For throwing: "T=2 sqrt((2h)/g)
$

==== 2. Circular

$
  theta = omega t \
  omega = (d theta) / (d t) \
  "("arrow(omega)": angular velocity)" \
  arrow(v)=R cos(omega t) arrow(i)+R sin(omega t) arrow(j) \
  arrow(v)=(d r)/(d t)=-omega R sin(omega t) arrow(i)+omega R cos(omega t) arrow(j) \
  |arrow(v)|=omega R \
  "Centripetal acceleration: "arrow(a)=-omega^2 R cos(omega t) arrow(i)-omega^2 R sin(omega t) arrow(j) \
  |arrow(a)|=omega ^2 R
$

==== 3. Polar coordinate
$
  arrow(e_r)=cos theta arrow(i)+ sin theta arrow(j) \ 
  arrow(e_theta)=-sin theta arrow(i) + cos theta arrow(j) \ 
  frac(d arrow(e_r),d theta)=arrow(e_theta) \
  frac(d arrow(e_theta),d theta)=-arrow(e_r) \
  arrow(r)=r arrow(e_r) \
  frac(d r,d t) = frac(d r,d t)arrow(e_r)+r frac(d r,d arrow(e_r))=frac(d r,d t)arrow(e_r)+arrow(w)r arrow(e_theta) \
  arrow(a)=frac(d arrow(v),d t)=d/(d t)(frac(d r,d t)arrow(e_r)+r frac(d r,d arrow(e_r)))="(after a long process) " ((d^2 r)/(d t^2)-omega^2 r)arrow(e_r)+(r (d w)/(d t)+2 omega (d r)/(d t))arrow(e_theta)
$

Review #datetime(day:9,month:3,year:2026).display()

$Delta vct(r) != Delta |vct(r)| = Delta r \ |dif vct(r)|=dif s$

划船速度分解问题的真实严谨解法：

$x^2+y^2=r^2$，求导，
$2x dif x + 2y dif  y = 2 r dif r$，由于竖直方向没有速度，所以 $dif y=0$，所以 $dif r = (x/r) dif x$，所以划船的速度是 $vct(r)= (x/r) vct(x)$，即三角函数：$dfrac(x,t)=v_0 / (sin theta)$

还有奇怪的合成分解向量的求导：

$vct(r_(P O))=vct(r_(P O^'))+vct(r_(O O^'))$，求导后 $dfrac(vct(r_(P O)),t)=dfrac(( vct(r_(P O^'))),t)+dfrac((vct(r_(O O^'))),t)$，目前在 Translatimal 平动体系讨论。

纯滚动：
当最底部的点与地面接触时，$- omega R + v_0 = v_P= 0$，所以 $v_0 = omega R$。在并非顶点的时候，则是分量运算，比如说把最低点半径、当前位置半径的夹角叫做 $theta$，则 $v_P = 2 v_0 sin (theta/2)$。\*需要补图片。

=== (2) Newton's Laws
==== 1. Newton's First Law & Second Law
$vct(F)=0 => vct(v)="const" or vct(v)=0$

*Only useful in inertial (reference) frames 惯性参考系*

那么 non-inertial frame 怎么办？

举例：线性阻力的下落过程。对于一个物体自由落体，一个物体向上抛出，分别如下：

- for free fall:

$m g- alpha m v_1=m dfrac(v_1,t)$

Then $integral_0^t dif t= integral_0^(v_1) frac(dif v_1,g - alpha v_1)$, and $- alpha t= ln(g - alpha v_1) - ln(g) => v_1(t)=g/ alpha (1- e^(- alpha t))$,我的天哪神秘的积分！

- for throwing:

$m g - alpha m v_2 = m dfrac( v_2,  t) \ => integral_0^t dif t=integral_(-v_0)^(v_2) frac(dif v_2,g - alpha v_2) \ => 
v_2(t)=g / alpha - (g / alpha + v_0) e^(- alpha t)
$

把这两个再混合到一起：
$integral_0^(t_0) v_1(t) dif t=h+ integral_0^t v_2(t_0) dif t \
 => integral_0^(t_0) (v_1(t)-v_2(t)) dif t=h \
 => integral_0^(t_0) (g/alpha (1-e^(-alpha t))- (g/alpha - (g/alpha + v_0) e^(-alpha t))) dif t=h \
 => integral_0^(t_0) v_0 e^(-alpha t) dif t=h$

 ==== 2. Non-inertial frame
$vct(a_(O^'))+vct(a^')=vct(a)$

So $vct(a^')=vct(a)-vct(a_(O^'))$，其中 $vct(a_(O^'))$ 是非惯性参考系的加速度。同理，$vct(F)-m vct(a_(O^'))=m vct(a^')$

本质是为了减小运算难度。

比如在上面的例子，加入惯性力竖直向上的 $m g$， 则 $m g + alpha m vct(v_2^') #text(fill:blue,$- m g$) = m dfrac(v_2^', t) \
=> v_2^'=-v_0 e^(-alpha t) \
=> h = integral_0^(t_0) v_0 e^(-alpha t) dif t$

答案居然一样！因为我们在非惯性参考系中引入了一个等效的力来抵消非惯性参考系的加速度，所以最终的结果与在惯性参考系中计算得到的结果是相同的。这提醒我们，在非惯性参考系中引入惯性力是为了简化计算，但最终的物理结果应该与在惯性参考系中得到的结果一致。

举例：潮汐力

- 近日侧：$F_A=(G M_s m)/(R - r)^2-(G M_s m)/R^2 approx 2(G M_s m)/(R^3) r$，方向朝向太阳，向外拉伸。
- 远日侧：$F_B=(G M_s m)/(R + r)^2-(G M_s m)/R^2 approx - 2(G M_s m)/(R^3) r$，方向背向太阳，同样向外拉伸。
- 侧面，距离太太阳 $sqrt(R^2+r^2)$：引力在 x 方向分量和惯性力在 x 方向分量几乎相等，所以没有拉伸。在 y 方向上，$F_(-y)=-(G M_s m)/R^3 r$，向内压缩，系数恰好是近日远日点的一半。

