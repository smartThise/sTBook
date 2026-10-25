= 列表：循位置访问的链表实现
<列表循位置访问的链表实现>
向量与列表同属序列（sequence）：元素按线性次序排列，各有秩，相邻者互称前驱、后继。差别在于一条设计决策------#strong[循秩访问]把元素的物理地址与其逻辑次序绑定在一起，因此向量擅长静态操作（按下标读取、二分查找），动态操作却显吃力：插入、删除动辄搬迁整个后缀。#strong[列表]（list）把这条绑定剪断：各元素的物理次序不再与逻辑次序直接相关，逻辑上紧邻的一对前驱与后继，物理上既不必保持先后，更未必相互紧邻。作为补偿，每一对逻辑紧邻的元素彼此记录对方的物理位置------#strong[链接]（link）。链接抽象为元素的#strong[位置]（position）之后，访问方式从循秩换成#strong[循位置访问]（call-by-position）：正如借助名片由某位朋友找到他的亲戚，进而同事、同事的战友、战友的同学------循着位置，常数时间内从一个元素转入下一个，即可抵达列表中的任何一个元素。动态操作只涉及局部的常数个元素，与全局规模无关，这就是列表多数动态操作可在 $O\(1\)$ 完成的机制保证。

== 节点与链表：两级封装
<节点与链表两级封装>
列表的典型实现是#strong[链表]（linked list），分两级封装。对应于列表的元素，基本单位是#strong[节点]（node）：既封装数据项`data`，也以指针记录前驱、后继节点的位置：

```cpp
template <typename T> using LNP = ListNode<T>*;   //列表节点位置
template <typename T> struct ListNode {           //简洁起见，完全开放而不再严格封装
   T data;  LNP<T> pred, succ;                    //数值、前驱、后继
   ListNode() : data(), pred( nullptr ), succ( nullptr ) {}
   ListNode( const T& e, LNP<T> p = nullptr, LNP<T> s = nullptr )
      : data( e ), pred( p ), succ( s ) {}        //类T须已定义复制方法
   LNP<T> insertPred( const T& e );               //前插入
   LNP<T> insertSucc( const T& e );               //后插入
   void movePred( LNP<T> s );                     //转移至s之前
   void moveSucc( LNP<T> p );                     //转移至p之后
};
```

其上再封装列表模板类。对外接口与向量ADT几乎一致（`size/empty/first/last/insert/remove/sort/find/search/dedup/uniquify/traverse`），内部则私有持有规模`_size`与一对#strong[哨兵节点]`head`、`tail`------二者外部不可见、不存数据，却让首、末、中间节点处于完全同等的地位：首节点的秩可理解为0，末节点为 $n - 1$，头哨兵为 $- 1$，尾哨兵为 $n$。初始化只做一件事：让两个哨兵互指：

```cpp
template <typename T> void List<T>::init() {
   head = new ListNode<T>;  tail = new ListNode<T>;
   head->succ = tail;  tail->pred = head;  _size = 0;
}
```

== 模仿循秩访问：能用，但勿多用
<模仿循秩访问能用但勿多用>
为了兼容旧代码，列表也能模仿循秩访问------但代价立现：

```cpp
template <typename T> LNP<T> List<T>::operator[]( Rank r ) const
{ return *first() + r; }               //O(r)：虽方便，勿多用
template <typename T> LNP<T> ListNode<T>::operator+( Rank r ) {
   for ( LNP<T> p = this; ; p = p->succ, r-- )   //从当前节点出发
      if ( 0 == r ) return p;                    //顺数第r个节点即目标
}  //秩 == 前驱的总数
template <typename T> Rank ListNode<T>::operator-( LNP<T> h ) {   //h <= this
   for ( Rank d = 0; ; h = h->succ, d++ )
      if ( h == this ) return d;                 //区间内节点挨个报数
}  //O(n)
```

