#!/usr/bin/env python3
"""独立核对PS中的有限算例与计数；有限验证不替代正文证明。"""
from collections import Counter, deque
from functools import lru_cache
from itertools import permutations
from math import ceil, comb, floor, log2

checks = Counter()

def count_upper(a, x):
    lo, hi, cost = 0, len(a), 0
    while lo < hi:
        mid = lo + (hi-lo)//2
        cost += 1
        if x < a[mid]:
            hi = mid
        else:
            lo = mid+1
    return lo-1, cost

def check_search():
    for n in range(1, 301):
        a = [2*i for i in range(n)]
        success = [count_upper(a,x)[1] for x in a]
        failure = [count_upper(a,2*i-1)[1] for i in range(n+1)]
        N, k = n+1, floor(log2(n+1))
        D = N*(k+2)-2**(k+1)
        assert sum(failure) == D
        assert sum(success) == D-ceil(log2(n+1))
        for i in range(n):
            assert count_upper(a,a[i])[0] == i
        checks["二分均值与返回位置"] += n+2

def bubble(a):
    a = list(a)
    hi, passes, swaps = len(a), 0, 0
    while True:
        changed = False
        passes += 1
        for i in range(1,hi):
            if a[i-1] > a[i]:
                a[i-1],a[i] = a[i],a[i-1]
                swaps += 1
                changed = True
        hi -= 1
        if not changed:
            return a,passes,swaps

def inversions(a):
    return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))

def check_bubble():
    for half in range(1,5):
        m = 2*half
        values = []
        for a in permutations(range(m)):
            result,p,s = bubble(a)
            I = inversions(a)
            d = max(i-value for i,value in enumerate(a))
            assert result == list(range(m))
            assert s == I
            assert p == d+1
            if p == half:
                values.append(I)
            checks["冒泡全排列与逆序"] += 1
        d = half-1
        assert min(values) == d
        assert max(values) == m*d-d*(d+1)//2

def stack_outputs(source):
    n = len(source)
    out = []
    def go(i, stack, result):
        if len(result) == n:
            out.append(tuple(result))
            return
        if i<n:
            go(i+1,stack+(source[i],),result)
        if stack:
            go(i,stack[:-1],result+(stack[-1],))
    go(0,(),())
    return out

def catalan(n):
    return comb(2*n,n)//(n+1)

def check_stack():
    for n in range(1,9):
        out = stack_outputs(tuple(range(1,n+1)))
        assert len(set(out)) == len(out) == catalan(n)
        first = Counter(x[0] for x in out)
        for k in range(1,n+1):
            L = 2*n-k-1
            b = n-k-1
            predicted = comb(L,n-k)-(comb(L,b) if b>=0 else 0)
            assert first[k] == predicted
            checks["首弹分类与Catalan"] += 1
    out = stack_outputs(("C","Sa","T","D","Sb","A"))
    visible = lambda x: tuple("S" if a in ("Sa","Sb") else a for a in x)
    X = {visible(x) for x in out if x[-1]=="Sa"}
    Y = {visible(x) for x in out if x[-1]=="Sb"}
    assert (len(X),len(Y),len(X&Y),len(X|Y)) == (14,14,4,24)
    checks["重复S集合去重"] += 1

@lru_cache(None)
def shapes(n):
    if n==0:
        return (None,)
    return tuple((L,R) for a in range(n)
                 for L in shapes(a) for R in shapes(n-1-a))

def stats(t):
    if t is None:
        return 0,0,0
    L,R = t
    left,right = stats(L),stats(R)
    degree = int(L is not None)+int(R is not None)
    return tuple(left[i]+right[i]+int(degree==i) for i in range(3))

def externalize(t):
    if t is None:
        return ("external",)
    return externalize(t[0]),externalize(t[1])

def extended_stats(t):
    if t == ("external",):
        return 0,1
    a,b = extended_stats(t[0]),extended_stats(t[1])
    return 1+a[0]+b[0],a[1]+b[1]

def queue_peak(t):
    q=deque([t]) if t is not None else deque()
    best=len(q)
    while q:
        L,R=q.popleft()
        if L is not None:q.append(L)
        if R is not None:q.append(R)
        best=max(best,len(q))
    return best

def check_trees():
    for n in range(1,9):
        peak=0
        for t in shapes(n):
            n0,n1,n2=stats(t)
            assert n0==n2+1
            assert n-1==n1+2*n2
            assert extended_stats(externalize(t))==(n,n+1)
            peak=max(peak,queue_peak(t))
            assert queue_peak(t)<=ceil(n/2)
            checks["树形与扩充/层序空间"] += 1
        assert peak==ceil(n/2)

def main():
    check_search()
    check_bubble()
    check_stack()
    check_trees()
    for name,n in checks.items():
        print(f"{name}：{n}项通过")
    print(f"合计{sum(checks.values())}项有限核对。")

if __name__ == "__main__":
    main()
