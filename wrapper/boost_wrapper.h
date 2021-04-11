//
// Created by jcremona on 11/4/21.
//

#ifndef TINY_MC_BOOST_WRAPPER_H
#define TINY_MC_BOOST_WRAPPER_H

#ifdef __cplusplus
extern "C" {
#endif

    struct RNG *r;

    void initializeRNG();
    void seed(unsigned int c);

    float get_random();

    void deleteRNG();

#ifdef __cplusplus
}
#endif


#endif //TINY_MC_BOOST_WRAPPER_H
