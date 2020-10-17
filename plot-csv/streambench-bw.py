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
ax = sns.heatmap(data, xticklabels=nodes2, yticklabels=nodes, cmap='coolwarm', annot=True, fmt=".2f", annot_kws={"size":20})
plt.title("STREAM B/W (GB/s)", fontsize=20, fontweight='bold')
plt.show()
