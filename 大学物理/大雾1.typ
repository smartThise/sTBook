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

我们又来讨论 Rotation 了。Rotation 也有“非惯性系”。考虑一个盘子，有固有角速度 $omega$，圆心处有一个物体径向射出，速度为 $v_0$。

我们先假设一个物体在最简单的情况：只是站在圆盘上，以 $v$ 的速度往前走

则 $T=m v^2/r = m (v^'+omega r)^2 /r = m v^'^2 / r +2m v ^' omega + m omega^2 r$，这些东西分别叫做：非惯性系内向心力、科里奥利力、离心力。

科里奥利力是一个用来解释为什么你在参考系里像“后偏/前压”的力。当你从中心向边缘走的时候，你感受到的力是向后的，当你从边缘向中心走的时候，你感受到的力是向前的。这个力的大小取决于你的速度、角速度和距离。*方向始终由* $omega  times v$ *决定！*

一个典型的运用：傅科摆。

=== (3) Momentum
==== 1. Center of Mass
$vct(r_c)=(sum_i m_i vct(r_i)) / (sum _i m_i)$ or for uniform: $vct(r_c)=(integral rho vct(r) dif V) / (integral rho dif V)$

For each particle, 
$ m_i vct(a)_i = vct(F)_i + sum_(j != i) vct(f)_(i j) $

$ sum_i m_i vct(a)_i = sum_i vct(F)_i + sum_i sum_(j != i) vct(f)_(i j) $

*内力抵消！！！*

$ sum_i m_i vct(a)_i = sum_i vct(F)_i $

$ M vct(a)_C = sum_i vct(F)_i $

*(Euler's 1st Law)*

==== 2. Momentum
$vct(p)=m vct(v)$

$vct(F)=m dfrac(vct(v),t)=dfrac(m vct(v),t)=dfrac(vct(p),t) \
=> vct(F) dif t= dif vct(p),Delta vct(p)=integral vct(F) dif t,(sum vct(F_i))dif t= dif vct(p)$

$vct(P)=sum_i vct(p)_i = sum_i m_i vct(v)_i = (sum_i m_i) dfrac(vct(r_c),t)=M vct(v_c)$

推导出来：动量守恒定律！

$sum_i vct(F)_i = 0 => sum_i vct(p)_i = "const" $

朝花夕拾：火箭起飞问题

原始的完整式子：$M v=(M-dif m)(v + dif v) + dif m(-u+v)$，其中 $dif m$ 是火箭发射出去的燃料质量，$u$ 是燃料的喷射速度，$v$ 是火箭的速度，$M$ 是火箭的总质量。为什么两个都有 $ dif v$ 呢？这是因为火箭发射燃料时，燃料和火箭一起运动，所以火箭的速度和燃料的速度是相同的。

$M dif v=-u dif M$

$integral_0^v dif v = -u integral_(M_0)^(M_f) (dif M) / M \
=> v = -u ln(M_f/M_0)=u ln (M_0/M_f) \
$

==== 3. Angular Momentum

旋转不满足交换律。*角速度可以被定义为向量，方向沿轴（右手定则）*。

$vct(omega)=dfrac(theta,t)vct(e)$

举例：开普勒第二定律，即面积定律。面积定律指出，行星绕太阳运动的轨道面积与时间成正比。这可以通过角动量守恒定律来解释。

$
S= ((vct(r) times vct(v)) Delta t) / 2 = L/(2m) Delta t ;vct(L)=vct(r) times m vct(v)=vct(r) times vct(p) \
=> |vct(L)|=r m omega r=m omega r^2 "(only in circular motion)" \
$

另一个例子：圆锥摆

$
|vct(v)|= omega l sin theta \
|vct(L_O)|= l sin theta m omega l sin theta = m omega l^2 sin^2 theta "以底盘原点为中，此时角动量唯一且始终竖直向上，守恒"\

|vct(L_(O^'))|= l m omega l sin theta = m omega l^2 sin theta \ "以悬挂点为中心，角动量垂直于线，分解后竖直分量守恒，水平分量大小不变、方向始终背离圆心"\

"因此我们可以讨论（微元法/神秘分析）：" (|Delta vct(L_(O^'))|) /( Delta t ) = |Delta vct(L_(O^'))| cos theta omega = |vct(togrog)| = l m g sin theta = ... "反正最后发现本质相等"  \

"至于是怎么发现的：有一个很神秘的点请你注意到，那就是他妈的力矩的计算式子，叉乘的魅力这一块"\

dfrac(vct(L),t) = dfrac((vct(r) times vct(p)),t)= vct(r) times dfrac(vct(p),t)+vct(p) times dfrac(vct(r),t) = vct(r) times vct(F)  = vct(togrog) "力矩"
\

$

这个时候对于这个神秘的圆锥摆，我们很容易发现：（受力分析得到两力关系什么的）

$
cos theta = g/(omega^2 l) => theta = arccos(g/(omega^2 l)) \
$

*现在告诉你什么是角动量守恒：合力矩为零，角动量守恒。*

==== 4. System of Particles

有一堆神秘且漫长的消除、计算等等等等各种神秘的过程，最后得到一个结论：*内力矩相互抵消，只看外力矩。*

即：$sum_i vct(r_i) times vct(F_i) = dfrac((sum_i vct(L_i)),t)$

另一个例子：一个小球在正中间撞上了一根轻杆。

===== 定轴转动碰撞实验：角动量守恒与线动量丢失

在有固定转轴 $O$ 的系统中，当质量为 $m_2$ 的质点以 $v_0$ 撞击质量为 $m_1$ 的单摆中点时：

*角动量守恒 (Conservation of Angular Momentum)*

由于支点 $O$ 的瞬时冲力通过轴心，对 $O$ 点的力矩 $tau_O = 0$，故系统角动量守恒。
设碰撞后系统的共同角速度为 $omega$，则有：
$ m_2 v_0 l/2 = (m_2 (l/2)^2 + m_1 l^2) omega $

解得碰撞后的角速度：
$ omega = (2 m_2 v_0) / ((m_2 + 4 m_1) l) $

*线动量分析 (Linear Momentum Analysis)*

我们对比碰撞前后的系统总线动量 $P$：
- *碰撞前*：$P_"before" = m_2 v_0$
- *碰撞后*：
$ P_"after" &= m_2 v_(m_2) + m_1 v_(m_1) \
            &= m_2 (omega l/2) + m_1 (omega l) \
            &= (m_2/2 + m_1) l omega $

将 $omega$ 的表达式代入上式：
$ P_"after" &= (m_2/2 + m_1) l dot (2 m_2 v_0) / ((m_2 + 4 m_1) l) \
            &= (m_2 + 2 m_1) / (m_2 + 4 m_1) m_2 v_0 $

*结论*：

由于系数满足：
$ (m_2 + 2 m_1) / (m_2 + 4 m_1) < 1 $

故得出结论：
$ P_"after" < P_"before" $

*结论分析*：虽然系统的合外力矩为零导致角动量守恒，但由于支点 $O$ 在碰撞瞬间产生了向后的瞬时冲量 $vct(I)_O$，该外力导致了系统线动量的丢失。

===== 另一个例子：太典，跷跷板

$togrog=m_1 g l cos theta - m_2 g l cos theta = dif / (dif t) (-m_1 omega l^2-m_2 omega l^2) \
=> -(m_1+m_2) omega l^2 dfrac(omega,t) dif theta= (m_1-m_2) g l cos theta dif theta \
=> integral_(omega_0)^0 (m_1+m_2) l^2 omega dif omega = integral_(theta_0)^(- theta_0) (m_1-m_2) g l dif (sin theta)  \
=> omega_0 = 2/l sqrt(((m_1-m_2)g h) / (m_1+m_2))
$

哥们，神了。在质心系里面有奇妙的现象：

$
vct(r_c)=(sum_i m_i vct(r_i)) / (sum _i m_i) \ 
=> vct(r_i^')=vct(r_i)-vct(r_c) \
sum_i m_i vct(r_i^')=sum_i m_i vct(r_i) - sum_i m_i vct(r_c)  =0 \

"导数也为" 0, "所以质心系里面动量守恒" \
sum_i vct(F_i) =dfrac(vct(P_c),t)
$

以及神秘的质心系里的分配。假设两个质量快一上一下中间有根绳子。假设它们都向水平方向飞过去，那么获取质心：
$
v_c=(m_1 v_1+m_2 v_2) / (m_1+m_2) \
l_1=(m_2 l_2) / (m_1+m_2) \
l_2=(m_1 l_1) / (m_1+m_2) \
$

假设它们不同方向飞行：
#let vct(x) = $bold(arrow(#x))$

这部分内容推导了双质心系统在质心参考系（COM-frame）下的动力学描述及张力 $T$ 的求解。

首先定义质心速度 $v_c$：
$ v_c = (m_1 v_1 + m_2 v_2) / (m_1 + m_2) $

在质心系中，各质点的相对速度 $v_i'$ 为：
$ v_1' = v_1 - v_c = v_1 - (m_1 v_1 + m_2 v_2) / (m_1 + m_2) = - m_2 / (m_1 + m_2) (v_2 - v_1) $
$ v_2' = v_2 - v_c = v_2 - (m_1 v_1 + m_2 v_2) / (m_1 + m_2) = m_1 / (m_1 + m_2) (v_2 - v_1) $

由此可以定义系统的转动角速度 $omega$。由于 $m_1$ 和 $m_2$ 绕质心转动的半径分别为 $r_1 = m_2 / (m_1 + m_2) l$ 和 $r_2 = m_1 / (m_1 + m_2) l$，则有：
$ omega = (|v_1'|) / r_1 = (|v_2'|) / r_2 = (v_2 - v_1) / l $

最后，利用向心力公式求解绳子或杆的张力 $T$：
$ T = m_1 omega^2 r_1 = m_1 omega^2 (m_2 / (m_1 + m_2) l) $
$ T = m_2 omega^2 r_2 = m_2 omega^2 (m_1 / (m_1 + m_2) l) $

整理可得：
$ T = (m_1 m_2) / (m_1 + m_2) omega^2 l $

其中 $(m_1 m_2) / (m_1 + m_2)$ 即为该系统的折合质量 (Reduced Mass)。

不是哥们，真神了！为什么到底为什么这么强？！

同样的道理，你再看看角动量呢？！

$
vct(L_i)=vct(r_i) times m_i vct(v_i) \
sum_i vct(L_i) = vct(L_c) +sum_i vct(L_i^') "COM 的神秘力量！！！" \
= vct(r_c) times sum_i m_i vct(v_i) + sum_i vct(r_i^') times m_i vct(v_i^') \
"然后！！！"
\

vct(r_i)=vct(r_i^')+vct(r_c) \
sum_i vct(L_i) = sum_i vct(r_i) times m_i dfrac(vct(r_i),t) \
= sum_i (vct(r_c)+vct(r_i^')) times m_i (dfrac(vct(r_i^'),t)+dfrac(vct(r_c),t))  \

=  "消元之后" vct(r_c) times sum_i m_i vct(v_c)+ sum_i vct(r_i^') times m_i dfrac(vct(r_i^'),t) \
$

还有一个神秘的式子，听见你说：
$
dfrac(sum_i vct(L_i),t)=sum_i vct(togrog_i) \
dfrac(sum_i vct(L_i^'),t)=sum_i vct(r_i^') times vct(F_i) \
= "消元消元大消元" sum_i (vct(r_i)-vct(r_c)) times vct(F_i) \
$

== 二、 Energy 

回顾：质心说什么？！

$$