import numpy as np 
import matplotlib.pyplot as plt
data = np.loadtxt('size_vs_pps.txt')
fig, ax = plt.subplots()
ax.plot(data[:,0], data[:,1],'-o')

ax.set_xscale('log')
plt.xlabel("Number of photons")
plt.ylabel("Photons per second")
plt.title("Size vs. pps (avg. of 50 executions)")
fig.savefig("fig3.svg", format="svg")

