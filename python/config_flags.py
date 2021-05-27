import compilers as c

# flags for explore_flags.py
EXPLORE_FIXED_FLAGS = [c.FFAST_MATH, c.MARCH_NATIVE, c.FLTO]

# Fixed flags for lab 1
# DO NOT MODIFY!
LAB1_FLAGS = [c.O3, c.FFAST_MATH, c.MARCH_NATIVE]

LAB2_FLAGS = LAB1_FLAGS + [c.FTREE_VECTORIZE, c.VECT_INFO,c.OPEN_MP]

# Flags for execute_n_times.py (in addition to lab 1 flags)
ADDITIONAL_EXEC_N_FLAGS = []

# flags for compile.py
SIMPLE_COMPILE_FLAGS = [c.O3, c.FFAST_MATH, c.MARCH_NATIVE, c.FPROFILE_GENERATE] #EXECUTE_N_FIXED_FLAGS 



