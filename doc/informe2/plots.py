import csv
import numpy as np
import matplotlib.pyplot as plt


def plot_bars(csv_reader, output_path, labels, ylabel, cols, title, width, xlimmin, xlimmax):
    x = np.arange(len(labels))  # the label locations
    len_cols = len(cols)
    fig, ax = plt.subplots()
    for i,c in enumerate(cols):
       rect = ax.bar(x + ((-len_cols+1)/2. + i) * width, [float(r[c]) for r in csv_reader], width, label=c)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_xlim(xlimmin,xlimmax)
    fig.tight_layout()
    plt.savefig(output_path, format="svg")
   
def open_and_plot(input_path, output_path, title,width=0.15,xlimmin=-1, xlimmax=1):
    with open(input_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_reader = list(csv_reader)

    labels = [r['#Compiler'] for r in csv_reader]
    cols = list(csv_reader[0].keys())[1:]
    print(cols)
    plot_bars(csv_reader, output_path, labels, 'Photons per second', cols, title, width, xlimmin, xlimmax)

