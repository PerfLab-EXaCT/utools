#!/usr/bin/env python
# -*-Mode: python;-*-

import pandas
import numpy
import math
import matplotlib.pyplot as pyplt
import seaborn


fig, axes = pyplt.subplots(ncols=4, figsize=(15, 3))

#-------------------------------------------------------
# 1. random sample
#-------------------------------------------------------

x0 = numpy.random.normal(numpy.repeat(numpy.random.uniform(10, 20, 10), 100), 1)

seaborn.violinplot(x0, ax=axes[0])
axes[0].set_title('violin plot from original data')

#-------------------------------------------------------
# 2. make historgram
#-------------------------------------------------------

frequencies, bin_edges = numpy.histogram(x0)
axes[1].bar(bin_edges[:-1], frequencies, width=numpy.diff(bin_edges), ec='w', lw=1, align='edge')
axes[1].set_title('histogram')

#print(bin_edges)
#print(frequencies)

axes[2].hist(x = bin_edges[:-1], bins = bin_edges[:-1], weights = frequencies)
axes[2].set_title('histogram')

#-------------------------------------------------------
# 3. convert histogram to "wide form"
#-------------------------------------------------------

x1 = numpy.random.uniform(numpy.repeat(bin_edges[:-1], frequencies),
                          numpy.repeat(bin_edges[1:], frequencies))

#print("edges", bin_edges[:-1])
#print("edges", bin_edges[1:])
#print("x1", x1)

seaborn.violinplot(x1, ax=axes[3])
axes[3].set_title('violin plot from simulated data')

pyplt.tight_layout()
pyplt.show()


####

#   https://anvil.works/blog/tidy-data
#   https://sejdemyr.github.io/r-tutorials/basics/wide-and-long/
# dfrm_long = dfrm.melt('bw_bin', var_name='exe_ty', value_name='dram_bw')

