#include "helper_cuda.h"
#include "params.h"
#include "wtime.h"
#include <assert.h>
#include <cuda.h>

#ifndef BLOCK_SIZE
#define BLOCK_SIZE 512
#endif

#ifndef PHOTONS_PER_THREAD
#define PHOTONS_PER_THREAD 256
#endif

#define CUDA_WARP_SIZE 32

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

__device__ void photon(float* heat, float* heat2, pcg32_random_t* rng)
{
    const float albedo = MU_S / (MU_S + MU_A);
    const float one_minus_albedo = (1.0f - albedo);
    const float shells_per_mfp = 1e4 / MICRONS_PER_SHELL / (MU_A + MU_S);

    /* launch */
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    float u = 0.0f;
    float v = 0.0f;
    float w = 1.0f;
    float weight = 1.0f;
    int counter = 0;

    while (counter < PHOTONS_PER_THREAD) {
        float t = -logf(random_float(rng)); /* move */
        x += t * u;
        y += t * v;
        z += t * w;
        unsigned int shell = sqrtf(x * x + y * y + z * z) * shells_per_mfp; /* absorb */
        shell = min(shell, SHELLS - 1);

        unsigned int lane = threadIdx.x & (CUDA_WARP_SIZE - 1);
        unsigned int offset = (lane * SHELLS) + shell;
        atomicAdd(heat + offset, one_minus_albedo * weight);
        atomicAdd(heat2 + offset, one_minus_albedo * one_minus_albedo * weight * weight); /* add up squares */
        weight *= albedo;

        /* Rejection method */
        if (weight < 0.001f) { /* roulette */
            if (random_float(rng) > 0.1f) {
                x = 0.0f;
                y = 0.0f;
                z = 0.0f;
                u = 0.0f;
                v = 0.0f;
                w = 1.0f;
                weight = 1.0f;
                counter++;
                continue;
            }
            weight /= 0.1f;
        }

        /* New direction */
        float xi1, xi2;
        do {
            xi1 = 2.0f * random_float(rng) - 1.0f;
            xi2 = 2.0f * random_float(rng) - 1.0f;
            t = xi1 * xi1 + xi2 * xi2;
        } while (1.0f < t);
        u = 2.0f * t - 1.0f;
        v = xi1 * 2 * sqrtf(1.0f - t);
        w = xi2 * 2 * sqrtf(1.0f - t);
    }
}

__global__ void photon_kernel(float* heat, float* heat2, pcg32_random_t* rng, int n)
{
    int gtid = blockIdx.x * blockDim.x + threadIdx.x;
    if (gtid >= n) {
        return;
    }
    const int shared_array_size = SHELLS * CUDA_WARP_SIZE;
    __shared__ float shared_heat[shared_array_size];
    __shared__ float shared_heat2[shared_array_size];

    if (threadIdx.x == 0) {
        for (int i = 0; i < shared_array_size; i++) {
            shared_heat[i] = 0.0f;
            shared_heat2[i] = 0.0f;
        }
    }
    __syncthreads();

    pcg32_random_t local_rng = rng[gtid];
    photon(shared_heat, shared_heat2, &local_rng);

    __syncthreads();
    if (threadIdx.x == 0) {
        for (int i = 0; i < shared_array_size; i++) { // Better performance using SHELLS * warpSize. I don't know why
            atomicAdd(heat + (i % SHELLS), shared_heat[i]);
            atomicAdd(heat2 + (i % SHELLS), shared_heat2[i]);
        }
    }
}

// Ojo: Se rompe si a+b > 2^31
int div_ceil(int a, int b)
{
    return (a + b - 1) / b;
}

