import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nodes = ["0", "1", "2", "3"]
nodes2 = ["0", "1", "2", "3"]

#memory mode
mem_data_lt = np.array([[90.3,150.7,155.9,149.9],
                 [150.2,90.5,150.6,152.2],
                 [154.6,149.3,90.2,149.5],
                 [149.1,153.2,150.5,89.4]])
mem_data_bw = np.array([[107.3,16.78,16.8,16.73],
                 [16.78,107.48,16.74,16.8],
                 [16.79,16.73,107.37,16.77],
                 [16.73,16.8,16.77,107.34]])
#appdirect(dram)
dram_data_lt = np.array([[83.3,141,145.4,140.3],
                 [140.5,82.7,140.2,143.1],
                 [144.4,139.9,82.1,140.1],
                 [139.3,143.9,140.5,82.3]])
dram_data_bw = np.array([[111.94,16.78,16.8,16.78],
                 [16.78,112.24,16.77,16.8],
                 [16.8,16.77,112.19,16.77],
                 [16.75,16.8,16.77,112.28]])
sns.set_theme()
sns.set(font_scale=2)

#mem latency
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(mem_data_lt, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
ax.set_title("MEM Idle Latency (ns)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('mlc-lat-mem.pdf', bbox_inches='tight')

#mem bw
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(mem_data_bw, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
ax.set_title("MEM B/W (GB/s)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('mlc-bw-dram.pdf', bbox_inches='tight')

#dram latency
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(dram_data_lt, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
ax.set_title("DRAM Idle Latency (ns)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('mlc-lat-dram.pdf', bbox_inches='tight')

#dram bw
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(dram_data_bw, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":20})
ax.set_title("DRAM B/W (GB/s)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('mlc-bw-dram.pdf', bbox_inches='tight')

plt.show()
