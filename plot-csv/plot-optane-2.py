#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

import io

import pandas
import numpy
import math

import matplotlib.pyplot as pyplt
import matplotlib

import seaborn

import VTuneCSV as vtcsv

#****************************************************************************

title_txt_sz = 13

#****************************************n***********************************
# Grappolo, Single phase: Run time
#****************************************************************************


#----------------------------------------------------------------------------
# Run time (seconds)
#----------------------------------------------------------------------------

# time:   non-vtune, phase 1 only (excludes I/O)
# vrunte: vtune, entire run for 1 phase (includes I/O)

#-------------------------------------------------------
# 
#-------------------------------------------------------

# OMP_PLACES="", OMP_BIND=""
time_str_grappolo = """
graph        threads  mode   time          vtune

friendster	16	dram	5179.797055	nan
friendster	32	dram	2916.220665	nan
friendster	64	dram	1852.977476	nan
friendster	128	dram	983.782397	nan
friendster	192	dram	671.325544	669.594645

friendster	16	mem	5321.611106	nan
friendster	32	mem	3018.635678	nan
friendster	64	mem	1915.380128	nan
friendster	128	mem	1013.17759	nan
friendster	192	mem	689.835591	698.334183

friendster     16     kdax  5233.698846     nan
friendster     32     kdax  2925.995246     nan
friendster     64     kdax  1856.734987     nan
friendster    128     kdax   983.422625     nan
friendster    192     kdax   672.260361    674.307471

friendster	16	pdax	5328.551361	nan
friendster	32	pdax	2973.819253	nan
friendster	64	pdax	1890.541188	nan
friendster	128	pdax	1013.603767	nan
friendster	192	pdax	692.835406	878.044


moliere2016	16	dram	2667.57845	nan
moliere2016	32	dram	1870.452818	nan
moliere2016	64	dram	948.033326	nan
moliere2016	128	dram	1042.713159	nan
moliere2016	192	dram	990.80665	1000.8756

moliere2016	16	mem	1494.40757	nan
moliere2016	32	mem	1104.05022	nan
moliere2016	64	mem	1024.47122	nan
moliere2016	128	mem	1044.46817	nan
moliere2016	192	mem	1070.68616	1104.891963

moliere2016    16     kdax   2647.777439   nan
moliere2016    32     kdax   1860.307772   nan
moliere2016    64     kdax   936.922047    nan
moliere2016   128     kdax   1040.909062   nan
moliere2016   192     kdax   984.90577    987.575947

moliere2016	16	pdax	2746.567095	nan
moliere2016	32	pdax	1923.814033	nan
moliere2016	64	pdax	937.912878	nan
moliere2016	128	pdax	1066.13159	nan
moliere2016	192	pdax	980.399573	1394.221


clueweb12     192     dram      nan            nan

clueweb12	16	mem	9008.786655	nan
clueweb12	32	mem	7427.020428	nan
clueweb12	64	mem	5637.144076	nan
clueweb12	128	mem	4822.885993	nan
clueweb12	192	mem	4334.598601	4391.67807

clueweb12      16     kdax    10812.81699      nan
clueweb12      32     kdax     7882.519231     nan
clueweb12      64     kdax     6170.163424     nan
clueweb12     128     kdax     5074.019396     nan
clueweb12     192     kdax     4968.696484     5667.603504

clueweb12     192     pdax      nan            nan


uk2014        192     dram      nan                 nan

uk2014	        16	mem	2195.747492	nan
uk2014	        32	mem	1439.80749	nan
uk2014	        64	mem	1040.564312	nan
uk2014	        128	mem	768.970483	nan
uk2014	        192	mem	646.377239	698.740065

uk2014         16     kdax     2241.499411     nan
uk2014         32     kdax     2175.004603     nan
uk2014         64     kdax      934.446303     nan
uk2014        128     kdax      701.715529     nan
uk2014        192     kdax      604.974474      877.898523

uk2014        192     pdax      nan            nan
"""


time_str_ripples = """
graph  threads  mode   time          vtune

slash	2	dram	257.15	nan
slash	4	dram	129.29	nan
slash	8	dram	70.18	nan
slash	16	dram	50.18	nan
slash	32	dram	55.45	nan
slash	64	dram	58.10	38.73088936
slash	128	dram	53.16	nan
slash	192	dram	37.73	32.029196

slash	2	mem	258.25	nan
slash	4	mem	129.35	nan
slash	8	mem	70.55	nan
slash	16	mem	50.89	nan
slash	32	mem	57.62	nan
slash	64	mem	59.48	nan
slash	128	mem	53.11	nan
slash	192	mem	35.44	nan

slash	2	kdax	nan	nan
slash	4	kdax	nan	nan
slash	8	kdax	nan	nan
slash	16	kdax	nan	nan
slash	32	kdax	64.10	nan
slash	64	kdax	66.03	nan
slash	128	kdax	nan	nan
slash	192	kdax	46.58	nan


twitter	2	dram	468.68	nan
twitter	4	dram	235.69	nan
twitter	8	dram	128.54	nan
twitter	16	dram	97.61	nan
twitter	32	dram	113.30	nan
twitter	64	dram	112.73	67.45700489
twitter	128	dram	107.22	nan
twitter	192	dram	48.93	41.52928663

twitter	2	mem	461.16	nan
twitter	4	mem	227.37	nan
twitter	8	mem	127.34	nan
twitter	16	mem	97.53	nan
twitter	32	mem	119.96	nan
twitter	64	mem	118.32	nan
twitter	128	mem	108.72	nan
twitter	192	mem	50.23	nan

twitter	2	kdax	nan	nan
twitter	4	kdax	nan	nan
twitter	8	kdax	nan	nan
twitter	16	kdax	nan	nan
twitter	32	kdax	141.27	nan
twitter	64	kdax	125.70	nan
twitter	128	kdax	nan	nan
twitter	192	kdax	71.81	nan


talk	2	dram	606.44	nan
talk	4	dram	330.05	nan
talk	8	dram	163.14	nan
talk	16	dram	102.31	nan
talk	32	dram	90.14	nan
talk	64	dram	80.37	62.49747313
talk	128	dram	70.36	nan
talk	192	dram	54.48	52.85052325

talk	2	mem	616.27	nan
talk	4	mem	331.22	nan
talk	8	mem	166.28	nan
talk	16	mem	103.41	nan
talk	32	mem	90.40	nan
talk	64	mem	83.60	nan
talk	128	mem	70.46	nan
talk	192	mem	53.20	nan

talk	2	kdax	nan	nan
talk	4	kdax	nan	nan
talk	8	kdax	nan	nan
talk	16	kdax	nan	nan
talk	32	kdax	101.20	nan
talk	64	kdax	101.98	nan
talk	128	kdax	nan	nan
talk	192	kdax	123.27	nan


pokec	2	dram	22531.59	nan
pokec	4	dram	10796.75	nan
pokec	8	dram	5316.46	nan
pokec	16	dram	2773.61	nan
pokec	32	dram	1509.24	nan
pokec	64	dram	809.45	926.5572327
pokec	128	dram	578.64	nan
pokec	192	dram	686.34	673.5958796

pokec	2	mem	23462.17	nan
pokec	4	mem	11286.53	nan
pokec	8	mem	5540.75	        nan
pokec	16	mem	2877.33	        nan
pokec	32	mem	1619.55	        nan
pokec	64	mem	939.25	        nan
pokec	128	mem	718.31	        nan
pokec	192	mem	771.15	        nan

pokec	2	kdax	nan	nan
pokec	4	kdax	nan	nan
pokec	8	kdax	nan	nan
pokec	16	kdax	nan	nan
pokec	32	kdax	2450.37	nan
pokec	64	kdax	1639.97	nan
pokec	128	kdax	nan	nan
pokec	192	kdax	1974.83	nan


topcats	2	dram	22531.59	nan
topcats	4	dram	10796.75	nan
topcats	8	dram	5316.46	nan
topcats	16	dram	2773.61	nan
topcats	32	dram	1509.24	nan
topcats	64	dram	809.45	nan
topcats	128	dram	578.64	nan
topcats	192	dram	686.34	nan

topcats	2	mem	23462.17	nan
topcats	4	mem	11286.53	nan
topcats	8	mem	5540.75	nan
topcats	16	mem	2877.33	nan
topcats	32	mem	1619.55	nan
topcats	64	mem	939.25	nan
topcats	128	mem	718.31	nan
topcats	192	mem	771.15	nan

topcats	2	kdax	nan	nan
topcats	4	kdax	nan	nan
topcats	8	kdax	nan	nan
topcats	16	kdax	nan	nan
topcats	32	kdax	2450.37	nan
topcats	64	kdax	1639.97	nan
topcats	128	kdax	nan	nan
topcats	192	kdax	1974.83	nan
"""

#-------------------------------------------------------
#
#-------------------------------------------------------

# OMP_PLACES=cores, OMP_BIND=true
#   moliere2016  time (dram,pdax,kdax) 1054.31008  1059.69578  1087.108672
#   moliere2016  vtune                 1160.216    1394.221    1066.978739

# orkut         192     dram   19.486751     21.864      
# orkut         192     pdax   19.201794     31.600      
# orkut         192     kdax   19.957072     20.055675   
# orkut         192     mem     nan           nan   


#****************************************************************************
# Grappolo, Single phase, 192 threads: DRAM bandwidth
#****************************************************************************


#----------------------------------------------------------------------------
# friendster, 192 threads, DRAM bandwidth (GB/s)
#----------------------------------------------------------------------------

friendster_t192_dramBw_dram_str = """
dram_bw time                   class
    0	81.76752655810002	Low
    10	107.71000000000002	Low
    20	47.09	Low
    30	94.27000000000002	Low
    40	699.2400000000001	Low
    50	8.36	Low
    60	15.919999999999993	Low
    70	13.090000000000002	Low
    80	2.9099999999999997	Low
    90	1.640000000000001	Low
    100	1.9300000000000013	Low
    110	1.350000000000001	Low
    120	1.2400000000000009	Low
    130	1.1400000000000006	Low
    140	1.0600000000000005	Medium
    150	0.8600000000000004	Medium
    160	0.5800000000000002	Medium
    170	0.3800000000000002	Medium
    180	0.3200000000000001	Medium
    190	0.27	Medium
    200	0.07	Medium
    210	0.03	Medium
    220	0.01	Medium
    230	0.01	Medium
    240	0	Medium
    250	0.01	Medium
    260	0	Medium
    270	0.05	Medium
    280	0.07	Medium
    290	0.01	Medium
    300	0.01	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0.01	High
    350	0.02	High
    360	0.07	High
    370	0.31000000000000005	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

#----------------------------------------

friendster_t192_dramBw_mem_str = """
dram_bw time                   class
    0	121.29940788809998	Low
    9	54.870000000000005	Low
    18	104.99000000000001	Low
    27	16.569999999999997	Low
    36	13.08	Low
    45	52.949999999999996	Low
    54	74.87	Low
    63	311.21999999999986	Low
    72	43.210000000000015	Low
    81	1.1400000000000006	Low
    90	1.0200000000000005	Low
    99	1.0000000000000007	Low
    108	0.8000000000000005	Low
    117	0.9200000000000005	Low
    126	0.7200000000000004	Low
    135	0.6500000000000005	Medium
    144	0.4700000000000002	Medium
    153	0.4800000000000002	Medium
    162	0.4700000000000002	Medium
    171	0.5600000000000003	Medium
    180	0.7300000000000004	Medium
    189	0.8400000000000005	Medium
    198	0.7100000000000004	Medium
    207	0.5100000000000002	Medium
    216	0.6100000000000003	Medium
    225	0.6500000000000004	Medium
    234	0.4800000000000002	Medium
    243	0.19000000000000003	Medium
    252	0.11	Medium
    261	0.07	Medium
    270	0	Medium
    279	0	Medium
    288	0.02	Medium
    297	0.08	Medium
    306	0	Medium
    315	0	High
    324	0	High
    333	0	High
    342	0	High
    351	0	High
    360	0	High
    369	0	High
    378	0	High
    387	0	High
    396	0	High
    405	0	High
    414	0	High
    423	0	High
    432	0	High
    441	0	High
"""

friendster_t192_pmemBw_mem_str = """
dram_bw time                   class
    0	405.0294078881001	Low
    3	393.7900000000001	Low
    6	1.1500000000000004	Low
    9	2.3700000000000006	Low
    12	0.3700000000000001	Low
    15	0.4	Low
    18	0.37000000000000005	Low
    21	0.15	Low
    24	0.3500000000000001	Low
    27	0.7200000000000002	Low
    30	0.14	Low
    33	0.42000000000000004	Low
    36	0.26	Medium
    39	0.02	Medium
    42	0.15	Medium
    45	0.3700000000000001	Medium
    48	0.23	Medium
    51	0	Medium
    54	0	Medium
    57	0	Medium
    60	0	Medium
    63	0	Medium
    66	0	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""

#----------------------------------------

friendster_t192_dramBw_pdax_str = """
dram_bw time                   class
    0	188.37429006909997	Low
    10	79.14	Low
    20	77.32	Low
    30	34.379999999999995	Low
    40	14.96	Low
    50	42.56	Low
    60	51.85	Low
    70	222.13000000000005	Low
    80	155.11000000000007	Low
    90	3.269999999999998	Low
    100	1.330000000000001	Low
    110	1.0300000000000007	Low
    120	0.7400000000000004	Low
    130	0.8800000000000006	Low
    140	0.8500000000000004	Medium
    150	0.7300000000000004	Medium
    160	0.7800000000000004	Medium
    170	0.6300000000000003	Medium
    180	0.5200000000000002	Medium
    190	0.5000000000000002	Medium
    200	0.31000000000000005	Medium
    210	0.20000000000000007	Medium
    220	0.13	Medium
    230	0.09999999999999999	Medium
    240	0.13	Medium
    250	0.07	Medium
    260	0.01	Medium
    270	0	Medium
    280	0.01	Medium
    290	0	Medium
    300	0	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0	High
    350	0	High
    360	0	High
    370	0	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

friendster_t192_pmemBw_pdax_str = """
dram_bw time                   class
    0	749.0242900691	Low
    3	39.95000000000001	Low
    6	3.75	Low
    9	80.78999999999999	Low
    12	4.529999999999999	Low
    15	0	Low
    18	0	Low
    21	0	Low
    24	0	Low
    27	0	Low
    30	0	Low
    33	0	Low
    36	0	Medium
    39	0	Medium
    42	0	Medium
    45	0	Medium
    48	0	Medium
    51	0	Medium
    54	0	Medium
    57	0	Medium
    60	0	Medium
    63	0	Medium
    66	0	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""

#----------------------------------------

friendster_t192_dramBw_kdax_str = """
dram_bw time                   class
    0	89.90187841810001	Low
    10	67.88999999999999	Low
    20	94.74	Low
    30	23.95	Low
    40	9.880000000000004	Low
    50	36.730000000000004	Low
    60	80.32000000000001	Low
    70	224.06999999999988	Low
    80	126.36999999999999	Low
    90	1.1800000000000006	Low
    100	0.7900000000000005	Low
    110	0.6200000000000003	Low
    120	0.6000000000000003	Low
    130	0.41000000000000014	Low
    140	0.4600000000000002	Medium
    150	0.5300000000000002	Medium
    160	0.5100000000000002	Medium
    170	0.41000000000000014	Medium
    180	0.5100000000000002	Medium
    190	0.5700000000000003	Medium
    200	0.4600000000000002	Medium
    210	0.6000000000000002	Medium
    220	0.5800000000000003	Medium
    230	0.6200000000000004	Medium
    240	0.5200000000000002	Medium
    250	0.3500000000000001	Medium
    260	0.21	Medium
    270	0.09	Medium
    280	0.05	Medium
    290	0	Medium
    300	0	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0	High
    350	0	High
    360	0	High
    370	0	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

friendster_t192_pmemBw_kdax_str = """
dram_bw time                   class
    0	722.9718784181	Low
    3	40.49	Low
    6	0.46	Low
    9	0	Low
    12	0	Low
    15	0	Low
    18	0	Low
    21	0	Low
    24	0	Low
    27	0	Low
    30	0	Low
    33	0	Low
    36	0	Medium
    39	0	Medium
    42	0	Medium
    45	0	Medium
    48	0	Medium
    51	0	Medium
    54	0	Medium
    57	0	Medium
    60	0	Medium
    63	0	Medium
    66	0	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""


#----------------------------------------------------------------------------
# moliere2016, 192 threads, DRAM bandwidth (GB/s)
#----------------------------------------------------------------------------

moliere2016_t192_dramBw_dram_str = """
dram_bw time                   class
    0	1078.2306883761	Low
    10	5.409999999999998	Low
    20	3.1999999999999984	Low
    30	7.459999999999997	Low
    40	7.300000000000002	Low
    50	5.839999999999999	Low
    60	3.809999999999999	Low
    70	10.16	Low
    80	28.150000000000006	Low
    90	4.389999999999999	Low
    100	6.029999999999999	Low
    110	8.48	Low
    120	15.879999999999994	Low
    130	26.719999999999995	Low
    140	0.6100000000000001	Medium
    150	0.02	Medium
    160	0	Medium
    170	0	Medium
    180	0	Medium
    190	0	Medium
    200	0	Medium
    210	0	Medium
    220	0	Medium
    230	0	Medium
    240	0	Medium
    250	0	Medium
    260	0	Medium
    270	0	Medium
    280	0	Medium
    290	0	Medium
    300	0	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0	High
    350	0	High
    360	0	High
    370	0	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

    # 0	1126.5503917521	Low
    # 10	4.3599999999999985	Low
    # 20	3.889999999999998	Low
    # 30	4.389999999999997	Low
    # 40	10.799999999999997	Low
    # 50	5.019999999999998	Low
    # 60	10.409999999999997	Low
    # 70	13.4	Low
    # 80	24.070000000000007	Low
    # 90	4.539999999999997	Low
    # 100	6.349999999999998	Low
    # 110	11.049999999999999	Low
    # 120	17.340000000000007	Low
    # 130	18.2	Low
    # 140	0.03	Medium
    # 150	0	Medium
    # 160	0	Medium
    # 170	0	Medium
    # 180	0	Medium
    # 190	0	Medium
    # 200	0	Medium
    # 210	0	Medium
    # 220	0	Medium
    # 230	0	Medium
    # 240	0	Medium
    # 250	0	Medium
    # 260	0	Medium
    # 270	0	Medium
    # 280	0	Medium
    # 290	0	Medium
    # 300	0	Medium
    # 310	0	Medium
    # 320	0	High
    # 330	0	High
    # 340	0	High
    # 350	0	High
    # 360	0	High
    # 370	0	High
    # 380	0	High
    # 390	0	High
    # 400	0	High
    # 410	0	High
    # 420	0	High
    # 430	0	High
    # 440	0	High
    # 450	0	High

    # FIXME: OLD
    # 0	938.6064413860997	Low
    # 10	69.86	Low
    # 20	4.079999999999998	Low
    # 30	13.249999999999991	Low
    # 40	3.169999999999999	Low
    # 50	6.859999999999997	Low
    # 60	28.129999999999992	Low
    # 70	24.34	Low
    # 80	2.6	Low
    # 90	11.539999999999997	Low
    # 100	10.550000000000002	Low
    # 110	42.650000000000006	Low
    # 120	1.2700000000000005	Low
    # 130	0.16999999999999998	Low
    # 140	0.37000000000000005	Medium
    # 150	0.03	Medium
    # 160	0.24999999999999997	Medium
    # 170	1.7300000000000009	Medium
    # 180	0.04	Medium
    # 190	0.03	Medium
    # 200	0.02	Medium
    # 210	0	Medium
    # 220	0.02	Medium
    # 230	0.02	Medium
    # 240	0.01	Medium
    # 250	0.5400000000000003	Medium
    # 260	0.08	Medium
    # 270	0	Medium
    # 280	0	Medium
    # 290	0	Medium
    # 300	0	Medium
    # 310	0	Medium
    # 320	0	High
    # 330	0	High
    # 340	0	High
    # 350	0	High
    # 360	0	High
    # 370	0	High
    # 380	0	High
    # 390	0	High
    # 400	0	High
    # 410	0	High
    # 420	0	High
    # 430	0	High
    # 440	0	High
    # 450	0	High


#----------------------------------------

moliere2016_t192_dramBw_mem_str = """
dram_bw time                   class
    0	1254.5813556320995	Low
    9	18.64	Low
    18	14.35	Low
    27	21.109999999999996	Low
    36	9.749999999999996	Low
    45	6.409999999999997	Low
    54	3.369999999999999	Low
    63	11.030000000000003	Low
    72	31.11	Low
    81	8.129999999999995	Low
    90	5.829999999999993	Low
    99	3.7199999999999975	Low
    108	49.00999999999999	Low
    117	2.239999999999999	Low
    126	0.16000000000000003	Low
    135	0.10999999999999999	Medium
    144	0.19	Medium
    153	0.07	Medium
    162	0.08	Medium
    171	0	Medium
    180	0	Medium
    189	0	Medium
    198	0	Medium
    207	0	Medium
    216	0	Medium
    225	0	Medium
    234	0	Medium
    243	0	Medium
    252	0	Medium
    261	0	Medium
    270	0	Medium
    279	0	Medium
    288	0	Medium
    297	0	Medium
    306	0	Medium
    315	0	High
    324	0	High
    333	0	High
    342	0	High
    351	0	High
    360	0	High
    369	0	High
    378	0	High
    387	0	High
    396	0	High
    405	0	High
    414	0	High
    423	0	High
    432	0	High
    441	0	High
"""

moliere2016_t192_pmemBw_mem_str = """
dram_bw time                   class
    0	1146.4513556320999	Low
    3	154.82000000000002	Low
    6	41.150000000000006	Low
    9	41.29	Low
    12	55.9	Low
    15	0.18000000000000005	Low
    18	0	Low
    21	0.02	Low
    24	0.02	Low
    27	0.03	Low
    30	0.03	Low
    33	0	Low
    36	0	Medium
    39	0	Medium
    42	0	Medium
    45	0	Medium
    48	0	Medium
    51	0	Medium
    54	0	Medium
    57	0	Medium
    60	0	Medium
    63	0	Medium
    66	0	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""

#----------------------------------------

moliere2016_t192_dramBw_pdax_str = """
dram_bw time                   class
    0	1180.4308701981	Low
    10	68.97999999999999	Low
    20	2.8699999999999988	Low
    30	15.319999999999991	Low
    40	2.799999999999998	Low
    50	5.859999999999999	Low
    60	13.760000000000003	Low
    70	28.129999999999995	Low
    80	11.149999999999997	Low
    90	9.749999999999998	Low
    100	11.029999999999992	Low
    110	40.069999999999986	Low
    120	3.469999999999998	Low
    130	0.20000000000000004	Low
    140	0.35000000000000003	Medium
    150	0.02	Medium
    160	0.01	Medium
    170	0.01	Medium
    180	0	Medium
    190	0.01	Medium
    200	0	Medium
    210	0	Medium
    220	0	Medium
    230	0	Medium
    240	0	Medium
    250	0	Medium
    260	0	Medium
    270	0	Medium
    280	0	Medium
    290	0	Medium
    300	0	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0	High
    350	0	High
    360	0	High
    370	0	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

moliere2016_t192_pmemBw_pdax_str = """
dram_bw time                   class
    0	1145.7608701980998	Low
    3	98.57000000000002	Low
    6	5.019999999999997	Low
    9	137.79	Low
    12	7.08	Low
    15	0	Low
    18	0	Low
    21	0	Low
    24	0	Low
    27	0	Low
    30	0	Low
    33	0	Low
    36	0	Medium
    39	0	Medium
    42	0	Medium
    45	0	Medium
    48	0	Medium
    51	0	Medium
    54	0	Medium
    57	0	Medium
    60	0	Medium
    63	0	Medium
    66	0	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""

#----------------------------------------

moliere2016_t192_dramBw_kdax_str = """
dram_bw time                   class
    0	1148.9517153501001	Low
    10	43.74999999999999	Low
    20	6.879999999999998	Low
    30	5.009999999999998	Low
    40	9.439999999999998	Low
    50	4.149999999999998	Low
    60	9.63999999999999	Low
    70	13.809999999999993	Low
    80	22.560000000000006	Low
    90	5.039999999999997	Low
    100	6.139999999999995	Low
    110	11.159999999999995	Low
    120	17.5	Low
    130	18.18	Low
    140	0.03	Medium
    150	0	Medium
    160	0	Medium
    170	0	Medium
    180	0	Medium
    190	0	Medium
    200	0	Medium
    210	0	Medium
    220	0	Medium
    230	0	Medium
    240	0	Medium
    250	0	Medium
    260	0	Medium
    270	0	Medium
    280	0	Medium
    290	0	Medium
    300	0	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0	High
    350	0	High
    360	0	High
    370	0	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

moliere2016_t192_pmemBw_kdax_str = """
dram_bw time                   class
    0	1001.0617153501	Low
    3	281.96000000000004	Low
    6	37.5	Low
    9	0.04	Low
    12	0.7000000000000001	Low
    15	0.7900000000000003	Low
    18	0.19	Low
    21	0	Low
    24	0	Low
    27	0	Low
    30	0	Low
    33	0	Low
    36	0	Medium
    39	0	Medium
    42	0	Medium
    45	0	Medium
    48	0	Medium
    51	0	Medium
    54	0	Medium
    57	0	Medium
    60	0	Medium
    63	0	Medium
    66	0	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""


#----------------------------------------------------------------------------
# clueweb12, 192 threads, DRAM + PMEM bandwidth (GB/s)
#----------------------------------------------------------------------------

clueweb12_t192_dramBw_pdax_str = """
dram_bw time                   class
"""

#----------------------------------------

