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

- $1/2 m v^2$ *Kenetic Energy*
  - How to get it?
  $m (dif^2 x)/(dif t^2)=F(x) 
  \ m (dif^2 x)/(dif t^2) dif x = F(x) dif x \
  \ m dfrac(v,t) dif x = F(x) dif x
  \ => integral_0^t m v dif v = integral_0^t F(x) dif x \ 
  => 1/2 m v^2 - 1/2 m v_0^2 = integral_(x_0)^(x_t) F(x) dif x \ $
- $integral_(x_0)^(x_t) F(x) dif x= W_(x(t) x_0)=W_0^t$ *Work* on the object by the force

同理，对弹簧进行积分，得到：$1/2 k x^2$ *Potential Energy*

在*三维世界*里面，
$
  m dfrac(vct(v),t) = vct(F)(vct(r)) \ 
  m dfrac(vct(v),t) dif vct(r) = vct(F)(vct(r)) dif vct(r) \
  integral m vct(v) dif vct(v) = integral vct(F)(vct(r)) dif vct(r) \
  = integral dif(1/2 m v^2) = integral vct(F)(vct(r)) dif vct(r) = 1/2 m v^2 - 1/2 m v_0^2 = Delta K
$



=== 1. 动能定理 (Work-Energy Theorem)
合外力做的功等于物体动能的增量：
$ W = integral vct(F) dot d vct(r) = Delta K = 1/2 m v^2 - 1/2 m v_0^2 $
*物理意义 (Significance)*：建立了力场空间分布与物体运动状态的联系。

=== 2. 基础保守力实例 (Basic Conservative Forces)

- *重力 (Gravity)*：$F(y) = -m g$。
  $ W_G = integral_(h_0)^h (-m g) thin dif y = -m g h + m g h_0 $
- *弹性力 (Elastic Force)*：$F(x) = -k x$。
  $ W_s = integral_(x_0)^x (-k x) thin dif x = -1/2 k x^2 + 1/2 k x_0^2 $

=== 3. 有心力的路径无关性证明 (Central Force Path Independence)

设*有心力* (Central Force) 为 $vct(F)(vct(r)) = f(r) vct(e)_r$。在极坐标中，元位移分解为径向和切向：
$ dif vct(r) = (dif r) vct(e)_r + r d theta vct(e)_theta $


计算元功 (Infinitesimal Work)：
$ dif W = vct(F) dot dif vct(r) = f(r) dif r $
*推论 (Conclusion)*：切向分量 $r d theta$ 对功无贡献，因此功的大小只取决于始末径向距离 $r$，即*有心力必为保守力*。

=== 4. 引力势能模型 (Gravitational Potential Energy Model)

针对*平方反比力*(Inverse-Square Force)，令 $f(r) = -A/r^2$（如引力，$A=G M m$）：
$ W = integral_(r_0)^r (-A / r^2) d r = [A / r]_(r_0)^r = A / r - A / r_0 $

==== 势能函数 (Potential Energy Function)
物理学定义势能变化量为功的负值 $Delta U = -W$。若取无穷远处为零势能参考点 ($r_0 arrow.r oo$)：
$ U(r) = - A / r $


*图像特性 (Graph Characteristics)*：
  1. *负值 (Negative Value)*：代表引力束缚态 (Bound State)。
  2. *渐近线 (Asymptote)*：当 $r arrow.r 0$ 时，$U(r) arrow.r -oo$；当 $r arrow.r oo$ 时，$U(r) arrow.r 0$。
  3. *斜率 (Slope)*：曲线的斜率 $d U / d r$ 即对应于力的大小（负梯度）。

// 定义向量和梯度算符
#let vct(x) = $arrow(bold(#x))$
#let grad = $nabla$

#text(fill: rgb("#1a4a7c"), weight: "bold")[核心概念：势能变化与梯度力场 (Potential Energy & Gradient Force Field)]

---

=== 1. 势能的基本定义 (Definition of Potential Energy)

势能的变化量 $Delta U$ 定义为保守力做功的负值：
$ Delta U = -W = - integral_(vct(r)_0)^(vct(r)) vct(F) dot dif vct(r) $

