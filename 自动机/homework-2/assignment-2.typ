// Homework 2 — Formal Languages and Automata
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

== (b)

把这个自动机转换成 DFA。

// ============================================================
= Problem 2

（习题 2.5.3）为下面的语言设计 epsilon-NFA，尽量使用 $epsilon$ 转移来简化设计。

== (a) 

由零个或多个 $a$，接着零个或多个 $b$，再接着零个或多个 $c$ 组成的 string 全体。

分析一下

== (b)

由 $01$ 重复一次或多次，或者 $010$ 重复一次或多次构成的 string 全体。

== (c)

由 $0$ 和 $1$ 组成，且最后 $10$ 个位置中至少有一个 $1$ 的 string 全体。

// ============================================================
= Problem 3

为下面的语言写出正则表达式：

== (a) 

（习题 3.1.1 (b)）右边数第 $10$ 个符号是 $1$ 的 $0$、$1$ string 全体。

显然的是 $(0+1)^9 1 (0+1)^*$。

== (b)

（习题 3.1.1 (c)）至多含一对连续 $1$ 的 $0$、$1$ string 全体。

$(01)^*+(00)^*$

== (c)

（习题 3.1.2 (b)）$0$ 的个数能被 $5$ 整除的 $0$、$1$ string 全体。

$(0)1$

== (d)

（习题 3.1.3 (a)）不含子串 $101$ 的 $0$、$1$ string 全体。

$1^*0+01^*+(((00)(0)^*)^*+1)^*$

== (e)

（习题 3.1.3 (b)）$0$ 和 $1$ 的个数相等，且任何前缀中 $0$ 都不比 $1$ 多两个以上、$1$ 也不比 $0$ 多两个以上的 string 全体。

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

== (b)

给出该自动机的语言的正则表达式。

// ============================================================
= Problem 5 （选做）

设 $L_1$ 和 $L_2$ 分别是被有限自动机 $M_1$ 和 $M_2$ 接受的两个语言。证明 $L_1 inter L_2$ 也被某个有限自动机接受。
