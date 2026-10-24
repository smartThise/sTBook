// 作业 3 证明草稿：题目沿用 assignment-3.typ，仅填充解答。
#set document(title: "作业 3", author: "郭嘉乐")
#set text(font: ("New Computer Modern", "Songti SC"), size: 10pt, lang: "zh")
#set math.equation(numbering: none)
#set par(justify: true, first-line-indent: 0pt, leading: 0.55em, spacing: 0.65em)
#set page(
  paper: "a4",
  margin: (left: 44mm, right: 44mm, top: 46mm, bottom: 40mm),
  numbering: "1",
  number-align: center,
  header-ascent: 12mm,
  header: context [
    #if counter(page).get().first() == 1 {
      grid(columns: (1fr, 1fr),
        [形式语言与自动机 \ 2026 年秋季],
        align(right)[郭嘉乐 \ 2025013332],
      )
    } else {
      text(size: 9pt, grid(columns: (1fr, 1fr), [作业 3], align(right)[郭嘉乐]))
    }
    #v(3pt)
    #line(length: 100%, stroke: 1pt)
  ],
)

#let label(body) = text(font: ("Arial", "PingFang SC"), weight: "bold", body)
#let boxed(body) = box(inset: 5pt, stroke: 0.5pt, math.equation(body))
#let edge(body) = math.attach(sym.arrow.r.long, t: body)
#let problem(n, body) = block(above: 14pt, below: 6pt)[#label[问题 #n.] #body]
#let solution() = block(above: 6pt, below: 14pt)[#label[解答.]]
#let parts(..items) = enum(
  numbering: "(a)",
  indent: 0pt,
  body-indent: 1.8em,
  tight: false,
  spacing: 6pt,
  ..items.pos(),
)

#align(center, text(font: ("Arial", "PingFang SC"), size: 14.4pt, weight: "bold")[作业 3])
#v(10pt)

使用 GPT 6.1 Sol 翻译为中文题面；一部分表格和复杂的图形由于人手打得过慢，也是 AI 辅助生产的。

#problem(1)[（习题 2.3.4 (c)）使用 Thompson 方法，将正则表达式 $00(0+1)^*$ 转换为带有 $epsilon$ 转移的 NFA。]

#solution()

分别为两个前导 $0$ 建立基本自动机，再对 $0+1$ 做并运算构造，接着做 $*$ 闭包构造，最后用 $epsilon$ 转移连接这三个部分。

对于后半部分，取
$ Q = {q_0, q_1, dots, q_11}, quad Sigma = {0,1}, quad F = {q_11}. $
初始状态为 $q_0$。转移函数如下

#align(center, table(
  columns: 4, align: center, inset: (x: 8pt, y: 3pt), stroke: 0.4pt,
  table.header([状态], [$0$], [$1$], [$epsilon$]),
  [$q_0$], [$ {q_1} $], [$emptyset$], [$emptyset$],
  [$q_1$], [$emptyset$], [$emptyset$], [$ {q_2} $],
  [$q_2$], [$ {q_3} $], [$emptyset$], [$emptyset$],
  [$q_3$], [$emptyset$], [$emptyset$], [$ {q_10} $],
  [$q_4$], [$emptyset$], [$emptyset$], [$ {q_5, q_7} $],
  [$q_5$], [$ {q_6} $], [$emptyset$], [$emptyset$],
  [$q_6$], [$emptyset$], [$emptyset$], [$ {q_9} $],
  [$q_7$], [$emptyset$], [$ {q_8} $], [$emptyset$],
  [$q_8$], [$emptyset$], [$emptyset$], [$ {q_9} $],
  [$q_9$], [$emptyset$], [$emptyset$], [$ {q_4, q_11} $],
  [$q_10$], [$emptyset$], [$emptyset$], [$ {q_4, q_11} $],
  [$q_11$], [$emptyset$], [$emptyset$], [$emptyset$],
))

$q_4$ 和 $q_9$ 分别是并运算部分的入口和出口，$q_10$ 和 $q_11$ 分别是 $*$ 闭包部分的新入口和新出口，利用 $epsilon$ 作为连接每一个字符所“对应”的中转路径。

