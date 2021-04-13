import runtinymc as tmc

# flags for explore_flags.py
EXPLORE_FIXED_FLAGS = [tmc.FFAST_MATH, tmc.MARCH_NATIVE, tmc.FLTO]

# flags for execute_n_times.py
EXECUTE_N_FIXED_FLAGS = [tmc.O3,tmc.FFAST_MATH, tmc.MARCH_NATIVE, tmc.FPROFILE_USE]#, "-fopt-info-vec-missed"]

# flags for compile.py
SIMPLE_COMPILE_FLAGS = [tmc.O3, tmc.FFAST_MATH, tmc.MARCH_NATIVE, tmc.FPROFILE_GENERATE] #EXECUTE_N_FIXED_FLAGS 



