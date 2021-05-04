O0_ID = "O0"
O1_ID = "O1"
O2_ID = "O2"
O3_ID = "O3"
MARCH_NATIVE_ID = "march_native"
FFAST_MATH_ID = "ffast_math"
GDEBUG_ID = "gdebug"
FLTO_ID = "flto"
FPROFILE_GENERATE_ID = "fprofile_generate"  # FDO
FPROFILE_USE_ID = "fprofile_use"
FTREE_VECTORIZE_ID = "ftree_vectorize"


class Flag:
    def __init__(self, flag_id):
        self._id = flag_id
        self._has_argument = False
        self._arg = None

    def set_arg(self, argument):
        if argument is not None:
            self._arg = argument
            self._has_argument = True

    def get_arg(self):
        return self._arg

    def has_arg(self):
        return self._has_argument

    def get_id(self):
        return self._id


O0 = Flag(O0_ID)
O1 = Flag(O1_ID)
O2 = Flag(O2_ID)
O3 = Flag(O3_ID)
MARCH_NATIVE = Flag(MARCH_NATIVE_ID)
FFAST_MATH = Flag(FFAST_MATH_ID)
GDEBUG = Flag(GDEBUG_ID)
FLTO = Flag(FLTO_ID)
FPROFILE_GENERATE = Flag(FPROFILE_GENERATE_ID)
FPROFILE_USE = Flag(FPROFILE_USE_ID)
FTREE_VECTORIZE = Flag(FTREE_VECTORIZE_ID)


class Compiler:
    def get_flag_str(self, flag):
        flag_id = flag.get_id()
        flag_str = self._map_to_flags[flag_id]
        if flag.has_arg():
            return flag_str + "=" + flag.get_arg()

        return flag_str

    def get_compiler_str(self):
        return self._compiler_string

class GCCCompiler(Compiler):
    def __init__(self):
        self._map_to_flags = {O0_ID: "-O0",
                              O1_ID: "-O1",
                              O2_ID: "-O2",
                              O3_ID: "-O3",
                              MARCH_NATIVE_ID: "-march=native",
                              FFAST_MATH_ID: "-ffast-math",
                              GDEBUG_ID: "-g",
                              FLTO_ID: "-flto",
                              FPROFILE_GENERATE_ID: "-fprofile-generate",
                              FPROFILE_USE_ID: "-fprofile-use",
                              FTREE_VECTORIZE_ID: "-ftree-vectorize"}
        self._compiler_string = "gcc"


class ClangCompiler(Compiler):
    def __init__(self):
        self._map_to_flags = {O0_ID: "-O0",
                              O1_ID: "-O1",
                              O2_ID: "-O2",
                              O3_ID: "-O3",
                              MARCH_NATIVE_ID: "-march=native",
                              FFAST_MATH_ID: "-ffast-math",
                              GDEBUG_ID: "-g",
                              FLTO_ID: "-flto",
                              FPROFILE_GENERATE_ID: "-fprofile-instr-generate",
                              FPROFILE_USE_ID: "-fprofile-instr-use",
                              FTREE_VECTORIZE_ID: "-ftree-vectorize"}
        self._compiler_string = "clang"


GCC = GCCCompiler()
CLANG = ClangCompiler()