clueweb12_t192_dramBw_mem_str = """
dram_bw time                   class
    0	10693.952181253599	Low
    9	1442.6062797837003	Low
    18	288.3013359865	Low
    27	539.9722519298999	Low
    36	199.23374803930002	Low
    45	51.612468015699996	Low
    54	31.7509457034	Low
    63	38.8983447362	Low
    72	48.58856842489999	Low
    81	44.19016902009997	Low
    90	48.10749348999998	Low
    99	55.11744254140001	Low
    108	86.79966325410003	Low
    117	44.671243955000016	Low
    126	67.69411583950001	Low
    135	63.15826645330002	Medium
    144	0.20617497210000002	Medium
    153	0.0687249907	Medium
    162	0	Medium
    171	0.0687249907	Medium
    180	0	Medium
    189	0	Medium
    198	0	Medium
    207	0	Medium
    216	0	Medium
    225	0	Medium
    234	0	Medium
    243	0	Medium
    252	0	Medium
    261	0	Medium
    270	0	Medium
    279	0	Medium
    288	0	Medium
    297	0	Medium
    306	0	Medium
    315	0	High
    324	0	High
    333	0	High
    342	0	High
    351	0	High
    360	0	High
    369	0	High
    378	0	High
    387	0	High
    396	0	High
    405	0	High
    414	0	High
    423	0	High
    432	0	High
"""

clueweb12_t192_pmemBw_mem_str = """
dram_bw time                   class
    0	10822.9489887975	Low
    3	1541.0204664661003	Low
    6	146.5216801724	Low
    9	101.71298623599999	Low
    12	71.7488902908	Low
    15	297.71665971240003	Low
    18	275.3123127442	Low
    21	51.887367978499995	Low
    24	50.512868164500006	Low
    27	29.757920973099992	Low
    30	41.0288194479	Low
    33	26.321671438100005	Low
    36	32.0258456662	Medium
    39	18.005947563400003	Medium
    42	63.982966341700006	Medium
    45	36.0806201175	Medium
    48	9.7589486794	Medium
    51	37.45511993150001	Medium
    54	88.65523800299998	Medium
    57	1.9242997396000003	Medium
    60	0.2748999628	Medium
    63	0.3436249535	Medium
    66	0	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""

#----------------------------------------

clueweb12_t192_dramBw_kdax_str = """
dram_bw time                   class
    0	16658.9138215661	Low
    10	901.2163233950002	Low
    20	29.63890904500001	Low
    30	0.087949285	Low
    40	0	Low
    50	0	Low
    60	0	Low
    70	0	Low
    80	0	Low
    90	0	Low
    100	0	Low
    110	0	Low
    120	0	Low
    130	0	Low
    140	0	Medium
    150	0	Medium
    160	0	Medium
    170	0	Medium
    180	0	Medium
    190	0	Medium
    200	0	Medium
    210	0	Medium
    220	0	Medium
    230	0	Medium
    240	0	Medium
    250	0	Medium
    260	0	Medium
    270	0	Medium
    280	0	Medium
    290	0	Medium
    300	0	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0	High
    350	0	High
    360	0	High
    370	0	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

clueweb12_t192_pmemBw_kdax_str = """
dram_bw time                   class
    0	11744.0439279111	Low
    3	3556.757034685	Low
    6	567.360837535	Low
    9	315.474085295	Low
    12	221.36835034499998	Low
    15	180.91167924499996	Low
    18	180.12013568	Low
    21	76.51587795	Low
    24	46.96491818999999	Low
    27	68.160695875	Low
    30	64.02707948000001	Low
    33	57.51883239	Low
    36	50.48288959	Medium
    39	62.883738775	Medium
    42	54.70445527	Medium
    45	65.346318755	Medium
    48	67.10530445500001	Medium
    51	62.883738775000005	Medium
    54	87.86133571500001	Medium
    57	59.013970234999995	Medium
    60	0.087949285	Medium
    63	0	Medium
    66	0	Medium
    69	0.087949285	Medium
    72	0.17589857	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""


#----------------------------------------------------------------------------
# uk2014, 192 threads, DRAM bandwidth (GB/s)
#----------------------------------------------------------------------------

uk2014_t192_dramBw_pdax_str = """
dram_bw time                   class
"""

#----------------------------------------

uk2014_t192_dramBw_mem_str = """
dram_bw time                   class
    0	11561.841387734903	Low
    9	72.2230746768	Low
    18	245.12668551989995	Low
    27	520.0192215633001	Low
    36	123.05398864769997	Low
    45	32.8405647534	Low
    54	90.3442627977	Low
    63	87.59664582629999	Low
    72	43.634774283899986	Low
    81	16.681960183500006	Low
    90	32.90598420509999	Low
    99	14.850215535900007	Low
    108	10.728790078800007	Low
    117	11.31756514410001	Low
    126	106.04493120569998	Low
    135	111.14764843830001	Medium
    144	0.32709725850000004	Medium
    153	0.5233556136	Medium
    162	0.4579361619000001	Medium
    171	1.2429695823	Medium
    180	0.32709725850000004	Medium
    189	0.0654194517	Medium
    198	0.2616778068	Medium
    207	0.32709725850000004	Medium
    216	0	Medium
    225	0	Medium
    234	0	Medium
    243	0	Medium
    252	0	Medium
    261	0	Medium
    270	0	Medium
    279	0	Medium
    288	0	Medium
    297	0	Medium
    306	0	High
    315	0	High
    324	0	High
    333	0	High
    342	0	High
    351	0	High
    360	0	High
    369	0	High
    378	0	High
    387	0	High
    396	0	High
    405	0	High
    414	0	High
    423	0	High
"""

uk2014_t192_pmemBw_mem_str = """
dram_bw time                   class
    0	10898.3573085935	Low
    3	732.3707617815	Low
    6	40.62547950570001	Low
    9	102.3160224588	Low
    12	203.51991423869993	Low
    15	396.8343940122	Low
    18	178.92220039949999	Low
    21	109.25048433900001	Low
    24	44.1581298975	Low
    27	49.84962219540001	Low
    30	11.1867262407	Low
    33	10.7942095305	Low
    36	9.420401044800002	Medium
    39	11.121306789	Medium
    42	20.8033856406	Medium
    45	16.420282376700005	Medium
    48	9.747498303300002	Medium
    51	6.541945170000002	Medium
    54	7.4578174937999995	Medium
    57	9.0278843346	Medium
    60	32.186370236399995	Medium
    63	151.96938629910005	Medium
    66	31.008820105799998	Medium
    69	0	Medium
    72	0	Medium
    75	0	Medium
    78	0	Medium
    81	0	Medium
    84	0	High
    87	0	High
    90	0	High
    93	0	High
    96	0	High
    99	0	High
    102	0	High
    105	0	High
    108	0	High
    111	0	High
    114	0	High
    117	0	High
    120	0	High
"""

#----------------------------------------

uk2014_t192_dramBw_kdax_str = """
dram_bw time                   class
    0	12966.7667265124	Low
    10	632.6295530447998	Low
    20	124.00036069169998	Low
    30	65.76090358329999	Low
    40	11.6616922409	Low
    50	0	Low
    60	0	Low
    70	0	Low
    80	0	Low
    90	0	Low
    100	0	Low
    110	0	Low
    120	0	Low
    130	0	Low
    140	0	Medium
    150	0	Medium
    160	0	Medium
    170	0	Medium
    180	0	Medium
    190	0	Medium
    200	0	Medium
    210	0	Medium
    220	0	Medium
    230	0	Medium
    240	0	Medium
    250	0	Medium
    260	0	Medium
    270	0	Medium
    280	0	Medium
    290	0	Medium
    300	0	Medium
    310	0	Medium
    320	0	High
    330	0	High
    340	0	High
    350	0	High
    360	0	High
    370	0	High
    380	0	High
    390	0	High
    400	0	High
    410	0	High
    420	0	High
    430	0	High
    440	0	High
    450	0	High
"""

uk2014_t192_pmemBw_kdax_str = """
dram_bw time                   class
    0	10649.609179474399	Low
    3	1702.9520876519	Low
    6	297.4766582870999	Low
    9	247.65570090290007	Low
    12	224.26331232500004	Low
    15	80.734792437	Low
    18	67.0719814092	Low
    21	121.24019684769999	Low
    24	73.48936234649996	Low
    27	35.39910129929999	Low
    30	50.9250229218	Low
    33	36.365158644699996	Low
    36	6.555389129500001	Medium
    39	4.0022375738000004	Medium
    42	3.933233477700001	Medium
    45	13.2487864512	Medium
    48	8.418499724199998	Medium
    51	4.0022375738000004	Medium
    54	4.2782539582000005	Medium
    57	4.416262150400001	Medium
    60	3.1051843245000006	Medium
    63	2.4841474596000004	Medium
    66	2.6221556518000004	Medium
    69	4.1402457660000005	Medium
    72	8.073479243699998	Medium
    75	8.6255120125	Medium
    78	9.798581646199999	Medium
    81	9.108540685199998	Medium
    84	13.386794643399995	High
    87	14.766876565399999	High
    90	6.210368648999999	High
    93	3.2431925167000006	High
    96	2.3461392674000003	High
    99	2.0011187869000002	High
    102	8.4184997242	High
    105	20.011187869	High
    108	34.08802347340001	High
    111	12.351733201899998	High
    114	0	High
    117	0	High
    120	0	High
"""


#----------------------------------------------------------------------------
# XXX, 192 threads, DRAM bandwidth (GB/s)
#----------------------------------------------------------------------------

XXX_t192_dramBw_dram_str = """
dram_bw time                   class
"""

XXX_t192_dramBw_pdax_str = """
dram_bw time                   class
"""

XXX_t192_dramBw_kdax_str = """
dram_bw time                   class
"""

XXX_t192_dramBw_mem_str = """
dram_bw time                   class
"""


#****************************************************************************
# Grappolo, Single phase, 192 threads: Load Latency
#****************************************************************************

#----------------------------------------------------------------------------
# friendster, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

friendster_t192_latency_dram_str = """
    Latency	Loads
    6	32570268150
    7	393529223360
    8	36692404420
    9	19164747700
    11	63719110
    12	3102630510
    13	1230268970
    14	1906671830
    15	4278983310
    16	7357106470
    17	1333199840
    18	754826380
    19	455836710
    20	696008740
    21	416624950
    22	499949940
    23	857757250
    24	779333730
    25	607782280
    26	294088200
    27	210763210
    28	259777910
    29	181354390
    30	132339690
    31	147044100
    32	127438220
    33	107832340
    34	68620580
    35	83324990
    36	39211760
    37	68620580
    38	63719110
    39	39211760
    40	29408820
    41	68620580
    42	49014700
    43	63719110
    44	24507350
    45	58817640
    46	14704410
    47	24507350
    48	39211760
    49	24507350
    50	53916170
    51	58817640
    52	24507350
    53	29408820
    54	39211760
    55	29408820
    56	24507350
    57	14704410
    58	34310290
    59	49014700
    60	34310290
    61	24507350
    62	39211760
    63	19605880
    64	39211760
    65	44113230
    66	34310290
    67	34310290
    68	53916170
    69	49014700
    70	39211760
    71	49014700
    72	29408820
    73	49014700
    74	39211760
    75	24507350
    76	29408820
    77	49014700
    78	19605880
    79	19605880
    80	34310290
    81	73522050
    82	34310290
    83	19605880
    84	24507350
    85	39211760
    86	44113230
    87	29408820
    88	14704410
    89	44113230
    90	49014700
    91	49014700
    92	24507350
    93	39211760
    94	24507350
    95	39211760
    96	39211760
    97	24507350
    98	44113230
    99	34310290
    100	19605880
    101	68620580
    102	19605880
    103	39211760
    104	14704410
    105	14704410
    106	58817640
    107	14704410
    108	19605880
    109	4901470
    110	34310290
    111	39211760
    112	53916170
    113	14704410
    114	29408820
    115	9802940
    116	39211760
    117	19605880
    118	19605880
    119	19605880
    120	14704410
    121	24507350
    122	19605880
    123	29408820
    124	9802940
    125	14704410
    126	14704410
    127	9802940
    128	9802940
    129	19605880
    130	9802940
    131	14704410
    132	19605880
    133	9802940
    134	9802940
    135	34310290
    136	9802940
    137	9802940
    138	9802940
    139	4901470
    140	19605880
    141	19605880
    142	9802940
    143	9802940
    145	4901470
    146	4901470
    147	4901470
    148	9802940
    149	4901470
    150	9802940
    151	14704410
    152	19605880
    155	9802940
    156	4901470
    158	4901470
    159	9802940
    161	4901470
    162	4901470
    163	9802940
    164	9802940
    165	9802940
    167	14704410
    168	4901470
    169	4901470
    170	14704410
    171	4901470
    172	9802940
    173	4901470
    174	4901470
    175	4901470
    178	4901470
    180	4901470
    181	9802940
    183	4901470
    184	14704410
    185	9802940
    188	4901470
    189	4901470
    190	4901470
    191	4901470
    192	4901470
    195	4901470
    198	9802940
    199	9802940
    205	4901470
    207	4901470
    209	4901470
    210	4901470
    212	4901470
    213	4901470
    214	4901470
    217	4901470
    218	4901470
    219	19605880
    223	9802940
    225	14704410
    227	4901470
    230	4901470
    232	9802940
    234	19605880
    235	24507350
    236	4901470
    237	19605880
    238	4901470
    239	4901470
    240	4901470
    241	19605880
    242	14704410
    243	9802940
    244	19605880
    245	9802940
    246	9802940
    247	9802940
    248	9802940
    249	4901470
    251	9802940
    252	14704410
    253	4901470
    254	4901470
    255	9802940
    256	9802940
    257	9802940
    258	4901470
    260	4901470
    261	9802940
    262	19605880
    263	9802940
    264	9802940
    265	19605880
    266	4901470
    268	14704410
    269	29408820
    270	4901470
    272	19605880
    273	19605880
    274	9802940
    275	29408820
    276	9802940
    278	19605880
    279	19605880
    280	4901470
    281	14704410
    282	24507350
    283	29408820
    284	39211760
    285	4901470
    286	14704410
    287	14704410
    288	14704410
    289	24507350
    290	9802940
    291	4901470
    292	24507350
    293	4901470
    294	14704410
    295	24507350
    296	19605880
    297	29408820
    298	9802940
    300	4901470
    301	4901470
    302	19605880
    303	14704410
    304	19605880
    305	14704410
    307	9802940
    308	4901470
    309	4901470
    310	4901470
    311	9802940
    312	14704410
    313	14704410
    314	14704410
    315	4901470
    317	14704410
    318	4901470
    320	14704410
    322	4901470
    325	4901470
    326	9802940
    330	4901470
    331	4901470
    332	9802940
    333	19605880
    334	9802940
    335	4901470
    336	9802940
    337	4901470
    338	19605880
    339	4901470
    340	9802940
    342	9802940
    343	14704410
    345	4901470
    346	4901470
    347	4901470
    348	4901470
    352	14704410
    353	4901470
    355	4901470
    356	14704410
    357	9802940
    358	4901470
    362	4901470
    364	4901470
    365	9802940
    366	14704410
    367	9802940
    369	9802940
    371	9802940
    374	4901470
    375	4901470
    376	4901470
    378	4901470
    379	4901470
    381	9802940
    383	4901470
    384	9802940
    386	9802940
    390	4901470
    391	9802940
    392	4901470
    393	4901470
    394	9802940
    396	4901470
    397	4901470
    398	4901470
    399	9802940
    401	9802940
    402	9802940
    403	9802940
    405	9802940
    407	14704410
    408	9802940
    409	9802940
    411	19605880
    412	19605880
    413	9802940
    415	4901470
    416	24507350
    417	19605880
    418	14704410
    419	19605880
    420	9802940
    421	4901470
    422	9802940
    423	14704410
    424	24507350
    425	14704410
    426	14704410
    427	19605880
    428	19605880
    429	4901470
    430	14704410
    431	14704410
    432	24507350
    433	14704410
    434	39211760
    435	14704410
    436	9802940
    437	14704410
    438	29408820
    439	24507350
    440	14704410
    441	19605880
    442	9802940
    443	14704410
    444	24507350
    445	14704410
    446	19605880
    447	14704410
    448	19605880
    449	19605880
    450	29408820
    451	34310290
    452	29408820
    453	19605880
    454	24507350
    455	19605880
    456	34310290
    457	34310290
    458	29408820
    459	19605880
    460	39211760
    461	19605880
    462	24507350
    463	24507350
    464	14704410
    465	19605880
    466	24507350
    467	39211760
    468	19605880
    469	19605880
    470	24507350
    471	29408820
    472	34310290
    473	24507350
    474	29408820
    475	24507350
    476	24507350
    477	39211760
    478	14704410
    479	9802940
    480	29408820
    481	9802940
    482	19605880
    483	19605880
    484	24507350
    485	24507350
    486	24507350
    487	39211760
    488	29408820
    489	19605880
    490	29408820
    491	29408820
    492	14704410
    493	24507350
    494	14704410
    495	14704410
    496	24507350
    497	34310290
    499	14704410
    500	19605880
    501	19605880
    502	9802940
    503	14704410
    504	24507350
    505	24507350
    506	19605880
    507	14704410
    508	19605880
    509	24507350
    510	24507350
    511	4901470
    512	29408820
    513	14704410
    514	9802940
    515	19605880
    517	34310290
    518	9802940
    519	14704410
    520	9802940
    521	19605880
    522	24507350
    523	24507350
    524	14704410
    525	19605880
    526	9802940
    527	9802940
    528	9802940
    529	19605880
    530	9802940
    531	4901470
    532	44113230
    533	9802940
    534	29408820
    535	14704410
    536	14704410
    537	9802940
    538	9802940
    539	4901470
    540	9802940
    541	4901470
    542	9802940
    544	14704410
    545	4901470
    546	9802940
    547	14704410
    548	14704410
    549	9802940
    550	4901470
    552	9802940
    554	4901470
    555	9802940
    556	4901470
    557	4901470
    559	9802940
    560	9802940
    563	4901470
    564	9802940
    565	4901470
    566	4901470
    568	24507350
    569	9802940
    570	4901470
    571	4901470
    576	4901470
    577	4901470
    578	9802940
    580	9802940
    581	4901470
    582	4901470
    584	4901470
    586	4901470
    587	14704410
    588	4901470
    594	9802940
    595	9802940
    596	4901470
    597	19605880
    598	9802940
    600	9802940
    602	4901470
    604	4901470
    606	9802940
    607	4901470
    609	4901470
    610	9802940
    612	9802940
    613	19605880
    614	14704410
    615	4901470
    616	4901470
    618	4901470
    619	4901470
    621	9802940
    626	4901470
    627	4901470
    632	4901470
    633	4901470
    635	4901470
    638	4901470
    641	19605880
    643	4901470
    644	9802940
    645	4901470
    646	4901470
    649	14704410
    652	4901470
    653	19605880
    656	9802940
    657	4901470
    658	4901470
    659	4901470
    660	9802940
    661	4901470
    663	4901470
    667	4901470
    668	9802940
    669	4901470
    672	4901470
    673	4901470
    675	4901470
    678	4901470
    680	4901470
    681	9802940
    682	14704410
    684	4901470
    685	14704410
    686	4901470
    688	4901470
    689	4901470
    691	4901470
    692	4901470
    693	4901470
    697	4901470
    699	9802940
    704	4901470
    705	4901470
    706	4901470
    707	4901470
    710	4901470
    713	9802940
    715	4901470
    719	9802940
    720	4901470
    722	4901470
    724	4901470
    731	9802940
    738	4901470
    740	4901470
    748	4901470
    752	4901470
    754	4901470
    759	4901470
    762	14704410
    766	4901470
    769	9802940
    774	4901470
    775	4901470
    785	4901470
    789	14704410
    790	4901470
    793	9802940
    795	9802940
    796	4901470
    799	4901470
    803	4901470
    804	4901470
    808	4901470
    811	4901470
    814	4901470
    816	4901470
    821	4901470
    822	4901470
    824	4901470
    825	4901470
    827	4901470
    831	9802940
    839	4901470
    840	4901470
    845	9802940
    849	4901470
    853	4901470
    859	4901470
    860	4901470
    866	4901470
    867	4901470
    868	4901470
    869	4901470
    870	4901470
    872	4901470
    874	4901470
    875	4901470
    885	4901470
    889	4901470
    891	4901470
    892	4901470
    897	4901470
    898	4901470
    901	9802940
    906	4901470
    910	4901470
    915	9802940
    923	9802940
    925	9802940
    926	4901470
    927	4901470
    928	4901470
    931	9802940
    932	4901470
    933	9802940
    936	4901470
    938	4901470
    939	4901470
    943	4901470
    944	4901470
    946	9802940
    947	4901470
    950	9802940
    954	4901470
    955	9802940
    956	4901470
    957	9802940
    962	4901470
    963	4901470
    967	4901470
    970	9802940
    971	4901470
    973	4901470
    975	9802940
    976	9802940
    978	9802940
    979	4901470
    980	4901470
    981	4901470
    982	4901470
    983	9802940
    984	9802940
    986	14704410
    987	9802940
    988	9802940
    989	9802940
    990	4901470
    991	4901470
    992	4901470
    993	4901470
    994	4901470
    995	4901470
    996	4901470
    997	4901470
    1007	4901470
    1009	4901470
    1011	14704410
    1014	4901470
    1015	4901470
    1018	9802940
    1019	4901470
    1020	9802940
    1024	4901470
    1026	4901470
    1028	4901470
    1029	4901470
    1030	4901470
    1038	4901470
    1039	4901470
    1040	4901470
    1044	14704410
    1045	4901470
    1048	9802940
    1049	4901470
    1051	9802940
    1052	4901470
    1054	4901470
    1056	4901470
    1059	9802940
    1061	4901470
    1062	9802940
    1065	14704410
    1066	4901470
    1068	4901470
    1071	4901470
    1075	4901470
    1079	4901470
    1080	4901470
    1081	4901470
    1083	9802940
    1084	4901470
    1085	4901470
    1086	4901470
    1087	9802940
    1088	4901470
    1093	4901470
    1096	4901470
    1098	4901470
    1101	4901470
    1103	4901470
    1118	4901470
    1122	9802940
    1124	4901470
    1125	14704410
    1130	4901470
    1131	4901470
    1133	4901470
    1138	4901470
    1141	4901470
    1154	4901470
    1157	4901470
    1160	4901470
    1166	4901470
    1167	9802940
    1177	4901470
    1179	4901470
    1191	4901470
    1194	4901470
    1199	4901470
    1206	4901470
    1240	4901470
    1245	9802940
    1250	4901470
    1261	4901470
    1271	4901470
    1278	9802940
    1282	4901470
    1287	4901470
    1301	4901470
    1333	4901470
    1338	4901470
    1353	4901470
    1358	4901470
    1364	4901470
    1366	4901470
    1381	4901470
    1399	4901470
    1402	4901470
    1423	4901470
    1432	4901470
    1436	4901470
    1467	9802940
    1494	4901470
    1496	4901470
    1511	4901470
    1533	4901470
    1541	4901470
    1544	4901470
    1557	4901470
    1564	4901470
    1568	4901470
    1573	4901470
    1585	4901470
    1596	4901470
    1606	4901470
    1620	4901470
    1641	4901470
    1692	4901470
    1701	4901470
    1716	4901470
    1718	4901470
    1720	4901470
    1731	4901470
    1735	4901470
    1762	4901470
    1804	4901470
    1810	4901470
    1826	4901470
    1861	4901470
    1892	4901470
    1973	4901470
    1976	4901470
    2020	4901470
    2111	4901470
    2170	4901470
    2199	4901470
    2365	4901470
    2718	4901470
    3153	4901470
    3324	4901470
