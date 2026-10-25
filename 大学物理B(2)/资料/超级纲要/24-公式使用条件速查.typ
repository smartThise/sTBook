= 公式速查：先核对条件，再拿去算
<公式速查先核对条件再拿去算>
这份速查用于已经读过推导后的回忆。每个公式旁边的条件也是公式的一部分。出现似曾相识的题型时，先对照物体、边界和保持量，再决定能否使用。

== 拿到题目时，怎样选到表里的那一行
<拿到题目时怎样选到表里的那一行>
"给出球的总电荷，求球外E"：先问电荷是否球对称。若是，同心球面可把E提到积分外；若球外另放一个点电荷，原球对称被破坏，总场不能继续当作球面常数，虽然高斯通量定理仍成立。

"把介质拉入电容，求力"：先看电源是否接着。断开且无漏电，Q固定，可从$Q^2\/\(2 C\)$的减少量求机械功；接恒压源，要先求电源功$U thin d Q$，再扣场能增加。两种状态公式始终等价，区别是改变几何时哪个量被固定。

"求光在薄膜上的明暗"：先画两束到同一个出射波面的光线；算传播光程差，再检查两次反射有几个相对π。只给膜厚和折射率，尚不能跳过基底折射率直接选明暗式。

"给出波函数，求某区间概率"：先求$\|psi\|^2$，检查全空间是否积到1，再积指定区间。若问能量测量，才转到能量本征态展开系数；位置曲线的最高点不是能量概率。

"给出态密度g和费米函数f，求电子数"：用$integral g\(E\)f\(E\)d E$。先看g是每体积还是整块样品的、是否已含两种自旋，决定还要不要乘V或2。不要仅凭符号g猜定义。

== 静电场与电势
<静电场与电势>
这里$k = 1\/\(4 pi epsilon.alt_0\)$，约$8.99 times 10^9 thin upright(N thin m^2\/C^2)$。向量R从电荷源指向观察点，R的模记为R；电势V用伏特，势能U用焦耳，二者对电荷q的关系是U=qV。

#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([要算什么], [关系], [先核对什么],),
    table.hline(),
    [点电荷场], [$upright(bold(E)) = k q upright(bold(R))\/R^3$], [R从源指向观察点；真空静电点源；R≠0],
    [连续源场], [$upright(bold(E)) = k integral upright(bold(R)) thin d q\/R^3$], [dq对应线、面还是体；分量先投影],
    [闭面通量], [$integral.cont upright(bold(E)) dot.op d upright(bold(S)) = Q_(upright("总,内"))\/epsilon.alt_0$], [E含全部源；右边仅面内净电荷],
    [点源电势], [$V = k q\/r$], [无穷远零点；不含自势用于自身作用],
    [电势差], [$V_B - V_A = - integral_A^B upright(bold(E)) dot.op d upright(bold(l))$], [静电路径无关；变化磁场要小心],
    [场与势], [$upright(bold(E)) = - nabla V$], [负号表示沿场方向势下降],
    [功与势能], [$W = q\(V_A - V_B\)= - Delta U$], [q带符号；电子是−e],
    [导体外法向场], [$E_(upright("外,n")) = sigma\/epsilon.alt_0$], [静电平衡、外部真空、法向由金属向外],
  )]
  , kind: table
  )

高斯定理并不要求球对称；利用它直接求E才需要足够对称性。零通量一般不能推出零场，某点零电势也不能推出零场。薄球壳与均匀实心球外场相同，内场不同；半径r与物体半径R要分开。

== 介质、电容与能量
<介质电容与能量>
#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([关系], [条件与提醒],),
    table.hline(),
    [$upright(bold(D)) = epsilon.alt_0 upright(bold(E)) + upright(bold(P))$], [一般宏观定义；D单位C/m²],
    [$upright(bold(D)) = epsilon.alt upright(bold(E))$], [线性、各向同性；ε=ε₀εᵣ],
    [$integral.cont upright(bold(D)) dot.op d upright(bold(S)) = Q_f$], [只数自由电荷],
    [$D_(2 n) - D_(1 n) = sigma_f$], [统一法向从1到2；σf不含束缚电荷],
    [$E_(2 t) = E_(1 t)$], [静电界面切向条件],
    [$C = Q\/U$，平行板$C = epsilon.alt A\/d$], [线性几何；大板、忽略边缘],
    [$W = Q^2\/\(2 C\)= C U^2\/2$], [同一线性状态两式等价；比较变形或求力时按保持量选方便表达，恒压时还要计入电源做功],
    [$u_E = upright(bold(E)) dot.op upright(bold(D))\/2$], [线性可逆材料；非线性需积分],
    [$F_x = U^2 C'\(x\)\/2$], [恒压且把电源能量计入；方向按x定义],
  )]
  , kind: table
  )

电源断开通常意味着孤立极板净电荷固定；电源保持连接通常意味着电压固定。插介质、改板距、移动极板之前，把这一句写在纸上。并联同电压、串联等电荷的常用结论还要求中间孤立节点原先净电荷为0。

== 电流与暂态
<电流与暂态>
$I = integral upright(bold(j)) dot.op d upright(bold(S))$，均匀垂直流时I=jA；$upright(bold(j)) = n q upright(bold(v))_d$，q与漂移速度都可有方向。欧姆材料 $upright(bold(j)) = sigma upright(bold(E))$，均匀直棒 $R = rho ell\/A$。σ在不同章可能表示电导率或面电荷密度，单位能分清。