float run_photon_kernel(float* heat, float* heat2, int num_threads)
{
    printf("%d\n", num_threads);
    pcg32_random_t* rng;

    checkCudaCall(cudaMallocManaged(&rng, num_threads * sizeof(pcg32_random_t)));

    cudaEvent_t start, finish;
    checkCudaCall(cudaEventCreate(&start));
    checkCudaCall(cudaEventCreate(&finish));

    for (int i = 0; i < num_threads; ++i) {
        pcg32_srandom_r(rng + i, time(NULL) ^ (intptr_t)&printf + i, (intptr_t)&rng * i);
    }


    dim3 block(BLOCK_SIZE);
    dim3 grid(div_ceil(num_threads, block.x));

    checkCudaCall(cudaEventRecord(start));
    photon_kernel<<<grid, block>>>(heat, heat2, rng, num_threads);
    checkCudaCall(cudaGetLastError());

    checkCudaCall(cudaEventRecord(finish));
    checkCudaCall(cudaDeviceSynchronize());

    float gpu_elapsed;
    checkCudaCall(cudaEventElapsedTime(&gpu_elapsed, start, finish));
    checkCudaCall(cudaEventDestroy(start));
    checkCudaCall(cudaEventDestroy(finish));

    return gpu_elapsed;
}


int main(int argc, char* argv[])
{

    const char* heat_filepath;
    const char* photons_per_sec_filepath;
    if (argc == 3) {
        heat_filepath = argv[1];
        photons_per_sec_filepath = argv[2];
    } else {
        if (argc == 2) {
            fprintf(stderr, "ERROR: Argument missed!\nUsage: %s <HEAT_FILE_PATH> <PHOTONS_PER_SEC_FILE_PATH>\n", argv[0]);
            return -1;
        }
        heat_filepath = "heat.txt";
        photons_per_sec_filepath = "photons_per_sec.txt";
    }

    // heading
    //    printf("# %s\n# %s\n# %s\n", t1, t2, t3);
    //    printf("# Scattering = %8.3f/cm\n", MU_S);
    //    printf("# Absorption = %8.3f/cm\n", MU_A);


    //    for(int i=0; i<SHELLS; ++i) {
    //        heat_array[i].heat = 0.0f;
    //        heat_array[i].heat2 = 0.0f;
    //
    //    }

    float* heat;
    float* heat2;
    checkCudaCall(cudaMallocManaged(&heat, SHELLS * sizeof(float)));
    checkCudaCall(cudaMallocManaged(&heat2, SHELLS * sizeof(float)));

    for (int i = 0; i < SHELLS; ++i) {
        heat[i] = 0.0f;
        heat2[i] = 0.0f;
    }

    assert(!(PHOTONS % PHOTONS_PER_THREAD));
    double elapsed = run_photon_kernel(heat, heat2, PHOTONS / PHOTONS_PER_THREAD);
    elapsed *= 1e-3;

    FILE* heat_fp = fopen(heat_filepath, "w");
    FILE* photons_fp = fopen(photons_per_sec_filepath, "a");
    printf("########################################################\n");
    printf("# Photons    = %8d\n#\n", PHOTONS);
    printf("# Heat filepath: %s \n", heat_filepath);
    printf("# Photons filepath: %s \n", photons_per_sec_filepath);
    printf("# %lf seconds\n", elapsed);
    printf("# %lf K photons per second\n", 1e-3 * PHOTONS / elapsed);
    fprintf(photons_fp, "%lf\n", PHOTONS / elapsed);
    fclose(photons_fp);

    // 1e12 -> cubic micron to cubic cm
    // Volume of spherical shell (times PHOTONS): (t * (i * i + i + 1.0 / 3.0))
    // It is equivalent to https://en.wikipedia.org/wiki/Spherical_shell
    float t = 4.0f * M_PI * powf(MICRONS_PER_SHELL, 3.0f) * PHOTONS / 1e12;
    for (unsigned int i = 0; i < SHELLS - 1; ++i) {
        fprintf(heat_fp, "%6.0f\t%12.5f\t%12.5f\n", i * (float)MICRONS_PER_SHELL,
                heat[i] / t / (i * i + i + 1.0 / 3.0),
                sqrt(heat2[i] - heat[i] * heat[i] / PHOTONS) / t / (i * i + i + 1.0f / 3.0f));
    }

    fclose(heat_fp);
    printf("########################################################\n");
    return 0;
}