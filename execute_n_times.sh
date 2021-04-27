#!/bin/bash

# You can execute this script typing:
# ./execute_n_times N
#
# where N is the number of times that tiny_mc is executed
#
# If you omit the argument N:
# ./execute_n_times
#
# it is executed only once.

# Get full directory name of the script no matter where it is being called from
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

dt=$(date '+%Y%m%d_%H%M%S')
OUTPUT_DIR=$CURRENT_DIR/outputs/execute_n_${dt}
mkdir -p $OUTPUT_DIR
N_TIMES=${1:-1} # $1 if the script is called with an argument, otherwise 1 (one, default value)

python3 $CURRENT_DIR/python/execute_n_times.py $OUTPUT_DIR --working_dir $CURRENT_DIR --iterations $N_TIMES
echo "Saved to $OUTPUT_DIR"

