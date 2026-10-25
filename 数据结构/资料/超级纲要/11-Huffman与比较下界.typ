= Huffman编码与比较下界
<huffman编码与比较下界>
数字通讯中，字符要变成二进制位串才能上线传输。若每个字符固定用等长的编码，总长度可以预算；但不同字符的出现频度天差地别------高频字符配短码、低频字符配长码，总长可以大幅压缩。代价是必须#strong[前缀无关]（prefix-free）：任何字符的编码都不能是另一字符编码的前缀，否则解码者面对001无法判断它是字符I还是NM的开头。本章解决两个问题：怎样构造总编码长度最小的前缀无关编码（Huffman树），以及------一个更大的主题------#strong[怎样证明某个算法已经不可能再改进]（复杂度下界、比较树、线性归约）。

== 前缀无关编码与编码树
<前缀无关编码与编码树>
把字母表$Sigma$中的每个字符各作为一个叶节点，随意组成一棵#strong[真二叉树]：从根到叶x的通路即x的编码，左、右分支分别记0、1。通路上除终点外都是内部节点------叶不可能出现在另一叶的路径上，前缀无关性由树结构自然保证。这样的树称#strong[PFC编码树]；字符的编码长度即对应叶的深度，整体成本为所有字符编码长度之和CL。PFC并不唯一，何者CL最短？CL最短者称#strong[最优编码树]（OCT），必然存在（真二叉树只有有限多棵）------虽然未必唯一。

不加权的情形有一个干净的刻画：#strong[OCT的叶子只能出现在倒数两层]------否则深叶与浅叶交换总能降低CL；而"完全"的真二叉树即是OCT，$C L = n times ceil.l log_2 n ceil.r$ 量级。真正的难点在带权情形：字符的使用频度各不相同，衡量尺度换成#strong[带权平均编码长度]（叶深 × 字符频度的总和，即WPL）。均衡树在频度悬殊时（比如"小米加步枪"对"飞机加坦克"的悬殊对比）反而远远不是最优------需要的算法必须把频度考虑进来。

== Huffman树：贪心合并
<huffman树贪心合并>
#strong[Huffman算法]（1952）一句话说完：反复从森林中取出权重最小的两棵树，合并为一棵（新树权重为二者之和），插回森林；$n - 1$ 次迭代后森林中唯一所剩的那棵，即Huffman编码树。字符节点封装为：

```cpp
struct HuffChar {                       //Huffman字符：字符+频数
   char ch;  uint32_t weight;
   bool operator<( const HuffChar& hc ) //比较器
      { return weight > hc.weight; }    //故意大小颠倒
};                                      //便于delMax()取出最小者
```

森林就是一个优先级队列。贪心合并的实现：

```cpp
HuffTree huffTree( HuffForest& F ) {
   while ( 1 < F.size() ) {                       //每迭代一步，森林减一
      HuffTree T1 = F.delMax(), T2 = F.delMax();  //取出最小两棵（T2权重不小于T1）
      HuffTree S;  S.insert( HuffChar( Weight(T2) + Weight(T1) ) );
      S.attach( T2, S.root() );  S.attach( S.root(), T1 );   //合并
      F.insert( S );                              //插回森林
   }
   return F.delMax();   //层次序列必然单调非增
}
```

以频数 $A = 2$、$B = 3$、$C = 5$、$D = 8$ 为例的完整合并过程：

#figure(image("图片/演示-ds11-huffman-01.svg", alt: "逐步演示：Huffman贪心合并：2,3,5,8"),
  caption: [
    逐步演示：Huffman贪心合并：2,3,5,8
  ]
)

结果：A=110、B=111、C=10、D=0，$W P L = 3 times 2 + 3 times 3 + 2 times 5 + 1 times 8 = 33$------频数最高的D只占1位，最低的A占3位，高频短码、低频长码。

#strong[正确性]（归纳法）。关键引理：#strong[频数最低的两个字符x与y，必在某棵OCT中互为兄弟]------若在某最优树中不是兄弟，可通过两次交换使它们成对且WCL不增。设$\|Sigma\|< n$时Huffman算法生成OCT；对$\|Sigma\|= n$，令$Sigma'$为把x、y合并成新字符z（权重相加）后的字符集，两个字符集的PFC树集合之间存在一一对应（z展开为x、y兄弟 ⇔ x、y合并为z），且两种树形的WCL恰差一个固定值 $w\(x\)+ w\(y\)$------"差距固定，故最优必对应于最优"。归纳完成。

一个需要约定的细节：OWCT通常有多棵（同深子树可互换，甚至不同深也可能），Huffman算法对某些细节也未明确------约定#strong[以实现的版本为准]：左兄弟（深层者）不小于右兄弟。

== Huffman森林的实现：从O(n²)到O(n)
#label("huffman森林的实现从on²到on")
运行时间取决于森林的delMax()与insert()。#strong[列表实现]（ListPQ：insert插队尾、delMax摘最大）两操作合计每步$O\(n\)$，总体$O\(n^2\)$。改用完全二叉堆或左式堆（第12章）每步$O\(log n\)$，总体$O\(n log n\)$。有意思的是，#strong[直接用最简单的数据结构也能做到$O\(n\)$]------森林=栈+队列：

