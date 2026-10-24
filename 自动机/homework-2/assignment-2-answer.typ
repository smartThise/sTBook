// Homework 2 — Formal Languages and Automata（完整作答版，原稿见 assignment-2.typ）
#import "@preview/fletcher:0.5.8": diagram, node, edge

#set page(
  paper: "us-letter",
  margin: (x: 1.0in, y: 0.9in),
  numbering: "1",
  number-align: center,
)
#set text(font: ("Times New Roman", "Songti SC"), size: 11pt, lang: "zh")
#set par(justify: true, leading: 0.78em)
#show heading.where(level: 1): it => block(above: 1.4em, below: 0.6em, text(
  font: ("Times New Roman", "PingFang SC"), size: 12.5pt, weight: "bold", it.body,
))
#show heading.where(level: 2): it => block(above: 1.0em, below: 0.4em, text(
  font: ("Times New Roman", "PingFang SC"), size: 11.5pt, weight: "bold", it.body,
))

// 批注框：标出原稿的错误或空缺
#let note(body) = block(
  width: 100%,
  inset: (x: 7pt, y: 5pt),
  above: 0.6em, below: 0.6em,
  stroke: (left: 2.5pt + rgb("#c0392b")),
  fill: rgb("#fdf2f0"),
)[#text(fill: rgb("#c0392b"), weight: "bold")[批注：] #body]

#align(center)[
  #text(size: 15pt, weight: "bold")[Homework 2] \
  #v(0.2em)
  #text(size: 10.5pt)[郭嘉乐 #h(1.5em) 2025013332]
]
#v(0.6em)

助教好，由于英文实在看起来太累人了，但是不对照题目又不行，所以简单 LLM 翻译了一下。

// ============================================================
= Problem 1

（习题 2.5.2）考虑下面的 epsilon-NFA，起始状态是 $p$，接受状态是 $r$，其余状态既不接受也不起始：

#block(breakable: false, align(center, table(
    columns: 5,
    align: center + horizon,
    stroke: 0.5pt,
    table.header([状态], [$epsilon$], [$a$], [$b$], [$c$]),
    [$p$], [$\{q, r\}$], [$emptyset$], [$\{q\}$], [$\{r\}$],
    [$q$], [$emptyset$], [$\{p\}$], [$\{r\}$], [$\{p, q\}$],
    [$r$], [$emptyset$], [$emptyset$], [$emptyset$], [$emptyset$],
  )))

== (a)

给出该自动机接受的所有长度不超过 $3$ 的 string。



先求起始状态的 $epsilon$-闭包：$E(p) = \{p, q, r\}$。由于闭包中含接受状态 $r$，空串 $epsilon$ 被接受。

逐步模拟（每步读入后取 $epsilon$-闭包）：
- 读 $a$：$\{p,q,r\} arrow.r \{p,q,r\}$（$q arrow.r^(a) p$，通过闭包补回了 $q,r$）
- 读 $b$：$\{p,q,r\} arrow.r \{q,r\}$
- 读 $c$：$\{p,q,r\} arrow.r \{p,q,r\}$（$p arrow.r^(c) r$，$q arrow.r^(c) p,q$）

类似地，$\{q,r\}$ 读 $a,c$ 回到 $\{p,q,r\}$，读 $b$ 到 $\{r\}$；$\{r\}$ 读任何符号都到 $emptyset$。含 $r$ 的子集都是接受的，所以接受的串为：

- 长度 $0$：$epsilon$；
- 长度 $1$：$a, b, c$；
- 长度 $2$：`aa`, `ab`, `ac`, `ba`, `bb`, `bc`, `ca`, `cb`, `cc`（$9$ 个）；
- 长度 $3$：`aaa`, `aab`, `aac`, `aba`, `abb`, `abc`, `aca`, `acb`, `acc`, `baa`, `bab`, `bac`, `bca`, `bcb`, `bcc`, `caa`, `cab`, `cac`, `cba`, `cbb`, `cbc`, `cca`, `ccb`, `ccc`（$24$ 个）。

