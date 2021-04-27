import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Este es un codigo horrible, pero estaba apurado y copié y pegué uno de Internet y lo adapté en dos patadas
with open('boost_vs_optimization_flags_50_samples.txt') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    csv_reader = list(csv_reader)
    labels = ['O3-native','O3-native-ffast-math','O3-native-flto','O3-native-ffast-math-flto']
    x = np.arange(len(csv_reader))  # the label locations
    width = 0.15  # the width of the bars
    fig, ax = plt.subplots(figsize=(10,6))
    for i,row in enumerate(csv_reader):
    	lab = row['Algorithm']
    	row.pop('Algorithm', None)
    	values = [float(row[l]) for l in labels]
    	ax.bar(x + (-3/2. + i) * width, values, width, label=lab)


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Photons per second')
ax.set_title('Scores by algorithm and flag (avg of 50 executions)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
#plt.show()
plt.savefig("fig2.svg", format="svg")