"""

friendster_t192_latency_pdax_str = """
    Latency	Loads
    6	31879160880
    7	364812210840
    8	33526054800
    9	15258976320
    11	16805040
    12	2907271920
    13	646994040
    14	3638291160
    15	2092227480
    16	2109032520
    17	852855780
    18	575572620
    19	508352460
    20	340302060
    21	508352460
    22	294088200
    23	277283160
    24	176452920
    25	256276860
    26	138641580
    27	126037800
    28	159647880
    29	109232760
    30	130239060
    31	109232760
    32	151245360
    33	117635280
    34	88226460
    35	92427720
    36	96628980
    37	92427720
    38	151245360
    39	134440320
    40	58817640
    41	138641580
    42	163849140
    43	159647880
    44	105031500
    45	92427720
    46	63018900
    47	75622680
    48	54616380
    49	37811340
    50	54616380
    51	67220160
    52	46213860
    53	33610080
    54	33610080
    55	42012600
    56	37811340
    57	33610080
    58	25207560
    59	50415120
    60	50415120
    61	71421420
    62	46213860
    63	42012600
    64	58817640
    65	54616380
    66	63018900
    67	71421420
    68	109232760
    69	159647880
    70	210063000
    71	117635280
    72	109232760
    73	50415120
    74	50415120
    75	67220160
    76	37811340
    77	58817640
    78	29408820
    79	46213860
    80	58817640
    81	21006300
    82	25207560
    83	42012600
    84	29408820
    85	21006300
    86	33610080
    87	25207560
    88	21006300
    89	25207560
    90	21006300
    91	21006300
    92	16805040
    93	8402520
    94	16805040
    95	21006300
    96	12603780
    97	25207560
    98	33610080
    99	29408820
    100	25207560
    101	4201260
    102	21006300
    103	16805040
    104	21006300
    105	4201260
    106	8402520
    107	25207560
    108	12603780
    109	16805040
    110	25207560
    111	21006300
    112	25207560
    113	8402520
    114	12603780
    115	8402520
    116	16805040
    117	29408820
    118	8402520
    119	16805040
    120	8402520
    121	4201260
    122	16805040
    123	16805040
    124	16805040
    125	25207560
    126	12603780
    127	8402520
    128	12603780
    129	12603780
    130	4201260
    131	16805040
    132	16805040
    133	16805040
    134	25207560
    135	16805040
    136	8402520
    137	8402520
    138	21006300
    139	8402520
    140	12603780
    142	4201260
    143	21006300
    144	21006300
    145	12603780
    146	21006300
    147	12603780
    148	16805040
    149	16805040
    150	8402520
    151	16805040
    152	25207560
    153	4201260
    154	12603780
    155	16805040
    156	21006300
    157	12603780
    158	21006300
    159	4201260
    161	16805040
    162	16805040
    163	4201260
    164	8402520
    165	12603780
    166	21006300
    167	12603780
    168	21006300
    169	4201260
    170	25207560
    171	21006300
    172	12603780
    173	12603780
    174	21006300
    175	21006300
    176	16805040
    177	16805040
    178	21006300
    179	33610080
    180	29408820
    181	16805040
    182	25207560
    183	4201260
    184	21006300
    185	16805040
    186	21006300
    187	8402520
    188	25207560
    189	16805040
    190	16805040
    191	8402520
    192	21006300
    193	16805040
    194	16805040
    195	12603780
    196	8402520
    197	12603780
    198	16805040
    199	12603780
    200	8402520
    201	4201260
    202	21006300
    203	16805040
    204	21006300
    205	21006300
    206	25207560
    207	4201260
    208	21006300
    209	12603780
    210	4201260
    211	12603780
    212	25207560
    213	12603780
    214	4201260
    215	4201260
    216	12603780
    217	8402520
    218	16805040
    219	8402520
    220	21006300
    221	4201260
    222	4201260
    223	4201260
    224	4201260
    225	16805040
    226	4201260
    227	4201260
    228	8402520
    229	12603780
    230	8402520
    231	8402520
    232	4201260
    233	12603780
    234	25207560
    235	16805040
    237	8402520
    238	16805040
    239	4201260
    240	29408820
    241	4201260
    242	16805040
    244	16805040
    245	8402520
    246	21006300
    247	12603780
    248	4201260
    249	16805040
    250	25207560
    251	16805040
    252	25207560
    253	21006300
    254	21006300
    255	16805040
    256	21006300
    257	21006300
    258	4201260
    259	25207560
    260	12603780
    261	16805040
    262	16805040
    263	21006300
    264	33610080
    265	29408820
    266	8402520
    267	25207560
    268	16805040
    269	21006300
    270	16805040
    271	8402520
    272	16805040
    273	8402520
    274	12603780
    275	21006300
    276	12603780
    277	12603780
    278	16805040
    279	16805040
    280	25207560
    281	8402520
    282	29408820
    283	12603780
    284	16805040
    285	21006300
    286	16805040
    287	16805040
    288	29408820
    289	21006300
    290	25207560
    291	16805040
    292	16805040
    293	29408820
    294	12603780
    295	12603780
    296	25207560
    297	37811340
    298	21006300
    299	12603780
    300	12603780
    301	8402520
    302	4201260
    303	12603780
    304	16805040
    305	12603780
    306	8402520
    307	16805040
    308	12603780
    309	4201260
    310	12603780
    311	8402520
    312	8402520
    313	8402520
    314	12603780
    315	4201260
    316	4201260
    318	21006300
    319	16805040
    320	8402520
    321	4201260
    322	4201260
    324	4201260
    325	21006300
    327	12603780
    329	4201260
    330	4201260
    331	12603780
    332	4201260
    333	4201260
    334	8402520
    335	12603780
    337	8402520
    338	8402520
    339	4201260
    340	4201260
    342	4201260
    348	8402520
    350	8402520
    351	12603780
    352	8402520
    353	4201260
    354	4201260
    355	4201260
    359	4201260
    364	8402520
    365	4201260
    366	8402520
    367	4201260
    368	4201260
    370	4201260
    371	4201260
    372	12603780
    373	12603780
    374	4201260
    377	4201260
    378	4201260
    379	8402520
    380	4201260
    381	8402520
    382	8402520
    383	8402520
    384	8402520
    385	4201260
    386	8402520
    389	4201260
    390	12603780
    391	8402520
    392	8402520
    393	4201260
    394	4201260
    396	12603780
    400	12603780
    403	4201260
    405	8402520
    406	8402520
    407	4201260
    408	12603780
    410	4201260
    411	4201260
    413	8402520
    414	16805040
    415	4201260
    416	12603780
    417	16805040
    418	8402520
    419	4201260
    421	25207560
    422	12603780
    423	16805040
    424	21006300
    425	21006300
    426	8402520
    427	12603780
    428	16805040
    430	12603780
    431	12603780
    432	33610080
    433	8402520
    434	25207560
    435	16805040
    436	21006300
    437	25207560
    438	29408820
    439	8402520
    440	16805040
    441	16805040
    442	21006300
    443	16805040
    444	29408820
    445	16805040
    446	16805040
    447	12603780
    448	25207560
    449	25207560
    450	29408820
    451	12603780
    452	33610080
    453	21006300
    454	16805040
    455	21006300
    456	29408820
    457	16805040
    458	46213860
    459	21006300
    460	8402520
    461	4201260
    462	33610080
    463	25207560
    464	21006300
    465	25207560
    466	16805040
    467	29408820
    468	12603780
    469	50415120
    470	21006300
    471	42012600
    472	37811340
    473	8402520
    474	25207560
    475	29408820
    476	37811340
    477	37811340
    478	50415120
    479	16805040
    480	21006300
    481	25207560
    482	12603780
    483	16805040
    484	16805040
    485	46213860
    486	8402520
    487	21006300
    488	8402520
    489	12603780
    490	21006300
    491	37811340
    493	16805040
    494	29408820
    495	25207560
    496	4201260
    497	16805040
    498	16805040
    499	29408820
    500	25207560
    501	16805040
    502	8402520
    503	25207560
    504	12603780
    505	21006300
    506	16805040
    507	8402520
    508	46213860
    509	21006300
    510	21006300
    511	25207560
    512	8402520
    513	33610080
    514	21006300
    515	8402520
    516	8402520
    517	12603780
    518	16805040
    519	33610080
    521	8402520
    522	12603780
    523	21006300
    524	12603780
    525	21006300
    526	16805040
    527	16805040
    528	4201260
    529	16805040
    531	16805040
    532	4201260
    533	21006300
    534	16805040
    535	16805040
    536	8402520
    537	12603780
    538	4201260
    539	12603780
    540	16805040
    541	21006300
    542	8402520
    543	4201260
    544	8402520
    546	4201260
    547	12603780
    548	4201260
    549	16805040
    551	4201260
    552	4201260
    554	4201260
    555	4201260
    556	8402520
    558	16805040
    561	4201260
    564	8402520
    565	8402520
    566	8402520
    567	8402520
    568	4201260
    571	4201260
    572	4201260
    574	8402520
    575	8402520
    578	4201260
    580	4201260
    581	4201260
    582	12603780
    583	4201260
    584	8402520
    585	8402520
    586	4201260
    588	4201260
    589	4201260
    591	4201260
    592	8402520
    595	8402520
    597	4201260
    599	8402520
    600	8402520
    603	4201260
    605	8402520
    614	4201260
    618	4201260
    624	4201260
    627	4201260
    629	4201260
    630	4201260
    632	4201260
    635	4201260
    636	4201260
    640	4201260
    644	4201260
    647	8402520
    648	4201260
    651	8402520
    652	4201260
    657	8402520
    660	4201260
    662	8402520
    665	4201260
    669	8402520
    674	4201260
    677	4201260
    680	4201260
    681	4201260
    682	4201260
    683	4201260
    688	4201260
    690	4201260
    691	4201260
    694	4201260
    702	4201260
    707	4201260
    709	8402520
    710	4201260
    714	4201260
    715	4201260
    718	4201260
    727	4201260
    728	4201260
    729	4201260
    748	4201260
    755	4201260
    780	4201260
    797	4201260
    798	4201260
    801	4201260
    812	4201260
    826	4201260
    827	4201260
    829	4201260
    843	4201260
    845	4201260
    848	4201260
    849	4201260
    866	4201260
    873	4201260
    878	4201260
    895	4201260
    899	4201260
    908	4201260
    916	4201260
    923	4201260
    926	4201260
    967	4201260
    1010	4201260
    1011	4201260
    1028	4201260
    1049	4201260
    1061	4201260
    1062	4201260
    1067	4201260
    1089	4201260
    1103	4201260
    1157	4201260
    1182	4201260
    1199	4201260
    1221	4201260
    1259	4201260
    1342	4201260
    1363	4201260
    1389	4201260
    1395	4201260
    1403	4201260
    1476	4201260
    1503	4201260
    1581	4201260
    1592	4201260
    1599	4201260
    1600	4201260
    1644	4201260
    1798	4201260
    1839	4201260
    2786	4201260
"""

friendster_t192_latency_kdax_str = """
    Latency	Loads
    6	30202858140
    7	366026374980
    8	29345801100
    9	14901869220
    11	42012600
    12	3272781540
    13	621786480
    14	3718115100
    15	1646893920
    16	2243472840
    17	550365060
    18	369710880
    19	445333560
    20	260478120
    21	407522220
    22	268880640
    23	243673080
    24	180654180
    25	378113400
    26	201660480
    27	147044100
    28	147044100
    29	109232760
    30	159647880
    31	126037800
    32	100830240
    33	105031500
    34	105031500
    35	79823940
    36	109232760
    37	92427720
    38	88226460
    39	130239060
    40	134440320
    41	75622680
    42	105031500
    43	113434020
    44	121836540
    45	71421420
    46	42012600
    47	50415120
    48	50415120
    49	50415120
    50	37811340
    51	46213860
    52	37811340
    53	79823940
    54	42012600
    55	71421420
    56	37811340
    57	46213860
    58	79823940
    59	71421420
    60	37811340
    61	54616380
    62	54616380
    63	75622680
    64	67220160
    65	126037800
    66	130239060
    67	113434020
    68	100830240
    69	84025200
    70	46213860
    71	42012600
    72	54616380
    73	42012600
    74	50415120
    75	63018900
    76	75622680
    77	29408820
    78	16805040
    79	42012600
    80	37811340
    81	25207560
    82	25207560
    83	29408820
    84	25207560
    85	25207560
    86	21006300
    87	33610080
    88	21006300
    89	16805040
    90	16805040
    91	8402520
    92	25207560
    93	12603780
    94	8402520
    95	8402520
    96	16805040
    97	21006300
    98	21006300
    99	4201260
    100	12603780
    101	29408820
    102	25207560
    103	12603780
    104	12603780
    105	16805040
    107	16805040
    108	8402520
    109	29408820
    110	8402520
    111	16805040
    112	21006300
    113	25207560
    114	25207560
    115	8402520
    116	4201260
    117	4201260
    119	25207560
    120	16805040
    121	8402520
    122	12603780
    123	8402520
    124	8402520
    125	8402520
    126	12603780
    127	16805040
    128	21006300
    129	16805040
    130	21006300
    131	8402520
    132	21006300
    133	25207560
    134	25207560
    135	21006300
    136	8402520
    137	16805040
    138	29408820
    139	12603780
    140	25207560
    141	16805040
    142	16805040
    143	21006300
    144	4201260
    145	16805040
    146	12603780
    147	42012600
    148	29408820
    149	16805040
    150	21006300
    151	21006300
    152	21006300
    153	8402520
    154	33610080
    155	16805040
    156	4201260
    157	16805040
    158	21006300
    159	8402520
    160	29408820
    161	25207560
    162	21006300
    163	12603780
    164	8402520
    165	16805040
    166	16805040
    167	21006300
    168	21006300
    169	25207560
    170	16805040
    171	12603780
    172	12603780
    173	21006300
    174	21006300
    175	25207560
    176	4201260
    177	21006300
    178	21006300
    179	21006300
    180	25207560
    181	8402520
    182	33610080
    183	21006300
    184	21006300
    185	12603780
    186	16805040
    187	42012600
    188	21006300
    189	8402520
    190	4201260
    191	8402520
    192	16805040
    193	12603780
    194	25207560
    195	16805040
    196	21006300
    197	16805040
    198	8402520
    199	8402520
    200	8402520
    201	8402520
    202	4201260
    203	4201260
    204	12603780
    205	16805040
    206	4201260
    208	16805040
    209	8402520
    210	12603780
    211	8402520
    212	4201260
    213	16805040
    214	4201260
    215	16805040
    217	12603780
    218	29408820
    219	12603780
    220	4201260
    221	12603780
    222	4201260
    223	4201260
    224	8402520
    225	25207560
    226	12603780
    227	33610080
    228	21006300
    229	12603780
    230	16805040
    231	8402520
    232	8402520
    233	16805040
    234	25207560
    235	33610080
    236	42012600
    237	21006300
    238	33610080
    239	33610080
    240	8402520
    241	21006300
    242	16805040
    243	16805040
    244	21006300
    245	37811340
    246	12603780
    247	25207560
    248	8402520
    249	21006300
    250	16805040
    251	21006300
    252	50415120
    253	16805040
    254	21006300
    255	29408820
    256	42012600
    257	16805040
    258	42012600
    259	12603780
    260	37811340
    261	16805040
    262	33610080
    263	37811340
    264	29408820
    265	16805040
    266	21006300
    267	29408820
    268	21006300
    269	37811340
    270	4201260
    271	25207560
    272	12603780
    273	42012600
    274	4201260
    275	21006300
    276	12603780
    277	8402520
    278	29408820
    279	12603780
    280	16805040
    281	8402520
    282	4201260
    283	4201260
    284	21006300
    285	8402520
    286	8402520
    287	8402520
    288	12603780
    289	4201260
    290	21006300
    291	8402520
    293	4201260
    296	8402520
    297	4201260
    298	8402520
    299	8402520
    300	8402520
    301	12603780
    302	8402520
    303	8402520
    304	4201260
    305	8402520
    306	4201260
    307	8402520
    308	4201260
    309	4201260
    310	8402520
    311	4201260
    314	12603780
    317	4201260
    319	4201260
    320	4201260
    321	8402520
    322	4201260
    323	4201260
    324	4201260
    326	8402520
    327	8402520
    329	4201260
    330	4201260
    331	4201260
    332	4201260
    334	8402520
    336	4201260
    337	4201260
    338	4201260
    339	8402520
    340	8402520
    341	8402520
    342	4201260
    344	4201260
    345	8402520
    346	8402520
    347	4201260
    349	8402520
    353	4201260
    354	8402520
    356	4201260
    358	8402520
    359	4201260
    361	8402520
    363	8402520
    364	8402520
    365	12603780
    366	8402520
    367	4201260
    370	4201260
    372	4201260
    373	8402520
    374	8402520
    375	4201260
    376	8402520
    379	4201260
    381	4201260
    382	8402520
    383	4201260
    384	4201260
    385	8402520
    387	4201260
    388	4201260
    389	4201260
    390	4201260
    391	4201260
    393	8402520
    394	8402520
    395	16805040
    397	12603780
    398	12603780
    399	12603780
    400	12603780
    401	8402520
    402	8402520
    403	21006300
    404	25207560
    405	12603780
    406	8402520
    407	8402520
    408	8402520
    409	12603780
    410	12603780
    411	16805040
    412	16805040
    413	16805040
    414	21006300
    415	33610080
    416	16805040
    417	25207560
    418	12603780
    419	29408820
    420	33610080
    421	21006300
    422	29408820
    423	29408820
    424	4201260
    425	29408820
    426	12603780
    427	33610080
    428	29408820
    429	33610080
    430	16805040
    431	21006300
    432	16805040
    433	37811340
    434	37811340
    435	16805040
    436	25207560
    437	8402520
    438	33610080
    439	42012600
    440	33610080
    441	33610080
    442	25207560
    443	16805040
    444	25207560
    445	16805040
    446	37811340
    447	21006300
    448	37811340
    449	12603780
    450	21006300
    451	37811340
    452	16805040
    453	21006300
    454	37811340
    455	21006300
    456	25207560
    457	16805040
    458	33610080
    459	25207560
    460	4201260
    461	16805040
    462	25207560
    463	12603780
    464	12603780
    465	8402520
    466	21006300
    467	16805040
    468	29408820
    469	16805040
    470	33610080
    471	12603780
    472	8402520
    473	16805040
    475	21006300
    476	12603780
    477	4201260
    478	8402520
    479	12603780
    480	4201260
    483	4201260
    484	8402520
    485	4201260
    486	21006300
    488	16805040
    489	8402520
    490	8402520
    491	4201260
    492	8402520
    493	12603780
    495	12603780
    496	4201260
    497	8402520
    498	29408820
    502	4201260
    503	8402520
    504	8402520
    505	8402520
    506	4201260
    512	16805040
    513	4201260
    514	8402520
    516	4201260
    518	4201260
    519	4201260
    521	8402520
    522	8402520
    523	4201260
    526	4201260
    531	4201260
    532	4201260
    534	4201260
    535	4201260
    536	4201260
    539	4201260
    546	8402520
    548	4201260
    549	4201260
    550	4201260
    552	8402520
    553	4201260
    555	4201260
    557	4201260
    559	4201260
    562	4201260
    563	8402520
    564	8402520
    575	4201260
    586	4201260
    587	4201260
    593	4201260
    599	4201260
    612	4201260
    614	4201260
    636	4201260
    639	4201260
    662	4201260
    673	4201260
    675	4201260
    690	4201260
    698	4201260
    706	4201260
    710	4201260
    711	4201260
    712	4201260
    731	4201260
    732	4201260
    737	4201260
    744	4201260
    749	4201260
    764	8402520
    780	4201260
    785	4201260
    789	4201260
    790	4201260
    793	4201260
    795	4201260
    796	4201260
    805	8402520
    819	4201260
    843	4201260
    845	4201260
    850	4201260
    853	4201260
    864	4201260
    877	4201260
    878	4201260
    946	4201260
    982	4201260
    983	4201260
    984	4201260
    998	4201260
    1021	4201260
    1026	4201260
    1030	4201260
    1052	4201260
    1124	4201260
    1146	4201260
    1171	4201260
    1173	4201260
    1189	4201260
    1211	4201260
    1224	4201260
    1226	4201260
    1240	4201260
    1279	4201260
    1334	4201260
    1349	4201260
    1395	4201260
    1405	4201260
    1459	4201260
    1464	4201260
    1510	4201260
    1598	4201260
    1623	4201260
    1667	4201260
    2204	4201260
    2889	4201260
    3253	4201260
"""

friendster_t192_latency_mem_str = """
    Latency	Loads
    6	30744820680
    7	371748491100
    8	28047611760
    9	14679202440
    11	58817640
    12	3386215560
    13	701610420
    14	3352605480
    15	1516654860
    16	1844353140
    17	680604120
    18	369710880
    19	537761280
    20	365509620
    21	432729780
    22	289886940
    23	201660480
    24	189056700
    25	331899540
    26	130239060
    27	134440320
    28	151245360
    29	92427720
    30	163849140
    31	117635280
    32	126037800
    33	100830240
    34	92427720
    35	88226460
    36	138641580
    37	117635280
    38	92427720
    39	134440320
    40	109232760
    41	105031500
    42	109232760
    43	130239060
    44	96628980
    45	54616380
    46	42012600
    47	42012600
    48	50415120
    49	33610080
    50	63018900
    51	71421420
    52	37811340
    53	29408820
    54	50415120
    55	58817640
    56	50415120
    57	46213860
    58	67220160
    59	67220160
    60	75622680
    61	42012600
    62	67220160
    63	75622680
    64	126037800
    65	113434020
    66	130239060
    67	96628980
    68	109232760
    69	117635280
    70	54616380
    71	58817640
    72	37811340
    73	50415120
    74	33610080
    75	37811340
    76	71421420
    77	42012600
    78	46213860
    79	63018900
    80	29408820
    81	29408820
    82	25207560
    83	12603780
    84	50415120
    85	42012600
    86	25207560
    87	29408820
    88	8402520
    89	16805040
    90	16805040
    91	12603780
    92	8402520
    93	21006300
    94	21006300
    95	21006300
    96	29408820
    97	4201260
    98	25207560
    99	16805040
    100	21006300
    101	33610080
    102	16805040
    103	8402520
    104	25207560
    105	16805040
    106	4201260
    107	25207560
    108	12603780
    109	16805040
    110	4201260
    111	8402520
    112	25207560
    113	33610080
    114	25207560
    115	12603780
    117	16805040
    118	21006300
    119	21006300
    120	4201260
    121	12603780
    122	16805040
    123	25207560
    124	8402520
    125	16805040
    126	4201260
    127	16805040
    128	12603780
    129	21006300
    130	16805040
    131	16805040
    132	4201260
    133	16805040
    134	16805040
    135	16805040
    136	12603780
    137	4201260
    138	12603780
    139	12603780
    140	21006300
    141	12603780
    142	21006300
    143	21006300
    144	37811340
    145	29408820
    146	16805040
    147	16805040
    148	33610080
    149	25207560
    150	12603780
    151	12603780
    152	16805040
    153	12603780
    154	12603780
    155	12603780
    156	16805040
    157	29408820
    158	16805040
    159	16805040
    160	16805040
    161	16805040
    162	12603780
    163	29408820
    164	21006300
    165	21006300
    166	29408820
    167	25207560
    168	16805040
    169	12603780
    170	21006300
    171	37811340
    172	16805040
    173	4201260
    174	8402520
    175	21006300
    176	16805040
    177	16805040
    178	29408820
    179	8402520
    180	12603780
    182	8402520
    183	16805040
    184	12603780
    185	12603780
    186	21006300
    187	21006300
    188	21006300
    189	25207560
    190	16805040
    191	4201260
    192	8402520
    193	4201260
    194	21006300
    195	8402520
    196	12603780
    197	16805040
    198	12603780
    199	21006300
    200	8402520
    201	16805040
    202	12603780
    203	16805040
    204	8402520
    205	16805040
    206	16805040
    207	21006300
    208	16805040
    209	4201260
    210	16805040
    211	16805040
    212	4201260
    213	12603780
    214	16805040
    215	8402520
    216	4201260
    217	8402520
    218	4201260
    219	12603780
    220	4201260
    221	21006300
    222	12603780
    225	4201260
    226	8402520
    227	8402520
    228	8402520
    229	12603780
    230	12603780
    231	21006300
    232	8402520
    234	25207560
    235	16805040
    236	12603780
    237	16805040
    238	16805040
    239	25207560
    240	12603780
    241	12603780
    242	16805040
    243	21006300
    244	12603780
    245	25207560
    246	16805040
    247	16805040
    248	25207560
    249	12603780
    250	12603780
    251	8402520
    252	16805040
    253	16805040
    254	12603780
    255	37811340
    256	37811340
    257	16805040
    258	12603780
    259	63018900
    260	37811340
    261	37811340
    262	29408820
    263	16805040
    264	25207560
    265	16805040
    266	42012600
    267	33610080
    268	29408820
    269	37811340
    270	25207560
    271	33610080
    272	42012600
    273	37811340
    274	16805040
    275	12603780
    276	29408820
    277	29408820
    278	29408820
    279	16805040
    280	42012600
    281	21006300
    283	4201260
    284	4201260
    285	21006300
    286	12603780
    287	12603780
    288	8402520
    289	21006300
    291	12603780
    292	8402520
    293	21006300
    294	16805040
    295	4201260
    296	12603780
    297	12603780
    298	21006300
    299	12603780
    300	12603780
    302	16805040
    303	12603780
    304	33610080
    305	12603780
    306	8402520
    307	8402520
    308	21006300
    309	4201260
    311	8402520
    313	12603780
    314	4201260
    315	4201260
    316	8402520
    320	8402520
    321	12603780
    322	4201260
    323	4201260
    324	8402520
    325	4201260
    326	4201260
    327	4201260
    328	4201260
    330	4201260
    331	4201260
    332	4201260
    333	4201260
    337	4201260
    338	4201260
    339	12603780
    340	4201260
    343	4201260
    344	4201260
    345	8402520
    346	8402520
    348	4201260
    349	4201260
    351	4201260
    352	4201260
    353	8402520
    354	4201260
    356	8402520
    357	4201260
    358	4201260
    359	4201260
    361	4201260
    362	4201260
    364	8402520
    365	4201260
    366	4201260
    367	4201260
    368	8402520
    369	4201260
    370	4201260
    372	4201260
    373	4201260
    376	4201260
    377	12603780
    380	4201260
    382	8402520
    383	4201260
    384	8402520
    386	16805040
    387	4201260
    388	8402520
    389	4201260
    390	12603780
    392	8402520
    394	4201260
    395	4201260
    396	4201260
    398	4201260
    399	4201260
    400	4201260
    401	4201260
    403	8402520
    404	8402520
    405	4201260
    406	4201260
    407	8402520
    408	4201260
    409	16805040
    410	4201260
    411	8402520
    413	12603780
    415	8402520
    416	8402520
    417	4201260
    418	8402520
    419	16805040
    420	16805040
    421	12603780
    422	12603780
    423	4201260
    424	8402520
    425	8402520
    426	4201260
    427	21006300
    428	21006300
    429	8402520
    430	12603780
    431	12603780
    432	4201260
    433	4201260
    434	16805040
    435	16805040
    436	8402520
    437	12603780
    438	12603780
    439	21006300
    440	4201260
    441	12603780
    442	29408820
    443	29408820
    444	16805040
    445	21006300
    446	21006300
    447	16805040
    448	29408820
    449	21006300
    450	33610080
    451	21006300
    452	29408820
    453	33610080
    454	12603780
    455	12603780
    456	12603780
    457	33610080
    458	21006300
    459	25207560
    460	42012600
    461	12603780
    462	42012600
    463	21006300
    464	12603780
    465	50415120
    466	29408820
    467	21006300
    468	21006300
    469	21006300
    470	37811340
    471	29408820
    472	21006300
    473	37811340
    474	50415120
    475	12603780
    476	37811340
    477	21006300
    478	33610080
    479	16805040
    480	21006300
    481	25207560
    482	21006300
    483	12603780
    484	25207560
    485	16805040
    486	21006300
    487	21006300
    488	12603780
    489	16805040
    490	12603780
    491	8402520
    492	8402520
    493	21006300
    494	16805040
    495	8402520
    496	16805040
    497	4201260
    498	16805040
    499	25207560
    500	12603780
    501	16805040
    502	8402520
    503	16805040
    504	16805040
    505	12603780
    506	25207560
    508	8402520
    510	4201260
    511	8402520
    513	4201260
    514	4201260
    516	21006300
    517	8402520
    519	21006300
    520	4201260
    521	4201260
    523	4201260
    524	12603780
    525	8402520
    526	4201260
    527	4201260
    529	4201260
    530	4201260
    531	8402520
    534	8402520
    535	8402520
    541	4201260
    543	4201260
    544	4201260
    545	4201260
    547	4201260
    548	4201260
    549	4201260
    550	8402520
    552	8402520
    553	12603780
    555	4201260
    556	8402520
    561	4201260
    562	4201260
    565	4201260
    569	4201260
    570	4201260
    574	4201260
    578	4201260
    582	8402520
    588	8402520
    593	4201260
    597	4201260
    599	4201260
    603	4201260
    621	4201260
    624	4201260
    625	4201260
    627	4201260
    644	4201260
    645	4201260
    673	4201260
    676	4201260
    700	4201260
    711	4201260
    718	4201260
    720	4201260
    729	4201260
    741	4201260
    751	4201260
    756	4201260
    779	4201260
    781	8402520
    795	4201260
    800	4201260
    803	4201260
    805	4201260
    814	4201260
    832	4201260
    835	4201260
    839	4201260
    843	4201260
    881	4201260
    917	4201260
    935	4201260
    949	4201260
    962	4201260
    968	4201260
    983	4201260
    999	8402520
    1007	4201260
    1022	4201260
    1028	4201260
    1052	4201260
    1077	4201260
    1080	4201260
    1088	4201260
    1100	4201260
    1101	4201260
    1111	4201260
    1115	4201260
    1132	4201260
    1137	4201260
    1138	4201260
    1150	4201260
    1165	4201260
    1190	4201260
    1195	4201260
    1216	4201260
    1217	4201260
    1221	4201260
    1224	4201260
    1252	4201260
    1257	4201260
    1258	4201260
    1259	4201260
    1261	4201260
    1280	4201260
    1283	4201260
    1288	4201260
    1290	4201260
    1302	4201260
    1315	4201260
    1318	4201260
    1325	4201260
    1327	4201260
    1412	4201260
    1428	4201260
    1447	4201260
    1507	4201260
    1508	4201260
    2117	4201260
