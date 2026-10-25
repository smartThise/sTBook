= 二叉搜索树与AVL树
<二叉搜索树与avl树>
有序向量的查找是$O\(log n\)$，插入却是$O\(n\)$；列表的插入$O\(1\)$，查找却是$O\(n\)$。#strong[二叉搜索树]（BST）把"有序"搬进分叉关系里：每个节点的左子树所有键不大于它、右子树所有键不小于它（互异时严格）。于是查找只需每步比较一次、走向一侧------形态随机时$O\(log n\)$；而插入与删除只在局部改几根指针。本章还处理它唯一的隐患------树形可能失衡退化成单链------由此引出第一个平衡搜索树：AVL。

== BST：中序次序即全局次序
<bst中序次序即全局次序>
BST的#strong[顺序性]有一条等价刻画：#strong[中序遍历序列单调不降]。这使"树上查找"与"有序向量二分"在逻辑上完全同构。接口实现：

```cpp
template <typename T, bool H> BNP<T> BST<T, H>::search( const T& e ) {   //查找
   return searchIn( _root, e, _hot = nullptr );
}
template <typename T, bool H>   //典型实现：_hot指向命中节点的父节点（或将来接入处）
static BNP<T> searchIn( BNP<T> v, const T& e, BNP<T>& hot ) {
   if ( !v || ( e == v->data ) ) return v;    //递归基：命中或空树
   hot = v;
   return searchIn( ( e < v->data ) ? v->lc : v->rc, e, hot );
}  //O(h)：h为树高
```

#strong[插入]：先`search()`，失配之处即新节点的接入位置------新节点必为叶：

```cpp
template <typename T, bool H> BNP<T> BST<T, H>::insert( const T& e, int h ) {
   BNP<T> x = search( e );
   if ( x ) return x;                          //已存在，不再插入
   x = new BinNode<T>( e, parent = _hot );     //新节点作为叶子
   ( _hot ? ( e < _hot->data ? _hot->lc : _hot->rc ) : _root ) = x;
   _size++;  _p->updateHeightAbove();          //派生的AVL、红黑树会重写并自行更新
   return x;
}
```

#strong[删除]分两种情形。单枝或叶：直接用唯一的孩子顶替；#strong[双枝]：实际删除的是它的#strong[直接后继]succ()（右子树最左节点）------交换两者数据，问题转化为删除succ（succ必无左孩子，回到单枝情形）：

```cpp
template <typename T, bool H> bool BST<T, H>::remove( const T& e ) {
   BNP<T> x = search( e );
   if ( !x ) return false;
   removeAt( x, _hot );  _size--;
   return true;
}
template <typename T> static BNP<T> removeAt( BNP<T> x, BNP<T>& hot ) {
   BNP<T> w = x;                               //实际被摘除者
   BNP<T> succ = x->rc ? removeAt后的succ : nullptr;
   if ( !HasLChild( *x ) ) x = x->rc;          //左空：右子树（或nullptr）顶替
   else if ( !HasRChild( *x ) ) x = x->lc;     //右空：左子树顶替
   else { w = succ( x );  swap( x->data, w->data );   //双枝：与直接后继换数据
          BNP<T> u = w->parent;                //问题转化为摘除w（无左孩子）
          ( u == x ? u->rc : u->lc ) = x = w->rc; }
   hot = w->parent;
   if ( x ) x->parent = hot;
   delete w;  return x;
}
```

三种接口都正比于树高$O\(h\)$。好形态（随机插入序）$h = O\(log n\)$；坏形态（按序插入）退化成单链$h = O\(n\)$------remove()频繁succ()还可能加剧倾侧（可通过随机使用succ()/pred()缓解）。治本的方案是#strong[平衡]。

== 等价二叉搜索树与旋转
<等价二叉搜索树与旋转>
两棵BST若#strong[中序遍历序列相同]，则等价------"上下可变，左右不乱"。局部等价变换的基本构件是#strong[旋转]：zag（逆时针，左旋）与zig（顺时针，右旋）。以zag为例：$g$的左孩子$p$上浮为子树根，$g$带自己的右子树下沉为$p$的右孩子，$p$原来的右子树转而挂在$g$的左肩。旋转改变"上下"（深度），不改变"左右"（中序次序）------这正是 BST 重平衡的全部自由度：失衡靠旋转修复，正确性靠中序不变保障。

