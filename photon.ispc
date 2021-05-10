struct pcg32_random_t {
    uniform unsigned int64 state[programCount];
    uniform unsigned int64 inc[programCount];
};

uniform pcg32_random_t rng;


varying unsigned int pcg32_random_r()
{
    unsigned int64 oldstate = rng.state[programIndex];
    // Advance internal state
    rng.state[programIndex] = oldstate * 6364136223846793005ULL + (rng.inc[programIndex]|1);
    // Calculate output function (XSH RR), uses old state for max ILP
    unsigned int xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
    unsigned int rot = oldstate >> 59u;
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}

void pcg32_srandom_r(varying unsigned int64 initstate, varying unsigned int64 initseq)
{
    rng.state[programIndex] = 0U;
    rng.inc[programIndex] = (initseq << 1u) | 1u;
    pcg32_random_r();
    rng.state[programIndex] += initstate;
    pcg32_random_r();
}

//export void get_random(uniform unsigned int64 seeds[], uniform unsigned int64 seqs[], uniform float output[]){
//    pcg32_srandom_r(seeds[programIndex], seqs[programIndex]);
//    output[programIndex] = pcg32_random_r() / (float) 4294967295U;
//}

varying float random_float()
{
    return pcg32_random_r() / (float)4294967295U;
}


void photon(uniform int MICRONS_PER_SHELL, uniform float MU_S,uniform float MU_A, float *heat_, float *heat2_, uniform int SHELLS)
{
    const uniform float albedo = MU_S / (MU_S + MU_A);
    const uniform float shells_per_mfp = 1e4 / MICRONS_PER_SHELL / (MU_A + MU_S);
    const uniform float one_minus_albedo = (1.0f - albedo);

    /* launch */
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    float u = 0.0f;
    float v = 0.0f;
    float w = 1.0f;
    float weight = 1.0f;

    for (;;) {
        float t = -log(random_float()); /* move */

        x += t * u;
        y += t * v;
        z += t * w;

        int shell = sqrt(x * x + y * y + z * z) * shells_per_mfp; /* absorb */
        if (shell > SHELLS - 1) {
            shell = SHELLS - 1;
        }

        heat_[shell] += one_minus_albedo * weight;
        heat2_[shell] += one_minus_albedo * one_minus_albedo * weight * weight;
        weight *= albedo;


        /* Rejection method */
        if (weight < 0.001f) { /* roulette */
            if (random_float() > 0.1f) {
                break;
            }
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
        v = xi1 * sqrt((1.0f - u * u) / t);
        w = xi2 * sqrt((1.0f - u * u) / t);

    }
}

export void run_simulation(uniform int photons,
                           uniform int shells,
                           uniform int microns_per_shell,
                           uniform float mu_s,
                           uniform float mu_a,
                           uniform float heat[],
                           uniform float heat2[]) {
    uniform unsigned int64 seeds[programCount];
    uniform unsigned int64 seqs[programCount];
    seeds[programIndex] = (intptr_t)&seqs * (programIndex+1) + (intptr_t)&seeds;
    seqs[programIndex] = (intptr_t)&seeds * ((programIndex+1)*43) + (intptr_t)&seqs;
    pcg32_srandom_r(seeds[programIndex], seqs[programIndex]);

    float *heat_ = new float[shells];
    float *heat2_ = new float[shells];


    foreach(j = 0 ... photons) {
        photon(microns_per_shell, mu_s, mu_a, heat_, heat2_, shells);//, heat, heat2);
    }

    for(uniform int i=0; i < shells; i++) {
        heat[i] = reduce_add(heat_[i]);
        heat2[i] = reduce_add(heat2_[i]);
    }

    delete[] heat_;
    delete[] heat2_;
}