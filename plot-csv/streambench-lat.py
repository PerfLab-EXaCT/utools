import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nodes = ["Copy", "Scale", "Add", "Triad"]
nodes2 = ["mem", "dram", "pdax", "kdax"]

data = np.array([[0.062882,0.050042,8.707326,1.974689],
                 [0.06102,0.04914,13.095815,3.835484],
                 [0.082351,0.067204,8.472066,7.741135],
                 [0.081665,0.067247,14.099066,8.565123]])
sns.set_theme()
sns.set(font_scale=2)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))

ax = sns.heatmap(data, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
                 # cmap='coolwarm'

ax.set_title("STREAM Average Latency (s)", fontsize=20, fontweight='bold')

fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)

fig.savefig('my-file-name.pdf', bbox_inches='tight')

plt.show()
