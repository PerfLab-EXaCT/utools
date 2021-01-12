import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

if len(sys.argv) == 1:
    sys.exit("Expecting: python file.py path/to/csv-file")
data = np.genfromtxt(sys.argv[1], delimiter=',')
df = pd.DataFrame(data=data, columns=["dram", "mem", "kdax", "pdax"])
sns.set_theme()
sns.set(font_scale=2)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
ax = sns.violinplot(data=df, scale='width')
ax.set_title("Giga UPdates Per Seconds (GUPS)", fontsize=20, fontweight='bold')
fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
fig.savefig('gups-optane.pdf', bbox_inches='tight')
plt.show()
