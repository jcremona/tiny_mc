#!/bin/bash

# Get full directory name of the script no matter where it is being called from
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

dt=$(date '+%Y%m%d_%H%M%S')
OUTPUT_DIR=$CURRENT_DIR/outputs/execute_n_${dt}

function echoUsage()
{
  echo -e "Usage: ./execute_n_times.sh [-n <N_TIMES>] <COMPILER>\n\
          \t <COMPILER> is clang, icc or gcc \n\
          \t -n <N_TIMES>\t N_TIMES is the number of times that tiny_mc is executed\n\
          \t -p \t\t Enable OpenMP\n\
          \t -h \t\t Help." >&2
}

N_TIMES=1
ENABLE_OPEN_MP=0
shopt -s extglob
while getopts "hn:p" opt; do
    case "$opt" in
        h)  echoUsage
            exit 0
            ;;
        p)  ENABLE_OPEN_MP=1
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

COMPILER=$1
mkdir -p $OUTPUT_DIR

OPEN_MP_FLAG=""
if [ $ENABLE_OPEN_MP -eq 1 ] ; then
    OPEN_MP_FLAG="--openmp"
fi

python3 $CURRENT_DIR/python/execute_n_times.py $OUTPUT_DIR $COMPILER --working_dir $CURRENT_DIR --iterations $N_TIMES $OPEN_MP_FLAG
echo "Saved to $OUTPUT_DIR"