"""

#----------------------------------------------------------------------------
# moliere2016, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

moliere2016_t192_latency_dram_str = """
    Latency	Loads
    6	6621185760
    7	91137933180
    8	6671600880
    9	4180253700
    11	25207560
    12	878063340
    13	205861740
    14	474742380
    15	592377660
    16	1298189340
    17	231069300
    18	197459220
    19	138641580
    20	121836540
    21	130239060
    22	126037800
    23	138641580
    24	159647880
    25	264679380
    26	33610080
    27	100830240
    28	29408820
    29	33610080
    30	92427720
    31	25207560
    32	33610080
    33	33610080
    34	16805040
    35	12603780
    36	16805040
    37	21006300
    38	25207560
    39	12603780
    40	16805040
    41	25207560
    42	33610080
    43	12603780
    44	8402520
    45	29408820
    47	16805040
    48	21006300
    49	12603780
    50	4201260
    51	21006300
    52	4201260
    53	25207560
    54	16805040
    55	16805040
    56	12603780
    57	12603780
    58	37811340
    59	12603780
    60	8402520
    61	33610080
    62	21006300
    63	21006300
    64	12603780
    65	12603780
    66	29408820
    67	16805040
    68	33610080
    69	8402520
    70	29408820
    71	16805040
    72	12603780
    74	16805040
    75	16805040
    76	33610080
    77	21006300
    78	25207560
    79	29408820
    80	21006300
    81	16805040
    82	8402520
    83	8402520
    84	4201260
    86	12603780
    87	4201260
    88	21006300
    89	16805040
    90	12603780
    92	8402520
    96	16805040
    97	8402520
    98	8402520
    99	4201260
    100	8402520
    101	4201260
    102	12603780
    103	16805040
    104	8402520
    105	4201260
    106	4201260
    107	8402520
    108	4201260
    109	8402520
    110	4201260
    111	4201260
    112	4201260
    114	4201260
    115	4201260
    117	8402520
    118	4201260
    119	8402520
    120	4201260
    122	12603780
    124	4201260
    125	4201260
    126	4201260
    129	4201260
    130	4201260
    132	8402520
    133	4201260
    135	8402520
    136	8402520
    138	8402520
    139	4201260
    142	4201260
    143	4201260
    146	4201260
    148	4201260
    149	4201260
    151	4201260
    155	12603780
    157	4201260
    158	4201260
    160	4201260
    161	4201260
    162	12603780
    163	4201260
    164	4201260
    165	4201260
    166	8402520
    167	4201260
    168	8402520
    169	4201260
    170	4201260
    173	4201260
    176	4201260
    177	4201260
    181	4201260
    183	8402520
    184	4201260
    186	4201260
    188	8402520
    189	4201260
    191	8402520
    193	8402520
    195	8402520
    196	4201260
    198	4201260
    200	12603780
    201	8402520
    202	8402520
    203	8402520
    204	4201260
    205	4201260
    207	4201260
    209	4201260
    210	4201260
    211	4201260
    212	8402520
    215	8402520
    217	4201260
    218	4201260
    219	4201260
    220	4201260
    221	4201260
    229	4201260
    236	4201260
    237	8402520
    238	4201260
    240	8402520
    241	4201260
    242	4201260
    245	8402520
    246	4201260
    247	21006300
    248	16805040
    249	8402520
    250	8402520
    251	16805040
    252	4201260
    253	4201260
    254	4201260
    255	4201260
    256	4201260
    257	4201260
    258	16805040
    259	4201260
    260	4201260
    261	4201260
    262	12603780
    263	4201260
    264	8402520
    265	12603780
    267	8402520
    268	4201260
    269	4201260
    270	4201260
    271	8402520
    272	8402520
    275	8402520
    277	4201260
    278	4201260
    279	12603780
    280	8402520
    281	8402520
    283	8402520
    284	4201260
    285	8402520
    286	8402520
    288	4201260
    289	12603780
    290	12603780
    293	8402520
    294	8402520
    295	4201260
    296	8402520
    298	8402520
    300	4201260
    304	12603780
    306	8402520
    307	4201260
    308	4201260
    309	4201260
    311	4201260
    312	8402520
    313	4201260
    315	4201260
    318	4201260
    319	8402520
    320	4201260
    321	8402520
    322	12603780
    324	8402520
    325	8402520
    330	4201260
    331	8402520
    332	4201260
    335	8402520
    336	4201260
    339	4201260
    340	4201260
    343	4201260
    346	4201260
    348	4201260
    350	4201260
    352	4201260
    353	4201260
    354	4201260
    356	8402520
    360	4201260
    363	4201260
    364	4201260
    367	4201260
    370	4201260
    372	4201260
    376	4201260
    379	8402520
    381	4201260
    382	8402520
    387	4201260
    388	8402520
    390	12603780
    393	4201260
    395	4201260
    400	4201260
    401	4201260
    402	4201260
    403	4201260
    405	8402520
    407	8402520
    408	4201260
    409	4201260
    410	4201260
    411	4201260
    412	4201260
    413	12603780
    414	4201260
    415	4201260
    416	4201260
    417	4201260
    419	12603780
    420	8402520
    421	8402520
    422	4201260
    423	8402520
    424	8402520
    425	12603780
    426	4201260
    427	8402520
    428	4201260
    431	8402520
    432	4201260
    434	4201260
    435	8402520
    436	8402520
    437	8402520
    438	4201260
    439	12603780
    440	16805040
    441	4201260
    442	4201260
    443	8402520
    446	16805040
    447	25207560
    448	4201260
    449	16805040
    450	4201260
    451	12603780
    453	4201260
    454	4201260
    455	12603780
    457	16805040
    458	12603780
    460	4201260
    461	4201260
    462	8402520
    463	4201260
    465	4201260
    466	8402520
    468	4201260
    469	4201260
    470	4201260
    471	4201260
    472	4201260
    474	4201260
    475	8402520
    476	4201260
    477	4201260
    478	4201260
    479	4201260
    480	4201260
    481	8402520
    487	4201260
    488	8402520
    489	4201260
    491	4201260
    492	8402520
    493	4201260
    494	12603780
    495	4201260
    499	4201260
    500	8402520
    504	4201260
    505	4201260
    506	4201260
    507	4201260
    509	8402520
    510	4201260
    511	4201260
    514	8402520
    518	4201260
    519	4201260
    520	8402520
    524	4201260
    526	4201260
    532	8402520
    535	8402520
    538	4201260
    541	4201260
    545	12603780
    546	8402520
    547	12603780
    548	4201260
    552	8402520
    553	4201260
    555	8402520
    557	4201260
    558	4201260
    559	8402520
    562	4201260
    564	4201260
    566	4201260
    568	8402520
    572	4201260
    573	4201260
    580	4201260
    583	4201260
    587	4201260
    590	4201260
    594	4201260
    595	4201260
    597	4201260
    599	4201260
    601	4201260
    604	4201260
    610	4201260
    612	4201260
    613	4201260
    618	4201260
    620	4201260
    623	4201260
    625	4201260
    627	4201260
    631	4201260
    637	4201260
    641	8402520
    649	4201260
    654	4201260
    657	4201260
    662	4201260
    673	4201260
    681	4201260
    701	4201260
    722	4201260
    730	4201260
    749	4201260
    753	4201260
    756	4201260
    761	4201260
    779	4201260
    780	4201260
    786	4201260
    794	4201260
    807	4201260
    855	4201260
    860	4201260
    883	4201260
    903	4201260
    912	4201260
    931	4201260
    972	4201260
    976	4201260
    982	4201260
    996	4201260
    999	4201260
    1040	4201260
    1070	4201260
    1088	4201260
    1113	4201260
    1115	4201260
    1122	8402520
    1133	4201260
    1154	4201260
    1188	4201260
    1195	4201260
    1213	4201260
    1218	4201260
    1220	4201260
    1232	4201260
    1250	4201260
    1298	4201260
    1349	4201260
    1350	4201260
    1399	4201260
    1448	4201260
    1477	4201260
    1520	4201260
    1528	4201260
    1594	4201260
    1600	4201260
    1712	4201260
    1842	4201260
    2163	4201260
