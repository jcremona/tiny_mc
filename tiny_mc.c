/* Tiny Monte Carlo by Scott Prahl (http://omlc.ogi.edu)"
 * 1 W Point Source Heating in Infinite Isotropic Scattering Medium
 * http://omlc.ogi.edu/software/mc/tiny_mc.c
 *
 * Adaptado para CP2014, Nicolas Wolovick
 */

#include "params.h"
#include "wtime.h"
#include "photon.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

char t1[] = "Tiny Monte Carlo by Scott Prahl (http://omlc.ogi.edu)";
char t2[] = "1 W Point Source Heating in Infinite Isotropic Scattering Medium";
char t3[] = "CPU version, adapted for PEAGPGPU by Gustavo Castellano"
            " and Nicolas Wolovick";


static float heat[SHELLS]; // heat
static float heat2[SHELLS]; // heat square

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

    // simulation
    for (unsigned int i = 0; i < SHELLS; ++i) {
        heat[i] = 0.0f;
        heat2[i] = 0.0f;
    }
    // start timer
    double start = wtime();

    run_simulation(PHOTONS, SHELLS, MICRONS_PER_SHELL, MU_S, MU_A, heat, heat2);

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
                heat[i] / t / (i * i + i + 1.0 / 3.0),
                sqrt(heat2[i] - heat[i] * heat[i] / PHOTONS) / t / (i * i + i + 1.0f / 3.0f));
    }
//    printf("# extra\t%12.5f\n", heat_array[SHELLS - 1].heat / PHOTONS);
    fclose(heat_fp);
    printf("########################################################\n");
    return 0;
}
