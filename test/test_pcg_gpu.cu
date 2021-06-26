#include "helper_cuda.h"
#include "params.h"
#include "wtime.h"
#include <cuda.h>

#define BLOCK_SIZE 128

struct pcg_state_setseq_64 {
    uint64_t state; // RNG state.  All values are possible.
    uint64_t inc; // Controls which RNG sequence (stream) is
    // selected. Must *always* be odd.
};
typedef struct pcg_state_setseq_64 pcg32_random_t;

__device__ __host__ uint32_t pcg32_random_r(pcg32_random_t* rng)
{
    uint64_t oldstate = rng->state;
    rng->state = oldstate * 6364136223846793005ULL + rng->inc;
    uint32_t xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
    uint32_t rot = oldstate >> 59u;
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}

void pcg32_srandom_r(pcg32_random_t* rng, uint64_t initstate, uint64_t initseq)
{
    rng->state = 0U;
    rng->inc = (initseq << 1u) | 1u;
    pcg32_random_r(rng);
    rng->state += initstate;
    pcg32_random_r(rng);
}


__device__ float random_float(pcg32_random_t* rng)
{
    return pcg32_random_r(rng) / (float)UINT32_MAX;
}

__global__ void test_pcg(pcg32_random_t* rng, float* f, int n)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
        f[i] = random_float(rng + i);
}

// Ojo: Se rompe si a+b > 2^31
int div_ceil(int a, int b)
{
    return (a + b - 1) / b;
}

static void launch_kernel_test_pcg(int n)
{
    pcg32_random_t* rng;
    float* f;

    checkCudaCall(cudaMallocManaged(&rng, n * sizeof(pcg32_random_t)));
    checkCudaCall(cudaMallocManaged(&f, n * sizeof(float)));

    for (int i = 0; i < n; ++i) {
        f[i] = 0.0f;
        pcg32_srandom_r(rng + i, time(NULL) ^ (intptr_t)&printf + i, (intptr_t)&rng * i);
    }

    dim3 block(BLOCK_SIZE);
    dim3 grid(div_ceil(n, block.x));

    test_pcg<<<grid, block>>>(rng, f, n);
    checkCudaCall(cudaGetLastError());
    checkCudaCall(cudaDeviceSynchronize());

    for (int i = 0; i < n; ++i) {
        printf("%f\n", f[i]);
    }
    checkCudaCall(cudaFree(rng));
    checkCudaCall(cudaFree(f));
}

int main()
{
    int N = 128;
    launch_kernel_test_pcg(N);

    return 0;
}