- *重力情况*：$Delta U = m g h - m g h_0$
- *弹力情况*：$Delta U = 1/2 k x^2 - 1/2 k x_0^2$

=== 2. 力与势能的微分关系 (Differential Relationship)

在微小位移 $Delta x$ 下，功可以近似为 $W approx F(x) Delta x$，因此：
$ Delta U approx -F(x) Delta x $

取极限 $Delta x arrow.r 0$，得到一维下的基本关系：
$ (dif U) / (dif x) = -F(x) quad arrow.r.double quad F(x) = - (dif U) / (dif x) $
*物理直观*：力总是指向势能降低最快的方向。

=== 3. 梯度算符与高维推广 (The Gradient Operator $nabla$)

在三维空间中，力是一个矢量，而势能是一个标量场。板书上的“倒三角”符号 $nabla$（读作 Nabla 或 Del）代表*梯度算符*：

$ vct(F) = -nabla U $


其展开形式为：
$ vct(F) = -( (partial U) / (partial x) vct(i) + (partial U) / (partial y) vct(j) + (partial U) / (partial z) vct(k) ) $

=== 4. 图像分析：等势面与力线 (Equipotential Lines & Force Lines)

观察老师在黑板右下角画的示意图：
- *曲线（等势线）*：代表势能相等的轨迹（类似地图上的等高线）。
- *带箭头的直线（力线）*：代表力 $vct(F)$ 的方向。
- *关键特性*：
  1. *正交性*：力线（梯度方向）始终与等势面（$U$ 为常数的面）*垂直*。
  2. *方向性*：由于公式中有负号，力的方向指向势能*减小*的方向（从高处指向低处）。

---

#text(fill: rgb("#d32f2f"), weight: "bold")[物理专题：非保守力做功与广义能量守恒定律]

---

=== 1. 非保守力：摩擦力的路径相关性 (Non-conservative Force)

与重力或引力不同，*非保守力*（如摩擦力）做功的大小取决于物体运动的具体路径 (*path dependent*)。

* 物理特性 (Characteristics)：
  摩擦力 $vct(f)$ 的方向始终与瞬时位移 $d vct(r)$ 相反，即 $vct(f) dot d vct(r) = -f d s$。
* 数学对比 (Comparison)：
  如图所示，从起点到终点有两条路径：$s_1$（直线）和 $s_2$（曲线）。
  - 直线功：$W_(f 1) = -f s_1$
  - 曲线功：$W_(f 2) = -f s_2$
  由于 $s_2 > s_1$，故 $|W_(f 2)| > |W_(f 1)|$。这说明非保守力无法定义唯一的势能函数。


=== 2. 机械能的损耗与转化 (Energy Dissipation)

当系统中存在非保守力时，机械能（动能 $K$ + 势能 $U$）不再守恒。非保守力所做的功 $W_(n c)$ 等于系统机械能的变化量：
$ W_(n c) = Delta (K + U) $

*物理直观* (Intuition)：
  摩擦力通常做负功，导致系统的机械能“流失”。这种流失并不是能量消失了，而是转化为了微观层面的分子动能，即*热能* (Thermal Energy)。

=== 3. 广义能量守恒定律 (Law of Energy Conservation)

板书最后一节给出了能量守恒的终极形式。通过引入热能项 $E_(t h)$，我们可以描述一个封闭系统的总能量守恒：

$ K + U + E_(t h) = "const." $


*符号说明* (Nomenclature)：
  - $K$: *Kinetic Energy* (动能)
  - $U$: *Potential Energy* (势能)
  - $E_(t h)$: *Thermal Energy* (热能/内能)

*物理意义* (Physical Significance)：
  这是比机械能守恒更普适的规律。它表明在孤立系统中，能量既不会凭空产生，也不会凭空消失，只能从一种形式转化为另一种形式（例如通过摩擦将机械能转化为热能）。

---

// 物理笔记：动力学中的守恒定律与碰撞模型
#let vct(x) = $arrow(bold(#x))$

