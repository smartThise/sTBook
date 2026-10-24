= 必要的数学：先把箭头和一小块说清楚
<必要的数学先把箭头和一小块说清楚>
== 标量、矢量和分量
<标量矢量和分量>
温度、电势是标量，只需一个数加单位；场强E是矢量，还要方向。$upright(bold(E)) = E_x hat(upright(bold(x))) + E_y hat(upright(bold(y))) + E_z hat(upright(bold(z)))$，分量可以为负，大小$E = sqrt(E_x^2 + E_y^2 + E_z^2)$非负。把两个矢量的大小直接相加，只有同向等特殊情形才对。

点积$upright(bold(A)) dot.op upright(bold(B)) = A B cos theta$挑出平行部分；叉积大小$A B sin theta$，方向按右手，交换顺序会反号。电通量用点积，磁力用叉积，所以一个看投影、一个看垂直程度。

== 积分其实是在"把很多小份加起来"
<积分其实是在把很多小份加起来>
线电荷$lambda = d q\/d l$，面电荷$sigma = d q\/d S$，体电荷$rho = d q\/d V$，因此小份电荷分别写$lambda d l$、$sigma d S$、$rho d V$。每小份对观察点产生一个小场矢量，再把分量积分。观察点坐标是固定的，源点坐标是积分变量；混用两者会让距离和方向都错。

通量$Phi = integral upright(bold(E)) dot.op d upright(bold(S))$中，$d upright(bold(S))$是带法向的小面积。法向与场夹角为90°时穿过量为0；平行时最大。闭合曲面约定向外为正。环流$integral.cont upright(bold(E)) dot.op d upright(bold(l))$则沿回路切向累计，和通量不是同一种积分。

#figure(image("图片/老师原图-电通量.png", alt: "教师原图：开曲面与闭曲面的通量，注意法向箭头。"),
  caption: [
    教师原图：开曲面与闭曲面的通量，注意法向箭头。
  ]
)

== 梯度、散度、旋度，先用一句实在的话
<梯度散度旋度先用一句实在的话>
梯度$nabla phi$指向标量增长最快的方向；静电场$upright(bold(E)) = - nabla phi$指向电势下降最快的方向。散度衡量某点附近净流出的密度；旋度衡量局部绕转趋势。它们不是箭头真的流动或旋转的唯一解释，而是场的空间变化特征。

在一维$upright(bold(E)) = - d phi\/d x thin hat(upright(bold(x)))$。例如$phi\(x\)= 5 - 2 x$ V（x用米），导数为-2 V/m，所以E=+2 V/m，沿+x。不要因为电势表达式里有负号就直接说场沿负向。

== 量纲检查能救很多题
<量纲检查能救很多题>
电势单位J/C，场强N/C=V/m；电容C/V=F；磁通T·m²=Wb；感应电动势Wb/s=V；能量J。若算出的电场中只剩$k_e q\/r$，单位其实是电势，说明少除一个长度。

#strong[自测。] 一小块面积法向与场夹60°，通量是否$E S sin 60 degree$？答：不是，是$E S cos 60 degree = E S\/2$；若题目给的是"场与平面"的夹角，才需先换成法向夹角。
