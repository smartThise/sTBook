"""独立核对1-32中的开方条件和有限随机范围；仅用Python标准库。"""
from math import isqrt


def subtract_odds(n):
    k, calls = 0, 1
    while n > 0:
        n -= 2 * k + 1
        k += 1
        calls += 1
    return k, calls


def observed(n):
    i, checks, recursive_calls = 1, 0, 0
    while True:
        root, calls = subtract_odds(i)
        checks += 1
        recursive_calls += calls
        if i >= n // root:
            return i, checks, recursive_calls
        i += 1


def threshold_oracle(n):
    # 与逐轮相减不同：整数平方根 + 对单调谓词的二分。
    lo, hi = 1, n + 1
    while lo < hi:
        mid = (lo + hi) // 2
        r = isqrt(mid)
        r += r * r < mid
        if (mid + 1) * r <= n:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main():
    cases = 0
    for n in range(1, 513):
        i, checks, calls = observed(n)
        assert i == threshold_oracle(n)
        assert checks == i
        roots = [isqrt(j - 1) + 1 for j in range(1, i + 1)]
        assert calls == sum(r + 1 for r in roots)
        cases += 1
    for limit in range(33):
        for modulus in range(1, 65):
            divisible = sum(x % modulus == 0 for x in range(limit + 1))
            assert divisible == limit // modulus + 1
            cases += 1
    print(f'通过{cases}组核对：开方递归、整数除法停止位置、条件调用次数、有限随机范围取模。')


if __name__ == '__main__':
    main()
