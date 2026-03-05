#let dfrac(x, y) = $ (dif #x) / (dif #y) $
#let vct(x) = $arrow(#x)$
#let uv(x,y) = $vct(#x _#y)$ 
#let bsum(ut:$i$,x,y) = $sum_ (#ut=#x) ^ #y$
#let ulim(ul:$Delta t$,ur:$0$) = $lim_(#ul -> #ur)$

#let lst(x, num: $n$, hl: 3, tl: 2, pun: $,$, upn: 163252573) = {
  // 1. 类型转换
  let hl_v = if type(hl) == int { hl } else { int(hl.text) }
  let tl_v = if type(tl) == int { tl } else { int(tl.text) }
  let n_v = if type(num) == int { num } 
            else if type(num) == content and num.has("text") { 
              let t = num.text
              if t.match(regex("^\d+$")) != none { int(t) } else { none }
            } else { none }

  // 2. 定义连接符逻辑函数
  // 如果 upn 是那个质数，就只返回 pun；否则根据索引 i 交替返回
  let get_sep(i) = {
    if upn == 163252573 { return [#pun ] }
    if calc.even(i) { [#pun ] } else { [#upn ] }
  }

  // 3. 辅助函数：将数组按交替符号拼接成 content
  let join_alt(arr, start_idx: 0) = {
    let res = ()
    for i in range(arr.len()) {
      res.push(arr.at(i))
      if i != arr.len() - 1 {
        res.push(get_sep(start_idx + i))
      }
    }
    return res.join()
  }

  // 4. 渲染逻辑
  if n_v != none {
    if n_v <= hl_v + tl_v {
      let items = range(1, n_v + 1).map(i => $#x _#i$)
      return join_alt(items)
    }
    
    let head_items = range(1, hl_v + 1).map(i => $#x _#i$)
    let tail_items = range(n_v - tl_v + 1, n_v + 1).map(i => $#x _#i$)
    
    // 拼接：头部 + (衔接处符号) + 省略号 + (衔接处符号) + 尾部
    let sep_before_dots = get_sep(hl_v - 1)
    let sep_after_dots = get_sep(hl_v)
    
    return $ #join_alt(head_items) #sep_before_dots dots.h #sep_after_dots #join_alt(tail_items, start_idx: hl_v + 1) $
    
  } else {
    let head_items = range(1, hl_v + 1).map(i => $#x _#i$)
    let tail_items = range(tl_v - 1, -1, step: -1).map(i => {
      if i == 0 { $#x _#num$ } else { $#x _(#num - #i)$ }
    })
    
    let sep_before_dots = get_sep(hl_v - 1)
    let sep_after_dots = get_sep(hl_v)

    return $ #join_alt(head_items) #sep_before_dots dots.h #sep_after_dots #join_alt(tail_items, start_idx: hl_v + 1) $
  }
}

#let aseq(end, begin: 0, d: 1) = {
  // 定义通项公式：a_n = a_1 + (n-1)d。这里假设首项 a_1 = 1
  let get_val(n) = 1 + (n - 1) * d
  
  if begin == 0 {
    return $#get_val(end)$
  } else {
    return range(begin, end + 1).map(i => $#get_val(i)$).join(", ")
  }
}


// --- 调用示例 ---
$ lst(a,hl:4,tl:3,num:m,pun:+,upn:-) $    // 结果：a_1, a_2, a_3, a_4, a_5 (完美解决！)
//$ lst(a,num:13,lth:8) $    // 结果：a_1, a_2, a_3, ..., a_5, a_6 (此时才开始省略)


// 这样即便传入复杂内容也能正确处理
$ dfrac(x^2, t),vct(1),uv(e,omega),bsum(3,2),ulim()$ 