证明正确性： 从 $q_0$ 到 $q_11$ 的任何接受路径都必须先依次经过
$ q_0 edge(0) q_1 edge(epsilon) q_2 edge(0) q_3 edge(epsilon) q_10. $
此后可以直接经 $epsilon$ 到达 $q_11$，也可以进入 $q_4$，每次经由 $q_5,q_6$ 或 $q_7,q_8$ 读入一个 $0$ 或 $1$，到达 $q_9$ 后继续循环或退出。因此每条接受路径恰好读入形如 $00v$、$v in {0,1}^*$ 的字符串。

反过来，给定任意 $00v$，先沿上述路径读入 $00$，再按 $v$ 的各个符号选择相应的分支，最后退出到 $q_11$，便得到一条接受路径。故所得自动机的语言恰为 $L(00(0+1)^*)$。

#pagebreak()

#problem(2)[（习题 2.3.6）设 $A = (Q, Sigma, delta, q_0, {q_f})$ 是一个 $epsilon$-NFA，且没有进入 $q_0$ 的转移，也没有从 $q_f$ 出发的转移。用 $L = L(A)$ 描述对 $A$ 进行以下每种修改后所接受的语言：]

#parts(
  [通过向 $A$ 添加一条从 $q_f$ 到 $q_0$ 的 $epsilon$ 转移而构造的自动机。],
  [通过向 $A$ 添加从 $q_0$ 到每个从 $q_0$ 可达的状态的 $epsilon$ 转移而构造的自动机（沿着一条其标号既可以包含 $Sigma$ 中的符号，也可以包含 $epsilon$ 的路径）。],
  [通过向 $A$ 添加从每个能够沿某条路径到达 $q_f$ 的状态到 $q_f$ 的 $epsilon$ 转移而构造的自动机。],
  [通过对 $A$ 同时执行 (b) 和 (c) 而构造的自动机。],
)

#solution()

*(a)* 新自动机接受的语言为 $L^+$。

将新接受路径在每次经过新增转移 $q_f edge(epsilon) q_0$ 处切开，各段均为原自动机的接受路径，所以输入串是一个或多个 $L$ 中的串的连接，属于 $L^+$。反过来，任取 $w_1 dots w_k$，其中 $k >= 1$、$w_i in L$，依次运行各 $w_i$ 的原接受路径，并用新增转移连接相邻两段，即可接受该串。故新语言为 $L^+$。

*(b)* 新自动机接受 $L$ 中所有串的所有后缀，即
$ {v in Sigma^* bar.v exists u in Sigma^*, u v in L}. $

若 $u v in L$，则在 $A$ 的一条接受路径上，读完 $u$ 后到达某个状态 $r$。新自动机可以从 $q_0$ 经新增的 $epsilon$ 转移到达 $r$，再沿原路径读入 $v$ 并到达 $q_f$；若 $r=q_0$，则直接沿原路径读入 $v$。因此每个这样的 $v$ 都被接受。

反过来，由于原来没有进入 $q_0$ 的转移，而新增转移都从 $q_0$ 出发，删去可能的 $epsilon$ 自环后，接受路径至多在开头使用一次新增转移。设它跳到状态 $r$ 后沿原路径读入 $v$ 到达 $q_f$。由于 $r$ 在原自动机中从 $q_0$ 可达，存在某个 $u$ 使得原路径从 $q_0$ 读入 $u$ 到达 $r$，所以 $u v in L$。若没有使用新增转移，则取 $u=epsilon$。因此被接受的串都是 $L$ 中某个串的后缀。

*(c)* 新自动机接受 $L$ 中所有串的所有前缀，即
$ {u in Sigma^* bar.v exists v in Sigma^*, u v in L}. $

若 $u v in L$，则在原接受路径上读完 $u$ 到达的状态 $r$ 能够沿余下路径到达 $q_f$。因此新自动机读完 $u$ 后，可以经新增的 $epsilon$ 转移直接到达 $q_f$；若已经位于 $q_f$，则无需再转移。所以每个这样的 $u$ 都被接受。

反过来，由于原来没有从 $q_f$ 出发的转移，而新增转移都终止于 $q_f$，删去可能的 $epsilon$ 自环后，接受路径至多在末尾使用一次新增转移。若它先沿原路径读入 $u$ 到达 $r$，再跳到 $q_f$，则原来存在一条从 $r$ 到 $q_f$ 的路径。设该路径读入 $v$，便有 $u v in L$。若没有使用新增转移，则取 $v=epsilon$。故被接受的串都是 $L$ 中某个串的前缀。

