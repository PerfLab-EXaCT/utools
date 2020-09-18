#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

import io

import pandas
import numpy
import math
import matplotlib.pyplot as pyplt
import seaborn

#****************************************************************************
# Grappolo, Single phase, 192 threads
#****************************************************************************


#----------------------------------------------------------------------------
# Run time
#----------------------------------------------------------------------------

runtime_str = """
graph            dram      pmem   kmem
orkut          19.486    19.201   0
friendster   1081.808   878.044   739.163
moliere201   1054.310  1059.695   0
"""

runtime_data = io.StringIO(runtime_str)
dfrm = pandas.read_csv(runtime_data, sep='\s+', index_col=0)
print(dfrm)

# dfrm = pandas.DataFrame(data = timeL_med, index = timeL_ty)


#----------------------------------------------------------------------------
# friendster DRAM bandwidth (GB/sec)
#----------------------------------------------------------------------------

dram_bw_dram_str = """
dram_bw time
0	81.76752655810002
10	107.71000000000002
20	47.09
30	94.27000000000002
40	699.2400000000001
50	8.36
60	15.919999999999993
70	13.090000000000002
80	2.9099999999999997
90	1.640000000000001
100	1.9300000000000013
110	1.350000000000001
120	1.2400000000000009
130	1.1400000000000006
140	1.0600000000000005
150	0.8600000000000004
160	0.5800000000000002
170	0.3800000000000002
180	0.3200000000000001
190	0.27
200	0.07
210	0.03
220	0.01
230	0.01
240	0
250	0.01
260	0
270	0.05
280	0.07
290	0.01
300	0.01
310	0
320	0
330	0
340	0.01
350	0.02
360	0.07
370	0.31000000000000005
380	0
390	0
400	0
410	0
420	0
430	0
440	0
450	0
"""

dram_bw_pmem_str = """
dram_bw time
0	188.37429006909997
10	79.14
20	77.32
30	34.379999999999995
40	14.96
50	42.56
60	51.85
70	222.13000000000005
80	155.11000000000007
90	3.269999999999998
100	1.330000000000001
110	1.0300000000000007
120	0.7400000000000004
130	0.8800000000000006
140	0.8500000000000004
150	0.7300000000000004
160	0.7800000000000004
170	0.6300000000000003
180	0.5200000000000002
190	0.5000000000000002
200	0.31000000000000005
210	0.20000000000000007
220	0.13
230	0.09999999999999999
240	0.13
250	0.07
260	0.01
270	0
280	0.01
290	0
300	0
310	0
320	0
330	0
340	0
350	0
360	0
370	0
380	0
390	0
400	0
410	0
420	0
430	0
440	0
450	0
"""

dram_bw_kmem_str = """
dram_bw time
0	62.142981342099986
10	76.75000000000001
20	73.94999999999999
30	29.88
40	16.67
50	38.45000000000002
60	69.14000000000001
70	207.36999999999998
80	154.28000000000003
90	0.9600000000000005
100	0.9500000000000005
110	0.7700000000000002
120	0.38000000000000017
130	0.6200000000000003
140	0.6500000000000004
150	0.6300000000000003
160	0.5200000000000002
170	0.3900000000000001
180	0.4900000000000002
190	0.6600000000000004
200	0.7500000000000003
210	0.6500000000000004
220	0.5800000000000003
230	0.5800000000000003
240	0.40000000000000013
250	0.2700000000000001
260	0.10999999999999999
270	0.12
280	0.05
290	0
300	0
310	0
320	0
330	0
340	0
350	0
360	0
370	0
380	0
390	0
400	0
410	0
420	0
430	0
440	0
450	0
"""


#-------------------------------------------------------
# Create DataFrames
#-------------------------------------------------------

data_nmL =  ['dram', 'pmem', 'kmem']
data_strL = [ dram_bw_dram_str, dram_bw_pmem_str, dram_bw_kmem_str ]

dfrm_hist = pandas.DataFrame()
dfrm_wide = pandas.DataFrame()

idx = 0
for data_str in data_strL:
    #---------------------------------------
    # Create histogram
    #---------------------------------------

    str_data = io.StringIO(data_str)
    dfrm_hist_x = pandas.read_csv(str_data, sep='\s+', index_col=0)

    dfrm_hist_x.columns = [ data_nmL[idx] ]
    #print(dfrm_hist_x)

    #---------------------------------------
    # Convert the histogram to Seaborn 'wide form'
    #---------------------------------------
    #   https://stackoverflow.com/questions/62709719/violinplot-from-histogram-values
    #   https://anvil.works/blog/tidy-data
    #   https://sejdemyr.github.io/r-tutorials/basics/wide-and-long/

    hist_bin  = dfrm_hist_x.index
    hist_freq = dfrm_hist_x.iloc[:, 0]
    
    hist_smpl = numpy.random.uniform(numpy.repeat(hist_bin, hist_freq),
                                     numpy.repeat(hist_bin, hist_freq))

    dfrm_wide_x = pandas.DataFrame(hist_smpl, columns = [data_nmL[idx]])
    #print(dfrm_wide_x)

    #---------------------------------------
    # Merge into final result
    #---------------------------------------
    idx += 1

    if (dfrm_hist.empty):
        dfrm_hist = dfrm_hist_x
        dfrm_wide = dfrm_wide_x
    else:
        dfrm_hist = pandas.concat([dfrm_hist, dfrm_hist_x], axis=1)
        dfrm_wide = pandas.concat([dfrm_wide, dfrm_wide_x], axis=1)
        #dfrm.join(dfrm_hist_x, on='dram_bw')

dfrm_hist.reset_index(inplace=True)

#-------------------------------------------------------
# Plot
#-------------------------------------------------------

# print(dfrm_hist)
# print(dfrm_wide)

fig, axes = pyplt.subplots(ncols=2, figsize=(15, 4))

axes = seaborn.violinplot(data=dfrm_wide, ax=axes[0], cut = 0,
                          palette='muted', scale = 'area', inner = 'box')


#seaborn.plt.show()
pyplt.show()


# clueweb12
# uk2014

