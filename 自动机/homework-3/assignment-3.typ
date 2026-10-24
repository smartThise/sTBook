// 逐句译自 assignment-3.tex；保留原题、公式、占位信息和空白解答栏。
#set document(title: "作业 3", author: "学生姓名")
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
        align(right)[学生姓名 \ 2025000000],
      )
    } else {
      text(size: 9pt, grid(columns: (1fr, 1fr), [作业 3], align(right)[学生姓名]))
    }
    #v(3pt)
    #line(length: 100%, stroke: 1pt)
  ],
)

#let label(body) = text(font: ("Arial", "PingFang SC"), weight: "bold", body)
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

使用 GPT 6.1 Sol 翻译为中文题面。

#problem(1)[（习题 2.3.4 (c)）使用 Thompson 方法，将正则表达式 $00(0+1)^*$ 转换为带有 $epsilon$ 转移的 NFA。]

#solution()

#problem(2)[（习题 2.3.6）设 $A = (Q, Sigma, delta, q_0, {q_f})$ 是一个 $epsilon$-NFA，且没有进入 $q_0$ 的转移，也没有从 $q_f$ 出发的转移。用 $L = L(A)$ 描述对 $A$ 进行以下每种修改后所接受的语言：]

#parts(
  [通过向 $A$ 添加一条从 $q_f$ 到 $q_0$ 的 $epsilon$ 转移而构造的自动机。],
  [通过向 $A$ 添加从 $q_0$ 到每个从 $q_0$ 可达的状态的 $epsilon$ 转移而构造的自动机（沿着一条其标号既可以包含 $Sigma$ 中的符号，也可以包含 $epsilon$ 的路径）。],
  [通过向 $A$ 添加从每个能够沿某条路径到达 $q_f$ 的状态到 $q_f$ 的 $epsilon$ 转移而构造的自动机。],
  [通过对 $A$ 同时执行 (b) 和 (c) 而构造的自动机。],
)

#solution()

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

#problem(4)[证明或证伪以下关于正则表达式的每个陈述。]

#parts(
  [（习题 3.4.1 (g)）$(epsilon + R)^* = R^*$。],
  [（习题 3.4.2 (b)）$(R S + R)^* R = R (S R + R)^*$。],
  [（习题 3.4.2 (d)）$(R + S)^* S = (R^* S)^*$。],
)

#solution()

#pagebreak()

#problem(5)[为下面的每个正则语言构造一个 DFA：]

#parts(
  [在 ${a, b}$ 上的、含有且仅含有奇数个子串 $a b$ 的所有字符串。],
  [在 ${a, b}$ 上的、包含 $a b$ 但不包含 $b b$ 作为子串的所有字符串。],
)

#solution()

#problem(6)[为下面的每个正则语言给出一个正则表达式：]

#parts(
  [${x w x^R bar.v x, w in (a+b)^+}$。],
  [$brace.l w bar.v w in {0,1}^*, w$ 至少含有三个 $1$，且倒数第三个\
    位置是 $1 brace.r$。],
)

#solution()