合计 $37$ 个。

// #note[长度 $3$ 的 $27$ 个串中，`bba`、`bbb`、`bbc` 不被接受（读完 `bb` 后子集为 $\{r\}$，再读任何符号都进入死状态 $emptyset$），因此长度 $3$ 只有 $24$ 个。]

== (b)

把这个自动机转换成 DFA。

// #note[原稿为空白。下面用子集构造法。]

用子集构造，每个 DFA 状态对应一组 NFA 状态（均取 $epsilon$-闭包）。从起始闭包 $A = \{p,q,r\}$ 出发，可达的状态只有四个：

#block(breakable: false, align(center, table(
    columns: 4,
    align: center + horizon,
    stroke: 0.5pt,
    table.header([DFA 状态], [$a$], [$b$], [$c$]),
    [$A = \{p,q,r\}$（起始，接受）], [$A$], [$B$], [$A$],
    [$B = \{q,r\}$（接受）], [$A$], [$C$], [$A$],
    [$C = \{r\}$（接受）], [$D$], [$D$], [$D$],
    [$D = emptyset$], [$D$], [$D$], [$D$],
  )))

接受状态是 $A, B, C$（即子集含 $r$ 者）。这个 DFA 与原 $epsilon$-NFA 语言相同，可以验证它正好接受第 1(a) 题所列的 $37$ 个串。

#align(center)[#diagram(
  node-stroke: 0.8pt,
  edge-stroke: 0.8pt,
  spacing: (22mm, 24mm),
  node((0, 0), $A$, shape: circle, extrude: (-2.5, 0), name: <A>),
  node((1, 0), $B$, shape: circle, extrude: (-2.5, 0), name: <B>),
  node((2, 0), $C$, shape: circle, extrude: (-2.5, 0), name: <C>),
  node((3, 0), $D$, shape: circle, name: <D>),
  edge((-1, 0), <A>, "-|>", label: [起始], label-side: left),
  edge(<A>, <B>, "-|>", $b$, label-side: left),
  edge(<B>, <C>, "-|>", $b$, label-side: left),
  edge(<C>, <D>, "-|>", $a, b, c$, label-side: left),
  edge(<A>, <A>, "-|>", loop-angle: -90deg, label: $a, c$, label-side: left),
  edge(<B>, <A>, "-|>", bend: 35deg, label: $a, c$, label-side: right),
  edge(<D>, <D>, "-|>", loop-angle: -90deg, label: $a, b, c$, label-side: left),
)]

这里
图实在是太难画了……

// ============================================================
= Problem 2

（习题 2.5.3）为下面的语言设计 epsilon-NFA，尽量使用 $epsilon$ 转移来简化设计。

== (a)

由零个或多个 $a$，接着零个或多个 $b$，再接着零个或多个 $c$ 组成的 string 全体。

分析：三段分别用一个自环状态表示（$a^*$、$b^*$、$c^*$），段与段之间用 $epsilon$ 转移相连。这样自然保证顺序是 $a$ 段在前、$b$ 段居中、$c$ 段在后，而且每段都可以为空。

设状态 $q_0, q_1, q_2$，起始 $q_0$，接受 $q_2$。
- $q_0 arrow.r^(a) q_0$，$q_0 arrow.r^(epsilon) q_1$；
- $q_1 arrow.r^(b) q_1$，$q_1 arrow.r^(epsilon) q_2$；
- $q_2 arrow.r^(c) q_2$。

// #note[原稿此处只有一句“分析一下”，没有给出任何设计，属于空缺。]

== (b)

由 $01$ 重复一次或多次，或者 $010$ 重复一次或多次构成的 string 全体。

