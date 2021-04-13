import subprocess as sp

GCC = "g++"
CLANG = "clang"

O0 = "-O0"
O1 = "-O1"
O2 = "-O2"
O3 = "-O3"
MARCH_NATIVE = "-march=native"
FFAST_MATH = "-ffast-math"
GDEBUG = "-g"
FLTO = "-flto"
FPROFILE_GENERATE = "-fprofile-generate"  # FDO
FPROFILE_USE = "-fprofile-use"


def get_fprofile_use(file):
    return FPROFILE_USE + "=" + file


def build_compiler_param(compiler):
    return "CXX=" + compiler


def build_flag_list(flags):
    tmp = " ".join(flags)
    return "EXTRA_CFLAGS=" + tmp


def clean(cwd=None):
    sp.run(["make", "clean"], cwd=cwd)


def compile(compiler, flags, cwd=None, clean_required=False):
    # Compile tiny_mc using make. Compilation flags are passed as an argument.
    if clean_required:
        clean(cwd)
    flags_string_param = build_flag_list(flags)
    compiler_param = build_compiler_param(compiler)
    sp.run(["make", compiler_param, flags_string_param], cwd=cwd)


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