"""

# FIXME: dram + pmem?
    # 6	6780833640
    # 7	90831241200
    # 8	6419525280
    # 9	3865159200
    # 11	8402520
    # 12	840252000
    # 13	222666780
    # 14	546163800
    # 15	701610420
    # 16	1054516260
    # 17	222666780
    # 18	247874340
    # 19	180654180
    # 20	142842840
    # 21	126037800
    # 22	180654180
    # 23	151245360
    # 24	147044100
    # 25	243673080
    # 26	46213860
    # 27	88226460
    # 28	33610080
    # 29	46213860
    # 30	92427720
    # 31	25207560
    # 32	37811340
    # 33	16805040
    # 34	25207560
    # 35	12603780
    # 36	16805040
    # 37	33610080
    # 39	21006300
    # 40	8402520
    # 41	16805040
    # 42	29408820
    # 43	12603780
    # 44	42012600
    # 45	16805040
    # 46	16805040
    # 48	4201260
    # 49	12603780
    # 51	21006300
    # 52	4201260
    # 53	12603780
    # 54	12603780
    # 55	21006300
    # 56	29408820
    # 57	12603780
    # 58	21006300
    # 59	25207560
    # 60	25207560
    # 61	25207560
    # 62	4201260
    # 63	12603780
    # 64	12603780
    # 65	25207560
    # 66	25207560
    # 67	21006300
    # 68	25207560
    # 69	29408820
    # 70	8402520
    # 71	12603780
    # 72	8402520
    # 73	25207560
    # 74	8402520
    # 75	21006300
    # 77	21006300
    # 78	8402520
    # 79	16805040
    # 80	29408820
    # 82	16805040
    # 83	12603780
    # 84	21006300
    # 85	8402520
    # 86	16805040
    # 87	12603780
    # 88	21006300
    # 89	12603780
    # 90	4201260
    # 91	12603780
    # 92	12603780
    # 93	16805040
    # 94	4201260
    # 95	12603780
    # 96	4201260
    # 97	8402520
    # 98	12603780
    # 99	8402520
    # 100	8402520
    # 101	8402520
    # 102	12603780
    # 103	8402520
    # 104	8402520
    # 105	4201260
    # 107	8402520
    # 108	4201260
    # 109	4201260
    # 110	4201260
    # 111	4201260
    # 112	12603780
    # 114	4201260
    # 115	16805040
    # 117	12603780
    # 119	4201260
    # 121	4201260
    # 123	8402520
    # 125	4201260
    # 126	4201260
    # 127	4201260
    # 130	4201260
    # 132	4201260
    # 133	4201260
    # 134	4201260
    # 135	12603780
    # 136	12603780
    # 140	4201260
    # 141	4201260
    # 144	8402520
    # 145	4201260
    # 146	8402520
    # 150	4201260
    # 151	4201260
    # 152	8402520
    # 154	4201260
    # 156	4201260
    # 157	4201260
    # 158	12603780
    # 159	4201260
    # 162	8402520
    # 163	4201260
    # 165	4201260
    # 166	4201260
    # 167	16805040
    # 168	12603780
    # 171	4201260
    # 172	8402520
    # 173	4201260
    # 174	4201260
    # 176	8402520
    # 178	4201260
    # 179	4201260
    # 181	4201260
    # 182	4201260
    # 183	8402520
    # 184	4201260
    # 185	12603780
    # 186	8402520
    # 187	4201260
    # 188	4201260
    # 190	4201260
    # 192	4201260
    # 195	4201260
    # 196	4201260
    # 198	4201260
    # 199	4201260
    # 200	8402520
    # 207	4201260
    # 210	8402520
    # 211	8402520
    # 212	8402520
    # 215	4201260
    # 216	8402520
    # 219	4201260
    # 220	4201260
    # 223	4201260
    # 224	4201260
    # 227	8402520
    # 228	4201260
    # 229	4201260
    # 230	8402520
    # 234	8402520
    # 238	4201260
    # 240	4201260
    # 241	4201260
    # 242	4201260
    # 245	8402520
    # 246	4201260
    # 247	4201260
    # 249	4201260
    # 250	8402520
    # 253	8402520
    # 255	4201260
    # 258	4201260
    # 259	4201260
    # 260	4201260
    # 261	12603780
    # 262	4201260
    # 265	4201260
    # 266	4201260
    # 267	4201260
    # 270	16805040
    # 274	12603780
    # 276	16805040
    # 277	8402520
    # 278	16805040
    # 280	8402520
    # 281	4201260
    # 282	4201260
    # 283	4201260
    # 285	4201260
    # 288	8402520
    # 289	4201260
    # 290	4201260
    # 291	4201260
    # 294	4201260
    # 298	4201260
    # 299	8402520
    # 300	4201260
    # 301	4201260
    # 304	4201260
    # 307	8402520
    # 310	4201260
    # 312	8402520
    # 313	4201260
    # 314	4201260
    # 315	4201260
    # 316	4201260
    # 317	4201260
    # 318	8402520
    # 319	8402520
    # 320	4201260
    # 323	4201260
    # 324	4201260
    # 325	4201260
    # 327	4201260
    # 330	4201260
    # 331	8402520
    # 332	4201260
    # 334	4201260
    # 336	4201260
    # 337	4201260
    # 340	4201260
    # 341	4201260
    # 343	4201260
    # 344	4201260
    # 347	4201260
    # 349	4201260
    # 350	4201260
    # 351	8402520
    # 354	4201260
    # 357	8402520
    # 360	16805040
    # 365	8402520
    # 367	4201260
    # 368	4201260
    # 371	4201260
    # 373	4201260
    # 376	4201260
    # 377	4201260
    # 378	4201260
    # 380	4201260
    # 381	4201260
    # 383	4201260
    # 386	4201260
    # 387	8402520
    # 388	4201260
    # 391	4201260
    # 392	4201260
    # 393	12603780
    # 395	8402520
    # 396	4201260
    # 397	4201260
    # 401	8402520
    # 403	4201260
    # 405	8402520
    # 410	8402520
    # 411	4201260
    # 413	4201260
    # 414	4201260
    # 415	4201260
    # 416	21006300
    # 418	8402520
    # 419	8402520
    # 422	16805040
    # 423	4201260
    # 424	4201260
    # 425	8402520
    # 427	4201260
    # 428	4201260
    # 429	16805040
    # 430	4201260
    # 431	8402520
    # 432	4201260
    # 433	4201260
    # 434	4201260
    # 435	8402520
    # 436	8402520
    # 437	8402520
    # 438	8402520
    # 439	4201260
    # 440	8402520
    # 442	12603780
    # 443	4201260
    # 444	8402520
    # 445	12603780
    # 446	12603780
    # 447	4201260
    # 448	8402520
    # 450	12603780
    # 451	12603780
    # 452	12603780
    # 453	8402520
    # 454	8402520
    # 455	16805040
    # 456	4201260
    # 457	4201260
    # 458	4201260
    # 460	4201260
    # 461	4201260
    # 462	12603780
    # 463	8402520
    # 464	4201260
    # 466	4201260
    # 467	4201260
    # 469	8402520
    # 471	4201260
    # 473	4201260
    # 475	4201260
    # 478	8402520
    # 480	8402520
    # 481	21006300
    # 483	4201260
    # 484	4201260
    # 486	12603780
    # 487	8402520
    # 489	12603780
    # 490	12603780
    # 491	4201260
    # 492	12603780
    # 494	8402520
    # 496	16805040
    # 498	4201260
    # 499	8402520
    # 500	8402520
    # 501	4201260
    # 502	8402520
    # 504	4201260
    # 505	4201260
    # 509	4201260
    # 511	8402520
    # 512	4201260
    # 520	4201260
    # 522	4201260
    # 524	4201260
    # 527	4201260
    # 528	8402520
    # 529	4201260
    # 531	16805040
    # 532	4201260
    # 534	8402520
    # 535	8402520
    # 536	4201260
    # 541	4201260
    # 544	4201260
    # 546	4201260
    # 547	4201260
    # 550	4201260
    # 560	4201260
    # 564	4201260
    # 565	8402520
    # 566	8402520
    # 567	4201260
    # 568	4201260
    # 571	4201260
    # 572	4201260
    # 577	4201260
    # 580	4201260
    # 581	4201260
    # 583	4201260
    # 587	12603780
    # 590	4201260
    # 592	4201260
    # 596	12603780
    # 601	4201260
    # 602	4201260
    # 607	8402520
    # 608	4201260
    # 613	4201260
    # 614	8402520
    # 618	4201260
    # 619	4201260
    # 623	4201260
    # 626	4201260
    # 628	4201260
    # 632	4201260
    # 638	4201260
    # 641	4201260
    # 650	4201260
    # 653	4201260
    # 654	4201260
    # 670	8402520
    # 675	4201260
    # 679	4201260
    # 688	4201260
    # 689	4201260
    # 692	8402520
    # 695	4201260
    # 696	4201260
    # 749	4201260
    # 751	4201260
    # 754	8402520
    # 757	4201260
    # 759	4201260
    # 819	4201260
    # 826	4201260
    # 827	4201260
    # 835	4201260
    # 849	8402520
    # 860	4201260
    # 873	4201260
    # 880	4201260
    # 888	4201260
    # 914	4201260
    # 924	4201260
    # 939	4201260
    # 954	4201260
    # 976	4201260
    # 990	4201260
    # 1021	4201260
    # 1037	4201260
    # 1046	4201260
    # 1059	4201260
    # 1089	4201260
    # 1091	4201260
    # 1093	4201260
    # 1096	4201260
    # 1109	4201260
    # 1115	4201260
    # 1127	4201260
    # 1152	4201260
    # 1155	4201260
    # 1168	4201260
    # 1178	4201260
    # 1191	4201260
    # 1274	4201260
    # 1302	4201260
    # 1327	4201260
    # 1368	4201260
    # 1409	4201260
    # 1410	4201260
    # 1422	4201260
    # 1435	4201260
    # 1481	4201260
    # 1499	4201260
    # 1661	4201260
    # 1767	4201260
    # 1913	4201260
    # 1916	4201260

# FIXME: OLD
    # 6	6108632040
    # 7	91931971320
    # 8	7360607520
    # 9	4138241100
    # 11	9802940
    # 12	735220500
    # 13	246473920
    # 14	383715080
    # 15	830449060
    # 16	1590877120
    # 17	294088200
    # 18	261878540
    # 19	183455020
    # 20	144243260
    # 21	99429820
    # 22	145643680
    # 23	233870140
    # 24	200260060
    # 25	261878540
    # 26	68620580
    # 27	102230660
    # 28	67220160
    # 29	43413020
    # 30	95228560
    # 31	33610080
    # 32	40612180
    # 33	42012600
    # 34	30809240
    # 35	22406720
    # 36	11203360
    # 37	9802940
    # 38	9802940
    # 39	12603780
    # 40	18205460
    # 41	19605880
    # 42	11203360
    # 43	11203360
    # 44	25207560
    # 45	9802940
    # 46	14004200
    # 47	25207560
    # 48	12603780
    # 49	19605880
    # 50	16805040
    # 51	21006300
    # 52	21006300
    # 53	15404620
    # 54	9802940
    # 55	12603780
    # 56	18205460
    # 57	12603780
    # 58	12603780
    # 59	16805040
    # 60	19605880
    # 61	16805040
    # 62	21006300
    # 63	29408820
    # 64	28008400
    # 65	15404620
    # 66	25207560
    # 67	22406720
    # 68	16805040
    # 69	19605880
    # 70	16805040
    # 71	28008400
    # 72	25207560
    # 73	16805040
    # 74	19605880
    # 75	19605880
    # 76	22406720
    # 77	21006300
    # 78	11203360
    # 79	19605880
    # 80	11203360
    # 81	18205460
    # 82	12603780
    # 83	11203360
    # 84	22406720
    # 85	15404620
    # 86	15404620
    # 87	9802940
    # 88	14004200
    # 89	12603780
    # 90	12603780
    # 91	23807140
    # 92	7002100
    # 93	15404620
    # 94	22406720
    # 95	9802940
    # 96	12603780
    # 97	14004200
    # 98	12603780
    # 99	14004200
    # 100	14004200
    # 101	14004200
    # 102	9802940
    # 103	15404620
    # 104	5601680
    # 105	11203360
    # 106	9802940
    # 107	14004200
    # 108	14004200
    # 109	9802940
    # 110	15404620
    # 111	5601680
    # 112	2800840
    # 113	7002100
    # 114	11203360
    # 115	2800840
    # 116	11203360
    # 117	11203360
    # 118	4201260
    # 119	8402520
    # 120	7002100
    # 121	2800840
    # 122	11203360
    # 123	7002100
    # 124	8402520
    # 125	7002100
    # 126	9802940
    # 127	1400420
    # 128	14004200
    # 129	5601680
    # 130	7002100
    # 131	5601680
    # 132	4201260
    # 133	4201260
    # 134	8402520
    # 135	7002100
    # 136	5601680
    # 137	4201260
    # 139	2800840
    # 140	1400420
    # 141	5601680
    # 142	4201260
    # 143	7002100
    # 144	4201260
    # 145	5601680
    # 146	1400420
    # 147	5601680
    # 148	2800840
    # 150	8402520
    # 151	4201260
    # 152	7002100
    # 153	5601680
    # 154	4201260
    # 155	5601680
    # 156	7002100
    # 157	4201260
    # 158	2800840
    # 159	4201260
    # 160	7002100
    # 161	1400420
    # 162	2800840
    # 163	5601680
    # 164	7002100
    # 165	1400420
    # 166	1400420
    # 167	1400420
    # 168	2800840
    # 169	2800840
    # 170	8402520
    # 171	1400420
    # 172	4201260
    # 173	4201260
    # 174	2800840
    # 175	7002100
    # 177	2800840
    # 178	7002100
    # 179	4201260
    # 181	1400420
    # 182	2800840
    # 183	5601680
    # 184	2800840
    # 185	2800840
    # 186	1400420
    # 187	4201260
    # 188	1400420
    # 189	1400420
    # 190	1400420
    # 191	2800840
    # 194	1400420
    # 195	1400420
    # 196	1400420
    # 197	2800840
    # 199	4201260
    # 200	1400420
    # 201	5601680
    # 203	4201260
    # 205	1400420
    # 206	1400420
    # 208	1400420
    # 209	2800840
    # 210	2800840
    # 212	4201260
    # 213	2800840
    # 215	1400420
    # 216	2800840
    # 217	1400420
    # 219	4201260
    # 220	2800840
    # 223	5601680
    # 224	1400420
    # 225	4201260
    # 227	1400420
    # 228	5601680
    # 229	5601680
    # 230	5601680
    # 232	2800840
    # 233	5601680
    # 234	9802940
    # 235	1400420
    # 236	9802940
    # 237	7002100
    # 238	7002100
    # 239	2800840
    # 240	1400420
    # 241	4201260
    # 242	7002100
    # 243	5601680
    # 244	5601680
    # 245	4201260
    # 246	7002100
    # 247	5601680
    # 248	5601680
    # 249	8402520
    # 250	4201260
    # 251	14004200
    # 252	5601680
    # 253	5601680
    # 254	12603780
    # 255	9802940
    # 256	11203360
    # 257	2800840
    # 258	8402520
    # 259	7002100
    # 260	7002100
    # 261	4201260
    # 262	7002100
    # 263	8402520
    # 264	7002100
    # 265	11203360
    # 266	8402520
    # 267	8402520
    # 268	5601680
    # 269	16805040
    # 270	5601680
    # 271	7002100
    # 272	11203360
    # 273	5601680
    # 274	4201260
    # 275	2800840
    # 276	5601680
    # 277	11203360
    # 278	8402520
    # 279	7002100
    # 280	7002100
    # 281	4201260
    # 282	8402520
    # 283	7002100
    # 284	11203360
    # 285	8402520
    # 286	4201260
    # 287	11203360
    # 288	2800840
    # 289	5601680
    # 290	4201260
    # 291	5601680
    # 292	4201260
    # 293	1400420
    # 294	2800840
    # 295	4201260
    # 296	7002100
    # 297	2800840
    # 299	4201260
    # 300	4201260
    # 301	5601680
    # 302	2800840
    # 303	1400420
    # 304	2800840
    # 305	5601680
    # 306	7002100
    # 307	5601680
    # 308	4201260
    # 309	1400420
    # 310	8402520
    # 311	4201260
    # 312	4201260
    # 313	1400420
    # 314	8402520
    # 315	5601680
    # 316	2800840
    # 317	4201260
    # 318	4201260
    # 319	5601680
    # 320	2800840
    # 321	5601680
    # 322	4201260
    # 323	2800840
    # 324	4201260
    # 325	2800840
    # 326	4201260
    # 327	1400420
    # 328	2800840
    # 329	2800840
    # 330	4201260
    # 331	1400420
    # 332	2800840
    # 333	2800840
    # 334	1400420
    # 336	2800840
    # 337	1400420
    # 338	2800840
    # 339	1400420
    # 340	5601680
    # 342	2800840
    # 343	1400420
    # 344	4201260
    # 345	4201260
    # 347	1400420
    # 348	2800840
    # 349	1400420
    # 350	2800840
    # 351	4201260
    # 352	2800840
    # 353	4201260
    # 354	2800840
    # 355	4201260
    # 356	2800840
    # 357	2800840
    # 358	1400420
    # 360	1400420
    # 361	1400420
    # 362	4201260
    # 363	1400420
    # 364	2800840
    # 365	1400420
    # 366	1400420
    # 367	2800840
    # 368	1400420
    # 369	5601680
    # 372	1400420
    # 375	1400420
    # 376	2800840
    # 378	1400420
    # 379	1400420
    # 380	7002100
    # 381	1400420
    # 382	2800840
    # 383	2800840
    # 384	2800840
    # 385	2800840
    # 387	2800840
    # 391	1400420
    # 394	2800840
    # 395	2800840
    # 396	1400420
    # 397	1400420
    # 398	2800840
    # 400	1400420
    # 401	5601680
    # 402	2800840
    # 403	1400420
    # 404	2800840
    # 405	1400420
    # 406	5601680
    # 407	4201260
    # 408	1400420
    # 409	4201260
    # 410	7002100
    # 411	5601680
    # 412	4201260
    # 413	5601680
    # 414	1400420
    # 415	1400420
    # 416	8402520
    # 417	1400420
    # 418	5601680
    # 419	5601680
    # 420	2800840
    # 421	1400420
    # 422	4201260
    # 423	1400420
    # 424	5601680
    # 425	1400420
    # 426	4201260
    # 427	1400420
    # 428	4201260
    # 429	5601680
    # 430	2800840
    # 431	1400420
    # 432	2800840
    # 433	5601680
    # 434	4201260
    # 435	4201260
    # 436	1400420
    # 437	4201260
    # 438	2800840
    # 439	9802940
    # 440	2800840
    # 441	1400420
    # 442	2800840
    # 443	8402520
    # 444	5601680
    # 445	4201260
    # 446	8402520
    # 447	7002100
    # 448	11203360
    # 449	4201260
    # 450	1400420
    # 451	8402520
    # 452	2800840
    # 453	2800840
    # 454	7002100
    # 455	7002100
    # 456	4201260
    # 457	2800840
    # 458	8402520
    # 459	2800840
    # 460	1400420
    # 461	5601680
    # 462	5601680
    # 463	4201260
    # 464	4201260
    # 465	1400420
    # 466	9802940
    # 467	1400420
    # 468	4201260
    # 469	11203360
    # 470	1400420
    # 471	2800840
    # 472	4201260
    # 473	5601680
    # 474	7002100
    # 475	2800840
    # 476	9802940
    # 477	5601680
    # 478	4201260
    # 479	4201260
    # 480	2800840
    # 481	7002100
    # 482	2800840
    # 483	1400420
    # 484	4201260
    # 485	9802940
    # 486	4201260
    # 488	5601680
    # 489	2800840
    # 490	4201260
    # 491	5601680
    # 492	8402520
    # 493	2800840
    # 494	5601680
    # 495	2800840
    # 496	2800840
    # 497	5601680
    # 498	4201260
    # 499	7002100
    # 500	7002100
    # 501	5601680
    # 502	2800840
    # 503	1400420
    # 504	4201260
    # 505	4201260
    # 506	5601680
    # 507	7002100
    # 508	2800840
    # 509	1400420
    # 510	5601680
    # 511	1400420
    # 512	5601680
    # 513	2800840
    # 514	1400420
    # 515	2800840
    # 516	2800840
    # 517	4201260
    # 518	4201260
    # 519	4201260
    # 520	4201260
    # 521	4201260
    # 522	5601680
    # 523	2800840
    # 524	2800840
    # 525	1400420
    # 527	2800840
    # 528	5601680
    # 529	1400420
    # 530	1400420
    # 532	7002100
    # 533	5601680
    # 535	1400420
    # 536	1400420
    # 537	1400420
    # 538	1400420
    # 539	2800840
    # 540	1400420
    # 541	4201260
    # 543	1400420
    # 544	4201260
    # 545	2800840
    # 546	1400420
    # 547	5601680
    # 549	2800840
    # 550	2800840
    # 551	1400420
    # 552	1400420
    # 553	1400420
    # 554	1400420
    # 555	1400420
    # 556	2800840
    # 557	5601680
    # 558	1400420
    # 560	2800840
    # 561	1400420
    # 563	2800840
    # 564	4201260
    # 565	1400420
    # 566	4201260
    # 568	1400420
    # 569	4201260
    # 570	2800840
    # 572	1400420
    # 573	2800840
    # 574	1400420
    # 575	2800840
    # 576	4201260
    # 577	2800840
    # 578	4201260
    # 579	1400420
    # 583	2800840
    # 584	2800840
    # 585	2800840
    # 586	2800840
    # 588	1400420
    # 590	1400420
    # 591	2800840
    # 593	2800840
    # 596	2800840
    # 597	1400420
    # 598	1400420
    # 599	2800840
    # 600	1400420
    # 601	1400420
    # 602	1400420
    # 603	1400420
    # 604	1400420
    # 605	2800840
    # 606	2800840
    # 608	1400420
    # 609	2800840
    # 610	1400420
    # 611	1400420
    # 613	4201260
    # 614	1400420
    # 616	2800840
    # 619	1400420
    # 620	2800840
    # 621	1400420
    # 623	2800840
    # 625	1400420
    # 626	1400420
    # 629	1400420
    # 631	1400420
    # 632	1400420
    # 633	1400420
    # 634	2800840
    # 635	5601680
    # 638	2800840
    # 639	1400420
    # 640	1400420
    # 641	1400420
    # 644	1400420
    # 645	2800840
    # 646	1400420
    # 648	2800840
    # 649	1400420
    # 650	1400420
    # 651	2800840
    # 652	1400420
    # 653	2800840
    # 654	1400420
    # 656	1400420
    # 657	1400420
    # 658	1400420
    # 659	2800840
    # 661	4201260
    # 663	1400420
    # 664	1400420
    # 665	1400420
    # 667	1400420
    # 672	1400420
    # 673	2800840
    # 675	1400420
    # 677	1400420
    # 679	1400420
    # 682	2800840
    # 683	1400420
    # 685	2800840
    # 686	4201260
    # 687	1400420
    # 690	2800840
    # 691	1400420
    # 692	1400420
    # 694	4201260
    # 698	1400420
    # 699	2800840
    # 700	1400420
    # 701	1400420
    # 702	1400420
    # 703	1400420
    # 705	1400420
    # 706	1400420
    # 707	1400420
    # 708	2800840
    # 709	1400420
    # 712	1400420
    # 714	1400420
    # 717	1400420
    # 720	1400420
    # 727	1400420
    # 729	2800840
    # 730	2800840
    # 731	1400420
    # 732	1400420
    # 736	1400420
    # 739	1400420
    # 740	1400420
    # 741	1400420
    # 745	1400420
    # 747	1400420
    # 748	4201260
    # 749	2800840
    # 750	1400420
    # 752	2800840
    # 753	1400420
    # 755	1400420
    # 759	2800840
    # 761	4201260
    # 764	1400420
    # 766	1400420
    # 767	1400420
    # 769	1400420
    # 770	1400420
    # 772	2800840
    # 773	2800840
    # 777	1400420
    # 779	1400420
    # 781	1400420
    # 783	1400420
    # 784	2800840
    # 785	1400420
    # 787	1400420
    # 788	1400420
    # 791	1400420
    # 792	1400420
    # 793	2800840
    # 795	1400420
    # 796	1400420
    # 797	1400420
    # 803	1400420
    # 804	2800840
    # 806	1400420
    # 808	1400420
    # 813	1400420
    # 818	2800840
    # 819	1400420
    # 821	2800840
    # 825	2800840
    # 828	2800840
    # 831	1400420
    # 838	1400420
    # 840	1400420
    # 842	1400420
    # 844	2800840
    # 847	1400420
    # 848	2800840
    # 857	1400420
    # 858	1400420
    # 862	1400420
    # 864	1400420
    # 865	1400420
    # 866	1400420
    # 867	1400420
    # 868	1400420
    # 871	1400420
    # 872	2800840
    # 873	1400420
    # 877	1400420
    # 879	1400420
    # 880	2800840
    # 892	1400420
    # 895	1400420
    # 898	1400420
    # 901	1400420
    # 908	2800840
    # 915	1400420
    # 926	1400420
    # 930	1400420
    # 941	1400420
    # 948	1400420
    # 950	1400420
    # 982	1400420
    # 1000	1400420
    # 1003	1400420
    # 1004	2800840
    # 1005	1400420
    # 1008	1400420
    # 1016	1400420
    # 1018	1400420
    # 1020	1400420
    # 1021	1400420
    # 1037	2800840
    # 1044	2800840
    # 1045	2800840
    # 1050	1400420
    # 1054	1400420
    # 1069	1400420
    # 1070	1400420
    # 1071	1400420
    # 1073	1400420
    # 1074	1400420
    # 1075	1400420
    # 1090	1400420
    # 1094	1400420
    # 1102	1400420
    # 1103	1400420
    # 1107	1400420
    # 1110	1400420
    # 1113	1400420
    # 1119	1400420
    # 1122	1400420
    # 1129	1400420
    # 1133	1400420
    # 1143	1400420
    # 1150	1400420
    # 1170	2800840
    # 1173	1400420
    # 1175	1400420
    # 1179	1400420
    # 1181	1400420
    # 1185	1400420
    # 1187	1400420
    # 1194	2800840
    # 1197	1400420
    # 1198	1400420
    # 1199	1400420
    # 1212	1400420
    # 1218	2800840
    # 1233	1400420
    # 1244	2800840
    # 1247	1400420
    # 1263	1400420
    # 1274	1400420
    # 1287	1400420
    # 1294	1400420
    # 1295	1400420
    # 1296	1400420
    # 1300	1400420
    # 1310	1400420
    # 1313	1400420
    # 1322	1400420
    # 1329	1400420
    # 1341	1400420
    # 1344	1400420
    # 1345	1400420
    # 1349	1400420
    # 1361	1400420
    # 1367	1400420
    # 1368	1400420
    # 1372	1400420
    # 1374	1400420
    # 1375	1400420
    # 1380	1400420
    # 1383	1400420
    # 1395	1400420
    # 1396	1400420
    # 1398	1400420
    # 1399	1400420
    # 1405	1400420
    # 1407	1400420
    # 1408	1400420
    # 1410	1400420
    # 1418	1400420
    # 1420	1400420
    # 1421	1400420
    # 1425	1400420
    # 1427	1400420
    # 1448	1400420
    # 1487	1400420
    # 1495	1400420
    # 1499	1400420
    # 1501	1400420
    # 1509	1400420
    # 1513	1400420
    # 1514	1400420
    # 1521	1400420
    # 1522	1400420
    # 1533	1400420
    # 1560	1400420
    # 1629	1400420
    # 1634	1400420
    # 1682	1400420
    # 1709	1400420
    # 1712	1400420
    # 1718	1400420
    # 1747	1400420
    # 1753	1400420
    # 1759	1400420
    # 1768	1400420
    # 1782	1400420
    # 1837	1400420
    # 1844	1400420
    # 1860	1400420
    # 1958	1400420
    # 1962	1400420
    # 1968	1400420
    # 2065	1400420
    # 2104	1400420
    # 2174	1400420
    # 2196	1400420
    # 2257	1400420
    # 2325	1400420
    # 2399	1400420
    # 2578	1400420
    # 2591	1400420
    # 2613	1400420
    # 2725	1400420
    # 2767	1400420
    # 2824	1400420
    # 2926	1400420
    # 2954	1400420
    # 2964	1400420
    # 3016	1400420
    # 3339	1400420
    # 3580	1400420
    # 3678	1400420
    # 3732	1400420
    # 4014	1400420
    # 4045	1400420
    # 4049	1400420


moliere2016_t192_latency_pdax_str = """
    Latency	Loads
    6	14950883920
    7	101709703760
    8	7469840280
    9	8877262380
    11	14004200
    12	700210000
    13	210063000
    14	411723480
    15	826247800
    16	1575472500
    17	301090300
    18	326297860
    19	172251660
    20	168050400
    21	117635280
    22	184855440
    23	212863840
    24	198859640
    25	270281060
    26	96628980
    27	86826040
    28	57417220
    29	29408820
    30	88226460
    31	40612180
    32	29408820
    33	32209660
    34	25207560
    35	22406720
    36	9802940
    37	21006300
    38	15404620
    39	19605880
    40	16805040
    41	15404620
    42	14004200
    43	18205460
    44	19605880
    45	12603780
    46	14004200
    47	14004200
    48	11203360
    49	12603780
    50	11203360
    51	26607980
    52	12603780
    53	22406720
    54	7002100
    55	16805040
    56	12603780
    57	19605880
    58	9802940
    59	9802940
    60	14004200
    61	15404620
    62	19605880
    63	18205460
    64	18205460
    65	16805040
    66	14004200
    67	15404620
    68	16805040
    69	18205460
    70	18205460
    71	30809240
    72	22406720
    73	19605880
    74	23807140
    75	19605880
    76	11203360
    77	16805040
    78	18205460
    79	16805040
    80	11203360
    81	25207560
    82	16805040
    83	11203360
    84	9802940
    85	14004200
    86	14004200
    87	14004200
    88	15404620
    89	12603780
    90	16805040
    91	11203360
    92	11203360
    93	12603780
    94	8402520
    95	5601680
    96	11203360
    97	9802940
    98	9802940
    99	11203360
    100	11203360
    101	11203360
    102	14004200
    103	9802940
    104	16805040
    105	9802940
    106	12603780
    107	8402520
    108	9802940
    109	7002100
    110	8402520
    111	14004200
    112	7002100
    113	12603780
    114	9802940
    115	4201260
    116	2800840
    117	7002100
    118	7002100
    119	5601680
    120	4201260
    121	7002100
    122	4201260
    123	7002100
    124	1400420
    125	1400420
    126	5601680
    127	7002100
    128	4201260
    129	1400420
    130	1400420
    131	2800840
    132	5601680
    133	5601680
    134	4201260
    135	2800840
    136	1400420
    137	2800840
    138	2800840
    139	4201260
    140	1400420
    141	4201260
    142	4201260
    143	1400420
    144	2800840
    145	5601680
    146	5601680
    147	5601680
    148	5601680
    150	2800840
    151	4201260
    152	1400420
    153	4201260
    154	5601680
    155	2800840
    156	4201260
    157	1400420
    158	4201260
    159	4201260
    160	2800840
    161	2800840
    162	4201260
    163	1400420
    164	4201260
    165	1400420
    166	2800840
    167	4201260
    169	2800840
    170	4201260
    171	2800840
    172	2800840
    173	2800840
    174	2800840
    175	2800840
    176	2800840
    177	1400420
    178	2800840
    179	2800840
    180	4201260
    181	1400420
    182	2800840
    183	2800840
    185	1400420
    186	1400420
    187	1400420
    188	1400420
    189	5601680
    190	2800840
    191	1400420
    192	2800840
    193	1400420
    194	1400420
    195	2800840
    196	4201260
    198	2800840
    201	1400420
    202	2800840
    203	1400420
    204	1400420
    205	4201260
    206	2800840
    208	1400420
    210	4201260
    211	1400420
    212	2800840
    215	2800840
    217	2800840
    218	4201260
    219	1400420
    220	4201260
    221	2800840
    222	2800840
    223	7002100
    224	2800840
    226	1400420
    228	4201260
    229	4201260
    230	4201260
    232	5601680
    233	1400420
    234	2800840
    235	5601680
    236	8402520
    237	8402520
    238	5601680
    239	7002100
    240	5601680
    241	2800840
    242	4201260
    243	12603780
    244	9802940
    245	4201260
    246	5601680
    247	4201260
    248	8402520
    249	9802940
    250	2800840
    251	7002100
    252	8402520
    253	2800840
    254	2800840
    255	8402520
    256	7002100
    257	7002100
    258	11203360
    259	2800840
    260	8402520
    261	2800840
    262	5601680
    263	4201260
    264	4201260
    265	2800840
    266	5601680
    267	5601680
    268	7002100
    269	4201260
    270	5601680
    271	2800840
    272	4201260
    273	8402520
    274	5601680
    275	5601680
    276	5601680
    277	7002100
    278	8402520
    279	5601680
    280	9802940
    281	4201260
    282	8402520
    283	2800840
    284	7002100
    285	8402520
    286	9802940
    287	5601680
    288	8402520
    289	2800840
    290	4201260
    291	9802940
    292	4201260
    293	18205460
    294	7002100
    295	7002100
    296	8402520
    297	5601680
    298	8402520
    299	9802940
    300	4201260
    301	2800840
    302	1400420
    303	4201260
    304	7002100
    305	4201260
    306	4201260
    307	1400420
    308	2800840
    311	8402520
    312	5601680
    313	5601680
    315	9802940
    317	5601680
    318	4201260
    319	8402520
    321	2800840
    322	1400420
    324	2800840
    326	2800840
    327	1400420
    328	1400420
    329	1400420
    330	4201260
    331	1400420
    332	7002100
    333	4201260
    334	1400420
    335	1400420
    336	1400420
    337	5601680
    338	1400420
    339	1400420
    340	2800840
    341	4201260
    342	2800840
    344	2800840
    345	1400420
    346	2800840
    347	4201260
    348	5601680
    349	2800840
    350	4201260
    351	4201260
    352	2800840
    354	2800840
    355	2800840
    356	7002100
    357	2800840
    358	2800840
    360	2800840
    361	4201260
    362	1400420
    363	1400420
    364	1400420
    365	4201260
    366	1400420
    368	2800840
    369	1400420
    370	1400420
    371	1400420
    372	4201260
    373	1400420
    374	1400420
    375	5601680
    377	2800840
    378	4201260
    379	1400420
    380	5601680
    381	1400420
    382	2800840
    383	2800840
    384	2800840
    386	5601680
    387	2800840
    388	2800840
    389	1400420
    390	1400420
    391	1400420
    392	1400420
    393	1400420
    395	1400420
    396	5601680
    397	1400420
    398	7002100
    399	1400420
    400	4201260
    401	2800840
    402	1400420
    403	2800840
    404	1400420
    405	2800840
    406	1400420
    407	4201260
    408	5601680
    409	2800840
    410	2800840
    411	5601680
    412	1400420
    414	2800840
    415	2800840
    416	7002100
    417	5601680
    418	2800840
    419	2800840
    420	1400420
    421	2800840
    422	1400420
    423	8402520
    424	4201260
    425	4201260
    426	4201260
    427	5601680
    428	5601680
    429	2800840
    430	7002100
    431	4201260
    432	5601680
    433	7002100
    434	7002100
    435	2800840
    436	4201260
    437	7002100
    438	2800840
    439	1400420
    440	8402520
    442	4201260
    443	1400420
    444	8402520
    446	1400420
    447	2800840
    448	7002100
    449	4201260
    450	8402520
    451	5601680
    452	7002100
    453	4201260
    454	2800840
    455	7002100
    456	9802940
    457	1400420
    458	1400420
    459	12603780
    460	5601680
    461	4201260
    462	4201260
    463	4201260
    464	2800840
    465	5601680
    466	2800840
    467	7002100
    468	2800840
    469	2800840
    470	5601680
    471	8402520
    472	4201260
    474	8402520
    475	4201260
    476	7002100
    477	2800840
    478	7002100
    479	9802940
    480	4201260
    481	2800840
    482	4201260
    483	12603780
    484	1400420
    485	2800840
    486	5601680
    487	1400420
    488	2800840
    489	4201260
    490	5601680
    491	2800840
    492	1400420
    493	1400420
    494	2800840
    495	4201260
    496	5601680
    497	1400420
    498	2800840
    499	1400420
    500	4201260
    501	4201260
    502	4201260
    503	2800840
    504	4201260
    505	2800840
    506	8402520
    507	4201260
    508	5601680
    509	1400420
    510	4201260
    511	2800840
    512	4201260
    513	2800840
    514	7002100
    515	2800840
    516	4201260
    517	5601680
    518	2800840
    519	4201260
    520	2800840
    521	4201260
    522	4201260
    523	2800840
    524	4201260
    525	1400420
    526	2800840
    527	2800840
    528	1400420
    529	4201260
    531	7002100
    532	7002100
    533	1400420
    535	4201260
    536	4201260
    537	4201260
    538	11203360
    539	2800840
    540	2800840
    541	7002100
    542	1400420
    543	5601680
    545	4201260
    546	4201260
    547	5601680
    548	1400420
    549	5601680
    550	4201260
    552	2800840
    553	1400420
    554	1400420
    555	1400420
    556	1400420
    557	4201260
    558	4201260
    559	1400420
    560	1400420
    561	1400420
    562	1400420
    563	2800840
    564	2800840
    565	1400420
    566	2800840
    568	4201260
    569	2800840
    570	1400420
    571	2800840
    572	2800840
    573	2800840
    574	4201260
    575	1400420
    576	2800840
    578	1400420
    579	4201260
    580	1400420
    581	1400420
    582	2800840
    584	1400420
    586	5601680
    587	1400420
    588	1400420
    591	4201260
    592	4201260
    593	2800840
    595	1400420
    596	2800840
    597	1400420
    598	4201260
    602	8402520
    603	1400420
    604	1400420
    605	1400420
    607	1400420
    608	5601680
    609	4201260
    610	1400420
    612	2800840
    614	2800840
    618	1400420
    619	4201260
    620	4201260
    621	2800840
    623	2800840
    624	1400420
    625	4201260
    626	1400420
    627	2800840
    628	1400420
    630	1400420
    632	2800840
    633	1400420
    634	4201260
    635	1400420
    636	2800840
    638	1400420
    639	1400420
    642	1400420
    644	2800840
    646	1400420
    647	4201260
    648	2800840
    649	1400420
    650	2800840
    653	1400420
    655	4201260
    658	1400420
    660	2800840
    662	1400420
    666	1400420
    669	4201260
    670	1400420
    671	1400420
    672	2800840
    675	1400420
    677	1400420
    679	4201260
    680	1400420
    682	1400420
    684	2800840
    686	2800840
    690	1400420
    692	1400420
    693	1400420
    697	1400420
    699	1400420
    709	1400420
    712	2800840
    715	1400420
    717	2800840
    718	1400420
    719	1400420
    721	2800840
    725	2800840
    726	1400420
    728	1400420
    729	1400420
    731	2800840
    732	4201260
    734	4201260
    739	2800840
    745	1400420
    747	1400420
    748	1400420
    751	2800840
    752	2800840
    754	2800840
    755	1400420
    756	1400420
    757	1400420
    758	1400420
    760	2800840
    762	1400420
    767	1400420
    768	1400420
    770	1400420
    773	1400420
    775	1400420
    779	1400420
    781	1400420
    783	1400420
    786	2800840
    788	2800840
    791	1400420
    796	2800840
    797	1400420
    799	2800840
    801	4201260
    802	2800840
    803	1400420
    806	1400420
    807	1400420
    809	1400420
    814	1400420
    815	2800840
    817	1400420
    818	2800840
    821	1400420
    822	2800840
    824	1400420
    826	1400420
    828	1400420
    829	2800840
    830	1400420
    831	2800840
    836	1400420
    839	1400420
    843	1400420
    846	1400420
    847	2800840
    848	1400420
    850	1400420
    851	2800840
    855	2800840
    858	1400420
    859	1400420
    860	1400420
    874	1400420
    883	1400420
    884	1400420
    887	1400420
    890	4201260
    891	1400420
    892	1400420
    894	2800840
    896	1400420
    899	1400420
    900	1400420
    903	1400420
    906	1400420
    908	2800840
    919	1400420
    923	1400420
    932	1400420
    933	1400420
    935	1400420
    941	1400420
    942	1400420
    945	1400420
    948	1400420
    956	1400420
    957	2800840
    962	1400420
    963	1400420
    964	1400420
    965	1400420
    967	1400420
    970	1400420
    977	2800840
    980	1400420
    981	1400420
    982	1400420
    983	1400420
    997	1400420
    1002	1400420
    1005	1400420
    1008	2800840
    1009	1400420
    1021	1400420
    1022	2800840
    1028	1400420
    1031	1400420
    1033	1400420
    1035	1400420
    1041	1400420
    1042	1400420
    1047	1400420
    1048	1400420
    1050	1400420
    1051	1400420
    1054	1400420
    1055	1400420
    1062	1400420
    1072	1400420
    1076	1400420
    1077	1400420
    1080	1400420
    1081	1400420
    1086	1400420
    1094	1400420
    1096	1400420
    1101	1400420
    1102	2800840
    1103	2800840
    1105	1400420
    1107	1400420
    1108	1400420
    1109	1400420
    1112	1400420
    1114	1400420
    1121	1400420
    1130	1400420
    1144	1400420
    1152	1400420
    1154	2800840
    1158	1400420
    1162	2800840
    1163	1400420
    1167	1400420
    1174	1400420
    1176	1400420
    1190	1400420
    1191	1400420
    1201	1400420
    1202	1400420
    1213	1400420
    1219	1400420
    1223	1400420
    1247	1400420
    1248	1400420
    1254	1400420
    1259	1400420
    1263	1400420
    1272	1400420
    1279	1400420
    1288	1400420
    1290	1400420
    1291	1400420
    1292	1400420
    1305	1400420
    1311	1400420
    1315	1400420
    1328	1400420
    1348	1400420
    1354	1400420
    1393	1400420
    1406	1400420
    1410	1400420
    1416	1400420
    1421	1400420
    1428	1400420
    1433	1400420
    1444	1400420
    1446	1400420
    1457	1400420
    1463	1400420
    1470	1400420
    1476	1400420
    1484	1400420
    1487	1400420
    1500	1400420
    1516	1400420
    1524	1400420
    1531	1400420
    1538	1400420
    1611	1400420
    1612	1400420
    1626	1400420
    1632	1400420
    1634	1400420
    1642	1400420
    1650	1400420
    1666	1400420
    1683	1400420
    1710	1400420
    1713	1400420
    1723	1400420
    1741	1400420
    1748	1400420
    1763	1400420
    1768	1400420
    1839	1400420
    1923	1400420
    1965	1400420
    1980	1400420
    2000	1400420
    2006	1400420
    2029	1400420
    2039	1400420
    2193	1400420
    2243	1400420
    2342	1400420
    2389	1400420
    2540	1400420
    2555	1400420
    2608	1400420
    2967	1400420
    3117	1400420
    3125	1400420
    3326	1400420
    3346	1400420
    3367	1400420
    3413	1400420
    4034	1400420
