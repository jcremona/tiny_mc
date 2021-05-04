/* Tiny Monte Carlo by Scott Prahl (http://omlc.ogi.edu)"
 * 1 W Point Source Heating in Infinite Isotropic Scattering Medium
 * http://omlc.ogi.edu/software/mc/tiny_mc.c
 *
 * Adaptado para CP2014, Nicolas Wolovick
 */

#include "params.h"
#include "wtime.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

char t1[] = "Tiny Monte Carlo by Scott Prahl (http://omlc.ogi.edu)";
char t2[] = "1 W Point Source Heating in Infinite Isotropic Scattering Medium";
char t3[] = "CPU version, adapted for PEAGPGPU by Gustavo Castellano"
            " and Nicolas Wolovick";


// global state
typedef struct heat_struct {
    float heat; // heat
    float heat2; // heat square
} heat_struct;

static heat_struct heat_array[SHELLS];

struct pcg_state_setseq_64 {
    uint64_t state;             // RNG state.  All values are possible.
    uint64_t inc;               // Controls which RNG sequence (stream) is
    // selected. Must *always* be odd.
};
typedef struct pcg_state_setseq_64 pcg32_random_t;

uint32_t pcg32_random_r(pcg32_random_t* rng)
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

pcg32_random_t global_rng;

static inline float random_float() {
    return (pcg32_random_r(&global_rng) / (float)UINT32_MAX);
}

/***
 * Photon
 ***/

static void photon(void)
{
    const float albedo = MU_S / (MU_S + MU_A);
    const float shells_per_mfp = 1e4 / MICRONS_PER_SHELL / (MU_A + MU_S);

    /* launch */
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    float u = 0.0f;
    float v = 0.0f;
    float w = 1.0f;
    float weight = 1.0f;

    for (;;) {
        float t = -logf(random_float()); /* move */
        x += t * u;
        y += t * v;
        z += t * w;

        unsigned int shell = sqrtf(x * x + y * y + z * z) * shells_per_mfp; /* absorb */
        if (shell > SHELLS - 1) {
            shell = SHELLS - 1;
        }

        heat_array[shell].heat += (1.0f - albedo) * weight;
        heat_array[shell].heat2 += (1.0f - albedo) * (1.0f - albedo) * weight * weight; /* add up squares */
        weight *= albedo;

        /* Rejection method */
        if (weight < 0.001f) { /* roulette */
            if (random_float() > 0.1f)
                break;
            weight /= 0.1f;
        }

        /* New direction */
        float xi1, xi2;
        do {
            xi1 = 2.0f * random_float() - 1.0f;
            xi2 = 2.0f * random_float() - 1.0f;
            t = xi1 * xi1 + xi2 * xi2;
        } while (1.0f < t);
        u = 2.0f * t - 1.0f;
        v = xi1 * sqrtf((1.0f - u * u) / t);
        w = xi2 * sqrtf((1.0f - u * u) / t);

    }
}


/***
 * Main matter
 ***/

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
//    printf("# Photons    = %8d\n#\n", PHOTONS);

    pcg32_srandom_r(&global_rng, time(NULL) ^ (intptr_t)&printf, (intptr_t)&heat_array);

    // start timer
    double start = wtime();
    // simulation
    for (unsigned int i = 0; i < PHOTONS; ++i) {
        photon();
    }
    // stop timer
    double end = wtime();
    assert(start <= end);
    double elapsed = end - start;

    FILE* heat_fp = fopen(heat_filepath, "w");
    FILE* photons_fp = fopen(photons_per_sec_filepath, "a");
    printf("########################################################\n");
    printf("# Heat filepath: %s \n", heat_filepath);
    printf("# Photons filepath: %s \n", photons_per_sec_filepath);
    printf("# %lf seconds\n", elapsed);
    printf("# %lf K photons per second\n", 1e-3 * PHOTONS / elapsed);
    fprintf(photons_fp, "%lf\n", PHOTONS / elapsed);
    fclose(photons_fp);

//    printf("# Radius\tHeat\n");
//    printf("# [microns]\t[W/cm^3]\tError\n");
    // 1e12 -> cubic micron to cubic cm
    // Volume of spherical shell (times PHOTONS): (t * (i * i + i + 1.0 / 3.0))
    // It is equivalent to https://en.wikipedia.org/wiki/Spherical_shell
    float t = 4.0f * M_PI * powf(MICRONS_PER_SHELL, 3.0f) * PHOTONS / 1e12;
    for (unsigned int i = 0; i < SHELLS - 1; ++i) {
        fprintf(heat_fp, "%6.0f\t%12.5f\t%12.5f\n", i * (float)MICRONS_PER_SHELL,
                heat_array[i].heat / t / (i * i + i + 1.0 / 3.0),
                sqrt(heat_array[i].heat2 - heat_array[i].heat * heat_array[i].heat / PHOTONS) / t / (i * i + i + 1.0f / 3.0f));
    }
//    printf("# extra\t%12.5f\n", heat_array[SHELLS - 1].heat / PHOTONS);
    fclose(heat_fp);
    printf("########################################################\n");
    return 0;
}
