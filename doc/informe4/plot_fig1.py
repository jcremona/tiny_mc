import numpy as np
import matplotlib.pyplot as plt

def plot():
    plt.figure(figsize=(6, 6))
    results = [142.5, 392.2, 495.9,539.5,547]
    xaxis = ["1e5", "1e6", "1e7", "1e8", "1e9"]

    plt.bar(xaxis, results)
    plt.title("Max. performance obtained per number of simulated photons")
    plt.xlabel("Number of simulated photons")
    plt.ylabel("Millons of photons per sec")
    plt.savefig("fig1.svg", format="svg")

plot()