```cpp
struct HuffForest {                       //一个栈 + 一个队列
   Stack<HuffTree> S;  Queue<HuffTree> Q; //两者全程各自有序
   HuffForest( uint32_t* freq, char s, char t ) {   //初始化：字符按频数排序后入栈
      for ( char c = s; c < t; c++ ) S.push( HuffTree().insert({ freq[c-s], c }) );
      S.sort();                                       //频数逆序
   }
   void insert( HuffTree t ) { Q.enqueue( t ); }      //合并树只进队列
   HuffTree delMax() {                                //最小树只可能在栈顶或队首
      return S.empty() || ( !Q.empty() && ( Q.front() > S.top() ) )
             ? Q.dequeue() : S.pop();
   }
};
```

原理：按频数排序后所有字符入栈（频数逆序，栈顶最小）；此后只出不进；合并生成的树单调不降，恰好构成一个有序队列。两个有序序列的delMax只需比较栈顶与队首，$O\(1\)$；insert也是$O\(1\)$。第09章"有序序列合并"的思想在此再度发力。

== 下界与最优：比较树
<下界与最优比较树>
同一问题的不同算法，复杂度可能相差悬殊；但针对任何一个具体计算问题，算法的改进不可能持续获得------#strong[改进的尽头称作该问题的复杂度下界]（lower bound），达到下界的算法即#strong[最坏情况最优算法]（worst-case optimal, WCOA）。怎样证明下界？看一个热身：从4个外观相同的苹果中找出唯一的重量不同者，借助天平只需2次称量------为什么2次就够、又不会再少？

#strong[比较树]（comparison tree）。基于比较的算法（comparison-based algorithm, CBA）的每次比较至多有分支数种走向，整个运行过程对应一棵树：运行的输出对应叶节点，运行的过程对应从根到叶的路径，消耗的时间即路径长度，最坏情况耗时即#strong[树的高度]。若问题有n种输出（比如n个互异元素的一种排序），树至少需要n片叶；而高为h的二叉树至多$2^h$片叶，故

$ n lt.eq 2^h arrow.r.double.long h gt.eq ceil.l log_2 n ceil.r $

这就是比较树的下界通式。#strong[苹果甄别]：4种输出（谁是异重者），下界$ceil.l log_2 4 ceil.r = 2$次称量，且2次称量的算法存在------下界紧。#strong[n个元素的排序]：共有$n !$种输入/输出，下界

$ ceil.l log_2 n ! ceil.r = Omega\(n log n\) $

由Stirling公式$log_2 n ! approx n log_2 n - 1.44 log_2 n$。归并排序的$O\(n log n\)$与之匹配，故属于WCOA------第06章"最坏情况最优"的断言在此兑现。

== 线性归约：下界的传染性
<线性归约下界的传染性>
每个问题的下界都要这样一对一地证明吗？不必。#strong[线性归约]（linear-time reduction）：若问题W可在$O\(n\)$时间内转化为问题U的输入，且U的输出可$O\(n\)$转化回W的输出，则W的任何算法都对应于U的一个算法（曲径通幽：输入转化→U算法→输出转化），于是

$ Omega\(n log n\)lt.eq\|W\|lt.eq\|U\| $

U的下界"传染"给W。两个实例：

#strong[SORTING ≤N HUFFMAN]：排序的每个输入（n个实数）可以直接理解为Huffman的一个输入（n个字符的频数）；Huffman输出的编码树经层次遍历，必然得到有序序列（包含所有内部与叶节点）------$O\(n\)$双向转换。因此Huffman本身也具有$Omega\(n log n\)$的下界：上一节栈+队列的$O\(n\)$实现并不与此矛盾------下界针对的是基于#strong[比较]的模型，$O\(n\)$实现绕开的正是比较（它利用了"频数可排序预处理"这一额外信息）。

#strong[SORTING ≤N RBM]（红蓝匹配）：给平面上互不重合的红、蓝点各n个，用n条无交线段联结异色点。排序的每个输入映射为x正半轴上的n个红点（预处理$O\(n\)$），y正半轴上有序的n个蓝点即成RBM实例；RBM的输出一趟遍历即可转回排序的输出。故RBM也是$Omega\(n log n\)$。

下界一旦确立，便沿归约关系成片"传染"------这正是第02章"SubsetSum是NP完全"那一页的另一种回声：难，是成批地难；同样，最优，也是成批地最优。

== 本章要点
<本章要点>
- 前缀无关编码=编码树（叶=字符，通路=编码）；OCT叶子只在倒数两层，均衡真二叉树即OCT；带权情形衡量尺度为WPL。
- Huffman算法：贪心合并最小两棵，$n - 1$次迭代；正确性归纳基于"最小字符成对"引理与"差距固定"对应。
- 森林实现：列表$O\(n^2\)$、堆$O\(n log n\)$、#strong[栈+队列$O\(n\)$]（有序序列合并思想，且绕开比较模型、不受$Omega\(n log n\)$下界约束）。
- 比较树：CBA对应二叉树，n种输出⇒高≥⌈log₂n⌉；排序下界Ω(nlogn)，归并排序WCOA；苹果甄别⌈log₂4⌉=2。
- 线性归约传递下界：SORTING ≤N HUFFMAN、SORTING ≤N RBM，成片确立Ω(nlogn)。