"""

moliere2016_t192_latency_kdax_str = """
    Latency	Loads
    6	6885865140
    7	105346594500
    8	6856456320
    9	4264278900
    11	16805040
    12	802440660
    13	214264260
    14	575572620
    15	613383960
    16	1520856120
    17	340302060
    18	226868040
    19	163849140
    20	142842840
    21	113434020
    22	88226460
    23	109232760
    24	159647880
    25	256276860
    26	96628980
    27	96628980
    28	58817640
    29	50415120
    30	96628980
    31	16805040
    32	21006300
    33	37811340
    34	25207560
    35	4201260
    36	16805040
    37	21006300
    38	21006300
    39	8402520
    40	16805040
    41	21006300
    42	21006300
    43	12603780
    44	8402520
    45	21006300
    46	21006300
    47	21006300
    48	16805040
    49	8402520
    50	21006300
    51	12603780
    54	16805040
    55	8402520
    56	21006300
    57	16805040
    58	8402520
    59	25207560
    60	16805040
    61	16805040
    62	12603780
    63	29408820
    64	12603780
    65	16805040
    66	8402520
    67	21006300
    68	21006300
    69	21006300
    70	4201260
    71	21006300
    72	21006300
    73	21006300
    74	16805040
    75	25207560
    76	21006300
    77	4201260
    78	16805040
    79	21006300
    80	21006300
    81	12603780
    83	12603780
    84	4201260
    85	33610080
    86	12603780
    88	12603780
    89	4201260
    91	8402520
    92	8402520
    94	4201260
    95	12603780
    96	4201260
    97	12603780
    99	4201260
    100	12603780
    101	4201260
    102	8402520
    103	4201260
    104	8402520
    108	21006300
    110	12603780
    111	12603780
    112	8402520
    113	12603780
    115	12603780
    118	4201260
    119	16805040
    120	4201260
    122	4201260
    123	8402520
    124	8402520
    125	8402520
    126	4201260
    129	8402520
    130	4201260
    131	4201260
    133	4201260
    136	8402520
    137	4201260
    138	4201260
    140	4201260
    141	8402520
    143	4201260
    144	8402520
    146	4201260
    147	12603780
    148	4201260
    150	12603780
    151	4201260
    153	4201260
    154	8402520
    155	4201260
    156	4201260
    157	4201260
    158	16805040
    160	12603780
    162	4201260
    164	4201260
    165	8402520
    166	8402520
    169	4201260
    170	8402520
    171	4201260
    172	4201260
    173	4201260
    179	4201260
    180	4201260
    182	8402520
    183	4201260
    185	4201260
    187	8402520
    195	4201260
    196	4201260
    198	4201260
    199	8402520
    202	4201260
    205	4201260
    207	8402520
    209	4201260
    211	8402520
    212	4201260
    217	4201260
    220	4201260
    226	4201260
    227	4201260
    228	4201260
    229	4201260
    231	8402520
    232	4201260
    233	8402520
    234	4201260
    235	4201260
    236	4201260
    237	4201260
    240	8402520
    241	4201260
    243	4201260
    244	4201260
    245	8402520
    250	4201260
    251	4201260
    253	12603780
    254	12603780
    255	4201260
    256	4201260
    257	8402520
    258	21006300
    259	4201260
    260	8402520
    261	8402520
    262	12603780
    263	12603780
    265	4201260
    266	8402520
    267	12603780
    269	4201260
    270	4201260
    271	8402520
    272	12603780
    273	12603780
    274	4201260
    275	12603780
    276	8402520
    277	16805040
    278	4201260
    279	8402520
    280	4201260
    281	4201260
    283	4201260
    284	4201260
    285	8402520
    286	4201260
    287	4201260
    288	8402520
    289	4201260
    292	8402520
    293	8402520
    294	8402520
    297	12603780
    298	4201260
    300	4201260
    301	4201260
    303	4201260
    304	4201260
    305	4201260
    306	4201260
    307	4201260
    308	4201260
    311	4201260
    312	8402520
    314	12603780
    315	8402520
    322	4201260
    328	4201260
    329	4201260
    332	8402520
    333	12603780
    336	4201260
    338	4201260
    340	4201260
    341	4201260
    342	16805040
    343	4201260
    345	4201260
    346	4201260
    354	4201260
    356	4201260
    358	4201260
    365	8402520
    368	4201260
    370	4201260
    373	4201260
    375	4201260
    376	12603780
    377	8402520
    378	4201260
    379	8402520
    381	4201260
    382	4201260
    386	4201260
    387	4201260
    390	8402520
    395	4201260
    396	4201260
    402	4201260
    405	4201260
    406	8402520
    407	4201260
    408	4201260
    410	4201260
    411	4201260
    412	4201260
    413	4201260
    414	4201260
    418	4201260
    419	4201260
    421	8402520
    422	4201260
    423	12603780
    424	4201260
    425	8402520
    427	8402520
    428	12603780
    430	8402520
    431	8402520
    433	8402520
    434	4201260
    436	4201260
    438	12603780
    441	4201260
    442	4201260
    443	8402520
    444	8402520
    445	8402520
    446	4201260
    447	4201260
    448	4201260
    449	4201260
    450	8402520
    451	8402520
    452	4201260
    453	8402520
    454	4201260
    455	4201260
    456	4201260
    459	4201260
    460	8402520
    461	4201260
    462	4201260
    463	4201260
    464	8402520
    466	4201260
    468	4201260
    469	4201260
    473	12603780
    474	8402520
    477	8402520
    478	12603780
    481	4201260
    482	4201260
    484	12603780
    486	4201260
    487	12603780
    489	4201260
    492	4201260
    493	8402520
    494	4201260
    495	4201260
    496	4201260
    497	8402520
    498	4201260
    501	8402520
    504	8402520
    506	8402520
    508	4201260
    509	16805040
    510	8402520
    513	16805040
    516	4201260
    517	4201260
    519	4201260
    520	8402520
    522	8402520
    526	8402520
    531	16805040
    535	4201260
    541	4201260
    542	4201260
    544	4201260
    545	4201260
    548	8402520
    549	4201260
    555	4201260
    558	4201260
    560	8402520
    564	4201260
    565	4201260
    567	8402520
    570	4201260
    571	4201260
    572	4201260
    573	4201260
    575	4201260
    586	4201260
    589	4201260
    590	12603780
    592	4201260
    594	4201260
    598	8402520
    600	4201260
    602	4201260
    603	8402520
    605	4201260
    606	4201260
    607	4201260
    610	4201260
    611	4201260
    617	4201260
    620	4201260
    624	4201260
    627	8402520
    630	4201260
    638	4201260
    639	4201260
    641	4201260
    642	4201260
    649	4201260
    654	4201260
    656	4201260
    661	4201260
    665	4201260
    684	8402520
    687	4201260
    697	4201260
    701	4201260
    704	8402520
    705	4201260
    718	4201260
    721	4201260
    725	4201260
    737	4201260
    751	4201260
    765	4201260
    771	8402520
    786	4201260
    787	4201260
    794	4201260
    841	4201260
    865	4201260
    869	4201260
    870	4201260
    882	4201260
    902	4201260
    983	4201260
    1006	4201260
    1021	4201260
    1049	4201260
    1050	4201260
    1069	4201260
    1076	4201260
    1083	4201260
    1084	4201260
    1098	4201260
    1141	4201260
    1164	4201260
    1166	4201260
    1192	4201260
    1195	4201260
    1213	4201260
    1245	4201260
    1263	4201260
    1278	4201260
    1280	4201260
    1313	4201260
    1324	4201260
    1382	4201260
    1401	4201260
    1402	4201260
    1417	4201260
    1463	4201260
    1472	4201260
    1498	4201260
    1525	4201260
    1538	4201260
    1553	4201260
    1561	4201260
    1639	4201260
    1767	4201260
    1805	4201260
    1840	4201260
    1877	4201260
    1997	4201260
    2000	4201260
    2375	4201260
    2894	4201260
"""

moliere2016_t192_latency_mem_str = """
    Latency	Loads
    6	7108531920
    7	91847946120
    8	5869160220
    9	3764328960
    11	12603780
    12	806641920
    13	138641580
    14	537761280
    15	588176400
    16	1268780520
    17	218465520
    18	163849140
    19	142842840
    20	121836540
    21	63018900
    22	130239060
    23	163849140
    24	134440320
    25	231069300
    26	63018900
    27	79823940
    28	33610080
    29	54616380
    30	92427720
    31	12603780
    32	42012600
    33	29408820
    34	21006300
    35	21006300
    36	16805040
    37	8402520
    38	33610080
    39	33610080
    40	21006300
    41	21006300
    42	16805040
    43	12603780
    44	21006300
    45	29408820
    46	12603780
    47	21006300
    48	16805040
    49	4201260
    50	4201260
    51	8402520
    52	12603780
    53	46213860
    54	4201260
    55	16805040
    56	4201260
    57	29408820
    58	16805040
    59	12603780
    60	21006300
    61	46213860
    62	21006300
    63	8402520
    64	16805040
    65	29408820
    66	21006300
    67	21006300
    68	12603780
    69	37811340
    70	29408820
    71	16805040
    72	33610080
    73	21006300
    74	4201260
    75	16805040
    76	16805040
    77	25207560
    78	21006300
    80	21006300
    81	4201260
    82	12603780
    83	8402520
    84	21006300
    85	16805040
    86	29408820
    87	21006300
    89	12603780
    90	12603780
    91	4201260
    92	8402520
    93	16805040
    94	8402520
    95	4201260
    96	21006300
    97	8402520
    98	16805040
    99	21006300
    100	8402520
    102	4201260
    103	8402520
    104	8402520
    105	8402520
    106	8402520
    107	4201260
    108	8402520
    109	4201260
    110	4201260
    111	16805040
    112	4201260
    113	12603780
    116	8402520
    117	4201260
    118	4201260
    119	8402520
    120	4201260
    122	4201260
    123	8402520
    124	4201260
    126	8402520
    127	8402520
    129	4201260
    132	4201260
    133	8402520
    136	4201260
    137	12603780
    138	8402520
    140	4201260
    143	4201260
    146	4201260
    148	4201260
    149	8402520
    151	4201260
    152	8402520
    153	8402520
    154	8402520
    156	4201260
    157	4201260
    158	8402520
    160	8402520
    162	4201260
    163	8402520
    164	4201260
    165	4201260
    166	4201260
    168	8402520
    170	4201260
    173	4201260
    175	4201260
    176	8402520
    177	4201260
    178	4201260
    179	4201260
    180	4201260
    181	4201260
    182	8402520
    183	4201260
    185	4201260
    187	4201260
    188	4201260
    191	4201260
    192	4201260
    193	8402520
    194	4201260
    195	4201260
    197	4201260
    198	8402520
    199	8402520
    204	4201260
    207	4201260
    208	8402520
    212	12603780
    215	4201260
    216	4201260
    217	8402520
    224	8402520
    235	4201260
    236	4201260
    240	4201260
    241	8402520
    245	12603780
    246	8402520
    247	4201260
    248	4201260
    249	4201260
    250	8402520
    251	12603780
    252	12603780
    253	16805040
    255	8402520
    256	4201260
    257	12603780
    258	4201260
    259	8402520
    260	16805040
    261	4201260
    262	4201260
    263	8402520
    264	12603780
    265	12603780
    266	8402520
    267	12603780
    268	8402520
    269	4201260
    270	8402520
    272	12603780
    273	4201260
    274	12603780
    275	12603780
    277	12603780
    279	8402520
    280	8402520
    282	8402520
    283	4201260
    284	4201260
    286	4201260
    287	4201260
    288	8402520
    289	8402520
    290	8402520
    293	12603780
    299	4201260
    304	8402520
    305	8402520
    308	4201260
    310	4201260
    312	4201260
    315	4201260
    316	4201260
    321	4201260
    324	4201260
    325	4201260
    329	4201260
    333	4201260
    339	4201260
    341	8402520
    345	8402520
    346	8402520
    347	4201260
    350	12603780
    352	8402520
    353	4201260
    360	4201260
    367	4201260
    370	4201260
    373	4201260
    375	8402520
    381	8402520
    385	8402520
    386	8402520
    389	4201260
    390	8402520
    393	8402520
    395	4201260
    396	8402520
    398	4201260
    399	4201260
    400	8402520
    401	4201260
    417	8402520
    420	4201260
    421	4201260
    423	4201260
    424	4201260
    425	4201260
    426	4201260
    427	4201260
    428	4201260
    429	4201260
    431	4201260
    432	4201260
    435	8402520
    436	12603780
    437	4201260
    438	8402520
    439	8402520
    440	12603780
    441	4201260
    443	4201260
    445	4201260
    446	4201260
    451	16805040
    452	8402520
    454	8402520
    455	4201260
    456	8402520
    457	8402520
    459	12603780
    460	16805040
    461	16805040
    462	8402520
    463	16805040
    464	16805040
    467	12603780
    468	8402520
    469	4201260
    470	4201260
    471	16805040
    472	8402520
    473	4201260
    474	8402520
    475	16805040
    476	12603780
    478	8402520
    479	12603780
    480	12603780
    482	12603780
    483	8402520
    484	12603780
    485	8402520
    486	8402520
    487	8402520
    488	4201260
    489	8402520
    490	8402520
    491	12603780
    493	8402520
    494	12603780
    495	4201260
    496	4201260
    497	4201260
    498	8402520
    500	8402520
    501	4201260
    502	8402520
    503	8402520
    507	4201260
    508	4201260
    509	4201260
    511	4201260
    515	4201260
    517	4201260
    518	8402520
    520	4201260
    521	4201260
    522	8402520
    523	4201260
    524	4201260
    526	4201260
    529	4201260
    531	8402520
    533	4201260
    534	4201260
    535	4201260
    536	4201260
    537	4201260
    538	8402520
    540	4201260
    543	4201260
    546	4201260
    552	4201260
    553	4201260
    559	4201260
    568	8402520
    570	4201260
    576	4201260
    578	4201260
    579	8402520
    580	4201260
    583	8402520
    584	4201260
    589	12603780
    590	8402520
    593	4201260
    595	4201260
    596	4201260
    597	4201260
    599	8402520
    600	4201260
    601	4201260
    602	4201260
    603	4201260
    610	4201260
    612	4201260
    614	8402520
    615	4201260
    618	4201260
    623	4201260
    628	4201260
    630	4201260
    634	4201260
    639	4201260
    660	8402520
    667	4201260
    668	4201260
    670	4201260
    682	4201260
    684	4201260
    703	4201260
    704	8402520
    709	4201260
    732	8402520
    755	4201260
    765	4201260
    772	4201260
    785	4201260
    788	4201260
    815	4201260
    819	4201260
    821	4201260
    829	4201260
    831	4201260
    837	4201260
    842	4201260
    861	4201260
    887	4201260
    890	4201260
    894	4201260
    944	4201260
    962	4201260
    963	4201260
    989	4201260
    1050	4201260
    1058	4201260
    1077	4201260
    1084	4201260
    1086	4201260
    1117	4201260
    1120	4201260
    1132	4201260
    1142	4201260
    1188	4201260
    1196	4201260
    1203	4201260
    1209	4201260
    1213	4201260
    1265	4201260
    1268	4201260
    1294	4201260
    1307	4201260
    1327	4201260
    1340	4201260
    1356	4201260
    1373	4201260
    1384	4201260
    1449	4201260
    1484	4201260
    1495	4201260
    1526	4201260
    1603	4201260
    1614	4201260
    1728	4201260
    1915	4201260
    2042	4201260
    2170	4201260
    2357	4201260
    2477	4201260
    2570	4201260
    2786	4201260
    2995	4201260
"""


#----------------------------------------------------------------------------
# clueweb12, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

clueweb12_t192_latency_pdax_str = """
    Latency	Loads
"""

clueweb12_t192_latency_kdax_str = """
    Latency	Loads
    2	12603780
    6	31685902920
    7	721755461700
    8	40823643420
    9	25547862060
    11	214264260
    12	5911172820
    13	1222566660
    14	4676002380
    15	4020605820
    16	13397818140
    17	1726717860
    18	1600680060
    19	1020906180
    20	718415460
    21	794038140
    22	1046113740
    23	3050114760
    24	1714114080
    25	4739021280
    26	554566320
    27	2281284180
    28	756226800
    29	428528520
    30	2079623700
    31	289886940
    32	731019240
    33	252075600
    34	151245360
    35	226868040
    36	252075600
    37	252075600
    38	264679380
    39	163849140
    40	75622680
    41	252075600
    42	163849140
    43	176452920
    44	138641580
    45	403320960
    46	126037800
    47	75622680
    48	100830240
    49	126037800
    50	100830240
    51	189056700
    52	567170100
    53	75622680
    54	75622680
    55	151245360
    56	126037800
    57	126037800
    58	189056700
    59	151245360
    60	100830240
    61	163849140
    62	189056700
    63	126037800
    64	126037800
    65	138641580
    66	214264260
    67	277283160
    68	226868040
    69	138641580
    70	63018900
    71	75622680
    72	75622680
    73	25207560
    74	138641580
    75	88226460
    76	88226460
    77	63018900
    78	37811340
    79	37811340
    80	138641580
    81	100830240
    82	63018900
    83	88226460
    84	75622680
    85	50415120
    86	88226460
    87	100830240
    88	37811340
    89	63018900
    90	63018900
    91	88226460
    92	50415120
    93	63018900
    94	25207560
    95	50415120
    96	88226460
    97	25207560
    98	63018900
    99	25207560
    101	50415120
    102	37811340
    103	63018900
    104	12603780
    105	100830240
    106	25207560
    107	37811340
    108	63018900
    109	12603780
    110	37811340
    111	63018900
    112	37811340
    114	25207560
    115	12603780
    116	37811340
    117	37811340
    118	37811340
    119	37811340
    120	12603780
    121	37811340
    122	37811340
    124	12603780
    125	25207560
    126	25207560
    127	63018900
    128	25207560
    129	12603780
    130	25207560
    131	25207560
    132	12603780
    133	25207560
    134	12603780
    136	12603780
    138	25207560
    139	12603780
    141	25207560
    142	12603780
    143	12603780
    144	12603780
    145	25207560
    147	12603780
    148	12603780
    149	12603780
    150	12603780
    152	12603780
    153	12603780
    155	25207560
    157	25207560
    159	25207560
    160	12603780
    161	25207560
    162	12603780
    163	12603780
    164	25207560
    167	25207560
    168	25207560
    169	12603780
    170	25207560
    172	25207560
    173	25207560
    174	37811340
    176	12603780
    177	12603780
    178	25207560
    179	25207560
    181	25207560
    182	25207560
    183	12603780
    184	37811340
    185	25207560
    186	12603780
    187	25207560
    189	25207560
    190	25207560
    192	25207560
    194	12603780
    195	12603780
    196	12603780
    197	12603780
    199	12603780
    200	12603780
    201	25207560
    202	12603780
    203	12603780
    205	12603780
    206	12603780
    207	12603780
    208	12603780
    209	37811340
    212	12603780
    214	12603780
    215	12603780
    216	12603780
    217	25207560
    219	12603780
    221	37811340
    222	25207560
    226	12603780
    231	12603780
    240	12603780
    241	12603780
    242	12603780
    246	12603780
    249	12603780
    250	12603780
    256	12603780
    260	12603780
    263	12603780
    265	25207560
    273	12603780
    276	12603780
    277	12603780
    278	12603780
    279	12603780
    280	12603780
    281	12603780
    284	25207560
    286	12603780
    294	12603780
    298	12603780
    300	12603780
    301	25207560
    307	12603780
    308	12603780
    311	25207560
    313	12603780
    316	12603780
    317	12603780
    319	12603780
    320	12603780
    322	12603780
    323	12603780
    325	12603780
    328	25207560
    329	25207560
    332	50415120
    335	12603780
    339	12603780
    345	12603780
    357	25207560
    358	12603780
    359	12603780
    366	12603780
    367	12603780
    368	12603780
    373	12603780
    378	12603780
    379	12603780
    380	12603780
    383	12603780
    389	12603780
    392	25207560
    393	12603780
    394	12603780
    406	12603780
    411	12603780
    414	12603780
    419	12603780
    422	12603780
    423	12603780
    426	12603780
    428	12603780
    429	12603780
    431	12603780
    432	12603780
    433	25207560
    439	12603780
    442	12603780
    445	12603780
    446	12603780
    448	12603780
    451	12603780
    452	12603780
    455	12603780
    459	12603780
    473	12603780
    474	25207560
    475	12603780
    480	12603780
    483	12603780
    485	37811340
    486	12603780
    492	12603780
    496	50415120
    499	12603780
    507	25207560
    513	12603780
    515	12603780
    519	12603780
    522	12603780
    525	12603780
    531	25207560
    536	12603780
    539	12603780
    540	12603780
    549	12603780
    554	12603780
    555	12603780
    557	12603780
    559	12603780
    561	12603780
    563	12603780
    566	12603780
    569	12603780
    584	12603780
    586	12603780
    587	12603780
    597	12603780
    619	12603780
    621	12603780
    622	25207560
    625	12603780
    629	12603780
    637	12603780
    639	12603780
    646	12603780
    651	12603780
    653	12603780
    656	12603780
    667	12603780
    671	12603780
    674	12603780
    676	12603780
    679	12603780
    680	12603780
    684	12603780
    686	12603780
    687	12603780
    691	12603780
    697	12603780
    698	12603780
    705	12603780
    714	12603780
    717	25207560
    719	12603780
    727	12603780
    729	25207560
    745	12603780
    751	12603780
    754	12603780
    783	12603780
    789	12603780
    791	12603780
    792	12603780
    795	12603780
    803	12603780
    809	12603780
    810	12603780
    815	12603780
    817	12603780
    823	12603780
    830	12603780
    834	12603780
    837	12603780
    843	12603780
    846	12603780
    848	12603780
    859	12603780
    865	12603780
    866	12603780
    868	12603780
    870	12603780
    871	12603780
    877	12603780
    883	12603780
    885	12603780
    895	12603780
    903	12603780
    906	12603780
    913	12603780
    914	12603780
    926	12603780
    933	12603780
    941	12603780
    951	12603780
    963	12603780
    972	12603780
    990	12603780
    993	12603780
    1003	12603780
    1019	12603780
    1025	37811340
    1029	12603780
    1030	12603780
    1043	12603780
    1049	12603780
    1050	25207560
    1062	12603780
    1068	12603780
    1070	12603780
    1073	12603780
    1074	12603780
    1077	12603780
    1088	12603780
    1089	25207560
    1092	12603780
    1097	12603780
    1098	12603780
    1099	12603780
    1100	12603780
    1105	12603780
    1112	12603780
    1113	12603780
    1119	12603780
    1120	12603780
    1121	12603780
    1139	12603780
    1153	12603780
    1158	12603780
    1160	25207560
    1161	12603780
    1162	12603780
    1164	12603780
    1165	12603780
    1167	12603780
    1168	12603780
    1171	12603780
    1174	12603780
    1180	12603780
    1186	12603780
    1189	12603780
    1192	12603780
    1196	12603780
    1200	12603780
    1203	12603780
    1204	12603780
    1208	12603780
    1209	25207560
    1212	12603780
    1214	12603780
    1236	12603780
    1240	12603780
    1241	12603780
    1243	12603780
    1245	12603780
    1248	12603780
    1251	12603780
    1254	12603780
    1262	12603780
    1266	12603780
    1267	25207560
    1273	12603780
    1277	12603780
    1279	12603780
    1286	12603780
    1289	12603780
    1292	12603780
    1293	12603780
    1294	12603780
    1301	12603780
    1303	12603780
    1306	12603780
    1322	12603780
    1323	12603780
    1325	12603780
    1333	12603780
    1335	12603780
    1342	25207560
    1344	12603780
    1356	25207560
    1357	12603780
    1359	12603780
    1363	12603780
    1366	12603780
    1368	12603780
    1373	12603780
    1375	12603780
    1386	12603780
    1392	12603780
    1395	12603780
    1399	12603780
    1400	37811340
    1402	12603780
    1403	37811340
    1407	25207560
    1414	12603780
    1416	12603780
    1418	12603780
    1430	12603780
    1433	12603780
    1434	25207560
    1438	12603780
    1443	12603780
    1445	12603780
    1455	12603780
    1457	12603780
    1458	12603780
    1470	12603780
    1473	12603780
    1477	12603780
    1478	12603780
    1482	12603780
    1483	12603780
    1486	12603780
    1489	12603780
    1494	12603780
    1496	12603780
    1499	12603780
    1502	12603780
    1503	12603780
    1505	12603780
    1508	12603780
    1512	12603780
    1516	12603780
    1518	12603780
    1519	12603780
    1527	12603780
    1538	12603780
    1539	12603780
    1540	12603780
    1543	12603780
    1544	12603780
    1552	12603780
    1554	12603780
    1555	12603780
    1556	12603780
    1562	12603780
    1569	12603780
    1588	12603780
    1593	12603780
    1596	12603780
    1599	25207560
    1603	25207560
    1604	12603780
    1607	12603780
    1612	12603780
    1615	12603780
    1623	12603780
    1632	12603780
    1646	12603780
    1649	12603780
    1653	12603780
    1656	12603780
    1661	12603780
    1662	12603780
    1669	12603780
    1682	12603780
    1695	12603780
    1704	12603780
    1717	12603780
    1721	25207560
    1727	12603780
    1731	12603780
    1741	12603780
    1746	12603780
    1748	12603780
    1753	12603780
    1760	12603780
    1763	12603780
    1774	12603780
    1775	12603780
    1793	12603780
    1799	12603780
    1809	12603780
    1818	12603780
    1842	12603780
    1870	12603780
    1875	12603780
    1905	12603780
    1942	12603780
    1948	12603780
    1956	12603780
    1960	12603780
    1961	12603780
    1975	12603780
    1977	12603780
    1984	12603780
    1990	12603780
    1994	12603780
    2003	12603780
    2011	12603780
    2029	12603780
    2040	12603780
    2045	12603780
    2049	12603780
    2055	12603780
    2058	12603780
    2088	12603780
    2102	12603780
    2107	12603780
    2122	12603780
    2178	12603780
    2180	12603780
    2186	12603780
    2189	12603780
    2200	12603780
    2222	12603780
    2237	12603780
    2238	12603780
    2248	12603780
    2269	12603780
    2279	12603780
    2308	25207560
    2332	12603780
    2349	12603780
    2361	12603780
    2377	12603780
    2439	12603780
    2442	12603780
    2449	12603780
    2451	12603780
    2452	12603780
    2471	12603780
    2507	12603780
    2520	12603780
    2522	12603780
    2533	12603780
    2537	12603780
    2546	12603780
    2563	12603780
    2604	12603780
    2608	12603780
    2632	12603780
    2664	12603780
    2673	12603780
    2712	12603780
    2724	12603780
    2746	12603780
    2788	12603780
    2789	12603780
    2792	12603780
    2810	12603780
    2813	12603780
    2827	12603780
    2845	12603780
    2862	12603780
    2864	12603780
    2880	12603780
    2881	12603780
    2900	25207560
    2924	12603780
    2928	12603780
    2931	12603780
    2962	12603780
    2963	12603780
    2975	12603780
    2980	12603780
    2997	12603780
    3004	12603780
    3064	12603780
    3069	12603780
    3091	12603780
    3100	12603780
    3135	12603780
    3163	12603780
    3241	12603780
    3272	12603780
    3290	12603780
    3328	12603780
    3355	12603780
    3360	12603780
    3365	12603780
    3381	12603780
    3392	12603780
    3396	12603780
    3404	12603780
    3422	12603780
    3423	12603780
    3435	12603780
    3442	12603780
    3445	12603780
    3446	12603780
    3511	12603780
    3519	12603780
    3601	12603780
    3604	12603780
    3641	12603780
    3680	25207560
    3740	12603780
    3755	12603780
    3875	12603780
    3972	12603780
    4045	12603780
    4058	12603780
    4076	12603780
