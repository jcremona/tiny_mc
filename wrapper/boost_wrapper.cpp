#include "boost_wrapper.h"

#include <boost/random/mersenne_twister.hpp>
//#include <boost/random/variate_generator.hpp>
//#include <boost/random/uniform_real.hpp>
#include <boost/random/uniform_real.hpp>
#include <boost/random/variate_generator.hpp>
#include "boost/generator_iterator.hpp"
#include <iostream>

typedef boost::mt19937 RNGAlgorithm ;
struct RNG {
    boost::variate_generator< RNGAlgorithm, boost::uniform_real<> > gen;
};

extern "C" {

    void initializeRNG() {
        r = (struct RNG*)malloc(sizeof(struct RNG));
    }

    void seed(unsigned int seed) {
        RNGAlgorithm rng(seed);
        boost::uniform_real<> uni_dist(0,1);
        boost::variate_generator< RNGAlgorithm, boost::uniform_real<> > uni(rng, uni_dist);
        r->gen = uni;
    }

    float get_random() {
        return (float)(r->gen.operator()());
    }

    void deleteRNG() {
        free(r);
    }
}
