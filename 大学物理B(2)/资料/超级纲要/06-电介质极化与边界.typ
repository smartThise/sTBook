= 电介质：电荷没跑远，也能改变电场
<电介质电荷没跑远也能改变电场>
== 自由电荷与束缚电荷
<自由电荷与束缚电荷>
导体中自由电荷可宏观移动；电介质中正负电荷中心通常只能小幅分离，或原有电偶极转向。这叫极化。极化强度$upright(bold(P))$是单位体积的电偶极矩，单位C/m²。束缚体电荷密度$rho_b = - nabla dot.op upright(bold(P))$，表面密度$sigma_b = upright(bold(P)) dot.op hat(upright(bold(n)))$，法向取介质向外。

均匀极化介质内部散度为0，不表示整个介质没有束缚电荷；边界仍可能有正负面电荷。它们产生附加场，常抵消一部分外场。

== D把自由与束缚分开记
<d把自由与束缚分开记>
定义$upright(bold(D)) = epsilon.alt_0 upright(bold(E)) + upright(bold(P))$，于是$integral.cont upright(bold(D)) dot.op d upright(bold(S)) = Q_(f\,upright(i n))$，只统计自由电荷。若介质线性、各向同性，$upright(bold(P)) = epsilon.alt_0 chi_e upright(bold(E))$，所以$upright(bold(D)) = epsilon.alt upright(bold(E))$，$epsilon.alt = epsilon.alt_0\(1 + chi_e\)$。非线性或各向异性材料不能无条件用一个标量ε概括。

E的高斯定律右边仍是#strong[全部]电荷，D的右边才是自由电荷。把D说成"真正的电场"会误导：试探电荷受力仍用E。

== 边界条件，方向要统一
<边界条件方向要统一>
令单位法向n由介质1指向2，静电条件下

$ D_(2 n) - D_(1 n) = sigma_f\,#h(2em) E_(2 t) = E_(1 t) . $

第一条来自跨界面薄柱；第二条来自跨界面窄回路的零环流。若σ\_f=0，D法向连续，但E法向一般不连续。若两介电常数不同，场线可在界面转向，不能凭"没有自由面电荷"就把整个E都设连续。

#figure(image("图片/老师原图-电介质边界.png", alt: "教师原图：薄柱和窄回路分别控制法向与切向。"),
  caption: [
    教师原图：薄柱和窄回路分别控制法向与切向。
  ]
)

== 带介质球壳的例子
<带介质球壳的例子>
半径a导体球带自由电荷Q，a\<r\<b间充均匀介质ε，外面真空。球对称给$D_r = Q\/\(4 pi r^2\)$；介质层$E_r = Q\/\(4 pi epsilon.alt r^2\)$，外部$E_r = Q\/\(4 pi epsilon.alt_0 r^2\)$，导体内0。先由自由电荷求D，再按每区材料换成E，顺序比同时猜束缚电荷简单。

#strong[自测。] 极板自由电荷固定、均匀介质完全填满理想平板间隙时，E怎样变？答：变成原来的1/εᵣ。若电容器连着理想电压源保持电压，则E≈V/d保持，增加的是自由电荷；前提不同答案不同。