"""

clueweb12_t192_latency_mem_str = """
    Latency	Loads
    6	32152242780
    7	585483392340
    8	41907568500
    9	24716012580
    11	189056700
    12	5734719900
    13	1499849820
    14	3944983140
    15	4423926780
    16	14242271400
    17	1903170780
    18	1814944320
    19	1247774220
    20	768830580
    21	831849480
    22	1222566660
    23	3050114760
    24	1525057380
    25	3995398260
    26	478943640
    27	2218265280
    28	731019240
    29	315094500
    30	2470340880
    31	352905840
    32	529358760
    33	214264260
    34	100830240
    35	138641580
    36	151245360
    37	151245360
    38	163849140
    39	138641580
    40	126037800
    41	138641580
    42	151245360
    43	151245360
    44	88226460
    45	264679380
    46	163849140
    47	37811340
    48	100830240
    49	88226460
    50	100830240
    51	239471820
    52	441132300
    53	113434020
    54	88226460
    55	100830240
    56	138641580
    57	88226460
    58	189056700
    59	151245360
    60	126037800
    61	151245360
    62	189056700
    63	126037800
    64	151245360
    65	214264260
    66	138641580
    67	176452920
    68	226868040
    69	138641580
    70	100830240
    71	88226460
    72	113434020
    73	100830240
    74	75622680
    75	100830240
    76	50415120
    77	37811340
    78	50415120
    79	113434020
    80	37811340
    81	138641580
    82	88226460
    83	63018900
    84	63018900
    85	37811340
    86	37811340
    87	63018900
    88	113434020
    89	25207560
    90	88226460
    91	50415120
    92	88226460
    93	25207560
    94	50415120
    95	88226460
    96	63018900
    97	63018900
    98	37811340
    99	25207560
    100	88226460
    101	25207560
    102	50415120
    103	12603780
    104	50415120
    105	25207560
    106	63018900
    107	50415120
    108	12603780
    109	50415120
    110	63018900
    111	12603780
    112	12603780
    113	37811340
    115	25207560
    116	12603780
    117	12603780
    118	12603780
    119	63018900
    121	12603780
    122	25207560
    123	37811340
    125	12603780
    126	12603780
    127	12603780
    128	37811340
    129	25207560
    130	12603780
    131	25207560
    132	25207560
    133	25207560
    134	12603780
    135	25207560
    137	50415120
    138	25207560
    139	25207560
    140	63018900
    141	12603780
    142	25207560
    143	25207560
    144	12603780
    146	37811340
    149	37811340
    150	12603780
    151	25207560
    152	12603780
    153	25207560
    155	12603780
    156	12603780
    157	25207560
    158	25207560
    159	25207560
    160	12603780
    161	25207560
    162	50415120
    163	12603780
    164	25207560
    165	25207560
    166	25207560
    167	12603780
    168	12603780
    172	37811340
    173	37811340
    174	12603780
    175	25207560
    176	25207560
    177	12603780
    178	12603780
    179	12603780
    180	12603780
    181	12603780
    182	25207560
    185	25207560
    187	12603780
    188	25207560
    190	12603780
    191	12603780
    193	25207560
    194	12603780
    195	37811340
    199	12603780
    200	12603780
    204	12603780
    205	12603780
    207	12603780
    208	25207560
    210	25207560
    213	12603780
    214	25207560
    215	12603780
    218	12603780
    219	25207560
    223	25207560
    224	12603780
    226	12603780
    228	12603780
    229	25207560
    233	25207560
    240	25207560
    246	12603780
    249	37811340
    253	12603780
    254	12603780
    255	25207560
    257	25207560
    260	12603780
    261	12603780
    262	12603780
    263	12603780
    264	12603780
    265	12603780
    270	12603780
    272	12603780
    274	12603780
    275	12603780
    278	25207560
    280	12603780
    284	50415120
    285	12603780
    287	25207560
    288	50415120
    290	37811340
    291	25207560
    294	12603780
    295	12603780
    296	37811340
    298	37811340
    299	50415120
    300	50415120
    301	50415120
    302	63018900
    303	25207560
    305	12603780
    307	12603780
    309	12603780
    310	12603780
    311	25207560
    314	25207560
    315	37811340
    316	25207560
    318	25207560
    319	12603780
    320	25207560
    321	25207560
    326	25207560
    327	12603780
    329	25207560
    330	12603780
    331	37811340
    334	37811340
    335	12603780
    336	12603780
    338	25207560
    339	12603780
    340	12603780
    341	25207560
    342	12603780
    346	25207560
    347	12603780
    351	25207560
    360	12603780
    362	12603780
    363	25207560
    364	12603780
    370	12603780
    372	12603780
    373	12603780
    376	25207560
    377	12603780
    382	25207560
    385	12603780
    389	12603780
    393	25207560
    394	25207560
    399	12603780
    405	12603780
    408	12603780
    410	12603780
    412	37811340
    414	12603780
    417	12603780
    419	12603780
    420	12603780
    422	25207560
    423	37811340
    424	12603780
    429	12603780
    431	12603780
    432	12603780
    433	37811340
    435	37811340
    440	12603780
    442	12603780
    445	12603780
    452	12603780
    453	12603780
    454	12603780
    457	37811340
    458	25207560
    460	25207560
    461	12603780
    464	12603780
    468	12603780
    469	12603780
    478	25207560
    479	12603780
    480	25207560
    483	12603780
    484	25207560
    488	12603780
    492	12603780
    494	12603780
    498	12603780
    500	12603780
    501	12603780
    502	12603780
    504	12603780
    505	25207560
    506	12603780
    507	12603780
    508	12603780
    511	12603780
    512	12603780
    516	25207560
    517	25207560
    519	12603780
    521	12603780
    527	50415120
    529	12603780
    530	12603780
    533	25207560
    535	12603780
    536	25207560
    545	25207560
    547	25207560
    548	25207560
    549	12603780
    551	12603780
    554	12603780
    562	25207560
    563	37811340
    565	12603780
    566	25207560
    567	12603780
    568	25207560
    570	37811340
    577	12603780
    579	25207560
    580	25207560
    582	25207560
    587	12603780
    588	12603780
    593	12603780
    595	12603780
    596	12603780
    597	25207560
    599	12603780
    600	12603780
    605	12603780
    609	12603780
    610	12603780
    613	25207560
    614	12603780
    615	12603780
    616	12603780
    619	12603780
    620	25207560
    621	12603780
    623	25207560
    631	12603780
    634	25207560
    642	12603780
    644	12603780
    645	12603780
    646	25207560
    652	12603780
    654	12603780
    657	12603780
    660	12603780
    664	12603780
    671	12603780
    673	12603780
    676	12603780
    683	12603780
    684	12603780
    685	12603780
    687	12603780
    688	25207560
    689	25207560
    694	25207560
    697	12603780
    702	12603780
    704	12603780
    705	12603780
    706	12603780
    709	12603780
    711	12603780
    716	12603780
    720	12603780
    730	12603780
    732	12603780
    734	12603780
    738	12603780
    744	12603780
    752	25207560
    754	12603780
    755	12603780
    761	12603780
    766	12603780
    767	12603780
    770	12603780
    771	12603780
    776	12603780
    777	12603780
    778	12603780
    783	12603780
    786	12603780
    790	12603780
    793	12603780
    796	12603780
    800	12603780
    802	12603780
    803	12603780
    804	12603780
    808	12603780
    817	12603780
    824	12603780
    827	12603780
    828	25207560
    829	12603780
    831	12603780
    832	25207560
    834	12603780
    851	12603780
    855	12603780
    865	12603780
    868	12603780
    870	12603780
    880	12603780
    882	12603780
    886	12603780
    890	12603780
    895	25207560
    920	12603780
    924	12603780
    928	12603780
    936	12603780
    937	12603780
    950	12603780
    962	12603780
    965	12603780
    969	12603780
    976	12603780
    980	12603780
    982	12603780
    983	12603780
    990	12603780
    993	12603780
    995	12603780
    998	12603780
    1012	12603780
    1028	12603780
    1039	25207560
    1048	12603780
    1057	12603780
    1070	25207560
    1071	12603780
    1085	12603780
    1088	12603780
    1093	12603780
    1094	12603780
    1096	12603780
    1114	12603780
    1119	12603780
    1139	12603780
    1151	12603780
    1153	12603780
    1163	37811340
    1171	12603780
    1172	12603780
    1182	12603780
    1195	12603780
    1200	25207560
    1214	12603780
    1215	12603780
    1216	12603780
    1242	12603780
    1243	12603780
    1258	12603780
    1262	25207560
    1287	12603780
    1290	12603780
    1308	25207560
    1313	12603780
    1318	12603780
    1320	12603780
    1324	12603780
    1326	12603780
    1333	12603780
    1337	12603780
    1345	12603780
    1374	12603780
    1381	12603780
    1389	12603780
    1402	12603780
    1405	12603780
    1414	12603780
    1415	12603780
    1417	12603780
    1424	12603780
    1429	12603780
    1436	12603780
    1440	12603780
    1450	12603780
    1454	12603780
    1468	12603780
    1469	12603780
    1482	12603780
    1492	12603780
    1496	12603780
    1501	12603780
    1517	12603780
    1520	12603780
    1532	25207560
    1539	12603780
    1567	12603780
    1589	12603780
    1610	12603780
    1611	12603780
    1625	12603780
    1640	12603780
    1641	12603780
    1658	12603780
    1659	12603780
    1660	12603780
    1666	25207560
    1673	12603780
    1680	12603780
    1684	12603780
    1704	12603780
    1716	12603780
    1729	12603780
    1733	12603780
    1750	12603780
    1765	12603780
    1792	12603780
    1793	12603780
    1814	12603780
    1818	12603780
    1825	12603780
    1857	12603780
    1863	12603780
    1864	12603780
    1876	12603780
    1877	12603780
    1882	12603780
    1884	12603780
    1912	12603780
    1913	12603780
    1914	12603780
    1928	12603780
    1932	12603780
    1934	12603780
    1987	12603780
    1993	12603780
    2007	12603780
    2033	12603780
    2050	12603780
    2063	12603780
    2072	12603780
    2083	12603780
    2150	12603780
    2156	25207560
    2160	12603780
    2175	12603780
    2177	12603780
    2183	12603780
    2198	12603780
    2212	12603780
    2225	12603780
    2228	12603780
    2276	12603780
    2288	12603780
    2295	12603780
    2299	12603780
    2308	12603780
    2328	12603780
    2343	12603780
    2377	12603780
    2382	12603780
    2428	12603780
    2429	12603780
    2437	12603780
    2448	12603780
    2476	12603780
    2481	12603780
    2484	12603780
    2506	12603780
    2518	12603780
    2519	12603780
    2520	12603780
    2569	12603780
    2577	12603780
    2590	12603780
    2615	12603780
    2654	12603780
    2675	12603780
    2678	12603780
    2718	12603780
    2731	12603780
    2742	12603780
    2781	12603780
    2837	12603780
    2840	12603780
    2843	12603780
    2853	12603780
    2864	12603780
    2891	12603780
    2900	12603780
    2902	12603780
    2918	12603780
    2978	12603780
    2987	25207560
    3058	12603780
    3063	12603780
    3067	12603780
    3080	12603780
    3168	12603780
    3174	12603780
    3179	12603780
    3198	12603780
    3246	12603780
    3302	12603780
    3351	12603780
    3401	12603780
    3471	12603780
    3534	12603780
    3860	12603780
    3894	12603780
    3909	12603780
    3919	12603780
    3946	12603780
    4057	12603780
    4091	12603780
"""


#----------------------------------------------------------------------------
# uk2014, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

uk2014_t192_latency_pdax_str = """
    Latency	Loads
"""

uk2014_t192_latency_kdax_str = """
    Latency	Loads
    6	29291184720
    7	758760159780
    8	49898365020
    9	26316692640
    11	239471820
    12	6289286220
    13	1462038480
    14	3881964240
    15	3970190700
    16	13032308520
    17	2130038820
    18	2520756000
    19	1739321640
    20	1146943980
    21	857057040
    22	1323396900
    23	1638491400
    24	1890567000
    25	1499849820
    26	415924740
    27	466339860
    28	264679380
    29	352905840
    30	340302060
    31	277283160
    32	390717180
    33	226868040
    34	189056700
    35	163849140
    36	126037800
    37	214264260
    38	277283160
    39	239471820
    40	239471820
    41	201660480
    42	252075600
    43	151245360
    44	189056700
    45	88226460
    46	75622680
    47	113434020
    48	63018900
    49	75622680
    50	100830240
    51	75622680
    52	63018900
    53	138641580
    54	75622680
    55	75622680
    56	88226460
    57	63018900
    58	25207560
    59	12603780
    60	37811340
    61	88226460
    62	88226460
    63	37811340
    64	75622680
    65	63018900
    66	138641580
    67	50415120
    68	126037800
    69	126037800
    70	113434020
    71	75622680
    72	63018900
    73	50415120
    74	50415120
    75	37811340
    76	88226460
    77	75622680
    78	50415120
    79	37811340
    80	37811340
    81	25207560
    82	100830240
    83	25207560
    84	50415120
    85	100830240
    86	50415120
    87	63018900
    88	50415120
    89	12603780
    91	12603780
    92	25207560
    93	37811340
    94	25207560
    95	12603780
    96	37811340
    97	25207560
    98	88226460
    99	63018900
    101	25207560
    102	25207560
    103	37811340
    104	12603780
    105	25207560
    106	12603780
    107	37811340
    108	37811340
    109	12603780
    114	75622680
    115	37811340
    116	12603780
    117	12603780
    118	12603780
    121	25207560
    122	25207560
    123	25207560
    124	12603780
    125	63018900
    126	25207560
    127	25207560
    128	12603780
    129	12603780
    132	37811340
    133	25207560
    134	12603780
    135	12603780
    136	25207560
    138	25207560
    140	25207560
    141	12603780
    142	12603780
    143	12603780
    146	12603780
    147	25207560
    148	25207560
    149	37811340
    151	12603780
    153	25207560
    154	12603780
    155	12603780
    156	25207560
    157	12603780
    159	25207560
    160	25207560
    162	12603780
    163	25207560
    164	25207560
    165	12603780
    166	25207560
    167	12603780
    168	25207560
    170	25207560
    172	12603780
    173	12603780
    174	12603780
    176	12603780
    177	25207560
    178	12603780
    179	12603780
    181	12603780
    182	37811340
    183	25207560
    184	25207560
    188	25207560
    189	25207560
    191	12603780
    192	12603780
    193	12603780
    195	12603780
    196	12603780
    199	12603780
    203	12603780
    207	12603780
    208	12603780
    210	25207560
    211	12603780
    215	12603780
    217	12603780
    219	37811340
    221	37811340
    222	12603780
    226	12603780
    231	25207560
    235	12603780
    238	12603780
    239	12603780
    240	12603780
    241	25207560
    242	12603780
    247	12603780
    248	12603780
    249	12603780
    252	25207560
    255	12603780
    256	25207560
    261	25207560
    267	12603780
    280	25207560
    283	12603780
    284	12603780
    285	12603780
    286	12603780
    287	12603780
    289	12603780
    291	25207560
    298	12603780
    303	12603780
    308	25207560
    310	12603780
    311	25207560
    319	12603780
    321	12603780
    322	12603780
    323	12603780
    324	12603780
    326	12603780
    330	12603780
    331	12603780
    333	12603780
    336	12603780
    337	12603780
    343	12603780
    346	12603780
    349	25207560
    351	12603780
    356	12603780
    359	12603780
    365	25207560
    369	12603780
    372	12603780
    374	12603780
    387	12603780
    391	12603780
    392	25207560
    393	12603780
    394	12603780
    397	12603780
    399	12603780
    402	12603780
    406	12603780
    408	12603780
    409	12603780
    412	12603780
    417	12603780
    420	12603780
    422	12603780
    425	12603780
    436	12603780
    438	12603780
    444	12603780
    453	12603780
    456	12603780
    460	12603780
    466	12603780
    474	12603780
    475	25207560
    477	12603780
    479	25207560
    480	12603780
    485	12603780
    488	12603780
    493	12603780
    501	12603780
    503	12603780
    505	12603780
    507	12603780
    508	25207560
    511	12603780
    513	12603780
    514	25207560
    516	12603780
    518	12603780
    520	12603780
    521	12603780
    523	12603780
    532	12603780
    538	12603780
    539	12603780
    541	12603780
    552	12603780
    554	12603780
    555	12603780
    564	12603780
    566	12603780
    570	12603780
    573	12603780
    574	12603780
    575	25207560
    576	12603780
    580	12603780
    582	12603780
    598	12603780
    599	12603780
    602	12603780
    603	12603780
    608	12603780
    616	12603780
    619	12603780
    625	12603780
    626	12603780
    629	25207560
    633	25207560
    634	12603780
    639	12603780
    652	12603780
    655	12603780
    657	37811340
    658	12603780
    661	12603780
    663	12603780
    664	12603780
    665	12603780
    668	12603780
    669	12603780
    673	12603780
    678	25207560
    684	12603780
    685	12603780
    686	12603780
    687	12603780
    694	12603780
    704	12603780
    710	12603780
    711	12603780
    713	12603780
    719	12603780
    725	12603780
    729	12603780
    741	12603780
    742	12603780
    746	12603780
    753	12603780
    765	12603780
    769	12603780
    772	12603780
    773	12603780
    778	12603780
    782	12603780
    784	12603780
    792	12603780
    794	12603780
    795	12603780
    796	12603780
    798	12603780
    800	12603780
    808	12603780
    812	12603780
    820	12603780
    832	12603780
    834	12603780
    837	12603780
    838	12603780
    851	12603780
    860	12603780
    864	12603780
    867	12603780
    872	25207560
    877	12603780
    886	50415120
    889	12603780
    890	12603780
    903	12603780
    905	12603780
    918	12603780
    923	12603780
    926	12603780
    931	12603780
    945	12603780
    949	12603780
    973	12603780
    985	12603780
    988	25207560
    989	12603780
    990	12603780
    1001	12603780
    1011	12603780
    1014	12603780
    1026	12603780
    1034	12603780
    1036	12603780
    1053	12603780
    1074	25207560
    1092	12603780
    1093	12603780
    1096	12603780
    1112	12603780
    1121	12603780
    1131	12603780
    1137	12603780
    1151	12603780
    1157	12603780
    1185	12603780
    1199	12603780
    1203	12603780
    1219	12603780
    1258	12603780
    1265	12603780
    1267	12603780
    1273	12603780
    1280	12603780
    1295	12603780
    1296	12603780
    1302	12603780
    1303	12603780
    1315	12603780
    1317	12603780
    1328	12603780
    1353	12603780
    1382	12603780
    1390	12603780
    1397	12603780
    1400	12603780
    1405	12603780
    1406	12603780
    1421	12603780
    1439	12603780
    1440	12603780
    1460	12603780
    1472	12603780
    1476	12603780
    1478	12603780
    1491	12603780
    1496	12603780
    1504	12603780
    1533	12603780
    1545	12603780
    1546	12603780
    1550	12603780
    1579	12603780
    1590	12603780
    1593	12603780
    1613	12603780
    1615	12603780
    1642	12603780
    1653	12603780
    1654	12603780
    1667	12603780
    1683	12603780
    1697	12603780
    1713	12603780
    1746	12603780
    1754	12603780
    1755	12603780
    1756	12603780
    1786	12603780
    1814	12603780
    1817	12603780
    1828	12603780
    1833	12603780
    1857	12603780
    1863	12603780
    1915	12603780
    1919	12603780
    1957	12603780
    1998	12603780
    2026	12603780
    2027	12603780
    2049	12603780
    2062	12603780
    2107	12603780
    2131	25207560
    2133	12603780
    2138	12603780
    2146	12603780
    2148	12603780
    2165	12603780
    2177	12603780
    2240	12603780
    2247	12603780
    2378	12603780
    2380	12603780
    2401	12603780
    2403	12603780
    2445	12603780
    2452	12603780
    2467	12603780
    2469	12603780
    2477	12603780
    2491	12603780
    2506	12603780
    2533	12603780
    2564	25207560
    2572	12603780
    2576	12603780
    2589	25207560
    2592	12603780
    2601	12603780
    2627	12603780
    2716	12603780
    2718	12603780
    2761	12603780
    2780	12603780
    2842	12603780
    2856	12603780
    2868	12603780
    2872	12603780
    2926	12603780
    3001	12603780
    3004	12603780
    3067	12603780
    3077	12603780
    3159	12603780
    3203	12603780
    3209	12603780
    3252	12603780
    3276	12603780
    3308	12603780
    3369	12603780
    3387	12603780
    3403	25207560
    3409	12603780
    3411	12603780
    3483	12603780
    3544	12603780
    3584	12603780
    3585	12603780
    3786	12603780
    3813	12603780
    3836	12603780
    3890	12603780
    3902	12603780
    3914	12603780
    4023	12603780
    4052	12603780
    4090	12603780
