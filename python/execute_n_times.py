import compilationlibrary as complib


def compile_and_execute_n(compiler, flags, heat_file_paths, photons_file_paths, cwd=None, iterations=10):
    complib.compile(compiler, flags, cwd=cwd, clean_required=True)
    for i in range(iterations):
        complib.execute(heat_file_paths[i], photons_file_paths[i], cwd=cwd)


if __name__ == "__main__":
    import argparse
    import os
    import numpy as np
    import config_flags
    import compilers as c

    parser = argparse.ArgumentParser(
        description='Compile code using march=native, FDO, (and additional flags) and execute it n times')
    parser.add_argument("output", help="Output directory")
    parser.add_argument("compiler", choices=['gcc', 'clang'], help="Compiler.")
    parser.add_argument("--working_dir", help="Working directory")
    parser.add_argument("--iterations", type=int)
    args = parser.parse_args()
    output = args.output
    cwd = args.working_dir
    iterations = args.iterations

    if args.compiler == "gcc":
        compiler = complib.get_gcc_compiler()
    elif args.compiler == "clang":
        compiler = complib.get_clang_compiler()

    # FDO
    # Build an instrumented version of the program for edge and value profiling
    complib.compile(compiler, config_flags.LAB1_FLAGS + [c.FPROFILE_GENERATE], cwd=cwd, clean_required=True)
    # Run the instrumented version. It generates a profile data file (tiny_mc.gcda).
    complib.execute("foo.txt", "bar.txt", cwd=cwd)
    profile_use_flag = c.FPROFILE_USE
    if args.compiler == "clang":
        # Clang needs to execute llvm-profdata merge
        out_profiling = "tiny_mc.profdata"
        complib.clang_profiling("default.profraw", out_profiling)
        profile_use_flag.set_arg(out_profiling)

    heat_file_paths_ = [os.path.join(output, "heat_{}.txt".format(i)) for i in range(iterations)]
    photons_file_path_ = os.path.join(output, "photons.txt")
    photons_file_paths_ = [photons_file_path_ for i in range(iterations)]
    # Re build the source with the profile data as feedback and run it N times.
    flags_ = config_flags.LAB1_FLAGS + [profile_use_flag] + config_flags.ADDITIONAL_EXEC_N_FLAGS
    compile_and_execute_n(compiler, flags_, heat_file_paths_, photons_file_paths_, cwd=cwd,
                              iterations=iterations)
    results = np.loadtxt(photons_file_path_)
    print("Average photons per second ({} iterations)".format(iterations))
    print(results.mean())
