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
#include <stdbool.h>

char t1[] = "Tiny Monte Carlo by Scott Prahl (http://omlc.ogi.edu)";
char t2[] = "1 W Point Source Heating in Infinite Isotropic Scattering Medium";
char t3[] = "CPU version, adapted for PEAGPGPU by Gustavo Castellano"
            " and Nicolas Wolovick";

static const int LANES = 8;

// global state
typedef struct heat_struct {
    float heat; // heat
    float heat2; // heat square
} heat_struct;

static heat_struct heat_array[SHELLS];

typedef struct {
    uint64_t state[LANES];
    uint64_t inc[LANES];
} pcg32vect_random_t;


static inline uint32_t randcalc(uint64_t oldstate)
{
//    uint64_t oldstate = rng->state;
//    rng->state = oldstate * 6364136223846793005ULL + rng->inc;
    uint32_t xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
    uint32_t rot = oldstate >> 59u;
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}


void pcg32vect_srandom_r(pcg32vect_random_t* rng, uint64_t* seeds, uint64_t* seqs)
{

    for(int i=0; i < LANES; i++){
        rng->state[i] = 0U;
        rng->inc[i] = (seqs[i] << 1u) | 1u;
        rng->state[i] = rng->state[i] * 6364136223846793005ULL + rng->inc[i];
//        pcg32_random_r(rng);
        rng->state[i] += seeds[i];
        rng->state[i] = rng->state[i] * 6364136223846793005ULL + rng->inc[i];
//        pcg32_random_r(rng);

//        pcg32_srandom_r(rng->gen+i, seeds[i], seqs[i]);
    }

}

pcg32vect_random_t global_rng;

static inline float random_float(int i) {
    uint64_t oldstate = global_rng.state[i];
    uint64_t inc = global_rng.inc[i];
    uint64_t newstate = oldstate * 6364136223846793005ULL + inc;
    global_rng.state[i] = newstate;
    return randcalc(oldstate) / (float)UINT32_MAX; //pcg32_random_r(&global_rng.gen[i]) / (float)UINT32_MAX;
}


/***
 * Photon
 ***/
static void photon(void)
{
    const float albedo = MU_S / (MU_S + MU_A);
    const float shells_per_mfp = 1e4 / MICRONS_PER_SHELL / (MU_A + MU_S);

    /* launch */
    float x[LANES];
    float y[LANES];
    float z[LANES];
    float u[LANES];
    float v[LANES];
    float w[LANES];
    float weight[LANES];
    float t[LANES];
    unsigned int shell[LANES];
    int break_count = 0;
    float random_roulette[LANES];
    float random_xi1[LANES];
    float random_xi2[LANES];
    float random_tmp[LANES];
    float random_t[LANES];
    float heat[LANES];
    float heat2[LANES];
//    bool need_clean[LANES];
    bool mask_exec[LANES] __attribute__((aligned(32)));
    for(int i=0; i<LANES; i++){
        x[i] = 0.0f;
        y[i] = 0.0f;
        z[i] = 0.0f;
        u[i] = 0.0f;
        v[i] = 0.0f;
        w[i] = 1.0f;
        weight[i] = 1.0f;
        t[i] = -logf(random_float(i));
        heat[i] = 0.0f;
        heat2[i] = 0.0f;
        mask_exec[i] = true;
    }

    while (break_count < PHOTONS){

        for (int i=0; i<LANES; i++) {
            if(mask_exec[i]) {
                x[i] += t[i] * u[i];
                y[i] += t[i] * v[i];
                z[i] += t[i] * w[i];
                //        printf("%f %f %f\n", x[i], y[i], z[i]);
                unsigned int shell_ = sqrtf(x[i] * x[i] + y[i] * y[i] + z[i] * z[i]) * shells_per_mfp; /* absorb */
                if (shell_ > SHELLS - 1) {
                    shell[i] = SHELLS - 1;
                } else {
                    shell[i] = shell_;
                }
                heat[i] += (1.0f - albedo) * weight[i];
                heat2[i] += (1.0f - albedo) * (1.0f - albedo) * weight[i] * weight[i]; /* add up squares */
                weight[i] *= albedo;
            }

//            /* Rejection method */
            if (mask_exec[i] && weight[i] < 0.001f && random_float(i) > 0.1f) { /* roulette */
                x[i] = 0.0f;
                y[i] = 0.0f;
                z[i] = 0.0f;
                u[i] = 0.0f;
                v[i] = 0.0f;
                w[i] = 1.0f;
                weight[i] = 1.0f;
                break_count++;
            }
            else{
                random_xi1[i] = 2.0f * random_float(i) - 1.0f;
                random_xi2[i] = 2.0f * random_float(i) - 1.0f;
                random_tmp[i] = random_xi1[i] * random_xi1[i] + random_xi2[i] * random_xi2[i];
                if(random_tmp[i] < 1.0f) {
                    u[i] = 2.0f * random_tmp[i] - 1.0f;
                    v[i] = random_xi1[i] * 2 * sqrtf(1.0f - random_tmp[i]);
                    w[i] = random_xi2[i] * 2 * sqrtf(1.0f - random_tmp[i]);
                    mask_exec[i] = true;
                }
                else
                    mask_exec[i] = false;
            }
            t[i] = -logf(random_float(i));

            if(weight[i] < 0.001f && mask_exec[i]) {
                weight[i] /= 0.1f;
            }
            else
                weight[i] *= 1.0f;

        }
        for(int i=0; i < LANES; i++){
            heat_array[shell[i]].heat += heat[i];
            heat_array[shell[i]].heat2 += heat2[i];
            heat[i] = 0.0f;
            heat2[i] = 0.0f;
        }
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


    uint64_t seeds[LANES];
    uint64_t seqs[LANES];
    for(int i=0; i < LANES; i++) {
        seeds[i] = i * time(NULL) + (intptr_t)&seqs; //pcg32_random_r(&initial_rng);
        seqs[i] = M_PI * i * time(NULL) + (intptr_t)&seeds;//pcg32_random_r(&initial_rng);
    }

    pcg32vect_srandom_r(&global_rng, seeds, seqs);
    // start timer
    double start = wtime();
    // simulation
    photon();

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
