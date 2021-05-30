import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def prepare_data(input_csv):
    df = pd.read_csv(input_csv)
    df['icc_opt'] = df['Cores'].multiply(df['icc'][0])
    df['gcc_opt'] = df['Cores'].multiply(df['gcc'][0])
    # df['clang_opt']=df['Cores'].multiply(df['clang'][0])

    df['icc_efficiency'] = df['icc'].divide(df['icc_opt'])
    df['icc_efficiency'] *= 100  # percentage

    df['gcc_efficiency'] = df['gcc'].divide(df['gcc_opt'])
    df['gcc_efficiency'] *= 100  # percentage

    return df


def plot_scatter(input_csv, output_path, title, with_optimal_line=True):
    df = prepare_data(input_csv)

    ax1 = df.plot(kind='scatter', x='Cores', y='icc', color='r', label='icc')
    ax2 = df.plot(kind='scatter', x='Cores', y='gcc', color='b', label='gcc', ax=ax1)

    if with_optimal_line:
        ax3 = df.plot(kind='line', x='Cores', y='icc_opt', color='r', ax=ax2, linewidth=0.5, linestyle='-.')
        ax4 = df.plot(kind='line', x='Cores', y='gcc_opt', color='b', ax=ax3, linewidth=0.5, linestyle='-.')

    ax1.legend()
    ax1.set_ylabel("Photons per sec")
    ax1.set_ylim([0, 31 * 1e6])
    plt.ticklabel_format(axis="y", style="sci", scilimits=(6, 6))  # Fix y axis to 1e6
    plt.title(title, y=1.07)
    print(df)
    plt.savefig(output_path, format="svg")

    # data = np.genfromtxt('my_file.csv', names=True,delimiter=',')
    # print(data.shape)


def plot_efficiency(input_csv, output_path, title):
    df = prepare_data(input_csv)
    ax1 = df.plot(kind='scatter', x='Cores', y='icc_efficiency', color='r', label='icc')
    ax2 = df.plot(kind='scatter', x='Cores', y='gcc_efficiency', color='b', label='gcc', ax=ax1)

    ax1.legend()
    ax1.set_ylabel("Efficiency (%)")
    ax1.set_ylim([0, 105])
    plt.title(title)
    print(df)
    plt.savefig(output_path, format="svg")
