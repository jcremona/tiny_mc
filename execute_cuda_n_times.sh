#!/bin/bash

# Get full directory name of the script no matter where it is being called from
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

dt=$(date '+%Y%m%d_%H%M%S')
OUTPUT_DIR=$CURRENT_DIR/outputs/execute_n_${dt}

function echoUsage()
{
  echo -e "Usage: ./execute_cuda_n_times.sh [-n <N_TIMES>] \n\
          \t -n <N_TIMES>\t N_TIMES is the number of times that tiny_mc is executed\n\
          \t -h \t\t Help." >&2
}

N_TIMES=1

shopt -s extglob
while getopts "hn:" opt; do
    case "$opt" in
        h)  echoUsage
            exit 0
            ;;
        n)  case $OPTARG in
                (+([0-9])) N_TIMES=$OPTARG ;;
                *) echo "ERROR: a number must be provided"; echoUsage; exit 1 ;;
            esac
            ;;
        *)
            echoUsage
            exit 1
            ;;
    esac
done

shift $((OPTIND - 1))

mkdir -p $OUTPUT_DIR

python3 $CURRENT_DIR/python/execute_cuda.py $OUTPUT_DIR --working_dir $CURRENT_DIR --iterations $N_TIMES
echo "Saved to $OUTPUT_DIR"