*(d)* 新自动机接受 $L$ 中所有串的所有子串，即
$ {v in Sigma^* bar.v exists u,z in Sigma^*, u v z in L}. $

若 $u v z in L$，在原接受路径上，设读完 $u$ 到达 $r$，继续读完 $v$ 到达 $t$。由于 $r$ 从 $q_0$ 可达，且 $t$ 能到达 $q_f$，新自动机可以先从 $q_0$ 经新增的 $epsilon$ 转移到 $r$，再沿原路径读入 $v$ 到达 $t$，最后经新增的 $epsilon$ 转移到 $q_f$。若 $r=q_0$ 或 $t=q_f$，省去相应转移即可。因此每个这样的 $v$ 都被接受。

反过来，由题设的两个无转移条件，删去可能的 $epsilon$ 自环后，一条新接受路径只能在开头从 $q_0$ 跳到某个原来可达的状态 $r$，在中间沿原路径读入 $v$ 到达某个能到达 $q_f$ 的状态 $t$，并在末尾跳到 $q_f$。开头或末尾的跳转可以不发生，此时分别取 $r=q_0$ 或 $t=q_f$。选择原路径从 $q_0$ 读入 $u$ 到达 $r$，再从 $t$ 读入 $z$ 到达 $q_f$，拼接便得到 $u v z in L$。故被接受的串都是 $L$ 中某个串的子串。

#pagebreak()

#problem(3)[（习题 3.2.3）使用第 3.2.2 节的状态消除技术，将下列 DFA 转换为正则表达式。]

#align(center, table(
  columns: (auto, 1.5pt, auto, auto),
  align: (right, center, center, center),
  inset: (x: 6pt, y: 2pt),
  stroke: none,
  table.vline(x: 1, stroke: 0.4pt),
  table.vline(x: 2, stroke: 0.4pt),
  table.vline(x: 3, stroke: 0.4pt),
  [], table.cell(inset: 0pt)[], [$0$], [$1$],
  table.hline(stroke: 0.4pt),
  table.cell(colspan: 4, inset: 0pt, block(height: 1.5pt)),
  table.hline(stroke: 0.4pt),
  [$arrow.r * p$], table.cell(inset: 0pt)[], [$s$], [$p$],
  [$q$], table.cell(inset: 0pt)[], [$p$], [$s$],
  [$r$], table.cell(inset: 0pt)[], [$r$], [$q$],
  [$s$], table.cell(inset: 0pt)[], [$q$], [$r$],
))

#solution()

按 $r,q,s$ 的顺序消除状态，保留同时为初始状态和接受状态的 $p$。消除状态 $k$ 时，对所有剩余状态 $i,j$ 更新
$ E_(i j) <- E_(i j) + E_(i k)(E_(k k))^* E_(k j). $


*第一步：消除 $r$。* 因为 $s edge(1) r$、$r edge(0) r$、$r edge(1) q$，所以从 $s$ 到 $q$ 的边更新为
$ 0 + 1 0^* 1. $
此时其余非空边为 $p edge(1) p$、$p edge(0) s$、$q edge(0) p$、$q edge(1) s$。

*第二步：消除 $q$。* 状态 $q$ 没有自环，故其自环闭包为 $emptyset^* = epsilon$。于是增加
$ s edge((0+1 0^* 1)0) p, quad s edge((0+1 0^* 1)1) s. $
留下的非空边为
$
  p &edge(1) p, quad p edge(0) s, \
  s &edge((0+1 0^* 1)0) p, quad s edge((0+1 0^* 1)1) s.
$

*第三步：消除 $s$。* 留在 $p$ 上的自环标号为
$ 1 + 0((0+1 0^* 1)1)^*(0+1 0^* 1)0. $
初始状态和唯一接受状态均为 $p$，故任意接受路径恰为零次或多次这样的循环，所求正则表达式为
$ (1 + 0((0+1 0^* 1)1)^*(0+1 0^* 1)0)^* $


#pagebreak()

#problem(4)[证明或证伪以下关于正则表达式的每个陈述。]

#parts(
  [（习题 3.4.1 (g)）$(epsilon + R)^* = R^*$。],
  [（习题 3.4.2 (b)）$(R S + R)^* R = R (S R + R)^*$。],
  [（习题 3.4.2 (d)）$(R + S)^* S = (R^* S)^*$。],
)