== AVL树：渐近平衡
<avl树渐近平衡>
#strong[平衡因子]（balance factor）：$b a l F a c\(x\)= h\(x . l c\)- h\(x . r c\)$。AVL树（G. Adelson-Velsky & E. Landis, 1962）约定所有节点 $\|b a l F a c\|lt.eq 1$：

```cpp
auto BalFac = []( auto x ) { return Height( x->lc ) - Height( x->rc ); };
auto AvlBalanced = []( auto x ) { return ( -2 < BalFac( x ) ) && ( BalFac( x ) < 2 ); };
template <typename T> class AVL : public BST<T, false> {
public:
   BNP<T> insert( const T& );   //重写
   bool remove( const T& );     //重写
};                              //BST::search()等接口直接沿用
```

#strong[AVL是渐近平衡的]：高度$h$的AVL树规模至少为$S\(h\)= S\(h - 1\)+ S\(h - 2\)+ 1$（最瘦情形：根的两侧分别是高$h - 1$与$h - 2$的最瘦AVL）------即Fibonacci数！$S\(h\)= f i b\(h + 2\)- 1$，数列依次为1, 2, 4, 7, 12, 20, 33, 54, 88, 143, 232, …。于是$n$节点的AVL高度$h = O\(log n\)$------最瘦也不失对数高度。Fibonaccian树内部节点的balFac均为+1或−1，删除任何节点高度都会下降。

== AVL插入：失衡与双旋
<avl插入失衡与双旋>
插入或删除后，沿父链上溯的某些祖先可能失衡。#strong[最低的失衡节点g]（不低于新节点的祖父）是复衡的入口；定义 $p = upright("TallerChild")\(g\)$、$v = upright("TallerChild")\(p\)$------名分唯一确定。按p与v的同侧/异侧分两种情形：

#strong[单旋]（LL或RR）：p与v同侧，一次zag（或zig）即可。子树不仅恢复平衡，#strong[高度也复原]------更高祖先即便此前失衡也必一揽子复衡，整个插入至多做一次旋转。

#strong[双旋]（LR或RL）：p与v异侧，先以v为轴旋p（zag或zig），再旋g。以插入序列5、3、4为例------4落在3的右肩，g=5失衡，p=3与v=4异侧（LR）：

#figure(image("图片/演示-ds12-avl-lr-01.svg", alt: "逐步演示：AVL双旋：LR失衡与复衡"),
  caption: [
    逐步演示：AVL双旋：LR失衡与复衡
  ]
)

双旋后v=4升为子树根，3、5各归两侧；中序序列3\<4\<5保持不变。同样，高度复原、更高祖先一揽子复衡。故AVL插入的总代价为$O\(log n\)$------search $O\(log n\)$ + 旋转$O\(1\)$ + 高度更新$O\(log n\)$。

== AVL删除：可能连锁失衡
<avl删除可能连锁失衡>
删除导致的失衡更顽固：g复衡后子树高度#strong[可能下降]，更高祖先可能接连失衡------需要逐层上溯检查、逐一旋转，最坏$O\(log n\)$次旋转。因此AVL的remove()虽仍为$O\(log n\)$，常数与实现复杂度都高于insert()。

== 本章要点
<本章要点>
- BST顺序性=中序单调；search/insert/remove均$O\(h\)$；插入必为叶，双枝删除转化为删除直接后继。
- 坏形态退化为$O\(n\)$单链：需要重平衡。
- 等价BST=中序相同；旋转zig/zag上下可变、左右不乱，是重平衡的全部自由度。
- AVL：$\|b a l F a c\|lt.eq 1$；$S\(h\)= f i b\(h + 2\)- 1$渐近平衡，$h = O\(log n\)$；Fibonaccian树是最瘦AVL。
- 插入失衡：最低失衡g、p=TallerChild(g)、v=TallerChild(p)；同侧单旋、异侧双旋；高度复原，至多一次旋转。
- 删除失衡可能连锁：逐层上溯，最坏$O\(log n\)$次旋转。
