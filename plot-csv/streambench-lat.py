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
ax = sns.heatmap(data, xticklabels=nodes2, yticklabels=nodes, cmap='coolwarm', annot=True, fmt=".2f", annot_kws={"size":20})
plt.title("STREAM Average Latency (s)", fontsize=20, fontweight='bold')
plt.show()
