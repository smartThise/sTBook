// Homework 2 — Formal Languages and Automata
//
// 本文件把用户粘贴的外部答案（覆盖 Problem 1、2、3(a)）转存为 Typst。
// 逐条用穷举模拟核对过（脚本 /tmp/verify_hw2.py），结论：
//   · P1(a) 穷举长度 0..3 的全部 1+3+9+27 个串，结果与本文完全一致；
//   · P1(b) 子集构造：可达子集恰为 {p,q,r}、{q,r}、{r}、∅，转移表逐格一致；
//   · P2(a)(b)(c) 的三个 ε-NFA 与各自目标语言在长度 ≤ 6 / 8 / 12 上完全一致；
//   · P3(a) $(0+1)^*1(0+1)^9$ 与「右数第 10 个符号是 1」完全等价；
//     原稿 $(0+1)^9 1 (0+1)^*$ 写反了（最小反例 0000000001）。
// 注意：粘贴内容在 Problem 3(a) 的批注处被截断，未包含 3(b)–(e)、Problem 4、Problem 5。
// 原题见 assignment-2.typ；完整解答另见 solution-2.typ / assignment-2-answer.typ。
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

#let note(body) = block(
  width: 100%,
  inset: (x: 7pt, y: 5pt),
  above: 0.6em, below: 0.6em,
  stroke: (left: 2.5pt + rgb("#c0392b")),
  fill: rgb("#fdf2f0"),
)[#text(fill: rgb("#c0392b"), weight: "bold")[注：] #body]

#align(center)[
  #text(size: 15pt, weight: "bold")[Homework 2 解答（Problem 1–3(a) 核对稿）] \
  #v(0.2em)
  #text(size: 10.5pt)[郭嘉乐 #h(1.5em) 2025013332]
]
#v(0.6em)

= Problem 1（习题 2.5.2）

先求 $epsilon$-闭包：
$ E C (p) = \{p, q, r\}, quad E C (q) = \{q\}, quad E C (r) = \{r\}. $

== (a) 长度不超过 $3$ 的被接受串

由下面的 DFA 可知，接受状态为含 $r$ 的子集。

- 长度 $0$：$epsilon$ 被接受。
- 长度 $1$：所有单字符 $a, b, c$ 都被接受。
- 长度 $2$：所有 $3^2 = 9$ 个串都被接受：$a a, a b, a c, b a, b b, b c, c a, c b, c c$。
- 长度 $3$：总共有 $27$ 个串，其中不被接受的只有 $b b a, b b b, b b c$，所以其余 $24$ 个都被接受。

因此所有长度不超过 $3$ 的被接受串为：$epsilon$；$a, b, c$；
$a a, a b, a c, b a, b b, b c, c a, c b, c c$；
以及长度 $3$ 中除 $b b a, b b b, b b c$ 外的全部串。

== (b) 转成 DFA

用子集构造法。初始状态
$ A = E C (p) = \{p, q, r\}. $

计算转移：

- $A = \{p, q, r\}$：$a arrow.r E C (\{p\}) = \{p, q, r\} = A$，$b arrow.r E C (\{q, r\}) = \{q, r\} = B$，$c arrow.r E C (\{p, q, r\}) = \{p, q, r\} = A$。
- $B = \{q, r\}$：$a arrow.r E C (\{p\}) = \{p, q, r\} = A$，$b arrow.r E C (\{r\}) = \{r\} = C$，$c arrow.r E C (\{p, q\}) = \{p, q, r\} = A$。
- $C = \{r\}$：$a, b, c arrow.r emptyset = D$。
- $D = emptyset$：$a, b, c arrow.r D$。

DFA 转移表如下：

#block(breakable: false, align(center, table(
    columns: 4,
    align: center + horizon,
    stroke: 0.5pt,
    table.header([状态], [$a$], [$b$], [$c$]),
    [$arrow.r A = \{p, q, r\}$（接受）], [$A$], [$B$], [$A$],
    [$B = \{q, r\}$（接受）], [$A$], [$C$], [$A$],
    [$C = \{r\}$（接受）], [$D$], [$D$], [$D$],
    [$D = emptyset$], [$D$], [$D$], [$D$],
  )))

其中 $A, B, C$ 都是接受状态，因为都含 $r$。起始状态是 $A$。

= Problem 2（习题 2.5.3）

== (a) $a^* b^* c^*$

设计 $epsilon$-NFA：状态 $q_0$（起始）、$q_1$、$q_2$（接受）。

转移：
$ q_0 arrow.r^a q_0, quad q_0 arrow.r^epsilon q_1, quad
  q_1 arrow.r^b q_1, quad q_1 arrow.r^epsilon q_2, quad
  q_2 arrow.r^c q_2. $

接受状态为 $q_2$。由于 $epsilon$ 闭包包含 $q_2$，所以空串也被接受。

== (b) $(0 1)^+ union (0 1 0)^+$

设计两个分支，用 $epsilon$ 从起始状态进入。

状态：$q_0$ 起始；分支 1 为 $A_1, A_2, A_3$，其中 $A_3$ 接受；分支 2 为 $B_1, B_2, B_3, B_4$，其中 $B_4$ 接受。

转移：
$ q_0 arrow.r^epsilon A_1, quad q_0 arrow.r^epsilon B_1. $

分支 1，识别 $(0 1)^+$：
$ A_1 arrow.r^0 A_2, quad A_2 arrow.r^1 A_3, quad A_3 arrow.r^0 A_2. $

分支 2，识别 $(0 1 0)^+$：
$ B_1 arrow.r^0 B_2, quad B_2 arrow.r^1 B_3, quad B_3 arrow.r^0 B_4, quad B_4 arrow.r^0 B_2. $

接受状态为 $A_3, B_4$。

== (c) 最后 $10$ 个位置中至少有一个 $1$

思路：非确定性地「猜」最后 $10$ 位中的某个 $1$，然后保证它后面最多还有 $9$ 个符号。

状态：$q_0$ 起始，循环读任意 $0, 1$；$s$；$r_1, r_2, dots, r_(10)$，其中 $r_1, dots, r_(10)$ 都是接受状态。

转移：
$ q_0 arrow.r^(0,1) q_0, quad q_0 arrow.r^epsilon s, quad s arrow.r^1 r_1. $

对 $i = 1, dots, 9$：
$ r_i arrow.r^(0,1) r_(i+1). $

$r_(10)$ 不再有出边。

这样，如果猜到的那个 $1$ 后面还有 $k <= 9$ 个符号，则路径停在 $r_(k+1)$，而 $r_(k+1)$ 是接受状态；如果后面还有 $10$ 个或更多符号，则该路径无法在接受状态结束。因此该 $epsilon$-NFA 接受且仅接受「最后 $10$ 个位置中至少有一个 $1$」的串。

= Problem 3 正则表达式

== (a) 右边数第 $10$ 个符号是 $1$

正确表达式：
$ (0 + 1)^* 1 (0 + 1)^9. $

理由：最后 $10$ 个位置中，第 $10$ 个（从右往左数）是 $1$，它右边还有 $9$ 个任意符号，左边任意。

#note[你写的是 $(0 + 1)^9 1 (0 + 1)^*$，方向反了：那是「左边数第 $10$ 个符号是 $1$」。
最小反例是 $0000000001$——它被原式接受，但从右数第 $10$ 个符号是 $0$，不属于本题语言。]

#note[粘贴内容到此截断：本稿只有 Problem 1、2 和 3(a)，不含 Problem 3(b)–(e)、Problem 4、Problem 5。
原题目见 `assignment-2.typ`，其余各问的解答见 `solution-2.typ`。]
