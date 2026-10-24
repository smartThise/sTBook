#!/usr/bin/env python3
"""笔记中算法的独立小规模核对。运行 python3 算法检查.py；不含个人 PA 提交。"""
import bisect
import heapq
import itertools
import math
import random
import re
from fractions import Fraction
from pathlib import Path


def lower(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if a[mid] < x: lo = mid + 1
        else: hi = mid
    return lo


def largest_rectangle(a):
    stack, best = [], 0
    for i, v in enumerate(a + [0]):
        while stack and a[stack[-1]] > v:
            h = a[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, h * (i - left))
        stack.append(i)
    return best


def rectangle_oracle(a):
    return max([0] + [min(a[i:j]) * (j-i) for i in range(len(a)) for j in range(i+1,len(a)+1)])


def edit(a, b, k=None):
    # 插入/删除各成本1；不允许替换。带外状态只保留大于预算的哨兵。
    inf = len(a) + len(b) + 1
    prev = {j:j for j in range(len(b)+1) if k is None or j <= k}
    for i in range(1,len(a)+1):
        cur = {0:i} if k is None or i <= k else {}
        lo = 1 if k is None else max(1,i-k)
        hi = len(b) if k is None else min(len(b),i+k)
        for j in range(lo,hi+1):
            cur[j] = min(prev.get(j,inf)+1,cur.get(j-1,inf)+1,
                         prev.get(j-1,inf) if a[i-1]==b[j-1] else inf)
        prev = cur
    return prev.get(len(b),inf)


def gift(pairs, limit):
    n=len(pairs)//2
    def sums(ps):
        values=[0]
        for a,b in ps: values=[s+x for s in values for x in (a,b)]
        return values
    left=sorted(sums(pairs[:n]))
    return sum(bisect.bisect_right(left,limit-v) for v in sums(pairs[n:]))


def kmp(text, pattern):
    if not pattern:return list(range(len(text)+1))
    pi=[0]*len(pattern)
    for i in range(1,len(pattern)):
        j=pi[i-1]
        while j and pattern[i]!=pattern[j]:j=pi[j-1]
        if pattern[i]==pattern[j]:j+=1
        pi[i]=j
    out=[];j=0
    for i,c in enumerate(text):
        while j and c!=pattern[j]:j=pi[j-1]
        if c==pattern[j]:j+=1
        if j==len(pattern):out.append(i-j+1);j=pi[j-1]
    return out


def huffman(values):
    a=values[:];heapq.heapify(a);cost=0
    while len(a)>1:
        v=heapq.heappop(a)+heapq.heappop(a);cost+=v;heapq.heappush(a,v)
    return cost


def merge_oracle(values):
    if len(values)<2:return 0
    return min(values[i]+values[j]+merge_oracle([x for k,x in enumerate(values) if k not in (i,j)]+[values[i]+values[j]])
               for i in range(len(values)) for j in range(i+1,len(values)))


def parse_expression(source):
    tokens=re.findall(r'\d+|!!|[()+*/^!\-]',source)
    if ''.join(tokens)!=re.sub(r'\s+','',source):raise ValueError('未知字符')
    pos=0
    def expr(minimum=0):
        nonlocal pos
        if pos>=len(tokens):raise ValueError('缺少操作数')
        t=tokens[pos];pos+=1
        if t=='(':
            node=expr()
            if pos>=len(tokens) or tokens[pos]!=')':raise ValueError('括号失配')
            pos+=1
        elif t.isdigit():node=('num',int(t))
        else:raise ValueError('需要数字或左括号')
        while pos<len(tokens):
            op=tokens[pos]
            if op in ('!','!!'):
                if 40<minimum:break
                pos+=1;node=(op,node);continue
            if op not in ('+','-','*','/','^'):break
            precedence={'+':10,'-':10,'*':20,'/':20,'^':30}[op]
            if precedence<minimum:break
            pos+=1;rhs=expr(precedence if op=='^' else precedence+1);node=(op,node,rhs)
        return node
    node=expr()
    if pos!=len(tokens):raise ValueError('多余token')
    return node


def rpn(node):
    if node[0]=='num':return [str(node[1])]
    return rpn(node[1])+(rpn(node[2]) if len(node)==3 else [])+[node[0]]


def operate(op, a, b=None):
    if op in ('!','!!'):
        if a.denominator!=1 or a<0:raise ValueError('阶乘域错误')
        n=int(a)
        return Fraction(math.factorial(n) if op=='!' else math.prod(range(n,0,-2)))
    if op=='+':return a+b
    if op=='-':return a-b
    if op=='*':return a*b
    if op=='/':return a/b
    if op=='^':
        if b.denominator!=1:raise ValueError('本示例仅支持整数指数')
        return a**int(b)
    raise ValueError(op)


def evaluate_tree(node):
    if node[0]=='num':return Fraction(node[1])
    return operate(node[0],evaluate_tree(node[1]),evaluate_tree(node[2]) if len(node)==3 else None)


def evaluate_rpn(tokens):
    stack=[]
    for t in tokens:
        if t.isdigit():stack.append(Fraction(t));continue
        if t in ('!','!!'):stack.append(operate(t,stack.pop()));continue
        b=stack.pop();a=stack.pop();stack.append(operate(t,a,b))
    if len(stack)!=1:raise ValueError('RPN栈不合法')
    return stack[0]


EXPRESSIONS = [
'(0+1+2-3+4+5+6)*(7+8)*9',
'(0*1+2)*3!/4!*5*6*(7+8)*9',
'0!+(1+2)!!*3-4-5!-6-7-8+9',
'(0+1+2)/3!/4!*5!*6*(7+8)*9',
'(0!^1/2*3!!/(4+5)*6-7-8)*9',
'((0*(1-2)+3+4)*5*6+(7+8))*9',
'(0!-1!+2)*3!/4!*5*6*(7+8)*9',
'((0-1)^2*(3!!/4-5+6*7+8))*9',
'((0-1)^2*(3!!/4-5-6+7*8))*9',
'(0!+1+2)!+(3!-4)^(5+6)-7*8+9',
'(0+(1+2))^3/(4+5)*6!-(7+8)*9',
'((0-1)^2!*(3!!/4-5+6*7+8))*9',
'((0-1)^2!*(3!!/4-5-6+7*8))*9',
'(0!+1)*(2+3)*(4+5)/6*(7+8)*9',
'(0!^1/2*3!!/(4+5)*6-(7+8))*9',
'((0-1)^2*(3!!/4-5*(6-7-8)))*9',
'((0-1)^2!*(3!!/4-5*(6-7-8)))*9',
'((0!+1!)^2+(3!-4)+5*6)*(7*8)+9',
'((0!+1)*2)!+(3!-4)^(5+6)-7*8+9',
'((0!^1+2)!!/(3!-4-5+6)-(7+8))*9',
'((0!^1+2)!!/(3!-(4+(5-6)))-(7+8))*9',
]


def main():
    rng=random.Random(20261025);checks=0
    for n in range(10):
        for _ in range(50):
            a=[rng.randrange(8) for _ in range(n)]
            assert largest_rectangle(a)==rectangle_oracle(a);checks+=1
            a.sort()
            for x in [-1,0,3,7,8]:assert lower(a,x)==bisect.bisect_left(a,x);checks+=1
    strings=[''.join(p) for n in range(5) for p in itertools.product('ab',repeat=n)]
    for a in strings:
        for b in strings:
            d=edit(a,b)
            for k in range(4):
                band=edit(a,b,k);assert (band==d if d<=k else band>k);checks+=1
            expected=[i for i in range(len(a)+1) if a.startswith(b,i)]
            assert kmp(a,b)==expected;checks+=1
    for n in range(7):
        for _ in range(20):
            ps=[(rng.randint(-3,5),rng.randint(-3,5)) for _ in range(n)];limit=rng.randint(-5,15)
            expected=sum(sum(v)<=limit for v in itertools.product(*ps))
            assert gift(ps,limit)==expected;checks+=1
    for n in range(1,6):
        for _ in range(8):
            a=[rng.randint(1,9) for _ in range(n)];assert huffman(a)==merge_oracle(a);checks+=1
    for s in EXPRESSIONS:
        tree=parse_expression(s);assert evaluate_tree(tree)==evaluate_rpn(rpn(tree));checks+=1
    assert evaluate_rpn(rpn(parse_expression('2^3^2')))==512
    assert evaluate_rpn(rpn(parse_expression('6!!')))==48
    print(f'通过 {checks} 次独立小规模核对；含二分、单调栈、带状DP、KMP、中间相遇、Huffman及21式RPN。')
    if '--export' in __import__('sys').argv:
        lines=['# PS04 的21个表达式：RPN与检查过程','',
        '统一约定：乘方右结合，阶乘/双阶乘是高优先级后缀运算；`!!`表示双阶乘，除法采用精确有理数语义，非C++整数截断。老师具体程序若用别的优先表或浮点类型，须按其定义对照。下面RPN由可读解析树生成，再由独立栈求值与树求值交叉核对。','']
        for i,s in enumerate(EXPRESSIONS,1):
            tree=parse_expression(s);lines += [f'## 第{i}式','',f'原式：`{s}`','', '```text',' '.join(rpn(tree)),'```','',f'依上述语义的值：{evaluate_tree(tree)}。','']
        (Path(__file__).resolve().parent.parent/'30-表达式逐项走读.md').write_text('\n'.join(lines).rstrip()+'\n')

if __name__=='__main__':main()