设起始状态 $s$，两条分支分别识别 $(01)^+$ 和 $(010)^+$，两分支只通过 $epsilon$ 与 $s$ 和终态相连接、互不打扰。
- $s arrow.r^(epsilon) a_1$，$s arrow.r^(epsilon) b_1$；
- 分支 $(01)^+$：$a_1 arrow.r^(0) a_2 arrow.r^(1) a_3$，$a_3 arrow.r^(epsilon) a_1$，$a_3 arrow.r^(epsilon) f$；
- 分支 $(010)^+$：$b_1 arrow.r^(0) b_2 arrow.r^(1) b_3 arrow.r^(0) b_4$，$b_4 arrow.r^(epsilon) b_1$，$b_4 arrow.r^(epsilon) f$。

接受状态为 $f$。

== (c)

由 $0$ 和 $1$ 组成，且最后 $10$ 个位置中至少有一个 $1$ 的 string 全体。

分析：“猜测”哪一个 $1$ 处在最后 $10$ 个位置之内。
- 状态 $s$（起始）：$s arrow.r^(0,1) s$（前面的符号随意），$s arrow.r^(1) t_1$（猜测这就是那个 $1$）；
- $t_k arrow.r^(0,1) t_(k+1)$，$1 <= k <= 9$：猜测的 $1$ 之后最多还有 $9$ 个符号；
- 接受状态为 $t_1, t_2, dots, t_(10)$。

正确性：若某个 $1$ 处在最后 $10$ 个位置内，它之后的符号不超过 $9$ 个，因而能被上述路径接受；反之，路径接受时猜出的那个 $1$ 之后至多 $9$ 个符号，它必在最后 $10$ 个位置内。对于长度不足 $10$ 的串，任何一个 $1$ 都满足条件，与题意一致。

// #note[原稿此题空缺。这个 $epsilon$-NFA 只用了非 $epsilon$ 转移，本身已是最简；如果需要，也可以直接给出 DFA 的 $2^(10)$ 状态版本，但会远比这复杂。]

// ============================================================
= Problem 3

为下面的语言写出正则表达式：

== (a)

（习题 3.1.1 (b)）右边数第 $10$ 个符号是 $1$ 的 $0$、$1$ string 全体。

$(0+1)^* 1 (0+1)^9$

理由：右边数第 $10$ 个符号是 $1$，意味着该 $1$ 之后恰好有 $9$ 个任意符号，之前是任意串。

// #note[你的 $(0+1)^9 1 (0+1)^*$ 是“左边数第 $10$ 个符号是 $1$”，方向写反了。例如串 $0000000001$ 从左数第 10 位是 $1$，但从右数第 10 位是 $0$，它不属于本题语言，却被你的式子接受。]

== (b)

（习题 3.1.1 (c)）至多含一对连续 $1$ 的 $0$、$1$ string 全体。

$(0+10)^* (epsilon + 1) + (0+10)^* 11 (epsilon + 0 (0+10)^* (epsilon + 1))$

理由：题意相当于“子串 $11$ 至多出现一次”。
- 不含 $11$ 的串：不含连续的 $1$，所以可以拆成 $0$ 与 $10$ 的拼接，最后可选地补一个 $1$。
- 恰含一次 $11$ 的串：前半部分不含 $11$ 且不以 $1$ 结尾（否则会形成 $111$），因此是 $(0+10)^*$；接着是 $11$；后半部分必须以 $0$ 开始（否则也出现 $111$），之后仍是不含 $11$ 的串。

// #note[你的 $(01)^* + (00)^*$ 远远不够。例如 $10$ 不含 $11$，应被接受，但不属于 $(01)^*$ 也不属于 $(00)^*$；$0110$ 恰含一对 $11$，同样被你的式子拒绝。]

== (c)

（习题 3.1.2 (b)）$0$ 的个数能被 $5$ 整除的 $0$、$1$ string 全体。

$1^* (0 1^* 0 1^* 0 1^* 0 1^* 0 1^*)^*$

理由：$1$ 可以随意插入，所以只需控制 $0$ 的个数。把串按每 $5$ 个 $0$ 切成一块，每块形如 $0 1^* 0 1^* 0 1^* 0 1^* 0 1^*$（$1$ 可以出现在任意位置）即可。


