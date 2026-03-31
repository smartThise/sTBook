#import "../module/myutils.typ" : *
#import "engine.typ":*

#show : conf

#let g = 9.80

= 大学物理 英 1 作业 紫荆 53 郭嘉乐

#outline()

== HW 2 #datetime(year:2026,month:3,day:19).display()

=== 1. Rock Climber

==== a
 #image("../Assets/img/20260319_224719.png",width:150pt)

==== b
根据受力分析，由牛顿第一定律，人在水平方向受力平衡，故 $F_L=F_R$；则对于摩擦力， $f_L=1.2 F_L,f_R=0.8 F_R$ 且 $G = f_L + f_R=1.2 F_L + 0.8 F_R = 2 F_L = m g= cal("55 * 9.8") "N"$，那么可知  $F_L=F_R= G / 2 = cal("55 * 9.8 / 2",digits:#1) "N"$

==== c
显然的这个比例是 $iota = mu_1 / (mu_1+mu_2) = cal("1.2 / (1.2+0.8)")$

=== 2. Three-Mass Pulley System

==== a
设绳 1 张力为 $T_1$，绳 2 张力为 $T_2$。设 $m_1$ 向上加速度为 $a_1$，则动滑轮 $B$ 向下加速度亦为 $a_1$。设 $m_2$ 相对于滑轮 $B$ 向下的加速度为 $a_r$。
$
cases(
  T_1 - m_1 g = m_1 a_1,
  T_1 = 2 T_2,
  m_2 g - T_2 = m_2 (a_1 + a_r),
  T_2 - m_3 g = m_3 (a_r - a_1)
)
$
代入数据 $m_1=0.20 "kg", m_2=0.10 "kg", m_3=0.05 "kg"$：
$a_1 = (2 m_2 m_3 - m_1(m_2 + m_3)) / (m_1(m_2 + m_3) + 4 m_2 m_3) g$
$a_1 = -3.92 "m/s"^2$ （负号表示 $m_1$ 实际向下加速）：
- $m_1$ 加速度：$3.92 "m/s"^2$ (向下)
- $m_2$ 加速度：$0.78 "m/s"^2$ (向下)
- $m_3$ 加速度：$8.62 "m/s"^2$ (向上)

==== b
$T_1 = m_1 (g + a_1) = 0.20 times (9.80 - 3.92) = 1.18 "N"$
$T_2 = T_1 / 2 = 0.59 "N"$

=== 3\*. 斜面问题

（卡住了一会……难……）

对于斜面而言：由牛顿第二定律，实际上受力分析只能得到 $N sin theta = M a_2$

对于小物块而言，以地面作为惯性参考系，我们看到此时他对于垂直斜面方向的加速度为 $a_"垂"$，则

$
a_"垂" = a_2 sin theta \ 
m a_"垂" = m g cos theta - N\
$
联立上述三个方程，得到 $a_2=(m g sin theta cos theta) / (M+ m sin^2 theta)$



=== 4. Blocks and Pulley on an Accelerating Cart I

若 $m_1, m_2$ 相对小车静止，系统共同水平加速度为 $a$：
对 $m_2$：$T = m_2 g$
对 $m_1$：$T = m_1 a$
得 $a = (m_2 g) / m_1$。
所需水平力：$F = (M + m_1 + m_2) (m_2 g) / m_1$

=== 5. Blocks and Pulley on an Accelerating Cart II

由于 $m_2$ 只能垂直移动，其水平加速度必与小车 $M$ 一致（设为 $A$）。
由水平方向合力为零：$(M + m_1 + m_2) A + m_1 a_r = 0$。
联立，解得 $A = 0$。
- (a) $T = (m_1 m_2 g) / (m_1 + m_2)$
- (b) $a_2 = (m_2 g) / (m_1 + m_2)$ (向下)
- (c) $A = 0$
- (d) $a_1 = (m_2 g) / (m_1 + m_2)$ (向右)

=== 6. Bead on a Rotating Circular Hoop

==== a
周期 $T = 0.450 "s"$ 时，$omega = (2 pi) / T$。
$ cos theta = g / (omega^2 R) = (g T^2) / (4 pi^2 R) $
代入数据：$cos theta = (9.80 times 0.450 times 0.450) / (4 times pi^2 times 0.15) approx 0.33$
解得：$theta approx 70.43 degree$

==== b
$T = 0.850 "s"$ 时，$cos theta approx 1.19 > 1$，故 $theta = 0 degree$。

=== 7. Pressure Inside a Self-Gravitating Sphere

==== a
（抽象）

考虑球内半径 $r$ 处厚度为 $dif r$ 的一个微元层。该层以内质量 $M(r) = 4/3 pi r^3 rho$，引力加速度 $g(r) = (G M(r)) / r^2 = 4/3 pi G rho r$。
层内外压力差抵消重力：$d p = - rho g(r) d r$。
$ integral_(p_c)^0 d p = - integral_0^R 4/3 pi G rho^2 r d r $
$ p_c = 2/3 pi G rho^2 R^2 $

==== b
代入 $rho approx 1.3 times 10^3 "kg/m"^3, R approx 7.0 times 10^8 "m"$：
$p_c approx 1.15 times 10^14 "Pa" approx 1.14 times 10^9 "atm"$

=== 8. Mass and String

==== a
忽略重力，角动量守恒：$m r_0^2 omega_0 = m (r_0 - V t)^2 omega(t)$。
$ omega(t) = omega_0 (r_0 / (r_0 - V t))^2 $

==== b
拉力 $F$ 提供向心力：
$ F = m omega(t)^2 r(t) = (m omega_0^2 r_0^4) / (r_0 - V t)^3 $

== HW 3 #datetime(year:2026,month:3,day:31).display()

=== 1. Bullet Fired into a Block
#[

助教你好，你接下来可能会看见一些奇怪的重复的物理量说明。但是这是我所使用的标记语言所必需的QAQ

#cpt("h=1",unit:"m")
#cpt("m=0.008",unit: "k g")
首先计算物块下落到地面的时间 #cpt("t=sqrt((2*h)/g)",unit:"s")
]