"""

uk2014_t192_latency_mem_str = """
    Latency	Loads
    6	29341599840
    7	653178294720
    8	50515950240
    9	27148542120
    11	214264260
    12	6012003060
    13	1424227140
    14	2936680740
    15	5041512000
    16	16712612280
    17	2898869400
    18	2621586240
    19	2268680400
    20	1222566660
    21	1033509960
    22	1008302400
    23	2155246380
    24	2873661840
    25	2029208580
    26	668000340
    27	529358760
    28	617585220
    29	327698280
    30	264679380
    31	453736080
    32	680604120
    33	252075600
    34	176452920
    35	264679380
    36	201660480
    37	88226460
    38	113434020
    39	163849140
    40	176452920
    41	138641580
    42	113434020
    43	151245360
    44	75622680
    45	189056700
    46	100830240
    47	75622680
    48	88226460
    49	50415120
    50	63018900
    51	88226460
    52	88226460
    53	25207560
    54	50415120
    55	12603780
    56	50415120
    57	50415120
    58	50415120
    59	75622680
    60	50415120
    61	63018900
    62	63018900
    63	50415120
    64	25207560
    65	25207560
    66	88226460
    67	88226460
    68	63018900
    69	75622680
    70	12603780
    71	50415120
    72	37811340
    73	75622680
    74	75622680
    75	50415120
    76	37811340
    77	25207560
    78	37811340
    79	75622680
    80	50415120
    81	37811340
    82	37811340
    83	113434020
    85	12603780
    86	25207560
    87	37811340
    88	63018900
    89	37811340
    90	37811340
    91	12603780
    92	25207560
    93	75622680
    94	25207560
    95	25207560
    96	63018900
    97	37811340
    98	37811340
    99	25207560
    101	50415120
    102	37811340
    104	75622680
    105	75622680
    106	37811340
    108	12603780
    109	12603780
    110	25207560
    111	25207560
    112	12603780
    113	25207560
    114	12603780
    115	63018900
    117	12603780
    118	25207560
    119	12603780
    122	12603780
    123	37811340
    126	12603780
    127	25207560
    128	12603780
    131	12603780
    132	12603780
    133	25207560
    134	25207560
    135	12603780
    136	12603780
    137	37811340
    138	12603780
    141	37811340
    142	12603780
    145	12603780
    148	12603780
    149	12603780
    152	12603780
    154	12603780
    155	12603780
    156	12603780
    158	25207560
    159	12603780
    160	25207560
    161	12603780
    166	12603780
    171	12603780
    172	12603780
    176	25207560
    190	12603780
    192	12603780
    198	12603780
    202	12603780
    203	12603780
    204	12603780
    208	12603780
    216	12603780
    218	12603780
    233	12603780
    236	25207560
    237	12603780
    240	12603780
    242	12603780
    244	12603780
    246	12603780
    248	12603780
    252	12603780
    254	12603780
    255	12603780
    264	12603780
    268	12603780
    270	12603780
    271	12603780
    273	25207560
    274	12603780
    280	25207560
    281	12603780
    282	12603780
    284	25207560
    287	25207560
    293	12603780
    294	12603780
    298	12603780
    303	12603780
    304	12603780
    305	25207560
    307	12603780
    321	12603780
    322	25207560
    327	12603780
    328	12603780
    332	12603780
    337	12603780
    340	12603780
    343	12603780
    346	25207560
    355	12603780
    360	12603780
    367	12603780
    369	12603780
    376	12603780
    380	12603780
    382	12603780
    398	12603780
    401	12603780
    402	12603780
    403	12603780
    405	12603780
    409	12603780
    414	12603780
    415	25207560
    421	25207560
    423	12603780
    425	12603780
    426	12603780
    427	12603780
    430	12603780
    431	25207560
    437	12603780
    440	25207560
    445	12603780
    447	12603780
    451	12603780
    457	12603780
    458	12603780
    459	25207560
    461	12603780
    464	25207560
    470	12603780
    471	12603780
    485	12603780
    486	12603780
    498	12603780
    499	12603780
    500	12603780
    506	12603780
    508	12603780
    520	12603780
    523	25207560
    525	25207560
    535	37811340
    537	12603780
    539	12603780
    542	12603780
    545	12603780
    551	25207560
    553	12603780
    555	12603780
    557	12603780
    563	12603780
    569	12603780
    572	12603780
    578	25207560
    587	12603780
    595	12603780
    596	12603780
    597	12603780
    601	12603780
    604	12603780
    618	12603780
    619	12603780
    620	25207560
    623	25207560
    632	12603780
    635	12603780
    637	12603780
    640	25207560
    641	12603780
    642	12603780
    662	12603780
    668	25207560
    677	12603780
    686	12603780
    688	12603780
    695	12603780
    698	12603780
    700	12603780
    704	12603780
    709	12603780
    714	12603780
    717	12603780
    720	12603780
    724	12603780
    727	12603780
    739	12603780
    743	12603780
    760	25207560
    779	12603780
    786	12603780
    797	12603780
    816	12603780
    818	12603780
    819	12603780
    820	12603780
    821	12603780
    829	12603780
    833	12603780
    834	12603780
    841	12603780
    845	12603780
    847	12603780
    849	25207560
    859	12603780
    863	12603780
    868	12603780
    873	12603780
    880	12603780
    884	12603780
    885	12603780
    886	12603780
    888	12603780
    890	12603780
    893	12603780
    895	12603780
    901	12603780
    902	12603780
    914	25207560
    926	12603780
    927	12603780
    938	12603780
    940	12603780
    948	25207560
    958	12603780
    963	12603780
    970	12603780
    987	12603780
    1008	12603780
    1013	12603780
    1016	12603780
    1026	12603780
    1030	12603780
    1056	12603780
    1060	12603780
    1067	12603780
    1068	12603780
    1069	12603780
    1081	12603780
    1092	12603780
    1093	12603780
    1115	12603780
    1118	12603780
    1126	12603780
    1130	12603780
    1131	12603780
    1135	12603780
    1141	12603780
    1142	12603780
    1155	12603780
    1159	12603780
    1160	12603780
    1163	12603780
    1169	12603780
    1172	12603780
    1173	12603780
    1205	12603780
    1226	12603780
    1229	12603780
    1240	12603780
    1254	12603780
    1266	12603780
    1268	12603780
    1273	25207560
    1279	12603780
    1280	12603780
    1288	12603780
    1291	12603780
    1294	12603780
    1295	12603780
    1303	12603780
    1315	12603780
    1320	12603780
    1327	12603780
    1330	12603780
    1339	12603780
    1348	12603780
    1349	12603780
    1356	12603780
    1360	12603780
    1361	12603780
    1374	12603780
    1375	12603780
    1379	12603780
    1380	12603780
    1384	12603780
    1386	12603780
    1399	12603780
    1409	12603780
    1436	12603780
    1438	12603780
    1440	12603780
    1449	12603780
    1460	12603780
    1462	12603780
    1466	25207560
    1468	12603780
    1471	12603780
    1474	12603780
    1477	12603780
    1485	12603780
    1492	12603780
    1494	12603780
    1495	25207560
    1498	12603780
    1500	12603780
    1510	12603780
    1527	12603780
    1531	25207560
    1546	12603780
    1549	12603780
    1559	12603780
    1565	12603780
    1571	12603780
    1600	12603780
    1601	12603780
    1606	12603780
    1638	12603780
    1642	12603780
    1668	12603780
    1670	12603780
    1686	12603780
    1689	12603780
    1694	12603780
    1709	12603780
    1718	12603780
    1721	12603780
    1725	12603780
    1737	12603780
    1755	12603780
    1758	12603780
    1766	12603780
    1779	12603780
    1781	12603780
    1793	12603780
    1819	25207560
    1832	12603780
    1840	12603780
    1851	12603780
    1869	12603780
    1870	12603780
    1871	12603780
    1879	12603780
    1904	12603780
    1921	12603780
    1929	12603780
    1931	25207560
    1932	12603780
    1939	12603780
    1942	12603780
    1943	12603780
    1952	12603780
    1973	12603780
    1986	12603780
    2004	12603780
    2005	12603780
    2016	12603780
    2069	12603780
    2084	12603780
    2089	12603780
    2107	12603780
    2110	12603780
    2123	12603780
    2125	12603780
    2131	12603780
    2153	12603780
    2166	12603780
    2180	12603780
    2184	12603780
    2188	12603780
    2215	12603780
    2230	12603780
    2257	12603780
    2260	25207560
    2267	12603780
    2292	12603780
    2312	12603780
    2333	12603780
    2378	12603780
    2382	12603780
    2404	12603780
    2406	12603780
    2407	12603780
    2414	12603780
    2420	12603780
    2424	12603780
    2436	12603780
    2440	12603780
    2472	12603780
    2474	12603780
    2480	25207560
    2515	12603780
    2518	12603780
    2556	12603780
    2566	12603780
    2573	12603780
    2575	12603780
    2591	25207560
    2651	12603780
    2680	12603780
    2687	12603780
    2693	12603780
    2699	12603780
    2707	12603780
    2715	12603780
    2733	12603780
    2761	12603780
    2767	12603780
    2774	12603780
    2794	12603780
    2796	12603780
    2799	12603780
    2811	12603780
    2813	12603780
    2818	12603780
    2837	12603780
    2873	12603780
    2879	12603780
    2882	12603780
    2939	12603780
    2943	12603780
    2967	12603780
    2968	12603780
    3008	12603780
    3020	12603780
    3044	12603780
    3063	25207560
    3073	12603780
    3075	12603780
    3081	12603780
    3096	12603780
    3132	12603780
    3139	12603780
    3162	12603780
    3164	12603780
    3198	12603780
    3215	12603780
    3249	12603780
    3253	12603780
    3273	12603780
    3277	12603780
    3302	12603780
    3324	12603780
    3333	12603780
    3347	12603780
    3395	12603780
    3419	12603780
    3456	12603780
    3476	12603780
    3495	12603780
    3522	12603780
    3582	12603780
    3591	12603780
    3614	12603780
    3615	12603780
    3632	12603780
    3662	12603780
    3665	12603780
    3725	12603780
    3738	12603780
    3755	12603780
    3799	12603780
    3812	12603780
    3842	12603780
    3870	12603780
    3887	12603780
    3932	12603780
    3963	12603780
    3977	12603780
    3991	12603780
    4001	12603780
    4018	12603780
    4024	12603780
    4063	12603780
"""


#----------------------------------------------------------------------------
# XXX, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

XXX_t192_latency_dram_str = """
    Latency	Loads
"""

XXX_t192_latency_pdax_str = """
    Latency	Loads
"""

XXX_t192_latency_kdax_str = """
    Latency	Loads
"""

XXX_t192_latency_mem_str = """
    Latency	Loads
"""


#****************************************************************************
# Helpers
#****************************************************************************

def plot_modes(dfrm, axes, nm_i, title, plt_sty, mrk_sty, ln_sty):

    ax = seaborn.lineplot(data=dfrm, x='mode', y=col_dst, hue='graph',
                          palette=plt_sty, ax=axes, marker=mrk_sty, linestyle=ln_sty)

    #y_lo = dfrm[col_dst].min(axis=0)
    #ax.set_ylim(bottom = y_lo * .80)

    if title:
        ax.set_title(title, size=title_txt_sz)

    ax.set_xlabel('')
    #ax.set_xticklabels([])

    ax.grid(linestyle='dashed')

    ax.legend().set_title('')
    
    if (nm_i != 0):
        ax.set_ylabel('')
        ax.get_legend().remove()


    # OLD:
    # ax = seaborn.lineplot(data=dfrm, x='mode', y=col_src, hue='graph', ax=ax,
    #                       palette='dark', marker='^')
    # ax.legend(title=col_src, loc='lower left',  bbox_to_anchor=(0.0, 0.35)) # prop={'size': text_sz}

    #ax1 = ax.twinx()

    # # Should not be necessary!
    # lineL = ax.legend().get_lines()
    # for x in lineL:
    #     x.set_linestyle(ln_sty)
    #     #x.set_marker(mrk_sty)
    # ax.legend(handles=lineL, loc='lower left', bbox_to_anchor=(0.0, 0.0)) # title=col_dst, prop={'size': text_sz}

    return ax



def plot_scaling(dfrm, graph_nm, axes, plt_sty, mrk_sty, ln_sty, nm_j):
    dfrm_me = dfrm.xs(graph_nm, level='graph')

    dfrm_me = dfrm_me.dropna(axis='rows', subset=[col_src])
    #print(dfrm_me)
    
    ax = seaborn.lineplot(data=dfrm_me, x='threads', y=col_src,
                          hue='mode', ax=axes,
                          palette=plt_sty, marker=mrk_sty, linestyle=ln_sty)

    ax.grid(linestyle='dashed')

    ax.set_xscale('log', base=2)

    ax.set_yscale('log', base=2)

    #ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True, useOffset=False))
    #ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # Adjust exponent of scientific formatter: Only works for x position!
    #ax.yaxis.get_offset_text().set_position((0.0,0.0)) # adjust exponent

    # Adjust exponent of scientific formatter: 'offset_text' has no value until plot time!
    #ax.set_yticklabels(ax.get_yticks()) # attempt to force
    #exp_txt = ax.yaxis.get_offset_text().get_text()
    #print(exp_txt)
    #ax.text(0.10, 0.5, exp_txt, ha='left', zorder=100) # , va='bottom'
    #ax.yaxis.offsetText.set_visible(False)
    
    if (nm_j == 0):
        ax.set_ylabel('Time (s) v. Threads', size=title_txt_sz)
    else:
        ax.set_ylabel('')

    ax.set_title(graph_nm, size=title_txt_sz)

    ax.set_xlabel('')

    return ax



def plot_bw_lat(ax_bw, ax_lat, bw_data_strL, lat_data_strL, graph,
                bw_data_nmL, lat_data_nmL, plt_sty, nm_j):
    #-------------------------------------------------------
    # BW
    #-------------------------------------------------------
    
    (bw_dfrm_hist, bw_dfrm_wide) = \
        makeFrameFromHistL(bw_data_nmL, bw_data_strL, convert = 'sample')

    bw_dfrm_mean = bw_dfrm_wide.mean(axis=0) # mean per column

    # print("bw_dfrm_hist\n", bw_dfrm_hist)
    # print("bw_dfrm_wide\n", bw_dfrm_wide)

    #-------------------------------------------------------
    
    ax = ax_bw
    ax = seaborn.violinplot(data=bw_dfrm_wide, ax=ax, cut = 0,
                            palette=plt_sty, scale = 'area', inner = 'box')
    xlim = ax.get_xlim()
    ax = seaborn.scatterplot(data = bw_dfrm_mean, ax=ax,
                             marker='d', color='white', zorder=10)

    ax.grid(linestyle='dashed')
    ax.set_axisbelow(True)

    max_mean = bw_dfrm_mean.max()
    y_hi = 2 * max_mean

    ax.set_xlim(xlim)
    ax.set_ylim(0, y_hi)

    if (nm_j == 0):
        ax.set_ylabel('Memory BW (GB/s)\n192 threads', size=title_txt_sz)

    #ax.set_title(graph, size=title_txt_sz)


    #-------------------------------------------------------
    # Lat
    #-------------------------------------------------------

    (lat_dfrm_hist, lat_dfrm_wide) = \
        makeFrameFromHistL(lat_data_nmL, lat_data_strL, convert = 'repeat',
                           scale = True)

    lat_dfrm_mean = lat_dfrm_wide.mean(axis=0)

    # print("lat_dfrm_hist\n", lat_dfrm_hist)
    # print("lat_dfrm_wide\n", lat_dfrm_wide)

    # print(lat_dfrm_wide.median(axis=0))
    # print(lat_dfrm_wide.mean(axis=0))

    #-------------------------------------------------------

    ax = ax_lat

    ax = seaborn.violinplot(data=lat_dfrm_wide, ax=ax, cut = 0, # alpha=.3
                            palette=plt_sty, scale = 'area', inner = 'box')
    xlim = ax.get_xlim()
    ax = seaborn.scatterplot(data = lat_dfrm_mean, ax=ax,
                             marker='d', color='white', zorder=10)

    ax.grid(linestyle='dashed')
    ax.set_axisbelow(True)

    lat_min = lat_dfrm_hist.index.min() # to_numpy()
    y_lo = lat_min / 2
    
    max_mean = lat_dfrm_mean.max()
    y_hi = 2 * max_mean
    
    ax.set_xlim(xlim)
    ax.set_ylim(y_lo, y_hi)

    if (nm_j == 0):
        ax.set_ylabel('Load Latency (cyc)\n192 threads', size=title_txt_sz)
        
   #ax.set_title(graph, size=title_txt_sz)



#****************************************************************************
#
#****************************************************************************

def makeRelTime(dfrm, row_srcL, col_src, col_dst):
    col_dat = []

    for (graph, thrd, ty) in dfrm.index:
        #print("{}: {}/{}/{}".format(makeRelTime.__name__,graph, thrd, ty))
        v = dfrm.at[(graph, thrd, ty),      col_src]

        try:
            #print("try1: {}/{}/{}".format(graph, thrd, row_srcL[0]))
            v_base = dfrm.at[(graph, thrd, row_srcL[0]), col_src]
        except:
            v_base = numpy.nan
            
        if (numpy.isnan(v_base)):
            #print("try2: {}/{}/{}".format(graph, thrd, row_srcL[1]))
            v_base = dfrm.at[(graph, thrd, row_srcL[1]), col_src]

        #except KeyError:
        #    vtcsv.err(("Warning: Incomplete: '%s %s %s'" % (graph, thrd, ty) ))
        #    v_base = 1.0
            
        v_norm = (v / v_base) # * 100
        col_dat.append(v_norm)

    dfrm[col_dst] = col_dat # concat
    #dfrm.insert(len(dfrm.columns), col_dst, col_dat)
    #print(dfrm)

    return dfrm


# When 'data_stringL' may contain duplicate to indicate merged results!
def makeFrameFromHistL(data_nameL, data_stringL, convert, scale = False):
    dfrm_hist = pandas.DataFrame()
    dfrm_wide = pandas.DataFrame()

    idx = 0
    for data_str in data_stringL:
        #---------------------------------------
        # Create histogram
        #---------------------------------------
        data_nm = data_nameL[idx]
        
        str_data = io.StringIO(data_str)
        dfrm_hist_x = pandas.read_csv(str_data, sep='\s+', index_col=0)

        # N.B.: Drop 'class' column
        if (dfrm_hist_x.columns.isin(['class']).any()): # df.shape[1]
            dfrm_hist_x.drop(['class'], axis=1, inplace=True)
        
        dfrm_hist_x.columns = [data_nm]
        #print(dfrm_hist_x)

        if (scale):
            s = dfrm_hist_x.min(axis=0)
            dfrm_hist_x = dfrm_hist_x.applymap(lambda x: x / s)

        #---------------------------------------
        # Convert the histogram to Seaborn 'wide form'
        #---------------------------------------
        #   https://stackoverflow.com/questions/62709719/violinplot-from-histogram-values
        #   https://anvil.works/blog/tidy-data
        #   https://sejdemyr.github.io/r-tutorials/basics/wide-and-long/

        hist_bin  = dfrm_hist_x.index
        hist_freq = dfrm_hist_x.iloc[:, 0]
        
        #print("hist_bin\n", hist_bin)
        #print("hist_freq\n", hist_freq)

        if (convert == 'repeat'):
            hist_smpl = numpy.repeat(hist_bin, hist_freq)
        elif (convert == 'sample'):
            hist_smpl = numpy.random.uniform(numpy.repeat(hist_bin, hist_freq),
                                             numpy.repeat(hist_bin, hist_freq))
        #print("hist_smpl\n", hist_smpl)

        dfrm_wide_x = pandas.DataFrame(hist_smpl)
        dfrm_wide_x.columns = [data_nm]
        
        #print("dfrm_wide_x\n", dfrm_wide_x)
        
        #---------------------------------------
        # Merge into final result
        #---------------------------------------
        idx += 1

        dfrm_hist = pandas.concat([dfrm_hist, dfrm_hist_x], axis=1)
        dfrm_wide = pandas.concat([dfrm_wide, dfrm_wide_x], axis=1)

        if (dfrm_hist.columns.tolist().count(data_nm) > 1):
            dfrm_hist_x = dfrm_hist[data_nm].sum(axis=1).copy()
            dfrm_wide_x = dfrm_wide[data_nm].sum(axis=1).copy()
            
            dfrm_hist.drop(data_nm, axis=1, inplace=True)
            dfrm_wide.drop(data_nm, axis=1, inplace=True)
            
            dfrm_hist[data_nm] = dfrm_hist_x
            dfrm_wide[data_nm] = dfrm_wide_x
            #print(dfrm_hist)
            #print(dfrm_wide)

        #if (data_nm in dfrm_hist.columns)

    # histogram bins will be unique, so retain them as index
    #dfrm_hist.reset_index(inplace=True)

    return (dfrm_hist, dfrm_wide)



#****************************************************************************
# Main
#****************************************************************************

fig1, axes1L = pyplt.subplots(nrows=2, ncols=3, figsize=(8, 3.5))

fig2, axes2A = pyplt.subplots(nrows=3, ncols=4, figsize=(14, 8.5),
                              gridspec_kw={'height_ratios': [4.0, 3.5, 3.5]})

fig3, axes3L = pyplt.subplots(nrows=1, ncols=5, figsize=(14, 2.5))


ln_sty = '-' # ':' # --
mrk_sty = 'o' # --

plt_sty1 = 'bright' # 'Set2' # 'muted' # 'bright'
plt_sty2 = 'deep' # 'dark'


#----------------------------------------------------------------------------
# Mode comparison
#----------------------------------------------------------------------------

tm_index = [0,1,2] # graph threads type

row_srcL = ['dram', 'mem']
col_src = 'time'
col_dst = 'relative time'


#-------------------------------------------------------
# grappolo
#-------------------------------------------------------

mode_thrdL = [32, 64, 192]

time_data_grp = io.StringIO(time_str_grappolo)
time_dfrm_grp = pandas.read_csv(time_data_grp, sep='\s+', index_col=tm_index)
#print(time_dfrm_grp)

makeRelTime(time_dfrm_grp, row_srcL, col_src, col_dst)

nm_i = 0
for num_t in mode_thrdL:
    mode_dfrm = time_dfrm_grp.xs(num_t, level='threads')
    #print(mode_dfrm)

    ttl = 'Community Detection/{}'.format(num_t)
    plot_modes(mode_dfrm, axes1L[0][nm_i], nm_i, ttl, plt_sty1, mrk_sty, ln_sty)
    nm_i += 1


#-------------------------------------------------------
# ripples
#-------------------------------------------------------

time_data_rip = io.StringIO(time_str_ripples)
time_dfrm_rip = pandas.read_csv(time_data_rip, sep='\s+', index_col=tm_index)
#print(time_dfrm_rip)

makeRelTime(time_dfrm_rip, row_srcL, col_src, col_dst)

nm_i = 0
for num_t in mode_thrdL:
    mode_dfrm = time_dfrm_rip.xs(num_t, level='threads')
    #print(mode_dfrm)

    ttl = 'Influence Maximization/{}'.format(num_t)
    plot_modes(mode_dfrm, axes1L[1][nm_i], nm_i, ttl, plt_sty1, mrk_sty, ln_sty)
    nm_i += 1


#----------------------------------------------------------------------------
# Grappolo: Per-graph Scaling + Memory histograms
#----------------------------------------------------------------------------


#-------------------------------------------------------
# friendster
#-------------------------------------------------------

nm = 'friendster'
nm_j = 0

bw_data_nmL =  ['dram', 'mem', 'kdax', 'kdax', 'pdax', 'pdax' ]
lat_data_nmL = ['dram', 'mem', 'kdax', 'pdax' ]

# TODO: Make pairs of (data_str, data_nm)

plot_scaling(time_dfrm_grp, nm, axes2A[0,nm_j], plt_sty1, mrk_sty, ln_sty, nm_j)

bw_data_strL = [ friendster_t192_dramBw_dram_str,

                 friendster_t192_dramBw_mem_str,
                 #friendster_t192_pmemBw_mem_str,
                 
                 friendster_t192_dramBw_kdax_str,
                 friendster_t192_pmemBw_kdax_str,
                 
                 friendster_t192_dramBw_pdax_str,
                 friendster_t192_pmemBw_pdax_str ]


lat_data_strL = [ friendster_t192_latency_dram_str,
                  friendster_t192_latency_mem_str,
                  friendster_t192_latency_kdax_str,
                  friendster_t192_latency_pdax_str ]

plot_bw_lat(axes2A[1,nm_j], axes2A[2,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)


#-------------------------------------------------------
# 
#-------------------------------------------------------

nm = 'moliere2016'
nm_j = 1

plot_scaling(time_dfrm_grp, nm, axes2A[0,nm_j], plt_sty1, mrk_sty, ln_sty, nm_j)

bw_data_strL = [ moliere2016_t192_dramBw_dram_str,

                 moliere2016_t192_dramBw_mem_str,
                 #moliere2016_t192_pmemBw_mem_str,
                 
                 moliere2016_t192_dramBw_kdax_str,
                 moliere2016_t192_pmemBw_kdax_str,
                 
                 moliere2016_t192_dramBw_pdax_str,
                 moliere2016_t192_pmemBw_pdax_str ]

lat_data_strL = [ moliere2016_t192_latency_dram_str,
                  moliere2016_t192_latency_mem_str,
                  moliere2016_t192_latency_kdax_str,
                  moliere2016_t192_latency_pdax_str ]

plot_bw_lat(axes2A[1,nm_j], axes2A[2,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)

#-------------------------------------------------------
# 
#-------------------------------------------------------

nm = 'clueweb12'
nm_j = 2

bw_data_nmL =  ['mem', 'kdax', 'kdax'] # 'mem',
lat_data_nmL =  ['mem', 'kdax']


plot_scaling(time_dfrm_grp, nm, axes2A[0,nm_j], plt_sty1, mrk_sty, ln_sty, nm_j)

bw_data_strL = [ clueweb12_t192_dramBw_mem_str,
                 #clueweb12_t192_pmemBw_mem_str,
                 
                 clueweb12_t192_dramBw_kdax_str,
                 clueweb12_t192_pmemBw_kdax_str ]

lat_data_strL = [ clueweb12_t192_latency_mem_str,
                  clueweb12_t192_latency_kdax_str ]

plot_bw_lat(axes2A[1,nm_j], axes2A[2,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)

#-------------------------------------------------------
# 
#-------------------------------------------------------

nm = 'uk2014'
nm_j = 3


plot_scaling(time_dfrm_grp, nm, axes2A[0,nm_j], plt_sty1, mrk_sty, ln_sty, nm_j)

bw_data_strL = [ uk2014_t192_dramBw_mem_str,
                 #uk2014_t192_pmemBw_mem_str,

                 uk2014_t192_dramBw_kdax_str,
                 uk2014_t192_pmemBw_kdax_str ]


lat_data_strL = [ uk2014_t192_latency_mem_str,
                  uk2014_t192_latency_kdax_str ]


plot_bw_lat(axes2A[1,nm_j], axes2A[2,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)


#----------------------------------------------------------------------------
# Ripples: Per-graph Scaling
#----------------------------------------------------------------------------

nmL = [ 'slash', 'twitter', 'talk', 'pokec', 'topcats' ]

nm_i = 0
for nm in nmL:
    plot_scaling(time_dfrm_rip, nm, axes3L[nm_i], plt_sty1, mrk_sty, ln_sty, nm_i)
    nm_i += 1


#----------------------------------------------------------------------------

adjustH1 = { 'left':0.05, 'right':0.99, 'bottom':0.03, 'top':0.97,
             'wspace':0.18, 'hspace':0.35 }

adjustH2 = { 'left':0.05, 'right':0.99, 'bottom':0.03, 'top':0.97,
             'wspace':0.18, 'hspace':0.15 }

fig1.subplots_adjust(**adjustH1)
fig2.subplots_adjust(**adjustH2)
fig3.subplots_adjust(**adjustH2)

fig1.savefig('chart-teaser.pdf', bbox_inches='tight')
fig2.savefig('chart-grappolo-sum.pdf', bbox_inches='tight')
fig3.savefig('chart-ripples-scaling.pdf', bbox_inches='tight')

#seaborn.plt.show()
pyplt.show()
