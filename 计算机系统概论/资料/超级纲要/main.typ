#import "../../../module/教材.typ": textbook
#show: textbook.with(title: [计算机系统概论], subtitle: [概念 · 推导 · 原图 · 例题 · 自测])

#{ set heading(numbering: none); include "00-先看这本书.typ" }
#counter(heading).update(0)
#include "01-位字节地址与端序.typ"
#counter(heading).update(1)
#include "02-整数补码与C语言边界.typ"
#counter(heading).update(2)
#include "03-浮点数与舍入.typ"
#counter(heading).update(3)
#include "04-汇编寻址与数据搬运.typ"
#counter(heading).update(4)
#include "05-条件码分支与循环.typ"
#counter(heading).update(5)
#include "06-函数调用栈与递归.typ"
#counter(heading).update(6)
#include "07-数组结构体与内存安全.typ"
#counter(heading).update(7)
#include "08-编译链接与动态库.typ"
#counter(heading).update(8)
#include "09-异常进程与fork.typ"
#counter(heading).update(9)
#include "10-信号与时序竞态.typ"
#counter(heading).update(10)
#include "11-虚拟内存与地址翻译.typ"
#counter(heading).update(11)
#include "12-动态内存分配.typ"
#counter(heading).update(12)
#include "13-系统级输入输出.typ"
#counter(heading).update(13)
#include "14-线程与并发.typ"
#counter(heading).update(14)
#include "15-互斥信号量与死锁.typ"
#counter(heading).update(15)
#include "16-性能与缓存补充.typ"
#counter(heading).update(16)
#include "17-综合走读与检查题.typ"
#counter(heading).update(17)
#include "18-机器表示实战工坊.typ"
#counter(heading).update(18)
#include "19-系统综合题与故障定位.typ"
#{ set heading(numbering: none); include "95-资料覆盖与图源.typ" }
#{ set heading(numbering: none); include "96-术语与记号.typ" }
