#let textbook(title: [], subtitle: [], accent: rgb("22577a"), body) = {
  let serif = sys.inputs.at("cjk-serif", default: "Songti SC")
  let sans = sys.inputs.at("cjk-sans", default: "PingFang SC")
  let mono = sys.inputs.at("mono", default: "Menlo")
  set document(title: title, author: "sTBook")
  set page(paper: "a4", margin: (x: 22mm, y: 21mm), numbering: "1",
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 8pt, fill: rgb("66717b"))
        grid(columns: (1fr, auto), title, [sTBook · 学习笔记])
        line(length: 100%, stroke: 0.4pt + rgb("c7d2dc"))
      }
    })
  set text(font: ("Libertinus Serif", serif), size: 10.5pt, lang: "zh")
  set par(justify: true, leading: 0.7em, spacing: 0.8em)
  set heading(numbering: "1.1")
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    block(above: 1em, below: 1.3em)[#text(size: 21pt, font: sans, fill: accent, weight: "bold", it)]
  }
  show heading.where(level: 2): set text(size: 14pt, font: sans, fill: accent)
  show heading.where(level: 3): set text(size: 11.5pt, font: sans, weight: "bold")
  show raw: set text(font: (mono, sans), size: 8pt)
  show raw.where(block: true): it => block(width: 100%, inset: 9pt, radius: 3pt, fill: rgb("f2f5f8"), breakable: true, it)
  show quote.where(block: true): it => block(inset: (left: 12pt, right: 8pt, y: 6pt), stroke: (left: 2pt + accent), fill: rgb("f3f7fa"), it.body)
  show link: set text(fill: accent)
  set table(inset: 6pt, stroke: 0.35pt + rgb("c7d2dc"))
  set figure(gap: 8pt)
  show figure.caption: set text(size: 9pt)
  align(center)[
    #v(25mm)
    #text(size: 13pt, fill: accent)[从第一步讲起]
    #v(14mm)
    #text(size: 34pt, font: sans, weight: "bold", title)
    #v(8mm)
    #text(size: 17pt)[超级纲要 · 教材式初稿]
    #v(10mm)
    #text(size: 11pt, subtitle)
    #v(24mm)
    #block(width: 85%, inset: 15pt, fill: rgb("f2f5f8"))[
      先弄懂问题，再看图，再一步一步算。\
      定义、公式、代码、例题和错误，都放在一起解释。
    ]
    #v(1fr)
    2026-10-25 · sTBook\
    Wiki 与 Typst 共用正文 · 原图均在图注中注明出处
  ]
  pagebreak()
  outline(title: [章节目录], depth: 1, indent: auto)
  pagebreak()
  body
}
