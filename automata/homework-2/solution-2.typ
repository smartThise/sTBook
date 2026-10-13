// Homework 2 — Formal Languages and Automata
// Completed copy; the original assignment-2.typ is unchanged.
#set page(paper: "us-letter", margin: (x: 1.0in, y: 0.9in), numbering: "1", number-align: center)
#set text(font: ("Times New Roman", "Songti SC"), size: 11pt, lang: "zh")
#set par(justify: true, leading: 0.78em)
#show heading.where(level: 1): it => block(above: 1.4em, below: 0.6em, text(font: ("Times New Roman", "PingFang SC"), size: 12.5pt, weight: "bold", it.body))
#show heading.where(level: 2): it => block(above: 1.0em, below: 0.4em, text(font: ("Times New Roman", "PingFang SC"), size: 11.5pt, weight: "bold", it.body))
#align(center)[#text(size: 15pt, weight: "bold")[Homework 2 — 完整解答] #linebreak() #text(size: 10.5pt)[郭嘉乐 #h(1.5em) 2025013332]]
#v(0.6em)

助教好，由于英文实在看起来太累人了，但是不对照题目又不行，所以简单 LLM 翻译了一下。

= Problem 1

初态 $p$、接受态 $r$ 的 epsilon-NFA 转移表：
#block(breakable: false, align(center, table(columns: 5, align: center + horizon, stroke: 0.5pt, table.header([状态], [$epsilon$], [$a$], [$b$], [$c$]), [$p$], [$\{q,r\}$], [$emptyset$], [$\{q\}$], [$\{r\}$], [$q$], [$emptyset$], [$\{p\}$], [$\{r\}$], [$\{p,q\}$], [$r$], [$emptyset$], [$emptyset$], [$emptyset$], [$emptyset$],)))

== (a)

初态 epsilon-closure 是 $\{p,q,r\}$，已含接受态，所以 $epsilon$ 被接受。每次读入后取 epsilon-closure，可达子集为 $A=\{p,q,r\}, B=\{q,r\}, C=\{r\}, D=emptyset$。转移：$A$ 读 $a,c$ 到 $A$、读 $b$ 到 $B$；$B$ 读 $a,c$ 到 $A$、读 $b$ 到 $C$；$C$ 读任何符号到 $D$；$D$ 自环。接受子集为 $A,B,C$。因此长度不超过 3 的接受串为
$\{"" + "a" + "b" + "c" + "aa" + "ab" + "ac" + "ba" + "bb" + "bc" + "ca" + "cb" + "cc" + "aaa" + "aab" + "aac" + "aba" + "abb" + "abc" + "aca" + "acb" + "acc" + "baa" + "bab" + "bac" + "bba" + "bbc" + "bca" + "bcb" + "bcc" + "caa" + "cab" + "cac" + "cba" + "cbb" + "cbc" + "cca" + "ccb" + "ccc"\}$。

// 更正：原稿此题空缺。起始闭包含 r，所以 epsilon 也接受。

== (b)

子集构造 DFA 初态 $A$，接受态 $A,B,C$：
#block(breakable: false, align(center, table(columns: 4, align: center + horizon, stroke: 0.5pt, table.header([状态],[a],[b],[c]), [$ arrow.r .r *A=\{p,q,r\}$],[$A$],[$B$],[$A$], [$*B=\{q,r\}$],[$A$],[$C$],[$A$], [$*C=\{r\}$],[$D$],[$D$],[$D$], [$D=emptyset$],[$D$],[$D$],[$D$],)))
每个子集记录原 NFA 的全部可能状态；子集中含 r 即接受，故自动机等价。

= Problem 2

未列转移均不存在。

== (a)

目标为 $a^*b^*c^*$。初态 $s_0$，接受态 $s_3$，转移为
$s_0 arrow.r {a}s_0, s_0 arrow.r {epsilon}s_1, s_1 arrow.r {b}s_1, s_1 arrow.r {epsilon}s_2, s_2 arrow.r {c}s_2, s_2 arrow.r {epsilon}s_3.$
自环分别生成各字母块，epsilon 边允许跳过空块。

== (b)

初态 $s$，接受态 $f,g$。epsilon 分支：
$s arrow.r {epsilon}u_0, u_0 arrow.r {0}u_1 arrow.r {1}u_2, u_2 arrow.r {epsilon}f, u_2 arrow.r {epsilon}u_0;$
$s arrow.r {epsilon}v_0, v_0 arrow.r {0}v_1 arrow.r {1}v_2 arrow.r {0}v_3, v_3 arrow.r {epsilon}g, v_3 arrow.r {epsilon}v_0.$
$f,g$ 无出边。两分支标签分别 $(01)^+$、$(010)^+$：必须先完成一块才可接受，且块后可循环。

== (c)

条件等价于存在一个 $1$，其后恰有 0 至 9 个符号。初态 $s_0$，接受态 $s_1, ..., s_{10}$。$s_0$ 对 0、1 均自环，并另有 $s_0 arrow.r "1" s_1$；对 $1<=  i<10$，$s_i$ 对 0、1 均转至 $s_{i+1}$；$s_{10}$ 无出边。NFA 猜测作为证据的 1，之后读零到九个字符。

= Problem 3

== (a)

$ (0+1)^*1(0+1)^9 $

