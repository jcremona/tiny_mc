import compilationlibrary as complib
from sklearn.model_selection import ParameterGrid
import utils
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def compile_and_execute_n(flags, heat_file_paths, photons_file_paths, cwd=None, iterations=10):
    complib.compile_cuda(flags, cwd=cwd, clean_required=True)
    for i in range(iterations):
        complib.execute(heat_file_paths[i], photons_file_paths[i], cwd=cwd)


def explore_n(flags, output_folder_path, cwd=None, iterations=10):
    block_sizes_list = 2 ** np.arange(5, 11)  # 32 to 1024 (powers of 2)
    ppt_list = 2 ** np.arange(13)  # 1 to 4096 (powers of 2)
    p = {'block_size': block_sizes_list, 'photons_per_thread': ppt_list}
    grid = list(ParameterGrid(p))
    log_info = []
    for grid_flags in grid:
        block_size = grid_flags['block_size']
        photons_per_thread = grid_flags['photons_per_thread']
        f = ["-DBLOCK_SIZE={}".format(block_size),
             "-DPHOTONS_PER_THREAD={}".format(photons_per_thread)]
        complib.compile_cuda(flags + f, cwd=cwd, clean_required=True)
        photons_file_path = os.path.join(output_folder_path,
                                         "photons_b{}_ppt{}.txt".format(block_size, photons_per_thread))
        for j in range(iterations):
            heat_file_path = os.path.join(output_folder_path,
                                          "heat_b{}_ppt{}_{}.txt".format(block_size, photons_per_thread, j))
            # Execute
            complib.execute(heat_file_path, photons_file_path, cwd=cwd)
        log_info.append({'block_size': block_size, 'photons_per_thread': photons_per_thread,
                         'photons_output': photons_file_path})
    utils.save_log_info(log_info, ['block_size', 'photons_per_thread', 'photons_output'],
                        os.path.join(output_folder_path, 'results.csv'))
    df = print_results(log_info)
    plot_results(df / 1e6, os.path.join(output_folder_path, 'results.svg'))


def print_results(log_info):
    # Given the results of the exploration, print the results
    plot_info = {}
    for l in log_info:
        arr = np.genfromtxt(l['photons_output'], delimiter=",")
        plot_info[(int(l['block_size']), int(l['photons_per_thread']))] = arr.mean()

    ser = pd.Series(list(plot_info.values()),
                    index=pd.MultiIndex.from_tuples(plot_info.keys()))
    df = ser.unstack()
    print(df)
    return df


def plot_results(df, output_path=None):
    fig, ax = plt.subplots(figsize=(15,7))
    sns.heatmap(df, annot=True, fmt="g", ax=ax)
    ax.tick_params(axis='both', labelsize=16)
    plt.title("Heatmap (Millons of photons per sec (pps))", fontsize=20)
    plt.xlabel("Photons per thread", fontsize=20)
    plt.ylabel("Block size", fontsize=20)
    cbar = ax.collections[0].colorbar
    # here set the labelsize by 20
    cbar.ax.tick_params(labelsize=20)
    if output_path:
        plt.savefig(output_path, format="svg")
    else:
        plt.show()


def load_results(path):
    log_info = utils.load_log_info(path)
    df = print_results(log_info)
    plot_results(df / 1e6)


def execute_n(output, cwd, iterations):
    heat_file_paths_ = [os.path.join(output, "heat_{}.txt".format(i)) for i in range(iterations)]
    photons_file_path_ = os.path.join(output, "photons.txt")
    photons_file_paths_ = [photons_file_path_ for i in range(iterations)]
    compile_and_execute_n([], heat_file_paths_, photons_file_paths_, cwd=cwd,
                          iterations=iterations)
    results = np.loadtxt(photons_file_path_)
    print("Average photons per second ({} iterations)".format(iterations))
    print(results.mean())


if __name__ == "__main__":
    import argparse
    import os
    import numpy as np

    parser = argparse.ArgumentParser(
        description='Compile code using march=native, FDO, (and additional flags) and execute it n times')
    parser.add_argument("output", help="Output directory")
    parser.add_argument("--working_dir", help="Working directory")
    parser.add_argument("--explore", action='store_true', help="Explore block size vs. photons per thread")
    parser.add_argument("--iterations", type=int)
    args = parser.parse_args()
    output = args.output
    cwd = args.working_dir
    iterations = args.iterations
    # load_results(output)
    if args.explore:
        explore_n([], output, cwd=cwd, iterations=iterations)
    else:
        execute_n(output, cwd, iterations)
