import numpy as np


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Script to compile.')
    parser.add_argument("input", help="Working directory")
    args = parser.parse_args()
    c = np.loadtxt(args.input)
    import matplotlib.pyplot as plt
    plt.scatter(c[:,0],c[:,1])
    plt.show()

