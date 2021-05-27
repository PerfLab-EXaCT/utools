#!/usr/bin/env python
# -*-Mode: python;-*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import nan

nodes = ["0", "1", "2", "3"]
nodes2 = ["0", "1", "2", "3"]

mem_data_ws = np.array([[nan,109.6,112.5,108.3],
                 [109.1,nan,109.2,111.7],
                 [113.4,109.4,nan,109.9],
                 [108.9,111.6,109,nan]])

mem_data_rs = np.array([[nan,188.4,192.6,187],
                 [187.5,nan,190,192],
                 [193.3,190.2,nan,194.4],
                 [192.7,196.3,193.6,nan]])

dram_data_ws = np.array([[nan,111.1,113.6,109.2],
                 [110.2,nan,110.5,112.7],
                 [113.7,110.5,nan,111.3],
                 [110.2,112.7,110.1,nan]])

dram_data_rs = np.array([[nan,183.8,191.9,185.2],
                 [182.5,nan,189.4,190.3],
                 [186.2,184.3,nan,192.6],
                 [184.9,190.3,193.5,nan]])

sns.set_theme()
sns.set(font_scale=2)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(mem_data_ws, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":18})
ax.set(xlabel="Reader", ylabel="Writer/Data")
ax.set_title("MEM L2 HITM (ns)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('mem_c2c_ws.pdf', bbox_inches='tight')

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(mem_data_rs, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":18})
ax.set(xlabel="Reader/Data", ylabel="Writer")
ax.set_title("MEM L2 HITM (ns)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('mem_c2c_rs.pdf', bbox_inches='tight')

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(dram_data_ws, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":18})
ax.set(xlabel="Reader", ylabel="Writer/Data")
ax.set_title("DRAM L2 HITM (ns)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('dram_c2c_ws.pdf', bbox_inches='tight')

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.0, 2.5))
ax = sns.heatmap(dram_data_rs, ax=axes,
                 xticklabels=nodes2, yticklabels=nodes,
                 cmap='RdBu_r', annot=True, fmt=".2f", annot_kws={"size":18})
ax.set(xlabel="Reader/Data", ylabel="Writer")
ax.set_title("DRAM L2 HITM (ns)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('dram_c2c_rs.pdf', bbox_inches='tight')

plt.show()
