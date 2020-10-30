import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nodes = ["Copy", "Scale", "Add", "Triad"]
nodes2 = ["mem", "dram", "pdax", "kdax"]

data_bw = np.array([[254.593,320.056,1.850,8.213],
                 [262.570,325.938,1.223,4.209],
                 [291.782,357.382,2.839,3.128],
                 [294.359,357.281,1.706,2.813]])
data_lt = np.array([[0.062882,0.050042,8.707326,1.974689],
                 [0.06102,0.04914,13.095815,3.835484],
                 [0.082351,0.067204,8.472066,7.741135],
                 [0.081665,0.067247,14.099066,8.565123]])
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
