import numpy as np
import matplotlib.pyplot as plt


def plot_hist(radius, heat, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(20, 10))

    # creating the bar plot
    radius_labels = [str(r) for r in radius]
    ax.bar(radius_labels, heat, width=0.7)  # color ='maroon',width = 0.4)
    ax.set_yscale('log')
    ax.xaxis.set_major_locator(plt.MaxNLocator(15))
    plt.xlabel(xlabel)
    # plt.xticks(rotation=90, fontsize=5)
    plt.ylabel(ylabel)
    plt.title(title)
    # fig.tight_layout()
    # fig.savefig("foo.pdf", bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Script to plot histograms.')
    parser.add_argument("option", choices=['file', 'dir'], help="Option")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--allflags", type=int, help="Number of combinations of flags.")
    parser.add_argument("--iter", type=int, help="Number of iterations.")
    args = parser.parse_args()
    if args.option == 'file':
        results = np.loadtxt(args.input)
        radius = [int(l) for l in results[:, 0]]
        heat = results[:, 1]
        plot_hist(radius, heat, title="Radius vs. heat", xlabel="Radius (microns)", ylabel="Heat (W/cm^3)")
    else:
        import os

        heat_filenames = [filename for filename in os.listdir(args.input) if filename.startswith("heat")]
        heat_filenames = sorted(heat_filenames)
        # TODO unificar con lo anterior, que es un caso especial para el cual heat_filenames tiene un solo elemento
        if heat_filenames:
            N = len(heat_filenames)
            results = np.loadtxt(os.path.join(args.input, heat_filenames[0]))
            radius = [int(l) for l in results[:, 0]]
            accum_heat = results[:, 1:]
            for f in heat_filenames[1:]:
                heat_results = np.loadtxt(os.path.join(args.input, f))
                accum_heat += heat_results[:, 1:]

            average_heat = accum_heat / N
            plot_hist(radius, average_heat[:, 0], title="Average heat of {} samples".format(N),
                      xlabel="Radius (microns)",
                      ylabel="Heat (W/cm^3)")