== (d)

（习题 3.1.3 (a)）不含子串 $101$ 的 $0$、$1$ string 全体。

$(0 + 1^+ 00)^* (epsilon + 1^+ + 1^+ 0)$

理由：不含 $101$ 等价于：每次出现 “$10$” 之后，下一个符号只能是 $0$ 或串结束。因此每一段 $1$ 之后若跟 $0$，必须是 $100$ 的形式或者已经达到末尾，于是串可以拆成 $0$ 与 $1^+00$ 的拼接，最后可选地跟一段 $1^+$ 或 $1^+0$。

// #note[你的 $1^* 0 + 01^* + (((00)(0)^*)^* + 1)^*$ 是错的。例如 $010$ 不含 $101$，应被接受，但它既不在 $1^*0$ 中，也不在 $01^*$ 中，而后面的括号部分只能生成以 $00$ 或 $1$ 为块的串，无法生成单独的 $0$ 后跟 $1$，所以它被拒绝。]

== (e)

（习题 3.1.3 (b)）$0$ 和 $1$ 的个数相等，且任何前缀中 $0$ 都不比 $1$ 多两个以上、$1$ 也不比 $0$ 多两个以上的 string 全体。

$(01 + 10)^*$

理由：设 $d$ 为前缀中“$0$ 的个数减 $1$ 的个数”。题意要求 $|d| <= 1$ 对所有前缀成立。由于每个符号使 $d$ 改变 $plus.minus 1$，所以 $d = 0$ 只能出现在偶数长度的前缀上，且假设从前缀开始向后延伸构造，0 和 1 都不可能在从前向后构造的过程中连续出现超过 2 次，否则不成立。于是串可以切成长度为 $2$ 的块，每块从 $d=0$ 出发，经过 $d = plus.minus 1$ 回到 $d = 0$，所以每块只能是 $01$ 或 $10$。反之，任何 $(01+10)^*$ 中的串满足条件。

// #note[原稿此题空缺。]

// ============================================================
= Problem 4

下面是一个 DFA 的转移表，起始状态是 $q_1$，接受状态是 $q_3$：

#block(breakable: false, align(center, table(
    columns: 3,
    align: center + horizon,
    stroke: 0.5pt,
    table.header([状态], [读 $0$], [读 $1$]),
    [$q_1$], [$q_2$], [$q_1$],
    [$q_2$], [$q_3$], [$q_1$],
    [$q_3$], [$q_3$], [$q_2$],
  )))

== (a)

给出所有的 $R^(2)_(i j)$，这些表达式尽量化简。

用归纳法。记 $R^((k))_(i j)$ 为从 $i$ 到 $j$、中间状态只取 $\{1, dots, k\}$ 的路径标签的正则表达式，递推式为
$ R^((k))_(i j) = R^((k-1))_(i j) + R^((k-1))_(i k) (R^((k-1))_(k k))^* R^((k-1))_(k j). $

*$R^((0))$*（直接转移，若 $i = j$ 则加上 $epsilon$）：
- $R^((0))_(11) = epsilon + 1$，$R^((0))_(12) = 0$，$R^((0))_(13) = emptyset$；
- $R^((0))_(21) = 1$，$R^((0))_(22) = epsilon$，$R^((0))_(23) = 0$；
- $R^((0))_(31) = emptyset$，$R^((0))_(32) = 1$，$R^((0))_(33) = epsilon + 0$。

*第 $k = 1$ 步*（允许经过 $q_1$）。由于 $(R^((0))_(11))^* = (epsilon + 1)^* = 1^*$：
- $R^((1))_(11) = 1^*$，$R^((1))_(12) = 1^* 0$，$R^((1))_(13) = emptyset$；
- $R^((1))_(21) = 1 + 1 1^* = 1 1^*$，$R^((1))_(22) = epsilon + 1 1^* 0$，$R^((1))_(23) = 0$；
- $R^((1))_(31) = emptyset$，$R^((1))_(32) = 1$，$R^((1))_(33) = epsilon + 0$。

