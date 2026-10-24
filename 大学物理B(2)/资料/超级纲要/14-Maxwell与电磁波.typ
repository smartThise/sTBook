= Maxwell方程：把四件事放到同一张图上
<maxwell方程把四件事放到同一张图上>
== 位移电流补上充电电容的缺口
<位移电流补上充电电容的缺口>
给电容充电时，导线中有电流，极板间介质却没有相同的传导电流。若只用旧安培定律，同一个回路选不同跨面会给出矛盾。补入$partial upright(bold(D))\/partial t$，可让电荷守恒与环路规律相容。位移电流密度单位也是A/m²，但不一定意味着真实载流子穿过真空间隙。

== 宏观方程的积分形式
<宏观方程的积分形式>
$ integral.cont_S upright(bold(D)) dot.op d upright(bold(S)) = Q_f\,#h(2em) integral.cont_S upright(bold(B)) dot.op d upright(bold(S)) = 0\, $ $ integral.cont_C upright(bold(E)) dot.op d upright(bold(l)) = - frac(d, d t) integral_S upright(bold(B)) dot.op d upright(bold(S))\, $ $ integral.cont_C upright(bold(H)) dot.op d upright(bold(l)) = I_f + frac(d, d t) integral_S upright(bold(D)) dot.op d upright(bold(S)) . $

这里回路与曲面固定在空间，正方向按右手对应。D/H形式右边是自由电荷/自由电流；真空中D=ε₀E、B=μ₀H。微分形式依次为散度D=ρ\_f、散度B=0、旋度E=-∂B/∂t、旋度H=J\_f+∂D/∂t。

== 真空波速为何由电磁常数决定
<真空波速为何由电磁常数决定>
无源真空中，对Faraday方程再取旋度，结合Ampère--Maxwell及div E=0，得$nabla^2 upright(bold(E)) = mu_0 epsilon.alt_0 partial_t^2 upright(bold(E))$，波速$c = 1\/sqrt(mu_0 epsilon.alt_0)$。平面波中E、B与传播方向互相垂直，大小E=cB，传播方向沿E×B。

线性均匀理想介质里相速度可写1/√(με)，真实材料有色散、吸收，ε/μ可能随频率变化，不能把这一简式无条件扩展到所有介质和信号速度。

== 能量由Poynting矢量描述
<能量由poynting矢量描述>
$upright(bold(S)) = upright(bold(E)) times upright(bold(H))$，单位W/m²。真空能量密度$u = epsilon.alt_0 E^2\/2 + B^2\/\(2 mu_0\)$。平面波中电磁两部分相等；若E₀为电场振幅，平均强度$chevron.l S chevron.r = epsilon.alt_0 c E_0^2\/2$，不是ε₀cE₀²，后者少了时间平均的1/2。

完全吸收表面的辐射压约I/c，垂直理想反射约2I/c；光既能传能也能传动量。这个结论可与后面的光子p=E/c互相检查。

#strong[自测。] 两个平面波分别满足E=cB，它们叠加后的任意局部场也一定同样满足吗？答：不一定；驻波等叠加场可能有不同的局部E/B关系，不能把单一行波关系当任意场恒等式。
