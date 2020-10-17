import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nodes = ["Copy", "Scale", "Add", "Triad"]
nodes2 = ["mem", "dram", "pdax", "kdax"]

data = np.array([[25.45,32,1.85,8.21],
                 [26.25,32.59,1.22,4.2],
                 [29.17,35.73,2.83,3.12],
                 [29.43,35.72,1.7,2.81]])
sns.set_theme()
sns.set(font_scale=2)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))

ax = sns.heatmap(data, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
                 # cmap='coolwarm'

ax.set_title("STREAM B/W (GB/s)", fontsize=20, fontweight='bold')

fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)

fig.savefig('streambench-bw.pdf', bbox_inches='tight')

plt.show()
