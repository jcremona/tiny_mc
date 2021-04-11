#include <stdio.h>
#include "boost_wrapper.h"
#include <time.h>

int main(void) {

    initializeRNG();
    seed(time(NULL));
    for(int i=0; i < 10000; i++)
        printf("%f %f\n", get_random(), get_random());
    deleteRNG();

    return 0;
}
