import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nodes = ["Copy", "Scale", "Add", "Triad"]
nodes2 = ["dram", "mem", "pdax", "kdax"]

data_bw = np.array([[320.05,254.59,1.85,8.21],
                   [325.93,262.57,1.22,4.20],
                   [357.38,291.78,2.83,3.12],
                   [357.28,294.35,1.70,2.81]])
data_lt = np.array([[0.050,0.062,8.70,1.97],
                 [0.049,0.061,13.09,3.83],
                 [0.067,0.082,8.47,7.74],
                 [0.067,0.081,14.09,8.56]])
sns.set_theme()
sns.set(font_scale=2)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(data_lt, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
ax.set_title("Latency (s)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('streambench-lat.pdf', bbox_inches='tight')

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.45, 2.5))
ax = sns.heatmap(data_bw, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
ax.set_title("B/W (GB/s)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('streambench-bw.pdf', bbox_inches='tight')

plt.show()
