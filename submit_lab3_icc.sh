#!/bin/bash

#SBATCH --job-name=tinymc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

NUM_ITER=25

if [ $SLURM_CPUS_PER_TASK -gt 1 ] ; then
	srun ./execute_n_times.sh -p -n $NUM_ITER icc
else
	srun ./execute_n_times.sh -n $NUM_ITER icc
fi

# Run using -c (cpus per task)
# sbatch -c <NUM_OF_THREADS> submit_lab3_icc.sh

