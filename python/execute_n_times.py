import compilationlibrary as complib


def compile_gcc_and_execute_n(flags, heat_file_paths, photons_file_paths, cwd=None, iterations=10):
    complib.compile_gcc(flags, cwd=cwd, clean_required=True)
    for i in range(iterations):
        complib.execute(heat_file_paths[i], photons_file_paths[i], cwd=cwd)


if __name__ == "__main__":
    import argparse
    import os
    import numpy as np
    import config_flags

    parser = argparse.ArgumentParser(
        description='Compile code using march=native (and additional flags) and execute it n times')
    parser.add_argument("output", help="Output directory")
    parser.add_argument("--working_dir", help="Working directory")
    parser.add_argument("--iterations", type=int)
    args = parser.parse_args()
    flags_ = config_flags.EXECUTE_N_FIXED_FLAGS
    heat_file_paths_ = [os.path.join(args.output, "heat_{}.txt".format(i)) for i in range(args.iterations)]
    photons_file_path_ = os.path.join(args.output, "photons.txt")
    photons_file_paths_ = [photons_file_path_ for i in range(args.iterations)]
    compile_gcc_and_execute_n(flags_, heat_file_paths_, photons_file_paths_, cwd=args.working_dir,
                              iterations=args.iterations)
    results = np.loadtxt(photons_file_path_)
    print(results.mean())
