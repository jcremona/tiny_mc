#include "pcg_basic.h"
#include <stdio.h>
#include <time.h>

int main(void)
{

    int points = 100000;
    pcg32_random_t rng;
    pcg32_srandom_r(&rng, time(NULL) ^ (intptr_t)&printf,
                    (intptr_t)&points);
    float x, y, t;
    for (int i = 0; i < points; i++) {
        do {
            x = 2.0f * (pcg32_random_r(&rng) / (float)UINT32_MAX) - 1.0f;
            y = 2.0f * (pcg32_random_r(&rng) / (float)UINT32_MAX) - 1.0f;
            t = x * x + y * y;
        } while (1.0f < t);
        printf("%f %f\n", x, y);
    }

    return 0;
}
