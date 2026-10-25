/* 把一条合法交错明确排成顺序语句，核对局部副本与共享状态。 */
#include <assert.h>
#include <stdatomic.h>
#include <stdio.h>

int main(void) {
    _Atomic int x = 5;
    int a = atomic_load(&x);     /* A读取5 */
    int b = atomic_load(&x);     /* B也读取5 */
    a = a + 1;
    b = b + 1;
    atomic_store(&x, a);         /* A写6 */
    atomic_store(&x, b);         /* B又写6 */
    int separate = atomic_load(&x);
    assert(separate == 6);

    atomic_store(&x, 5);
    atomic_fetch_add(&x, 1);
    atomic_fetch_add(&x, 1);
    int combined = atomic_load(&x);
    assert(combined == 7);
    printf("分开的原子读写：%d；原子读改写：%d\n", separate, combined);
    return 0;
}