#solution()

正则表达式之间的等号均按其所表示的语言相等来理解。

*(a) 成立。* 记 $K=L(R)$。因为 $K subset.eq {epsilon} union K$，所以
$ K^* subset.eq ({epsilon} union K)^*. $
反过来，任意 $w in ({epsilon} union K)^*$ 都可写为有限个因子的连接，其中每个因子属于 ${epsilon} union K$。删去取值为 $epsilon$ 的因子后，仍得到同一个串，而且所有剩余因子都属于 $K$。若没有剩余因子，则 $w=epsilon in K^*$；否则同样有 $w in K^*$。故
$ ({epsilon} union K)^* = K^*. $

*(b) 成立。* 记 $K=L(R)$、$J=L(S)$，并令 $B=J union {epsilon}$。利用代数分配律，有
$ L(R S + R) = K B, quad L(S R + R) = B K. $
以下证明对每个整数 $n >= 0$，均有
$ (K B)^n K = K(B K)^n. $
当 $n=0$ 时，两边都是 $K$。若对 $n$ 成立，则由连接的结合律，
$
  (K B)^(n+1)K
  &= (K B)^n K B K \
  &= K(B K)^n B K \
  &= K(B K)^(n+1).
$
归纳成立。对 $n >= 0$ 取并，并再次利用连接对并的分配律，得到
$
  (K B)^* K
  &= union.big_(n >= 0) (K B)^n K \
  &= union.big_(n >= 0) K(B K)^n \
  &= K(B K)^*.
$
代回 $K,B$，即得 $(R S+R)^* R = R(S R+R)^*$。

*(c) 不成立。* 取 $R=a$、$S=b$。右端为 $(a^* b)^*$，由于最外层是 $*$ 闭包，其语言包含 $epsilon$。左端为 $(a+b)^* b$，其中每个串都以 $b$ 结尾，长度至少为 $1$，所以不包含 $epsilon$。两端语言不同，因此原等式不成立。

#pagebreak()

#problem(5)[为下面的每个正则语言构造一个 DFA：]

#parts(
  [在 ${a, b}$ 上的、含有且仅含有奇数个子串 $a b$ 的所有字符串。],
  [在 ${a, b}$ 上的、包含 $a b$ 但不包含 $b b$ 作为子串的所有字符串。],
)

#solution()

*(a) 按 $a b$ 出现次数的奇偶性，以及当前最后一个字符是否为 $a$，记录状态。*

设 $M_1=(Q_1,{a,b},delta_1,E_N,F_1)$，其中
$ Q_1={E_N,E_A,O_N,O_A}, quad F_1={O_N,O_A}. $
字母 $E,O$ 分别表示 $a b$ 的出现次数为偶数、奇数；下标 $A$ 表示已读串以 $a$ 结尾，下标 $N$ 表示空串或最后一个字符不是 $a$。完整转移表为

#align(center, table(
  columns: 3, align: center, inset: 5pt, stroke: 0.4pt,
  table.header([状态], [$a$], [$b$]),
  [$arrow.r E_N$], [$E_A$], [$E_N$],
  [$E_A$], [$E_A$], [$O_N$],
  [$* O_N$], [$O_A$], [$O_N$],
  [$* O_A$], [$O_A$], [$E_N$],
))

正确性验证：对已读串长度归纳。读入空串时，$a b$ 出现 $0$ 次，且没有末尾 $a$，因此初始状态 $E_N$ 正确。假设状态对当前串的描述成立。再读入 $a$ 不会产生新的 $a b$，因此奇偶性不变，下标变为 $A$。再读入 $b$ 时，当且仅当此前最后一个字符是 $a$，才会在串尾新增恰好一次 $a b$，此时翻转奇偶性；无论如何下标都变为 $N$。这些规则与表完全一致。因此状态描述对所有输入成立，而恰好两个 $O$ 状态为接受状态，故恰好接受所求语言。

*(b) 同时记录是否已经出现 $a b$，以及是否产生了 $b b$。*

