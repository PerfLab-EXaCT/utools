import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nodes = ["mem (inj.)", "mem (max)", "dram (inj.)", "dram (max)"]
nodes2 = ["READ", "3R:1W", "2R:1W", "1R:1W", "TRIAD"]

data = np.array([[428.323,399.8086,399.2903,369.314,281.2601],
                 [432.53598,399.83292,400.28847,369.34486,294.72464],
                 [448.0314,413.7166,409.9748,387.7461,352.6466],
                 [449.18806,414.24501,408.97372,388.69415,371.43719]])

sns.set_theme()
sns.set(font_scale=2)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
ax = sns.heatmap(data, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
ax.set(ylabel="GB/s")
ax.set_title("Max/Peak Injection BW (GB/s)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('max_inj_bw.pdf', bbox_inches='tight')
plt.show()