`V[r]`在向量上是 $O\(1\)$，在列表上要数 $r$ 步；两个位置相减（求秩差）同样要 $O\(n\)$。列表的用法应当是：拿到一个位置之后，就沿着位置前进，不回头换算秩。

== 无序表的插入、删除与移动
<无序表的插入删除与移动>
插入接口有四个对外形态，内部全部落在节点的`insertPred`（或对称的`insertSucc`）上：

```cpp
LNP<T> List<T>::insert( const T& e, LNP<T> p ) { _size++;  return p->insertPred( e ); }  //e作p的前驱
LNP<T> List<T>::insert( LNP<T> p, const T& e ) { _size++;  return p->insertSucc( e ); }  //e作p的后继
LNP<T> List<T>::insertFirst( const T& e ) { _size++;  return head->insertSucc( e ); }    //e作首节点
LNP<T> List<T>::insertLast( const T& e ) { _size++;  return tail->insertPred( e ); }     //e作末节点

template <typename T> LNP<T> ListNode<T>::insertPred( const T& e ) {
   LNP<T> x = new ListNode( e, pred, this );   //创建新节点（pred或为head）
   pred->succ = x;  pred = x;  return x;       //列表接纳新节点（操作次序不可颠倒）
}
```

前插入共三根指针的写入，次序是刻意安排的：第一步构造新节点时就把X的两根外向指针接好；第二步`pred->succ = x`接通前驱的正向链；第三步`pred = x`补齐后继的反向链。逐步演示能看清为什么次序不能颠倒------中途任何一步停下，链表都保持可达：

#figure(image("图片/演示-ds07-insert-01.svg", alt: "逐步演示：前插入：三根指针的次序"),
  caption: [
    逐步演示：前插入：三根指针的次序
  ]
)

删除是对称的操作，两根指针让前后节点互相绕过被删者：

```cpp
template <typename T> T List<T>::remove( LNP<T> p ) {
   T e = p->data;                              //备份数据项
   p->pred->succ = p->succ;  p->succ->pred = p->pred;   //pred|succ或为head|tail
   delete p;  _size--;  return e;              //释放节点，更新规模，返回数据项
}
```

#figure(image("图片/演示-ds07-remove-01.svg", alt: "逐步演示：删除节点：让两侧指针绕过它"),
  caption: [
    逐步演示：删除节点：让两侧指针绕过它
  ]
)

#strong[移动]（move）是插入与删除的组合拳，却只需 $O\(1\)$：

```cpp
template <typename T> void ListNode<T>::movePred( LNP<T> s ) {   //s != this
   pred->succ = succ;  succ->pred = pred;               //取出当前节点
   pred = s->pred;  pred->succ = this;  succ = s;  s->pred = this;   //转移至紧靠于s之前
}  //moveSucc(p)完全对称，O(1)
```

这类操作是向量完全不具备的：把一个元素搬到任何地方，列表只动常数根指针。

== 复制与析构
<复制与析构>
#strong[深复制]（deep copy）需递归复制蓝本的每一层嵌套结构。列表版本的思路朴素：从蓝本区间出发，逐节点`insertLast`到新列表：

```cpp
void List<T>::copy( LNP<T> p, Rank n ) {          //复制蓝本区间[p, p+n)
   for ( init(); n--; p = p->succ )               //先建空表
      insertLast( p->data );                      //依次复制，O(1)每个
}
```

耗时线性正比于节点总数，以及每个T对象深复制所需的时间。#strong[析构]反过来逐个释放：

```cpp
template <typename T> List<T>::~List() {
   for ( LNP<T> x = head; x != tail; delete ( x = x->succ )->pred );
   delete tail;
}
```

一道思考题随课件附上：若换成只有`succ`指针的单向链表，又当如何析构？------提示：每删一个节点之前，先把它的`succ`存下来。

== 无序查找与去重
<无序查找与去重>
无序查找沿用第04章的哨兵技巧，只是从下标换成位置：