设 $M_2=(Q_2,{a,b},delta_2,s,F_2)$，其中
$ Q_2={s,n_a,n_b,y_a,y_b,d}, quad F_2={y_a,y_b}. $
各状态含义如下：$s$ 表示尚未读入字符；$n_a,n_b$ 表示尚未出现 $a b$、也未出现 $b b$，且分别以 $a,b$ 结尾；$y_a,y_b$ 表示已出现 $a b$、未出现 $b b$，且分别以 $a,b$ 结尾；$d$ 表示已经出现 $b b$。完整转移表为

#align(center, table(
  columns: 3, align: center, inset: 5pt, stroke: 0.4pt,
  table.header([状态], [$a$], [$b$]),
  [$arrow.r s$], [$n_a$], [$n_b$],
  [$n_a$], [$n_a$], [$y_b$],
  [$n_b$], [$n_a$], [$d$],
  [$* y_a$], [$y_a$], [$y_b$],
  [$* y_b$], [$y_a$], [$d$],
  [$d$], [$d$], [$d$],
))

正确性验证：空串对应 $s$。在尚未进入 $d$ 时，读入 $a$ 不会新产生 $a b$ 或 $b b$，只需把末字符改为 $a$；读入 $b$ 时，若原来以 $a$ 结尾，则新产生一个 $a b$，进入 $y_b$，若原来以 $b$ 结尾，则新产生 $b b$，进入 $d$。从 $s$ 读入首字符按相应末字符进入 $n_a$ 或 $n_b$。一旦出现 $b b$，继续添加字符无法消除它，因此 $d$ 为永久拒绝状态。由归纳，所有状态的描述始终成立。接受状态恰为已经出现 $a b$ 且尚未出现 $b b$ 的 $y_a,y_b$，所以该 DFA 接受且仅接受所求语言。

#pagebreak()

#problem(6)[为下面的每个正则语言给出一个正则表达式：]

#parts(
  [${x w x^R bar.v x, w in (a+b)^+}$。],
  [$brace.l w bar.v w in {0,1}^*, w$ 至少含有三个 $1$，且倒数第三个\
    位置是 $1 brace.r$。],
)

#solution()

(a)
$ a(a+b)^+ a + b(a+b)^+  b. $

证明原语言恰为“长度至少为 $3$，且首尾字符相同的 ${a,b}$ 上的字符串”即可。

若 $v=x w x^R$，且 $x,w in (a+b)^+$，则 $x,w$ 均非空，所以 $|v|=2|x|+|w| >= 3$。$x^R$ 的最后一个字符恰为 $x$ 的第一个字符，因此 $v$ 首尾字符相同。上述正则表达式恰好允许首尾同为 $a$ 或同为 $b$，中间部分由 $(a+b)^+$ 保证非空，故 $v$ 属于其语言。

反过来，任意由上述表达式表示的串都可写为 $c u c$，其中 $c in {a,b}$、$u in (a+b)^+$。取 $x=c$、$w=u$，则 $x^R=c$，从而 $c u c=x w x^R$，且满足原题的两个非空条件。故两种描述完全相同。

(b) 令 $U=(0+1)^*$，方便下文证明；正则表达式是

$
  &(0+1)^* 1(0+1)^* 1(0+1)^* 100 \
  &+ (0+1)^* 1(0+1)^* 1(01+10) \
  &+ (0+1)^* 111.
$

把任意倒数第三个字符为 $1$ 的串唯一分解为 $u 1 v$，其中 $u in {0,1}^*$、$|v|=2$。按末尾两个字符 $v$ 中的 $1$ 的个数分类：

#parts(
  [若 $v=00$，则指定的倒数第三个 $1$ 与末尾的 $00$ 一共只有一个 $1$，所以 $u$ 至少还须含有两个 $1$。恰好由 $U 1 U 1 U$ 表示的串可以在两个 1 的前后位置穿插任意个 0 或 1，满足此条件，对应第一项 $U 1 U 1 U 100$。],
  [若 $v in {01,10}$，则 $1v$ 含两个 $1$，所以 $u$ 至少还须含一个 $1$。恰好由 $U 1 U$ 表示的串满足此条件，对应第二项 $U 1 U 1(01+10)$。],
  [若 $v=11$，则 $1v=111$ 已含三个 $1$，故 $u$ 不受额外限制，对应第三项 $U 111$。],
)

以上三类互不遗漏。因此每个满足原条件的串都由相应一项表示；反过来，每一项都保证倒数第三个字符为 $1$，且总共有至少三个 $1$。故该正则表达式与题目语言相等。
