#let phys-vars = state("phys-vars", (g: 9.8, h: 1))

#let cpt(expr-str, digits: 3, unit: "") = {
  context {
    let vars = phys-vars.get()
    
    // 1. 基础解析
    let parts = expr-str.split("=")
    let var-name = if parts.len() > 1 { parts.at(0).trim() } else { "res" }
    let core-expr = if parts.len() > 1 { parts.at(1).trim() } else { expr-str.trim() }

    // 2. 环境与计算
    let ctx = (
      sin: calc.sin, cos: calc.cos, tan: calc.tan,
      sqrt: calc.sqrt, pi: calc.pi
    ) + vars
    let raw-val = eval(core-expr, scope: ctx)

    // 3. 更新变量状态
    phys-vars.update(v => {
      v.insert(var-name, raw-val)
      v
    })

    // 4. 复杂度逻辑判断
    // 检查是否含有字母变量
    let has-vars = false
    let sorted-keys = vars.keys().sorted(key: k => k.len()).rev()
    for k in sorted-keys {
      if core-expr.match(regex("\b" + k + "\b")) != none {
        has-vars = true
        break
      }
    }
    // 检查是否是纯数字（没有任何运算符）
    let is-single-num = core-expr.match(regex("^[\+\-]?\d+(\.\d+)?$")) != none

    // 5. 渲染工具
    let to-m(s) = eval(s, mode: "math")
    let res-rounded = str(calc.round(raw-val, digits: digits))
    
    // 公式部分：字母紧凑；数值部分：* 变 times
    let clean-algebra(s) = s.replace("*", "")
    let beauty-num(s) = s.replace("*", " #math.times ")

    set align(center)
    block(inset: 0pt, breakable: false)[
      #set par(leading: 0pt) 
      $ 
        // 核心逻辑控制
        #{
          if is-single-num {
            // 情况1：右侧只有数字 -> 一段 (var = num)
            [ #to-m(var-name) = #res-rounded ]
          } else if not has-vars {
            // 情况2：只有数字运算 -> 两段 (var = 1*2 = 2)
            [ #to-m(var-name) = #to-m(beauty-num(core-expr)) = #res-rounded ]
          } else {
            // 情况3：含有字母公式 -> 三段 (var = 字母 = 代入 = 结果)
            let substituted = core-expr
            for k in sorted-keys {
              let val = str(calc.round(vars.at(k), digits: digits))
              substituted = substituted.replace(regex("\b" + k + "\b"), val)
            }
            [ #to-m(var-name) = #to-m(clean-algebra(core-expr)) = #to-m(beauty-num(substituted)) = #res-rounded ]
          }
        }
        
        // 单位
        #if unit != "" [ #h(2pt) #math.upright(to-m(unit)) ]
      $
    ]
  }
}