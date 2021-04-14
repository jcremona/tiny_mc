import runtinymc as tmc
import time

# Compiler identifiers
COMPILERS = [tmc.GCC, tmc.CLANG]

# Flag identifiers
OPTIMIZATION_FLAGS = [tmc.O0, tmc.O1, tmc.O2, tmc.O3]


def compile_native(compiler, flags, clean_required, cwd=None):
    optim_flags = flags + [tmc.MARCH_NATIVE]
    tmc.compile(compiler, optim_flags, cwd=cwd, clean_required=clean_required)


def compile_gcc(flags, clean_required, cwd=None):
    tmc.compile(get_gcc_compiler(), flags, cwd=cwd, clean_required=clean_required)


def execute(heat_file_path=None, photons_file_path=None, cwd=None):
    timestr = time.strftime("%Y%m%d_%H%M%S")
    if heat_file_path is None:
        heat_file_path = "heat_tmp_{}.txt".format(timestr)
    if photons_file_path is None:
        photons_file_path = "photons_tmp_{}.txt".format(timestr)
    tmc.execute(heat_file_path, photons_file_path, cwd=cwd)


def get_gcc_compiler():
    return tmc.GCC


def get_clang_compiler():
    return tmc.CLANG


def get_O3():
    return tmc.O3


def get_O2():
    return tmc.O2