其右侧恰有九个符号。
// 更正：原式把九个符号放在 1 左侧，且末尾长度不限。

== (b)

$ (0+10)^*(epsilon+1+11)(0+01)^* $

在唯一可能的 $11$ 处切分：左边不含相邻 1 且不以 1 结尾，右边不含相邻 1 且不以 1 开始；中间选空串、$1$ 或 $11$。这恰为至多一对连续 1。
// 更正：原式 $(01)^*+(00)^*$ 漏掉如 $10$、$0110$。

== (c)

$1^*(01^*01^*01^*01^*01^*)^*$

每个括号贡献五个 0，1 可任意插入；零个括号表示零个 0。
// 更正：原式 $(0)1$ 未限制零的数目为 5 的倍数。

== (d)

$ (0+11)^*(epsilon+1) $

每个 0 单独成块，1 成对成块，至多留一个末尾 1；所以任意两个 0 间不可能恰有一个 1，不会出现 $101$。反过来，若串不含 $101$，每个夹在 0 之间的 1 段不可能长度为 1；按对配成 $11$ 块，余下单个 1 只能在末尾，故此式完整。
// 更正：原稿表达式没有正确排除 $101$。

== (e)

$ (01+10)^* $

前缀中 0 与 1 的数量差必须属于 $\{-1,0,1\}$。从差值 0 读一个符号后，须立即读相反符号回到 0，否则差值会到 2；末尾两数相等，故全串分解为 $01$ 或 $10$ 块。

= Problem 4

起始态 $q_1$，接受态 $q_3$。采用 Floyd 型递推。$R^{(k)}_(i j)$ 表示内部状态仅来自 $q_1,dots,q_k$ 的路径标签；$R^{(0)}_(i j)$ 是直接边标签，对角项并入 $epsilon$。递推：
$R^{(k)}_(i j)=R^{(k-1)}_(i j)+R^{(k-1)}_(i k)(R^{(k-1)}_(k k))^*R^{(k-1)}_(k j)$。

== (a)

基础情况的对角项并入 $epsilon$，而原始自环也保留（$q_1$ 的自环是 1，$q_3$ 的自环是 0）。允许 $q_1$ 后：
$R^{(1)}_{11}=1^*, R^{(1)}_{12}=1^*0, R^{(1)}_{13}=emptyset;$
$R^{(1)}_{21}=1, R^{(1)}_{22}=epsilon, R^{(1)}_{23}=0;$
$R^{(1)}_{31}=emptyset, R^{(1)}_{32}=emptyset, R^{(1)}_{33}=0^*$。

再允许 $q_2$，逐项用递推式计算：
$R^{(2)}_{11}=1^*+1^*0 1^*1, quad R^{(2)}_{12}=1^*0 1^*, quad R^{(2)}_{13}=1^*0 1^*0;$
$R^{(2)}_{21}=1+1^*0 1, quad R^{(2)}_{22}=epsilon+1^*0, quad R^{(2)}_{23}=0+1^*0;$
$R^{(2)}_{31}=emptyset, quad R^{(2)}_{32}=emptyset, quad R^{(2)}_{33}=0^*$。

例如按第二阶段定义，$R^{(2)}_{23}=R^{(1)}_{23}+R^{(1)}_{22}(R^{(1)}_{22})^*R^{(1)}_{23}=0+epsilon\,epsilon^*0=0$；其余各项同样直接代入递推式。

// 更正：原稿未作答；对角基础项要包括原自动机自环，例如 q3 上的 0。

== (b)

从 $q_1$ 到接受态 $q_3$ 的表达式为
$1^*0 1^*0(0^*1 1^*0)^*0^*.$
先在 $q_1$ 读若干 1 再读 0 到 $q_2$；在 $q_2$ 读若干 1 后读 0 到 $q_3$。在 $q_3$ 可读零个或多个 0，若读 1 则回到 $q_2$，随后在 $q_2$ 可读若干 1 再读 0 回到 $q_3$；该返回段可重复，最后在 $q_3$ 读若干个 0。

= Problem 5 （选做）

先将有限自动机确定化。令 $M_1=(Q_1, "Sigma", delta_1,s_1,F_1)$、$M_2=(Q_2, "Sigma", delta_2,s_2,F_2)$ 为 DFA。构造 $M=(Q_1 times Q_2,"Sigma",delta,(s_1,s_2),F_1 times F_2)$，基本转移定义为
$delta((p,q),a)=(delta_1(p,a),delta_2(q,a)).$

扩展转移函数记作 $delta^*$。归纳证明 $delta^*((s_1,s_2),w)=(delta_1^*(s_1,w),delta_2^*(s_2,w))$。空串时等式由定义成立。若对 $w$ 成立，则
$delta^*((s_1,s_2),w a)=delta(delta^*((s_1,s_2),w),a)
=(delta_1(delta_1^*(s_1,w),a),delta_2(delta_2^*(s_2,w),a))
=(delta_1^*(s_1,w a),delta_2^*(s_2,w a)).$
因此 $w in L(M)$ 当且仅当 $delta_1^*(s_1,w) in F_1$ 且 $delta_2^*(s_2,w) in F_2$，即 $w in L_1 inter L_2$。由于状态集有限，$M$ 是有限自动机。
