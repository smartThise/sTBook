#let fixed-star(radius: 80pt, circle-r: 15pt) = {
  // 1. 预计算 5 个顶点的精确坐标
  let pts = range(5).map(i => {
    let angle = (i * 72 - 90) * 1deg // 每 72 度一个点，减 90 度从正上方开始
    (radius * calc.cos(angle), radius * calc.sin(angle))
  })

  style(styles => {
    block(width: radius * 2.5, height: radius * 2.5, {
      // 2. 绘制连线 (这里你可以自由组合，不会乱)
      let connections = ((0,2), (2,4), (4,1), (1,3), (3,0)) // 内部星形
      // let connections = ((0,1), (1,2), (2,3), (3,4), (4,0)) // 外部五边形
      
      for (i, j) in connections {
        let p1 = pts.at(i)
        let p2 = pts.at(j)
        place(center + horizon, line(start: p1, end: p2, stroke: 0.5pt + gray))
      }

      // 3. 绘制等大圆圈 (放在连线之后，确保圆圈盖住线条末端)
      let labels = ("A", "B", "C", "D", "E")
      for i in range(5) {
        let (x, y) = pts.at(i)
        place(center + horizon, dx: x, dy: y, {
          circle(radius: circle-r, fill: white, stroke: 0.8pt)
          align(center + horizon, labels.at(i))
        })
      }
    })
  })
}

#fixed-star()