#text(fill: rgb("#1a4a7c"), size: 1.2em, weight: "bold")[专题：典型动力学系统的能量与动量分析]

---

=== 1. 变摆长单摆模型 (Variable Length Pendulum)
*场景*：摆球在运动过程中摆长由 $L$ 突变为 $l$（如线被钉子挡住）。

* *核心特征*：在摆长缩短的瞬间，系统满足*角动量守恒*。
  $ m v_0 L = m v l quad arrow.r.double quad v = v_0 L / l $
* *能量转化*：碰撞后（或缩短后）满足机械能守恒。设最高点高度为 $h = L(1-cos theta)$。
  - 长摆：$1/2 m v_0^2 = m g L (1 - cos theta)$
  - 短摆：$1/2 m v^2 = m g l (1 - cos theta')$
*比例结论*：
  $ (1 - cos theta') / (1 - cos theta) = L^3 / l^3 $
  由于 $L > l$，推得 $theta' > theta$。即*摆长越短，摆起角度越大*。



=== 2. 滑块-滑梯碰撞爬升模型 (Block-Slide Interaction)
*场景*：小物块 $m$ 以 $v_0$ 撞击并爬上水平面上静止的滑梯 $M$。

* *水平动量守恒*：在最高点时，二者具有共同水平速度 $v_c$。
  $ m v_0 = (m + M) v_c quad arrow.r.double quad v_c = m / (m + M) v_0 $
* *机械能守恒*：系统初动能转化为系统余下的动能与重力势能。
  $ 1/2 m v_0^2 = 1/2 (m + M) v_c^2 + m g h $
* *最大高度表达式*：
  $ h = M / (m + M) dot v_0^2 / (2g) $
* *结论*：上升高度受质量分配系数 $M / (m + M)$ 调制。



=== 3. 最低点完全非弹性碰撞模型 (Inelastic Collision at Bottom)
*场景*：单摆 $m$ 在最低点与静止物块 $M$ 碰撞并*结合为整体*后继续摆动。

* *动量守恒 (碰撞瞬间)*：
  $ m v_0 = (m + M) v' quad arrow.r.double quad v' = m / (m + M) v_0 $
* *机械能变化 (爬升阶段)*：
  结合体以速度 $v'$ 开始爬升，满足 $(m + M) g h' = 1/2 (m + M) v'^2$。
* *高度对比*：
  设不碰撞时的爬升高度为 $h_0 = v_0^2 / (2g)$，则碰撞后的高度为：
  $ h' = v'^2 / (2g) = ( m / (m + M) )^2 h_0 $
* *结论*：由于速度在碰撞中因动量分配而大幅减小，且机械能有耗散，*碰撞结合后爬升的高度明显更低* ($h' < h_0$)。



---

=== 总结与对比分析 (Comparative Summary)

#table(
  columns: (1fr, 1.2fr, 1.2fr, 1.6fr),
  inset: 10pt,
  align: horizon,
  [*模型 (Model)*], [*第一守恒准则*], [*第二守恒准则*], [*核心物理结果*],
  [变摆长单摆], [角动量守恒 \ $m v_0 L = m v l$], [机械能守恒 \ $Delta (K + U) = 0$], [$L arrow.b arrow.r.double v arrow.t$ \ $theta' > theta$ (摆角增大)],
  [滑块-滑梯], [水平动量守恒 \ $m v_0 = (m+M)v_c$], [机械能守恒 \ $Delta (K + U) = 0$], [$h = M / (m + M) dot v_0^2 / (2g)$ \ (能量重新分配)],
  [碰撞结合], [动量守恒 \ $m v_0 = (m+M)v'$], [机械能守恒 \ (仅限碰撞后爬升)], [$h' = (m / (m+M))^2 h_0$ \ (速度阶跃减小，高度降低)]
)

*重点提醒*：
1. 在“变摆长”中，速度增大是因为半径减小；在“碰撞结合”中，速度减小是因为总质量增大。
2. 注意区分“内力做功”：滑块模型中 $m$ 与 $M$ 间的法向力对系统整体不做功，但完全非弹性碰撞中内部有能量耗散。