```cpp
template <typename T>   //在无序列表区间(h, t)内，找到等于e的最靠前者
LNP<T> List<T>::find( LNP<T> h, const T& e, LNP<T> t ) const {   //h < t
   T bak = t->data;  t->data = e;                //预置哨兵
   while ( e != ( h = h->succ )->data );         //自前向后逐个比对
   t->data = bak;  return h == t ? nullptr : h;  //命中或出界
}  //O(n)
```

去重与向量版同为减治：对每个节点p，在前缀中查找相等者，命中即删除。复杂度的表达却多了一层细腻------

```cpp
template <typename T> void List<T>::dedup() {     //O(n^2)
   for ( LNP<T> p = first(); p != tail; p = p->succ )   //O(n)
      if ( LNP<T> q = find( head, p->data, p ) )         //O(n)
         remove( q );                                    //O(1)！
}
```

最坏情况（比如元素互异）为 $O\(n^2\)$，与`Vector::dedup()`一样；最好情况（比如全等）只需 $O\(n\)$------得益于摆脱了循秩访问的窠臼：向量的`remove(i)`每次要搬移 $O\(n - i\)$ 个后继，列表的`remove(q)`只动常数根指针。

== 遍历：函数指针与函数对象
<遍历函数指针与函数对象>
遍历接口与向量一致，沿`succ`链走一遍即可；统一操作同样以函数指针或函数对象传达。第04章的三个例子原样可用：`Increase`统一加一、`Cumulate`借助外部累加器统计总和、`Compare`每访问一个元素便与前驱比较，累加相邻逆序对------计数为零当且仅当列表整体有序。

== 有序列表：去重与查找
<有序列表去重与查找>
摒弃循秩访问换来的动态操作红利，在有序列表上继续兑现；但凡事一利一弊，静态操作的性能可能反降。

#strong[去重]：重复元素必然紧邻，一趟扫描即可：

```cpp
template <typename T> void List<T>::uniquify() {   //只需遍历一趟，O(n)
   if ( _size < 2 ) return;                        //过短的列表自然无重复
   for ( LNP<T> p = first(), q = p->succ; q != tail; q = p->succ )
      if ( p->data != q->data )                    //p与其后继q不等
         p = q;                                    //则前进一步
      else                                         //相等：直接删除后者
         remove( q );                              //不必如向量那样间接删除
}
```

对比第05章向量版uniquify的双指针搬运------列表的物理删除本就是 $O\(1\)$，无需保留区挤压的技巧。

#strong[查找]：有序列表的`search`找不到比 $O\(n\)$ 更好的办法------没有随机访问，二分无从谈起。课件版本自后向前扫描并预置哨兵：

```cpp
template <typename T>   //有序列表区间(h, t)：等效于h->data == -∞
LNP<T> List<T>::search( LNP<T> h, const T& e, LNP<T> t ) const {
   T bak = h->data;  h->data = e;                 //预置哨兵
   while ( e < ( t = t->pred )->data );           //自后向前逐个比较
   h->data = bak;  return t;                      //不大于e的最靠后者
}  //O(n)
```

== 列表排序三例：选择、插入、归并
<列表排序三例选择插入归并>
列表的排序器同样随机挑选算法测试，本节择要讲三个：选择排序、插入排序与归并排序------它们恰好构成"从 $O\(n^2\)$ 到 $O\(n log n\)$、从搬数据到搬指针"的一条演进线。

#strong[选择排序]。温故而知新：起泡排序每趟要做多次交换，但那趟扫描的实质无非是找出当前最大元素m并令其就位------经 $n - 1$ 次比较确定m之后，其实一次交换就足够了。列表版把这一实质挑明：

