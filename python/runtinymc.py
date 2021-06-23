import subprocess as sp
import os


def build_compiler_param(compiler):
    return "CC=" + compiler


def build_flag_list(flags):
    tmp = " ".join(flags)
    return "EXTRA_CFLAGS=" + tmp


def build_cuda_flag_list(flags):
    tmp = " ".join(flags)
    return "EXTRA_CUFLAGS=" + tmp


def clean(cwd=None):
    sp.run(["make", "clean"], cwd=cwd)


def compile(compiler, flags, cwd=None, clean_required=False):
    # Compile tiny_mc using make. Compilation flags are passed as an argument.
    if clean_required:
        clean(cwd)
    flags_string_param = build_flag_list(flags)
    compiler_param = build_compiler_param(compiler)
    sp.run(["make", compiler_param, flags_string_param], cwd=cwd)


def clean_cuda(makefile, cwd=None):
    sp.run(["make", "clean", "-f", makefile], cwd=cwd)


# TODO merge this method with compile.
#  It should be a special case of compile
def compile_cuda(flags, cwd=None, clean_required=False):
    # Compile tiny_mc (CUDA version) using make.
    # Compilation flags are passed as an argument.
    makefile = "Makefile.cuda"
    if cwd:
        makefile = os.path.join(cwd, makefile)

    if clean_required:
        clean_cuda(makefile, cwd)
    flags_string_param = build_cuda_flag_list(flags)
    sp.run(["make", "-f", makefile, flags_string_param], cwd=cwd)


def clang_profiling(raw, output):
    sp.run(["llvm-profdata", "merge", "-output=" + output, raw])


def clean_icc_profiling(working_dir):
    sp.call('rm ' + working_dir + "/*.dyn", shell=True)
    sp.call('rm ' + working_dir + "/*.dpi", shell=True)


def execute(heat_file_path, photons_file_path, cwd=None):
    # Execute tiny_mc
    sp.run(["./tiny_mc", heat_file_path, photons_file_path], cwd=cwd)

#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Script to compile and execute tiny_mc')
#     parser.add_argument("--cwd", default=None, help="Working directory")
#     args = parser.parse_args()
#     compile(GCC, [O2, MARCH_NATIVE], cwd=args.cwd, clean_required=True)
#     execute(cwd=args.cwd)
