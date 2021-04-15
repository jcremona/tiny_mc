import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Este es un codigo horrible, pero estaba apurado y copié y pegué uno de Internet y lo adapté en dos patadas
with open('boost_vs_optimization_flags_50_samples.txt') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    csv_reader = list(csv_reader)
    

labels = [r['Algorithm'] for r in csv_reader]
o3_native = [float(r['O3-native']) for r in csv_reader]
o3_native_math = [float(r['O3-native-ffast-math']) for r in csv_reader]
o3_native_flto = [float(r['O3-native-flto']) for r in csv_reader]
o3_native_math_flto = [float(r['O3-native-ffast-math-flto']) for r in csv_reader]

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width * 3/2., o3_native, width, label='O3-native')
rects2 = ax.bar(x - width/2., o3_native_flto, width, label='O3-native-flto')
rects3 = ax.bar(x + width/2., o3_native_math, width, label='O3-native-ffast-math')
rects4 = ax.bar(x + width * 3/2., o3_native_math_flto, width, label='O3-native-ffast-math-flto')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Photons per second')
ax.set_title('Scores by algorithm and flag (avg of 50 executions)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
plt.savefig("fig1.svg", format="svg")