```cpp
template <typename T> void List<T>::selectionSort( LNP<T> h, LNP<T> t ) {   //h < t
   for ( LNP<T> x = t->pred; h->succ != x; t = x, x = t->pred )   //无序前缀(h, x]
      swap( getMax( h, t )->data, x->data );   //找出最大者，交换令其就位
}   //亦可 getMax(h,t)->movePred(t)：同为O(1)，且能保证稳定性

template <typename T> LNP<T> List<T>::getMax( LNP<T> h, LNP<T> t ) {   //2 <= t-h
   LNP<T> m = t->pred;                          //当前最大者
   for ( t = m->pred; h != t; t = t->pred )     //自后向前逐个比较
      if ( m->data < t->data ) m = t;           //见贤思齐：严格更大才更新
   return m;                                    //即便有多个，也总取最靠后者
}  //O(n)：自后向前 + 严格比较 = 稳定性
```

性能上，$n$ 步迭代：`swap()`累计 $O\(n\)$，`getMax()`累计 $O\(n^2\)$------对任何输入都没有最好情况，主要消耗来自比较。好的一面：移动操作只需 $O\(n\)$ 次，远少于起泡排序；而就常系数而言，移动远贵于比较，实际收益可观。两条改进线索课件已经点出：`getMax()`若借助高级数据结构可降到 $O\(log n\)$，立即得到 $O\(n log n\)$ 的排序算法（第12章的堆排序正是这条路）；原地交换的浪费可借助#strong[轮换]（cycle）视角精确刻画------任何排列都可分解为若干轮换（最多n个、最少1个），交换前m与x同属一个轮换C且前后紧邻，交换后m从C中逸出自成轮换、C长度减一：C含 $k$ 个元素就会出现 $k$ 次原地交换。对互异元素的随机排列，期望而言原地交换的比例并不高，却也无法根除。

#strong[插入排序]。减而治之的又一形态：序列永远分成有序前缀 $S\[0\,r\)$ 与待排序后缀 $U\[r\,n\)$；反复取出后缀首元素e，在S中查得适当位置并插入。列表版把这个过程写成一行：

```cpp
template <typename T>   //逐一引入节点r，持续拓展有序前缀(h, r)
void List<T>::insertionSort( LNP<T> h, LNP<T> t ) {
   for ( LNP<T> r = h->succ, s = r->succ; r != t; r = s, s = r->succ )
      r->moveSucc( search( h, r->data, r ) );   //将[r]转移至(h,r)内的适当位置
}  //仅使用O(1)辅助空间：就地算法
```

得益于`search()`"返回不大于e的最靠后者"的接口语义，前缀总是保持有序，而且稳定------前缀中与r相等的元素都在r之前，r被安插到它们之后。可自行验证几种边界：前缀中有元素与r相等；r在前缀中最小或最大；前缀为空。复杂度是#strong[输入敏感]的（input-sensitive）：为插入 $e = A\[r\]$，比较次数恰为逆序对记账数 $I\(r\)$ 加1，总体比较 $Theta\(n + I\)$、移动 $O\(n\)$------序列含多少逆序对，就要花多少时间，正如衣物有多脏，洗涤就用多久。顺带回答一个自然的问题：前缀总是有序的，为何不二分？#strong[有实质的差异]：`binSearch()`抵达中点本身在列表上就是 $O\(r\)$，省下的比较全贴进了寻址。最后一个特质是#strong[在线]（online）：打牌的人都是边发边理牌，发完即理好------插入排序在数据完全就绪之前即可开始计算，这个能力多数排序算法并不具备。

#strong[归并排序]。列表版的分治主算法与向量版同构，只是切分要靠位置运算：

```cpp
template <typename T> void List<T>::mergeSort( LNP<T> h, LNP<T> t ) {   //h < t
   Rank n = *t - h - 1;  if ( n < 2 ) return;      //区间长度不足2，递归基
   LNP<T> x = *h + n / 2;                          //切分：(h,t) = (h,x] + (x,t)
   mergeSort( x, t );  mergeSort( h, x = x->succ );//后缀、前缀各自排序
   merge( h, x, t );                               //归并
}  //归并线性 → 总体O(nlogn)
```

