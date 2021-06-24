#!/bin/bash

#SBATCH --job-name=tinymc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive



TMPDIR=$HOME/tmp srun /opt/cuda/11.2.2/nsight-compute-2020.3.1/ncu -f -o tiny_kernel --set full ./tiny_mc

# Run
# sbatch submit_lab4_icc.sh

