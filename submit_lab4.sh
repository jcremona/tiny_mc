#!/bin/bash

#SBATCH --job-name=tinymc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive


NUM_ITER=1

srun ./execute_cuda_n_times.sh -n $NUM_ITER

# Run
# sbatch submit_lab4_icc.sh