列表的归并不再复制前缀------搬指针即可。实质上它是#strong[增量式的插入排序]：逐个把后缀节点转移进前缀的适当位置，小者优先（相等者优先取前缀侧）以保证稳定：

```cpp
template <typename T>   //将[y,t)中的节点，分别转移至(h,y)中的适当位置
LNP<T> List<T>::merge( LNP<T> h, LNP<T> y, LNP<T> t ) {
   for ( LNP<T> x = h->succ; ( x != y ) && ( y != t ); )
      if ( x->data > y->data )                     //y更小：转移到x之前
         ( y = y->succ )->pred->movePred( x );
      else                                         //否则x自然前进
         x = x->succ;
}  //O(n)，线性正比于节点总数
```

若归并可在线性时间内完成，整体运行时间即 $O\(n log n\)$。

== 逆序对：从计数到归并统计
<逆序对从计数到归并统计>
#strong[逆序对]（inversion）：若 $i < j$ 且 $S\[i\]> S\[j\]$，则 $\(i\,j\)$ 构成一个逆序对。为便于统计，统一把逆序对记到后者j的账上：$I\(j\)$ = j之前大于 $S\[j\]$ 的元素个数。讲义的三组实例：${ 5\,3\,1\,4\,2 }$ 各账目为 $0 + 1 + 2 + 1 + 3$，共7个；完全有序为0；完全逆序为 $0 + 1 + 2 + 3 + 4 = 10 = n\(n - 1\)\/2$，是上界。逆序对总数与序列的"乱度"精确对应：交换一对逆序元素，逆序对至少减1（相距越远的逆序对，一次交换期望修复越多）。由此重审本章算法：起泡排序每次交换的都是紧邻逆序对，逆序对只能逐一修复，最坏必然 $O\(n^2\)$；插入排序针对 $e = A\[r\]$ 的迭代恰做 $I\(r\)+ 1$ 次比较，若全序列含 $I$ 个逆序对，总比较 $Theta\(n + I\)$------它的时间就是序列脏污程度的直接读数。全局逆序对的统计也不必蛮力 $O\(n^2\)$：套用归并排序的框架，把逆序对按位置分成偏于前缀、偏于后缀、跨界三类，前两类递归统计；实质的跨界统计利用一个不变事实------假想归并排序进行至后缀元素j即将出列的时刻，前缀中剩下的恰是所有与j构成跨界逆序的元素，将此时的剩余个数累加到j的账上（$I\(j\)+ =\|upright("LR")\|$）即可，次序虽经调整，总数不变。全部分摊下来，$O\(n log n\)$。

== 本章要点
<本章要点>
- 列表与向量同属序列；列表以链接解耦物理与逻辑次序，循位置访问使动态操作只动局部常数根指针。
- 链表两级封装：ListNode（data + pred/succ）与 List（\_size + head/tail哨兵，秩−1、0、n−1、n）；`operator[]`为O(r)的模仿品，勿多用。
- 前插入三根指针次序不可颠倒：构造时接好X的外向两根，再改pred-\>succ，最后改pred；删除让两侧指针绕过被删者；移动=取出+转移，O(1)。
- 复制逐节点insertLast；析构逐个delete并留意单向链表的变体。
- 无序find带哨兵O(n)；dedup最坏O(n²)最好O(n)；遍历配函数对象（Increase/Cumulate/Compare）。
- 有序uniquify一趟O(n)直接删除后继；search自后向前O(n)------动态之利与静态之弊的对照。
- 列表排序：选择排序getMax自后向前+严格比较保稳定、getMax累计O(n²)无最好情况（堆排序是其上限改进）；插入排序 $Theta\(n + I\)$ 输入敏感、在线、就地稳定；归并排序搬指针不搬数据，O(n log n)。
- 逆序对记到后者账上；交换一对逆序至少修复1个；插入排序时间=脏污读数；归并框架下跨界逆序对在"j即将出列"时刻统计，总计O(n log n)。
