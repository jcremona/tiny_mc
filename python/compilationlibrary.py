import runtinymc as tmc
import compilers
import time

# Compiler identifiers
COMPILERS = [compilers.GCC, compilers.CLANG, compilers.ICC]

# Flag identifiers
OPTIMIZATION_FLAGS = [compilers.O0, compilers.O1, compilers.O2, compilers.O3]


def get_gcc_compiler():
    return compilers.GCC


def get_clang_compiler():
    return compilers.CLANG


def get_icc_compiler():
    return compilers.ICC


def get_O3():
    return compilers.O3


def get_O2():
    return compilers.O2


def compile(compiler, flags, clean_required, cwd=None):
    fs = [compiler.get_flag_str(f) for f in flags]
    tmc.compile(compiler.get_compiler_str(), fs, clean_required=clean_required, cwd=cwd)


def compile_native(compiler, flags, clean_required, cwd=None):
    optim_flags = flags + [compilers.MARCH_NATIVE]
    compile(compiler, optim_flags, clean_required, cwd=cwd)


def compile_gcc(flags, clean_required, cwd=None):
    compile(get_gcc_compiler(), flags, cwd=cwd, clean_required=clean_required)


def compile_clang(flags, clean_required, cwd=None):
    compile(get_clang_compiler(), flags, cwd=cwd, clean_required=clean_required)


def clang_profiling(raw, output):
    tmc.clang_profiling(raw, output)


def clean_icc_profiling(working_dir):
    tmc.clean_icc_profiling(working_dir)


def execute(heat_file_path=None, photons_file_path=None, cwd=None):
    timestr = time.strftime("%Y%m%d_%H%M%S")
    if heat_file_path is None:
        heat_file_path = "heat_tmp_{}.txt".format(timestr)
    if photons_file_path is None:
        photons_file_path = "photons_tmp_{}.txt".format(timestr)
    tmc.execute(heat_file_path, photons_file_path, cwd=cwd)
