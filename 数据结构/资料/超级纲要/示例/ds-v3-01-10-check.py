"""Run complete Python examples from chapters 01..10 against independent oracles."""
from pathlib import Path
import ast,itertools,bisect,math
BOOK=Path(__file__).resolve().parent.parent
ns={}
blocks=0
for n in range(1,11):
 text=next(BOOK.glob(f'{n:02d}-*.md')).read_text()
 import re
 for block in re.findall(r'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',text,re.M|re.S):
  tree=ast.parse(block)
  # A loop demonstrating counting is not a complete runnable program.
  if any(not isinstance(x,(ast.FunctionDef,ast.Import,ast.ImportFrom,ast.ClassDef)) for x in tree.body):
   continue
  exec(compile(tree,f'chapter-{n}', 'exec'),ns)
  blocks+=1
checks=0
for n in range(7):
 for tup in itertools.product((-2,-1,0,1,2),repeat=n):
  a=list(tup)
  assert ns['total'](a)==sum(a)
  b=a[:];ns['insertion_sort'](b);assert b==sorted(a)
  assert ns['merge_sort'](a)==sorted(a)
  assert ns['recursive_sum'](a)==sum(a)
  checks+=4
  if a:
   assert ns['maximum'](a)==max(a)
   val,l,r=ns['max_subarray'](a)
   oracle=max(sum(a[i:j]) for i in range(n) for j in range(i+1,n+1))
   assert 0<=l<r<=n and sum(a[l:r])==val==oracle
   checks+=2
  ordered=sorted(a)
  for x in (-3,-1,0,2,3):
   assert ns['lower_bound'](ordered,x)==bisect.bisect_left(ordered,x)
   checks+=1
  for w in range(1,n+1):
   assert ns['window_maximum'](a,w)==[max(a[i:i+w]) for i in range(n-w+1)]
   checks+=1
for a in range(40):
 for b in range(40):
  if a or b:
   assert ns['gcd'](a,b)==math.gcd(a,b);checks+=1
for expression,expected in [('3 2 4 + *',18),('8 3 -',5),('9 2 /',ns['Fraction'](9,2)),('10 2 3 * - 4 /',1)]:
 assert ns['evaluate_rpn'](expression)==expected;checks+=1
for bad,error in [('2 +',ValueError),('2 3',ValueError),('',ValueError),('1 0 /',ZeroDivisionError)]:
 try:ns['evaluate_rpn'](bad)
 except error:checks+=1
 else:raise AssertionError(bad)
class Tagged:
 def __init__(self,k,tag):self.k,self.tag=k,tag
 def __le__(self,o):return self.k<=o.k
 def __gt__(self,o):return self.k>o.k
a=[Tagged(2,'A'),Tagged(1,'B'),Tagged(2,'C'),Tagged(1,'D')]
for mode in ('insert','merge'):
 b=a[:]
 if mode=='insert':ns['insertion_sort'](b)
 else:b=ns['merge_sort'](b)
 assert [x.tag for x in b]==['B','D','A','C'];checks+=1
class Node:
 def __init__(self,data,left=None,right=None):
  self.data,self.left,self.right=data,left,right
  self.next=None
tree=Node('A',Node('B',Node('D'),Node('E')),Node('C',None,Node('F')))
assert ns['inorder'](tree)==list('DBEACF');checks+=1
a,b,c=Node('A'),Node('B'),Node('C');a.next=b;b.next=c
head=ns['reverse'](a)
assert head is c and c.next is b and b.next is a and a.next is None;checks+=1
assert ns['reverse'](None) is None;checks+=1
# Independent LCS table, checking every narrated cell and reconstruction length.
X,Y='ABC','BAC';D=[[0]*4 for _ in range(4)]
for i in range(1,4):
 for j in range(1,4):
  D[i][j]=D[i-1][j-1]+1 if X[i-1]==Y[j-1] else max(D[i-1][j],D[i][j-1])
assert D==[[0,0,0,0],[0,0,1,1],[0,1,1,1],[0,1,1,2]];checks+=1
# Exact costs narrated in chapters 02,04,06.
assert sum(len(range(0,8,i)) for i in range(1,9))==24;checks+=1
cap=2;cost=0;totals=[]
for size in range(9):
 if size==cap:cost+=size;cap*=2
 cost+=1;totals.append(cost)
assert totals==[1,2,5,6,11,12,13,14,23];checks+=1
assert sum(x>y for i,x in enumerate([4,1,3,2]) for y in [4,1,3,2][i+1:])==4;checks+=1
assert sum(x>y for x in [2,4] for y in [1,3])==3;checks+=1
print(f'{blocks} complete Python blocks executed; {checks} independent assertions passed.')
