#include <stdlib.h>

int main(void) {
    int *p = malloc(10 * sizeof *p);
    if (p == NULL) return EXIT_FAILURE;
    for (size_t i = 0; i <= 10; ++i)
        p[i] = (int)i; /* deliberate error: i==10 is out of bounds */
    free(p);
    return EXIT_SUCCESS;
}
