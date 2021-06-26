#include "pcg_basic.h"
#include <stdio.h>
#include <time.h>
#include <math.h>

float random_float(pcg32_random_t* rng) {
    return (pcg32_random_r(rng) / (float)UINT32_MAX);
}

int main(void)
{

    int points = 10000;
    pcg32_random_t rng;
    pcg32_srandom_r(&rng, time(NULL) ^ (intptr_t)&printf,
                    (intptr_t)&points);
    float x, y, t, ang, r;
    for (int i = 0; i < points; i++) {
        ang = random_float(&rng) * 2 * M_PI;
        t = random_float(&rng);
        r = sqrtf(t);
        x = r * cosf(ang);
        y = r * sinf(ang);
        printf("%f %f\n", x, y);
    }
    return 0;
}