RC电路时间常数τ=RC，恒压驱动下电容电压 $u_C\(t\)= U_oo +\[u_C\(0\)- U_oo\]e^(- t\/tau)$。RL电路τ=L/R，电流 $I\(t\)= I_oo +\[I\(0\)- I_oo\]e^(- t\/tau)$。必须先求开关前初值和开关后稳态值；不能只认出"指数"就把初值设0。

电容电压通常连续，理想电感电流通常连续，前提是没有无穷冲击电流或电压。真实突然开关过程还可能需要寄生电容、电感与击穿模型。

== 磁场、感应与波
<磁场感应与波>
#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([关系], [适用条件与方向],),
    table.hline(),
    [$upright(bold(F)) = q\(upright(bold(E)) + upright(bold(v)) times upright(bold(B))\)$], [先叉乘再看q正负],
    [$r = p_perp\/\(\|q\|B\)$], [均匀B；低速才用p=mv],
    [$T = 2 pi m\/\(\|q\|B\)$], [非相对论、均匀B],
    [$d upright(bold(B)) = mu_0 I thin d upright(bold(l)) times upright(bold(R))\/\(4 pi R^3\)$], [稳恒细电流，R从源到观察点],
    [$integral.cont upright(bold(H)) dot.op d upright(bold(l)) = I_f$], [稳恒；变化场需位移电流],
    [$integral.cont_C upright(bold(H)) dot.op d upright(bold(l)) = I_f + d integral_S upright(bold(D)) dot.op d upright(bold(S))\/d t$], [固定环路与跨面，二者方向按右手配对；$I_f$与D通量用同一面法向],
    [$B_(2 n) = B_(1 n)$，$hat(upright(bold(n))) times\(upright(bold(H))_2 - upright(bold(H))_1\)= upright(bold(K))_f$], [n从1到2，Kf为自由面电流；有电流层时H切向可跳变],
    [$upright(bold(B)) = mu_0\(upright(bold(H)) + upright(bold(M))\)$], [一般宏观定义；B=μH另需线性],
    [$cal(E) = - d Phi_B\/d t$], [闭回路，法向与正向右手配对],
    [$integral.cont\(upright(bold(E)) + upright(bold(u)) times upright(bold(B))\)dot.op d upright(bold(l))$], [运动回路电动势；u为导体元速度],
    [$cal(E)_L = - L thin d I\/d t$], [固定几何、常数L；一般用−dΨ/dt],
    [$W_L = L I^2\/2$], [线性电感],
    [$v = 1\/sqrt(mu epsilon.alt)$], [均匀线性无耗介质的简单波模型],
    [$I = epsilon.alt_0 c E_0^2\/2$], [真空正弦平面行波，E₀为峰值],
  )]
  , kind: table
  )

磁力不做功不表示电磁系统不能传能。楞次定律反对磁通变化，不是永远反对原磁场。E=cB适用于真空单一平面行波，不能对电容静场、线圈近场或任意驻波直接套用。

== 光学
<光学>
第15章沿用教师记号：$delta = L_(upright(o p t)\,2) - L_(upright(o p t)\,1)$是光程差，$Delta phi = phi.alt_1 - phi.alt_2 = 2 pi delta\/lambda_0 + Delta phi_0$是相位差，附加相位也按第一路减第二路。双缝Δx=λD/d要求远场、小角、相干与合适偏振；单缝暗纹a sinθ=mλ中m非零，中央全角宽近轴2λ/a。光栅主峰d sinθ=kλ，k为可正可负的整数级次，分辨本领$\|k\|N$采用理想Rayleigh判据；缺级要同时满足主峰与单缝暗纹条件。

薄膜传播光程差2nt cosr还要加反射相位差。先数相对多出的π，再选明暗条件。自然光透过第一片理想偏振片为I₀/2，线偏振透片按I=I入cos²θ；每一步θ针对当前入射偏振方向。四分之一波片只有在两轴等振幅输入时才把线偏振转为圆偏振。第17章采用$cos\(omega t - k z\)$，正的慢轴落后量$Delta phi.alt = 2 pi\(n_(upright("慢")) - n_(upright("快"))\)d\/lambda_0$对应带符号的慢轴相位改变量$delta_(upright("片")) = - Delta phi.alt$；补偿原有相位时使用带符号的量。

== 量子与固体
<量子与固体>
光子E=hf=hc/λ、p=h/λ；有质量粒子λ=h/p，低速p=√(2mK)，高速改用相对论动量。电子经电压U获得动能大小eU，并非把电子也当成E=pc的光子。

$rho =\|Psi\|^2$ 是概率密度，区间概率要积分；定态 $Psi = psi e^(- i E t\/ℏ)$ 的密度不变，相位仍变化。无限方阱0到L（教师中心坐标的总宽a=L）的 $E_n = n^2 h^2\/\(8 m L^2\)$、n从1起；谐振子 $E_n =\(n + 1\/2\)ℏ omega$、n从0起。不同模型的编号别混。

氢样单电子原子近似 $E_n = - 13.6 Z^2\/n^2$eV，多电子需考虑屏蔽与相互作用。泡利原理限制完整单粒子态，含自旋；同一空间轨道可放两个相反自旋电子。费米分布f(E)是态占据概率，算能量区间电子数还需态密度。半导体σ=e(nμn+pμp)，n型和p型通常整体近似电中性。
