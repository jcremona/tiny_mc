import config_flags
import compilationlibrary as complib

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Script to compile.')
    parser.add_argument("--working_dir", default=".", help="Working directory")
    args = parser.parse_args()
    complib.compile_gcc(config_flags.SIMPLE_COMPILE_FLAGS, clean_required=True, cwd=args.working_dir)
