import compilationlibrary as complib
import argparse
from sklearn.model_selection import ParameterGrid
import os
import csv
import numpy as np
import matplotlib.pyplot as plt


# import matplotlib.ticker as ticker

def explore(output_folder_path, cwd=None, iterations=10):
    # Explore different flags and plot the results
    p = {'compiler': complib.COMPILERS, 'optim': complib.OPTIMIZATION_FLAGS}
    grid = list(ParameterGrid(p))
    log_info = []
    for i, flags in enumerate(grid):
        compiler = flags['compiler']
        # Compile
        complib.compile_native(compiler, [flags['optim']], cwd=cwd, clean_required=True)
        photons_file_path = os.path.join(output_folder_path, "photons_{}.txt".format(i))
        for j in range(iterations):
            heat_file_path = os.path.join(output_folder_path, "heat_{}_{}.txt".format(i, j))
            # Execute
            complib.execute(heat_file_path, photons_file_path, cwd=cwd)
        log_info.append({'compiler': compiler, 'optim': flags['optim'], 'photons_output': photons_file_path})
    save_log_info(log_info, os.path.join(output_folder_path, 'results.csv'))
    print_results(log_info)


def print_results(log_info):
    # Given the results of the exploration, print the results
    plot_info = {}
    for l in log_info:
        a = np.genfromtxt(l['photons_output'], delimiter=",")
        compiler = l['compiler']
        label = l['optim']
        value = a
        if compiler not in plot_info:
            plot_info[compiler] = {'label': [label], 'value': [value]}
        else:
            plot_info[compiler]['label'].append(label)
            plot_info[compiler]['value'].append(value)
    plot_results(plot_info)


def plot_results(plot_info):
    # Plot results
    subplots = len(plot_info.keys())
    fig, axs = plt.subplots(1, subplots, sharey=True)

    for i, compiler in enumerate(plot_info):
        labels = plot_info[compiler]['label']
        # Plot mean
        values = [v.mean() for v in plot_info[compiler]['value']]
        axs[i].bar(labels, values)
        axs[i].set_xlabel(compiler)
        # scale_y = 1e3
        # ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
        # axs[i].yaxis.set_major_formatter(ticks_y)

    fig.text(0.05, 0.5, "Photons per second", ha="center", va="center", rotation=90)
    fig.suptitle('Average photons per sec by compiler and optimization flags (in addition to march=native).')
    plt.show()


def save_log_info(log_info, path):
    # Save a results.csv file containing the results of the exploration
    with open(path, 'w', newline='') as f:
        fieldnames = ['compiler', 'optim', 'photons_output']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_info)


def load_log_info(path):
    # Read a results.csv file and plot its content
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print_results(reader)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to explore compilation flags.')
    parser.add_argument("output", help="Output directory")
    parser.add_argument("--working_dir", help="Working directory")
    args = parser.parse_args()
    explore(args.output, cwd=args.working_dir)