*第 $k = 2$ 步*（允许经过 $q_1, q_2$）。记 $Y = 1 1^* 0$，则 $(R^((1))_(22))^* = (epsilon + Y)^* = Y^* = (1 1^* 0)^*$：
- $R^((2))_(11) = (1 + 0 1)^*$（由 $1^* + 1^* 0 (1 1^* 0)^* 1 1^*$ 化简而来）；
- $R^((2))_(12) = 1^* 0 (1 1^* 0)^*$；
- $R^((2))_(13) = 1^* 0 (1 1^* 0)^* 0$；
- $R^((2))_(21) = (1 1^* 0)^* 1 1^*$；
- $R^((2))_(22) = (1 1^* 0)^*$；
- $R^((2))_(23) = (1 1^* 0)^* 0$；
- $R^((2))_(31) = 1 (1 1^* 0)^* 1 1^*$；
- $R^((2))_(32) = 1 (1 1^* 0)^*$；
- $R^((2))_(33) = epsilon + 0 + 1 (1 1^* 0)^* 0$。


== (b)

给出该自动机的语言的正则表达式。

接受语言为 $L = R^((3))_(13)$。由递推式，$R^((3))_(13) = R^((2))_(13) + R^((2))_(13) (R^((2))_(33))^* R^((2))_(33)$，化简为 $R^((2))_(13) (R^((2))_(33))^*$，所以
$ L = 1^* 0 (1 1^* 0)^* 0 (epsilon + 0 + 1 (1 1^* 0)^* 0)^*. $



// ============================================================
= Problem 5 （选做）

设 $L_1$ 和 $L_2$ 分别是被有限自动机 $M_1$ 和 $M_2$ 接受的两个语言。证明 $L_1 inter L_2$ 也被某个有限自动机接受。

*证明* 设 $M_1 = (Q_1, Sigma, delta_1, s_1, F_1)$，$M_2 = (Q_2, Sigma, delta_2, s_2, F_2)$。若含 $epsilon$ 转移，先用闭包消去，不影响语言。构造
$ M = (Q_1 times Q_2, Sigma, delta, (s_1, s_2), F_1 times F_2), $
其中 $delta((p, q), a) = { (p', q') | p' in delta_1(p, a), q' in delta_2(q, a) }$。

*断言*：对任意串 $w$ 与任意 $p in Q_1, q in Q_2$，有
$ hat(delta)((p, q), w) = hat(delta)_1(p, w) times hat(delta)_2(q, w). $

按 $|w|$ 归纳。
- *基础* $w = epsilon$：左边 $= {(p,q)}$，右边 $= {p} times {q}$，相等。
- *归纳步*：设断言对 $w$ 成立，考虑 $w a$（$a in Sigma$）。由扩展转移函数的定义，
$ hat(delta)((p,q), w a) = union.big_((p', q') in hat(delta)((p,q), w)) delta((p', q'), a) = union.big_(p' in hat(delta)_1(p,w),\ q' in hat(delta)_2(q,w)) (delta_1(p', a) times delta_2(q', a)). $
利用 $(union_i A_i) times (union_j B_j) = union_(i,j) (A_i times B_j)$，得
$ = (union.big_(p' in hat(delta)_1(p,w)) delta_1(p', a)) times (union.big_(q' in hat(delta)_2(q,w)) delta_2(q', a)) = hat(delta)_1(p, w a) times hat(delta)_2(q, w a). $
得证。

*结论*：$w in L(M)$ 当且仅当 $hat(delta)((s_1, s_2), w)$ 含有某个 $(p, q) in F_1 times F_2$，即 $hat(delta)_1(s_1, w)$ 含 $p in F_1$ 且 $hat(delta)_2(s_2, w)$ 含 $q in F_2$，即 $w in L_1$ 且 $w in L_2$。故 $L(M) = L_1 inter L_2$，于是 $L_1 inter L_2$ 被有限自动机 $M$ 接受。
