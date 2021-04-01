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

# Application variant *2  uses prefetchnta

# OMP_PLACES="cores", OMP_BIND="spread"
time_str_grappolo = """
graph        threads  mode   time          vtune

friendster	16	dram	6108.146365	nan
friendster	32	dram	3291.561375	nan
friendster	64	dram	1737.327125	nan
friendster	128	dram	1206.608416	nan
friendster	192	dram	815.121272	nan

friendster     16     dram2  8900.193947    nan
friendster     32     dram2  4612.699978     nan
friendster     64     dram2  2586.44825     nan
friendster    128     dram2  2705.212855     nan
friendster    192     dram2  1866.698581 nan

friendster	16	mem	9049.91349	nan
friendster	32	mem	4712.569829	nan
friendster	64	mem	2395.902007	nan
friendster	128	mem	1472.592003	nan
friendster	192	mem	1001.308132	nan

friendster     16     mem2  6334.30156     nan
friendster     32     mem2  3422.950919     nan
friendster     64     mem2  1808.205431     nan
friendster    128     mem2  1331.800894     nan
friendster    192     mem2  910.551906   nan

friendster     16     kdax   6115.285544     nan
friendster     32     kdax   3277.245072     nan
friendster     64     kdax   1730.002233     nan
friendster    128     kdax   1217.872113     nan
friendster    192     kdax   831.718546   nan

friendster     16     kdax2  6315.315139     nan
friendster     32     kdax2  3405.996753     nan
friendster     64     kdax2  1795.703769     nan
friendster    128     kdax2  1280.399464     nan
friendster    192     kdax2  871.777816  nan


moliere2016	16	dram	1740.89824	nan
moliere2016	32	dram	1268.565434	nan
moliere2016	64	dram	1040.750488	nan
moliere2016	128	dram	1053.145704	nan
moliere2016	192	dram	1087.043682	nan

moliere2016    16     dram2  2196.201571   nan
moliere2016    32     dram2  1627.857007   nan
moliere2016    64     dram2  1353.701563   nan
moliere2016   128     dram2  1384.624448  nan
moliere2016   192     dram2  1487.071147   nan

moliere2016	16	mem	2283.23591	nan
moliere2016	32	mem	1509.721751	nan
moliere2016	64	mem	1213.933818	nan
moliere2016	128	mem	1172.088261	nan
moliere2016	192	mem	1184.648746	nan

moliere2016    16     mem2   1733.342295   nan
moliere2016    32     mem2   1267.900822   nan
moliere2016    64     mem2   1049.214647   nan
moliere2016   128     mem2   1033.591182  nan
moliere2016   192     mem2   1066.428858   nan

moliere2016    16     kdax   1687.235732   nan
moliere2016    32     kdax   1261.021346   nan
moliere2016    64     kdax   1025.460897   nan
moliere2016   128     kdax   1020.176169   nan
moliere2016   192     kdax   1044.276406   nan

moliere2016    16     kdax2   1752.35533   nan
moliere2016    32     kdax2  1295.938841   nan
moliere2016    64     kdax2   1065.963009   nan
moliere2016   128     kdax2   1056.69766  nan
moliere2016   192     kdax2   1089.281308   nan


clueweb12     192     dram      nan            nan

clueweb12	16	mem	8716.411615	nan
clueweb12	32	mem	8369.202979	nan
clueweb12	64	mem	6421.767673	nan
clueweb12	128	mem	6171.596182	nan
clueweb12	192	mem	5946.314627	4391.67807

clueweb12      16     mem2  8883.298213     nan
clueweb12      32     mem2  6093.823997    nan
clueweb12      64     mem2  4928.782831     nan
clueweb12     128     mem2  4630.196742     nan
clueweb12     192     mem2  4485.642789     nan

clueweb12      16     kdax   8527.07952     nan
clueweb12      32     kdax   7252.276714    nan
clueweb12      64     kdax   6873.644474    nan
clueweb12     128     kdax   5273.949972    nan
clueweb12     192     kdax   5201.659599    nan

clueweb12      16     kdax2  9422.80935     nan
clueweb12      32     kdax2 7650.283013    nan
clueweb12      64     kdax2  5774.39356     nan
clueweb12     128     kdax2  5347.667624     nan
clueweb12     192     kdax2  5311.055422     nan



uk2014        192     dram      nan                 nan

uk2014	        16	mem	2480.133789	nan
uk2014	        32	mem	1507.191533	nan
uk2014	        64	mem	1030.207204	nan
uk2014	        128	mem	820.76091	nan
uk2014	        192	mem	730.57113	nan

uk2014         16     mem2     2139.020451    nan
uk2014         32     mem2     1313.469828    nan
uk2014         64     mem2     998.098469    nan
uk2014        128     mem2     785.121212     nan
uk2014        192     mem2     639.85604     nan

uk2014         16     kdax     2045.68806    nan
uk2014         32     kdax     1343.271699   nan
uk2014         64     kdax     954.808604    nan
uk2014        128     kdax     711.649813    nan
uk2014        192     kdax     650.512289    nan

uk2014         16     kdax2    2056.676445    nan
uk2014         32     kdax2     1236.632777    nan
uk2014         64     kdax2     902.916839    nan
uk2014        128     kdax2     693.824208     nan
uk2014        192     kdax2     573.446422    nan
"""


# pdax is deprecated because others are more interesting
"""
friendster	16	pdax	6208.110773	nan
friendster	32	pdax	3315.598536	nan
friendster	64	pdax	1753.159035	nan
friendster	128	pdax	1254.869725	nan
friendster	192	pdax	862.197138	nan

moliere2016	16	pdax	1688.480594	nan
moliere2016	32	pdax	1243.435306	nan
moliere2016	64	pdax	1014.946138	nan
moliere2016	128	pdax	1010.317629	nan
moliere2016	192	pdax	1035.451193	nan

clueweb12     192     pdax      nan            nan

uk2014        192     pdax      nan            nan
"""


# kdax1a is default kdax with memkind-interleave
"""
friendster     16     kdax1a  6262.133789     nan
friendster     32     kdax1a  3339.329952     nan
friendster     64     kdax1a  1756.448787     nan
friendster    128     kdax1a  1229.417182     nan
friendster    192     kdax1a  835.125813    nan

moliere2016    16     kdax1a   1676.856578   nan
moliere2016    32     kdax1a   1227.871906   nan
moliere2016    64     kdax1a   1008.314671   nan
moliere2016   128     kdax1a   996.192363   nan
moliere2016   192     kdax1a   1018.043756   nan

clueweb12      16     kdax1a  9669.421129     nan
clueweb12      32     kdax1a  7572.09087     nan
clueweb12      64     kdax1a  6840.693432     nan
clueweb12     128     kdax1a  5814.080951     nan
clueweb12     192     kdax1a  5159.313038     nan

uk2014         16     kdax1a     2053.882734    nan
uk2014         32     kdax1a     1759.597141    nan
uk2014         64     kdax1a     942.007022     nan
uk2014        128     kdax1a     676.873518     nan
uk2014        192     kdax1a     665.310788     nan
"""



# OMP_PLACES="", OMP_BIND=""
time_str_grappolo_OLD = """
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

clueweb12	16	mem	9468.856975	nan
clueweb12	32	mem	6786.975992	nan
clueweb12	64	mem	6527.736969	nan
clueweb12	128	mem	4750.106394	nan
clueweb12	192	mem	4373.245214	4391.67807

clueweb12      16     kdax    10812.81699      nan
clueweb12      32     kdax     7882.519231     nan
clueweb12      64     kdax     6170.163424     nan
clueweb12     128     kdax     5074.019396     nan
clueweb12     192     kdax     4968.696484     5667.603504

clueweb12     192     pdax      nan            nan


uk2014        192     dram      nan                 nan

uk2014	        16	mem	2213.348559	nan
uk2014	        32	mem	1453.66062	nan
uk2014	        64	mem	1027.169626	nan
uk2014	        128	mem	734.025436	nan
uk2014	        192	mem	642.420118	698.740065

uk2014         16     kdax     2241.499411     nan
uk2014         32     kdax     1477.130957     nan
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

slash	2	kdax1	nan	nan
slash	4	kdax1	nan	nan
slash	8	kdax1	nan	nan
slash	16	kdax1	nan	nan
slash	32	kdax1	64.10	nan
slash	64	kdax1	66.03	nan
slash	128	kdax1	nan	nan
slash	192	kdax1	46.58	nan

slash	2	kdax2	nan	nan
slash	4	kdax2	nan	nan
slash	8	kdax2	nan	nan
slash	16	kdax2	nan	nan
slash	32	kdax2	40.23	45.664748
slash	64	kdax2	37.38	43.11986708
slash	128	kdax2	nan	nan
slash	192	kdax2	29.12	40.62709505

slash	2	kdax3	nan	nan
slash	4	kdax3	nan	nan
slash	8	kdax3	nan	nan
slash	16	kdax3	nan	nan
slash	32	kdax3	39.50	43.77249092
slash	64	kdax3	35.39	40.34433134
slash	128	kdax3	nan	nan
slash	192	kdax3	26.61	38.77803595


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

twitter	2	kdax1	nan	nan
twitter	4	kdax1	nan	nan
twitter	8	kdax1	nan	nan
twitter	16	kdax1	nan	nan
twitter	32	kdax1	141.27	nan
twitter	64	kdax1	125.70	nan
twitter	128	kdax1	nan	nan
twitter	192	kdax1	71.81	nan

twitter	2	kdax2	nan	nan
twitter	4	kdax2	nan	nan
twitter	8	kdax2	nan	nan
twitter	16	kdax2	nan	nan
twitter	32	kdax2	75.73	78.84232883
twitter	64	kdax2	70.83	77.23828308
twitter	128	kdax2	nan	nan
twitter	192	kdax2	33.21	55.70712258

twitter	2	kdax3	nan	nan
twitter	4	kdax3	nan	nan
twitter	8	kdax3	nan	nan
twitter	16	kdax3	nan	nan
twitter	32	kdax3	66.07	71.32162039
twitter	64	kdax3	59.45	63.05750133
twitter	128	kdax3	nan	nan
twitter	192	kdax3	37.97	50.44523449


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

talk	2	kdax1	nan	nan
talk	4	kdax1	nan	nan
talk	8	kdax1	nan	nan
talk	16	kdax1	nan	nan
talk	32	kdax1	101.20	nan
talk	64	kdax1	101.98	nan
talk	128	kdax1	nan	nan
talk	192	kdax1	123.27	nan

talk	2	kdax2	nan	nan
talk	4	kdax2	nan	nan
talk	8	kdax2	nan	nan
talk	16	kdax2	nan	nan
talk	32	kdax2	86.90	88.26351887
talk	64	kdax2	76.12	81.04203942
talk	128	kdax2	nan	nan
talk	192	kdax2	71.57	77.98582283

talk	2	kdax3	nan	nan
talk	4	kdax3	nan	nan
talk	8	kdax3	nan	nan
talk	16	kdax3	nan	nan
talk	32	kdax3	76.53	79.71498115
talk	64	kdax3	70.61	74.92748809
talk	128	kdax3	nan	nan
talk	192	kdax3	84.81	98.67837559


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

pokec	2	kdax1	nan	nan
pokec	4	kdax1	nan	nan
pokec	8	kdax1	nan	nan
pokec	16	kdax1	nan	nan
pokec	32	kdax1	2450.37	nan
pokec	64	kdax1	1639.97	nan
pokec	128	kdax1	nan	nan
pokec	192	kdax1	1974.83	nan

pokec	2	kdax2	nan	nan
pokec	4	kdax2	nan	nan
pokec	8	kdax2	nan	nan
pokec	16	kdax2	nan	nan
pokec	32	kdax2	2237.83	2199.75474
pokec	64	kdax2	1384.91	1437.639276
pokec	128	kdax2	nan	nan
pokec	192	kdax2	1262.70	1267.780125

pokec	2	kdax3	nan	nan
pokec	4	kdax3	nan	nan
pokec	8	kdax3	nan	nan
pokec	16	kdax3	nan	nan
pokec	32	kdax3	2659.48	2764.888682
pokec	64	kdax3	2338.70	2313.266827
pokec	128	kdax3	nan	nan
pokec	192	kdax3	3013.94	3153.660593


topcats	2	mem	19722.79	nan
topcats	4	mem	9400.69	nan
topcats	8	mem	4698.85	nan
topcats	16	mem	2543.83	nan
topcats	32	mem	1518.52	nan
topcats	64	mem	1041.00	nan
topcats	128	mem	880.35	nan
topcats	192	mem	867.02	nan

topcats	2	kdax1	nan	nan
topcats	4	kdax1	nan	nan
topcats	8	kdax1	nan	nan
topcats	16	kdax1	nan	nan
topcats	32	kdax1	2298.37	nan
topcats	64	kdax1	1891.35	nan
topcats	128	kdax1	nan	nan
topcats	192	kdax1	2368.92	nan

topcats	2	kdax2	nan	nan
topcats	4	kdax2	nan	nan
topcats	8	kdax2	nan	nan
topcats	16	kdax2	nan	nan
topcats	32	kdax2	2089.34	2065.797776
topcats	64	kdax2	1487.88	1499.681414
topcats	128	kdax2	nan	nan
topcats	192	kdax2	1437.10	1512.404942

topcats	2	kdax3	nan	nan
topcats	4	kdax3	nan	nan
topcats	8	kdax3	nan	nan
topcats	16	kdax3	nan	nan
topcats	32	kdax3	2842.89	2894.704997
topcats	64	kdax3	2778.72	2718.955827
topcats	128	kdax3	nan	nan
topcats	192	kdax3	3400.19	3375.656995
"""

# kdax4/X
# slash	2	kdaxX	nan	nan
# slash	4	kdaxX	nan	nan
# slash	8	kdaxX	nan	nan
# slash	16	kdaxX	nan	nan
# slash	32	kdaxX	37.79	40.4645827
# slash	64	kdaxX	34.47	38.49604419
# slash	128	kdaxX	nan	nan
# slash	192	kdaxX	25.45	41.54662348

# twitter	2	kdaxX	nan	nan
# twitter	4	kdaxX	nan	nan
# twitter	8	kdaxX	nan	nan
# twitter	16	kdaxX	nan	nan
# twitter	32	kdaxX	64.46	69.03614913
# twitter	64	kdaxX	58.11	65.7562004
# twitter	128	kdaxX	nan	nan
# twitter	192	kdaxX	37.14	55.71388362

# talk	2	kdaxX	nan	nan
# talk	4	kdaxX	nan	nan
# talk	8	kdaxX	nan	nan
# talk	16	kdaxX	nan	nan
# talk	32	kdaxX	73.46	73.77388803
# talk	64	kdaxX	69.65	75.43769374
# talk	128	kdaxX	nan	nan
# talk	192	kdaxX	88.87	104.2051243

# pokec	2	kdaxX	nan	nan
# pokec	4	kdaxX	nan	nan
# pokec	8	kdaxX	nan	nan
# pokec	16	kdaxX	nan	nan
# pokec	32	kdaxX	2480.16	2557.437547
# pokec	64	kdaxX	2711.26	2696.422974
# pokec	128	kdaxX	nan	nan
# pokec	192	kdaxX	6173.22	6303.312064

# topcats	2	kdaxX	nan	nan
# topcats	4	kdaxX	nan	nan
# topcats	8	kdaxX	nan	nan
# topcats	16	kdaxX	nan	nan
# topcats	32	kdaxX	2358.83	2369.970634
# topcats	64	kdaxX	4986.54	5099.429601
# topcats	128	kdaxX	nan	nan
# topcats	192	kdaxX	6396.29	6483.311098


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

# *** OLD ***

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

clueweb12_t192_dramBw_mem_str = """
dram_bw time                   class
    0	16352.126194196899	Low
    9	1071.0645441908998	Low
    18	290.72684328259993	Low
    27	206.25008894840005	Low
    36	108.7195315162	Low
    45	78.322818588	Low
    54	54.26652430740002	Low
    63	59.11507974380003	Low
    72	62.658254870400015	Low
    81	36.364165773	Low
    90	42.7978258713	Low
    99	26.480571998800016	Low
    108	23.8698113792	Low
    117	34.68581966040001	Low
    126	44.47617198389998	Low
    135	155.43349831690006	Medium
    144	0.5594487042	Medium
    153	0.2797243521	Medium
    162	0	Medium
    171	0	Medium
    180	0	Medium
    189	0	Medium
    198	0.0932414507	Medium
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

clueweb12_t192_pmemBw_mem_str = """
dram_bw time                   class
    0	17480.534230568297	Low
    3	301.72933446520005	Low
    6	73.84722895439998	Low
    9	65.82846419420001	Low
    12	56.411077673499996	Low
    15	106.20201234730001	Low
    18	77.48364553169998	Low
    21	45.1288621388	Low
    24	70.58377817990001	Low
    27	51.28279788500001	Low
    30	43.5437574769	Low
    33	10.8160082812	Low
    36	16.224012421799998	Medium
    39	23.496845576400002	Medium
    42	17.3429098302	Medium
    45	9.324145070000004	Medium
    48	13.053803097999996	Medium
    51	37.669546082800004	Medium
    54	106.76146105149999	Medium
    57	41.026238307999996	Medium
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

clueweb12_t192_dramBw_kdax_str = """
dram_bw time                   class
    0	16397.5725866291	Low
    10	666.355956993	Low
    20	157.2684075015	Low
    30	213.62948397950007	Low
    40	54.785766886999994	Low
    50	8.489168351499996	Low
    60	1.7503439899999997	Low
    70	1.0502063940000002	Low
    80	0.9626891945000002	Low
    90	0.9626891945000002	Low
    100	0.5251031970000001	Low
    110	0.0875171995	Low
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
    0	15660.590249639601	Low
    3	487.5583184145	Low
    6	307.27288744449993	Low
    9	238.13429983949996	Low
    12	193.58804529399995	Low
    15	89.3550606895	Low
    18	63.0999008395	Low
    21	45.50894374	Low
    24	23.979712663000008	Low
    27	19.953921486	Low
    30	29.668330630499995	Low
    33	32.556398214	Low
    36	43.93363414900001	Medium
    39	51.985216503000004	Medium
    42	15.052958314000001	Medium
    45	5.3385491695	Medium
    48	7.701513555999998	Medium
    51	6.0386867655	Medium
    54	5.951169565999999	Medium
    57	4.200825576000001	Medium
    60	6.476272763000002	Medium
    63	9.5393747455	Medium
    66	17.153371101999998	Medium
    69	17.9410258975	Medium
    72	13.827717520999999	Medium
    75	5.688617967499999	Medium
    78	7.789030755500002	Medium
    81	7.526479156999998	Medium
    84	28.88067583499999	High
    87	40.43294616899999	High
    90	16.5407507055	High
    93	0.175034399	High
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

uk2014_t192_dramBw_mem_str = """
dram_bw time                   class
    0	13020.645570780998	Low
    10	49.84270639199999	Low
    20	139.83648182200008	Low
    30	71.09508258969997	Low
    40	82.24046554680001	Low
    50	116.71500413460004	Low
    60	99.5469608218	Low
    70	28.798008137600004	Low
    80	31.56704738159999	Low
    90	18.27565901040001	Low
    100	12.8068065035	Low
    110	3.5305250360999985	Low
    120	3.4612990549999987	Low
    130	5.330400544699998	Low
    140	3.3228470927999987	Medium
    150	10.0377672595	Medium
    160	24.782901233799986	Medium
    170	53.65013535249999	Medium
    180	67.35687961029998	Medium
    190	0.3461299055	Medium
    200	0.3461299055	Medium
    210	0.4845818677	Medium
    220	0.4845818677	Medium
    230	0.3461299055	Medium
    240	0.2076779433	Medium
    250	0.1384519622	Medium
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

uk2014_t192_pmemBw_mem_str = """
dram_bw time                   class
    0	13005.831210825601	Low
    3	44.7892097717	Low
    6	16.2681055585	Low
    9	32.53621111700001	Low
    12	39.528035208100015	Low
    15	106.33110696960001	Low
    18	101.69296623590003	Low
    21	107.92330453490001	Low
    24	58.5651800106	Low
    27	30.320979721799997	Low
    30	42.366300433199996	Low
    33	20.1447605001	Low
    36	11.353060900400001	Medium
    39	25.7520649692	Medium
    42	10.1069932406	Medium
    45	17.3757212561	Medium
    48	4.2227848471	Medium
    51	3.1151691494999993	Medium
    54	1.384519622	Medium
    57	1.7998755086	Medium
    60	3.8766549416	Medium
    63	3.6689769983000007	Medium
    66	1.9383274708	Medium
    69	4.0843328849	Medium
    72	13.429840333399998	Medium
    75	14.122100144400003	Medium
    78	6.230338299	Medium
    81	10.1069932406	Medium
    84	106.12342902630002	High
    87	0.2076779433	High
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
    0	13649.725671445602	Low
    10	384.34874941269993	Low
    20	120.06916172479998	Low
    30	4.601707259500001	Low
    40	0.2123864889	Low
    50	0	Low
    60	0	Low
    70	0.0707954963	Low
    80	0.0707954963	Low
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
    0	13033.238489665202	Low
    3	110.79495170949998	Low
    6	222.36865387830002	Low
    9	294.3676736153999	Low
    12	35.326952653700005	Low
    15	12.955575822899998	Low
    18	13.451144297	Low
    21	16.424555141600003	Low
    24	18.760806519499997	Low
    27	30.3712679127	Low
    30	63.29117369219999	Low
    33	82.1935712043	Low
    36	36.6720670834	Medium
    39	2.2654558816	Medium
    42	2.5486378667999996	Medium
    45	0.9203414519	Medium
    48	0.35397748149999997	Medium
    51	0.35397748149999997	Medium
    54	0.9911369482000001	Medium
    57	1.0619324444999998	Medium
    60	1.6990919112	Medium
    63	1.6282964148999997	Medium
    66	1.0619324445	Medium
    69	0.9203414519	Medium
    72	0.8495459556	Medium
    75	1.6990919112	Medium
    78	1.6282964148999999	Medium
    81	2.4778423705000003	Medium
    84	4.955684740999999	High
    87	13.6635307859	High
    90	12.035234371	High
    93	9.132619022699998	High
    96	29.1677444756	High
    99	63.43276468479999	High
    102	34.7605886833	High
    105	1.2743189334000002	High
    108	0	High
    111	0	High
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
    6	30686003040
    7	395619450240
    8	32251272480
    9	17496447360
    11	43212960
    12	3058517280
    13	797039040
    14	1632489600
    15	3807541920
    16	4575772320
    17	1065919680
    18	556967040
    19	393718080
    20	480144000
    21	321696480
    22	393718080
    23	705811680
    24	480144000
    25	542562720
    26	244873440
    27	172851840
    28	230469120
    29	201660480
    30	158447520
    31	110433120
    32	129638880
    33	115234560
    34	81624480
    35	33610080
    36	52815840
    37	81624480
    38	43212960
    39	72021600
    40	43212960
    41	38411520
    42	33610080
    43	48014400
    44	62418720
    45	38411520
    46	48014400
    47	38411520
    48	48014400
    49	43212960
    50	28808640
    51	48014400
    52	9602880
    53	24007200
    54	48014400
    55	33610080
    56	33610080
    57	43212960
    58	62418720
    59	33610080
    60	48014400
    61	48014400
    62	33610080
    63	43212960
    64	81624480
    65	43212960
    66	38411520
    67	57617280
    68	43212960
    69	38411520
    70	52815840
    71	43212960
    72	24007200
    73	62418720
    74	48014400
    75	48014400
    76	76823040
    77	33610080
    78	28808640
    79	33610080
    80	43212960
    81	28808640
    82	43212960
    83	43212960
    84	24007200
    85	33610080
    86	33610080
    87	24007200
    88	33610080
    89	38411520
    90	52815840
    91	24007200
    92	43212960
    93	28808640
    94	48014400
    95	24007200
    96	24007200
    97	14404320
    98	14404320
    99	33610080
    100	19205760
    101	28808640
    102	28808640
    103	28808640
    104	14404320
    105	28808640
    106	33610080
    107	9602880
    108	28808640
    109	33610080
    110	28808640
    111	9602880
    112	9602880
    113	19205760
    114	4801440
    115	19205760
    116	19205760
    117	4801440
    118	14404320
    119	14404320
    120	28808640
    121	9602880
    122	4801440
    123	4801440
    124	14404320
    125	4801440
    126	4801440
    127	4801440
    129	9602880
    130	19205760
    132	14404320
    133	9602880
    134	4801440
    135	9602880
    136	14404320
    137	9602880
    138	14404320
    140	9602880
    141	9602880
    143	14404320
    144	4801440
    145	9602880
    146	9602880
    147	19205760
    148	24007200
    149	4801440
    150	14404320
    152	9602880
    153	4801440
    154	14404320
    155	19205760
    156	14404320
    157	4801440
    158	4801440
    159	14404320
    160	9602880
    162	4801440
    163	4801440
    165	4801440
    166	4801440
    167	9602880
    168	4801440
    169	9602880
    171	4801440
    172	14404320
    173	24007200
    174	4801440
    175	14404320
    176	9602880
    177	14404320
    180	4801440
    181	4801440
    182	4801440
    183	19205760
    184	4801440
    185	4801440
    186	4801440
    187	4801440
    189	4801440
    190	4801440
    192	14404320
    193	9602880
    195	4801440
    197	14404320
    198	4801440
    199	9602880
    200	4801440
    201	4801440
    202	4801440
    204	4801440
    205	4801440
    208	9602880
    211	9602880
    212	9602880
    213	4801440
    214	9602880
    215	4801440
    216	4801440
    219	14404320
    220	9602880
    221	14404320
    222	19205760
    223	4801440
    224	19205760
    225	4801440
    226	9602880
    227	4801440
    228	14404320
    229	4801440
    230	19205760
    231	14404320
    232	9602880
    233	14404320
    234	19205760
    235	24007200
    236	24007200
    237	38411520
    238	38411520
    239	9602880
    240	33610080
    241	33610080
    242	33610080
    243	38411520
    244	48014400
    245	43212960
    246	33610080
    247	62418720
    248	28808640
    249	38411520
    250	43212960
    251	19205760
    252	28808640
    253	28808640
    254	14404320
    255	38411520
    256	48014400
    257	38411520
    258	14404320
    259	52815840
    260	33610080
    261	57617280
    262	38411520
    263	48014400
    264	33610080
    265	33610080
    266	33610080
    267	52815840
    268	33610080
    269	4801440
    270	19205760
    271	43212960
    272	28808640
    273	38411520
    274	48014400
    275	19205760
    276	38411520
    277	24007200
    278	38411520
    279	43212960
    280	19205760
    281	38411520
    282	38411520
    283	24007200
    284	19205760
    285	24007200
    286	24007200
    287	33610080
    288	28808640
    289	4801440
    290	14404320
    291	24007200
    292	9602880
    293	33610080
    294	4801440
    295	14404320
    296	9602880
    297	14404320
    298	19205760
    299	4801440
    300	24007200
    301	14404320
    302	4801440
    303	24007200
    304	9602880
    305	9602880
    306	28808640
    307	19205760
    309	14404320
    310	4801440
    311	19205760
    312	4801440
    313	9602880
    314	9602880
    316	9602880
    318	19205760
    319	9602880
    321	4801440
    323	4801440
    326	14404320
    329	9602880
    330	4801440
    331	4801440
    333	4801440
    334	9602880
    335	19205760
    336	4801440
    337	4801440
    338	4801440
    339	14404320
    342	4801440
    344	4801440
    347	9602880
    348	4801440
    350	4801440
    356	14404320
    357	4801440
    358	4801440
    360	9602880
    363	14404320
    364	9602880
    365	4801440
    366	4801440
    369	4801440
    370	9602880
    374	4801440
    375	14404320
    377	4801440
    378	9602880
    382	4801440
    384	4801440
    386	4801440
    390	4801440
    391	4801440
    393	4801440
    395	4801440
    396	9602880
    398	9602880
    399	4801440
    401	9602880
    403	4801440
    404	4801440
    406	14404320
    407	4801440
    408	9602880
    409	19205760
    410	28808640
    411	19205760
    412	28808640
    413	4801440
    414	9602880
    415	4801440
    416	14404320
    417	14404320
    418	24007200
    419	24007200
    420	4801440
    421	4801440
    422	33610080
    423	4801440
    424	14404320
    425	4801440
    426	14404320
    427	9602880
    428	28808640
    429	9602880
    430	9602880
    431	33610080
    432	38411520
    433	38411520
    434	9602880
    435	33610080
    436	9602880
    437	19205760
    438	38411520
    439	24007200
    440	19205760
    441	19205760
    442	14404320
    443	19205760
    444	9602880
    445	28808640
    446	28808640
    447	19205760
    448	9602880
    449	24007200
    450	24007200
    451	33610080
    452	24007200
    453	4801440
    454	24007200
    455	28808640
    456	28808640
    457	24007200
    458	19205760
    459	4801440
    460	33610080
    461	19205760
    462	24007200
    463	28808640
    464	9602880
    465	24007200
    466	24007200
    467	4801440
    468	9602880
    469	14404320
    470	24007200
    471	4801440
    472	14404320
    473	4801440
    475	19205760
    477	24007200
    478	4801440
    479	9602880
    480	14404320
    481	14404320
    482	9602880
    483	19205760
    484	24007200
    486	9602880
    487	9602880
    488	28808640
    489	4801440
    490	19205760
    491	4801440
    492	19205760
    494	4801440
    495	4801440
    497	9602880
    498	9602880
    499	4801440
    500	14404320
    501	19205760
    502	4801440
    504	4801440
    505	14404320
    506	24007200
    508	19205760
    509	4801440
    510	4801440
    511	9602880
    512	4801440
    513	4801440
    515	9602880
    516	9602880
    517	19205760
    518	9602880
    519	24007200
    520	14404320
    521	4801440
    522	14404320
    524	4801440
    525	4801440
    526	14404320
    527	4801440
    528	19205760
    529	4801440
    530	9602880
    531	9602880
    532	14404320
    533	4801440
    535	14404320
    536	4801440
    537	9602880
    539	9602880
    540	4801440
    545	9602880
    546	4801440
    549	4801440
    550	4801440
    551	4801440
    552	4801440
    553	4801440
    555	4801440
    556	4801440
    558	4801440
    560	4801440
    561	4801440
    565	4801440
    566	4801440
    572	4801440
    580	4801440
    581	4801440
    582	4801440
    584	4801440
    594	4801440
    599	4801440
    604	4801440
    612	4801440
    613	4801440
    618	4801440
    623	4801440
    636	4801440
    643	4801440
    644	4801440
    652	4801440
    659	4801440
    661	4801440
    673	4801440
    693	4801440
    698	4801440
    699	4801440
    719	4801440
    725	4801440
    740	4801440
    786	4801440
    821	4801440
    826	4801440
    828	4801440
    838	4801440
    882	4801440
    889	4801440
    918	4801440
    957	4801440
    960	4801440
    984	9602880
    985	4801440
    1035	4801440
    1055	4801440
    1057	4801440
    1070	4801440
    1098	4801440
    1115	4801440
    1174	4801440
    1204	4801440
    1242	4801440
    1278	4801440
    1283	4801440
    1357	4801440
    1369	4801440
    1447	4801440
    1517	4801440
    1549	4801440
    1555	4801440
    1671	4801440
    1849	4801440
    1891	4801440
"""

friendster_t192_latency_pdax_str = """
    6	31247771520
    7	398572335840
    8	30239469120
    9	17366808480
    11	28808640
    12	2808842400
    13	792237600
    14	1339601760
    15	3226567680
    16	4134039840
    17	941082240
    18	552165600
    19	398519520
    20	494548320
    21	297689280
    22	369710880
    23	604981440
    24	456136800
    25	576172800
    26	254476320
    27	235270560
    28	177653280
    29	158447520
    30	124837440
    31	100830240
    32	115234560
    33	81624480
    34	100830240
    35	67220160
    36	81624480
    37	48014400
    38	76823040
    39	62418720
    40	43212960
    41	33610080
    42	57617280
    43	57617280
    44	33610080
    45	43212960
    46	28808640
    47	43212960
    48	48014400
    49	33610080
    50	52815840
    51	48014400
    52	52815840
    53	33610080
    54	24007200
    55	19205760
    56	52815840
    57	33610080
    58	28808640
    59	57617280
    60	57617280
    61	38411520
    62	33610080
    63	24007200
    64	62418720
    65	57617280
    66	43212960
    67	57617280
    68	38411520
    69	72021600
    70	57617280
    71	62418720
    72	57617280
    73	28808640
    74	33610080
    75	19205760
    76	33610080
    77	43212960
    78	43212960
    79	28808640
    80	57617280
    81	24007200
    82	19205760
    83	72021600
    84	33610080
    85	33610080
    86	33610080
    87	52815840
    88	24007200
    89	38411520
    90	38411520
    91	38411520
    92	24007200
    93	33610080
    94	28808640
    95	28808640
    96	33610080
    97	24007200
    98	38411520
    99	19205760
    100	38411520
    101	28808640
    102	43212960
    103	38411520
    104	28808640
    105	19205760
    106	14404320
    107	14404320
    108	4801440
    109	9602880
    110	19205760
    111	28808640
    112	9602880
    113	28808640
    114	38411520
    115	14404320
    116	9602880
    117	4801440
    118	19205760
    119	9602880
    120	28808640
    121	28808640
    122	28808640
    123	24007200
    124	9602880
    125	28808640
    126	4801440
    127	28808640
    129	28808640
    130	4801440
    131	24007200
    132	9602880
    133	14404320
    134	9602880
    136	4801440
    137	19205760
    138	14404320
    139	9602880
    141	9602880
    142	4801440
    143	9602880
    144	14404320
    145	9602880
    146	14404320
    147	4801440
    148	14404320
    149	4801440
    150	9602880
    152	19205760
    153	24007200
    154	14404320
    155	4801440
    156	9602880
    157	4801440
    158	9602880
    159	9602880
    160	19205760
    161	4801440
    162	19205760
    163	4801440
    164	4801440
    166	9602880
    168	4801440
    169	9602880
    170	4801440
    171	14404320
    172	24007200
    173	14404320
    174	9602880
    175	9602880
    176	4801440
    180	4801440
    181	9602880
    182	4801440
    183	14404320
    185	4801440
    187	4801440
    188	4801440
    189	9602880
    190	9602880
    191	9602880
    192	14404320
    193	4801440
    194	9602880
    195	4801440
    196	14404320
    197	4801440
    198	19205760
    199	4801440
    202	9602880
    204	4801440
    205	14404320
    206	9602880
    207	14404320
    208	9602880
    209	19205760
    210	4801440
    211	14404320
    212	4801440
    213	9602880
    214	24007200
    215	4801440
    217	4801440
    218	14404320
    219	19205760
    221	4801440
    222	9602880
    223	14404320
    224	28808640
    225	9602880
    227	4801440
    228	9602880
    229	28808640
    230	38411520
    231	14404320
    232	33610080
    233	52815840
    234	24007200
    235	19205760
    236	33610080
    237	38411520
    238	19205760
    239	19205760
    240	57617280
    241	14404320
    242	38411520
    244	33610080
    245	24007200
    246	48014400
    247	24007200
    248	19205760
    249	48014400
    250	57617280
    251	62418720
    252	57617280
    253	43212960
    254	43212960
    255	38411520
    256	67220160
    257	9602880
    258	4801440
    259	9602880
    260	33610080
    261	19205760
    262	24007200
    263	24007200
    264	43212960
    265	14404320
    266	33610080
    267	33610080
    268	33610080
    269	14404320
    270	38411520
    271	24007200
    272	38411520
    273	38411520
    274	28808640
    275	9602880
    276	28808640
    277	19205760
    278	28808640
    279	43212960
    280	19205760
    281	33610080
    282	9602880
    283	14404320
    284	43212960
    285	24007200
    286	14404320
    287	9602880
    288	4801440
    289	9602880
    290	4801440
    291	4801440
    292	24007200
    293	24007200
    294	19205760
    295	9602880
    296	24007200
    297	33610080
    298	4801440
    299	14404320
    300	19205760
    301	9602880
    302	24007200
    303	9602880
    304	24007200
    305	28808640
    306	4801440
    308	14404320
    309	14404320
    310	14404320
    311	4801440
    312	9602880
    313	4801440
    314	19205760
    315	14404320
    316	14404320
    318	9602880
    319	9602880
    320	4801440
    321	14404320
    322	4801440
    323	4801440
    324	4801440
    325	4801440
    327	9602880
    328	14404320
    329	4801440
    330	19205760
    332	14404320
    334	14404320
    335	4801440
    337	9602880
    338	9602880
    339	9602880
    341	4801440
    342	14404320
    343	4801440
    344	9602880
    345	4801440
    346	9602880
    349	9602880
    350	28808640
    351	9602880
    352	9602880
    353	4801440
    355	4801440
    358	4801440
    359	4801440
    360	4801440
    361	9602880
    362	4801440
    364	19205760
    365	9602880
    366	4801440
    368	14404320
    369	14404320
    370	19205760
    371	4801440
    374	4801440
    376	4801440
    377	4801440
    380	4801440
    383	4801440
    384	4801440
    387	9602880
    388	14404320
    389	4801440
    390	4801440
    393	4801440
    396	4801440
    398	4801440
    399	9602880
    400	24007200
    401	9602880
    402	14404320
    403	9602880
    404	9602880
    406	4801440
    407	14404320
    410	19205760
    412	19205760
    413	9602880
    414	33610080
    415	4801440
    416	9602880
    417	19205760
    419	4801440
    420	24007200
    421	9602880
    422	19205760
    423	14404320
    424	38411520
    425	14404320
    426	14404320
    427	4801440
    428	24007200
    429	19205760
    430	19205760
    431	9602880
    432	19205760
    433	9602880
    434	9602880
    435	9602880
    436	4801440
    437	19205760
    438	4801440
    439	14404320
    440	14404320
    441	14404320
    442	24007200
    443	4801440
    444	19205760
    445	4801440
    446	9602880
    447	9602880
    448	33610080
    449	38411520
    450	14404320
    452	19205760
    453	19205760
    454	19205760
    456	24007200
    457	28808640
    458	24007200
    459	19205760
    460	14404320
    462	28808640
    463	19205760
    464	9602880
    465	24007200
    466	19205760
    468	28808640
    469	4801440
    470	9602880
    471	9602880
    472	9602880
    473	9602880
    474	14404320
    475	19205760
    476	28808640
    477	9602880
    478	24007200
    479	24007200
    480	9602880
    481	9602880
    482	9602880
    483	14404320
    484	9602880
    485	19205760
    486	38411520
    487	14404320
    488	24007200
    489	14404320
    490	9602880
    491	14404320
    492	9602880
    493	19205760
    494	28808640
    495	14404320
    496	24007200
    497	4801440
    498	14404320
    499	33610080
    500	4801440
    501	24007200
    502	14404320
    503	4801440
    504	19205760
    505	9602880
    506	9602880
    507	19205760
    508	19205760
    510	19205760
    511	24007200
    512	19205760
    513	19205760
    514	24007200
    516	4801440
    517	19205760
    518	9602880
    519	4801440
    520	9602880
    521	14404320
    522	14404320
    523	19205760
    524	19205760
    525	9602880
    526	14404320
    527	9602880
    528	4801440
    529	9602880
    530	9602880
    531	4801440
    532	9602880
    533	4801440
    534	4801440
    535	4801440
    536	28808640
    537	9602880
    538	14404320
    539	14404320
    540	9602880
    542	4801440
    544	4801440
    546	19205760
    547	14404320
    548	9602880
    549	9602880
    551	9602880
    555	4801440
    557	4801440
    558	4801440
    559	4801440
    560	4801440
    564	4801440
    565	4801440
    566	4801440
    569	4801440
    570	4801440
    573	4801440
    575	4801440
    577	4801440
    578	14404320
    583	4801440
    585	9602880
    587	9602880
    591	4801440
    592	4801440
    593	4801440
    595	4801440
    598	4801440
    604	4801440
    606	9602880
    607	4801440
    610	4801440
    620	4801440
    621	4801440
    623	4801440
    624	4801440
    626	4801440
    635	4801440
    642	4801440
    643	9602880
    650	4801440
    652	9602880
    654	4801440
    658	4801440
    666	4801440
    670	4801440
    678	9602880
    681	4801440
    685	4801440
    690	4801440
    691	4801440
    694	4801440
    695	4801440
    701	9602880
    704	4801440
    710	4801440
    713	4801440
    725	4801440
    727	4801440
    728	4801440
    733	9602880
    735	4801440
    737	4801440
    741	9602880
    748	4801440
    759	4801440
    760	4801440
    765	4801440
    768	4801440
    769	9602880
    771	4801440
    776	4801440
    785	4801440
    786	4801440
    790	4801440
    809	4801440
    817	9602880
    828	4801440
    835	4801440
    844	4801440
    859	4801440
    863	4801440
    881	4801440
    910	4801440
    916	9602880
    921	4801440
    933	4801440
    942	4801440
    947	4801440
    949	4801440
    963	4801440
    966	4801440
    984	4801440
    993	4801440
    995	4801440
    1014	4801440
    1016	4801440
    1044	4801440
    1064	9602880
    1066	4801440
    1077	4801440
    1087	4801440
    1108	4801440
    1113	4801440
    1118	4801440
    1121	4801440
    1125	4801440
    1136	4801440
    1140	4801440
    1154	4801440
    1159	4801440
    1164	4801440
    1170	4801440
    1173	4801440
    1175	4801440
    1176	4801440
    1178	4801440
    1212	4801440
    1223	4801440
    1228	4801440
    1229	4801440
    1236	4801440
    1237	4801440
    1247	4801440
    1261	4801440
    1271	9602880
    1275	4801440
    1278	4801440
    1284	9602880
    1299	4801440
    1300	4801440
    1306	4801440
    1347	4801440
    1402	4801440
    1428	4801440
    1468	4801440
    1507	4801440
    1552	4801440
    1592	4801440
    1624	4801440
    1739	4801440
    1761	4801440
    1820	4801440
    1945	4801440
"""

friendster_t192_latency_kdax_str = """
    Latency	Loads
    6	31415821920
    7	398020170240
    8	31319793120
    9	17256375360
    11	57617280
    12	2674402080
    13	797039040
    14	1354006080
    15	3409022400
    16	4950284640
    17	792237600
    18	763428960
    19	412923840
    20	561768480
    21	340902240
    22	446533920
    23	595378560
    24	432129600
    25	508952640
    26	240072000
    27	201660480
    28	273682080
    29	182454720
    30	139241760
    31	105631680
    32	120036000
    33	67220160
    34	43212960
    35	76823040
    36	62418720
    37	52815840
    38	52815840
    39	24007200
    40	33610080
    41	57617280
    42	62418720
    43	38411520
    44	33610080
    45	48014400
    46	38411520
    47	67220160
    48	48014400
    49	67220160
    50	43212960
    51	67220160
    52	62418720
    53	43212960
    54	43212960
    55	24007200
    56	62418720
    57	48014400
    58	52815840
    59	38411520
    60	67220160
    61	38411520
    62	28808640
    63	62418720
    64	67220160
    65	52815840
    66	48014400
    67	91227360
    68	52815840
    69	52815840
    70	48014400
    71	62418720
    72	52815840
    73	24007200
    74	48014400
    75	28808640
    76	52815840
    77	33610080
    78	52815840
    79	48014400
    80	43212960
    81	33610080
    82	28808640
    83	24007200
    84	33610080
    85	38411520
    86	28808640
    87	33610080
    88	33610080
    89	48014400
    90	19205760
    91	24007200
    92	4801440
    93	24007200
    94	38411520
    95	24007200
    96	28808640
    97	33610080
    98	28808640
    99	24007200
    100	28808640
    101	24007200
    102	19205760
    103	43212960
    104	24007200
    105	14404320
    106	24007200
    107	14404320
    108	14404320
    109	19205760
    110	38411520
    111	38411520
    112	28808640
    113	9602880
    114	9602880
    115	9602880
    116	14404320
    117	24007200
    118	4801440
    119	4801440
    120	4801440
    121	19205760
    122	4801440
    123	4801440
    124	9602880
    125	14404320
    126	14404320
    127	9602880
    128	24007200
    129	14404320
    130	9602880
    131	9602880
    132	4801440
    133	4801440
    134	14404320
    136	4801440
    137	9602880
    138	19205760
    140	4801440
    141	4801440
    142	4801440
    143	4801440
    144	4801440
    145	14404320
    147	9602880
    149	9602880
    150	4801440
    151	14404320
    152	9602880
    153	4801440
    154	4801440
    155	4801440
    156	19205760
    157	19205760
    158	9602880
    159	4801440
    160	14404320
    162	4801440
    163	4801440
    165	9602880
    167	9602880
    168	4801440
    169	14404320
    171	14404320
    172	4801440
    175	14404320
    176	9602880
    177	9602880
    178	14404320
    179	4801440
    180	14404320
    182	4801440
    183	4801440
    184	24007200
    185	4801440
    186	19205760
    187	4801440
    188	4801440
    190	4801440
    191	4801440
    192	4801440
    194	4801440
    197	9602880
    198	14404320
    199	9602880
    201	14404320
    202	4801440
    203	4801440
    204	9602880
    205	4801440
    206	4801440
    207	4801440
    208	4801440
    209	4801440
    210	14404320
    211	4801440
    212	4801440
    214	9602880
    215	4801440
    216	4801440
    217	4801440
    218	9602880
    219	4801440
    220	9602880
    221	9602880
    222	9602880
    223	19205760
    224	14404320
    225	24007200
    226	24007200
    227	24007200
    228	9602880
    229	14404320
    230	28808640
    231	9602880
    232	33610080
    233	19205760
    234	19205760
    235	24007200
    236	19205760
    237	19205760
    238	14404320
    239	19205760
    240	24007200
    241	14404320
    242	24007200
    243	14404320
    244	57617280
    245	24007200
    246	28808640
    247	48014400
    248	28808640
    249	43212960
    250	38411520
    251	48014400
    252	72021600
    253	28808640
    254	28808640
    255	19205760
    256	43212960
    257	24007200
    258	57617280
    259	24007200
    260	28808640
    261	28808640
    262	24007200
    263	24007200
    264	24007200
    265	24007200
    266	38411520
    267	19205760
    268	24007200
    269	19205760
    270	43212960
    271	38411520
    272	43212960
    273	28808640
    274	24007200
    275	57617280
    276	28808640
    277	28808640
    278	33610080
    279	28808640
    280	33610080
    281	28808640
    282	38411520
    283	43212960
    284	14404320
    285	33610080
    286	33610080
    287	14404320
    288	19205760
    289	28808640
    290	14404320
    291	9602880
    292	9602880
    293	43212960
    294	24007200
    295	19205760
    296	9602880
    297	19205760
    298	9602880
    299	14404320
    300	9602880
    301	9602880
    302	19205760
    304	28808640
    305	14404320
    306	14404320
    307	9602880
    309	4801440
    310	19205760
    311	9602880
    312	4801440
    313	14404320
    314	9602880
    315	4801440
    317	9602880
    318	4801440
    321	4801440
    323	4801440
    325	14404320
    326	9602880
    329	9602880
    330	4801440
    331	9602880
    332	9602880
    333	14404320
    334	4801440
    336	4801440
    337	4801440
    339	4801440
    340	19205760
    341	19205760
    342	9602880
    343	9602880
    344	4801440
    345	4801440
    346	9602880
    347	4801440
    348	9602880
    350	4801440
    351	4801440
    352	14404320
    353	9602880
    354	4801440
    356	4801440
    357	9602880
    359	4801440
    360	4801440
    361	9602880
    362	9602880
    363	4801440
    364	4801440
    365	14404320
    366	4801440
    369	4801440
    372	9602880
    373	9602880
    376	4801440
    377	4801440
    378	19205760
    379	14404320
    383	4801440
    384	9602880
    389	4801440
    390	9602880
    392	9602880
    393	9602880
    394	4801440
    395	4801440
    397	9602880
    398	4801440
    399	14404320
    401	19205760
    402	4801440
    404	9602880
    405	24007200
    406	9602880
    408	9602880
    409	4801440
    410	19205760
    411	9602880
    412	14404320
    413	4801440
    414	28808640
    415	19205760
    416	9602880
    417	9602880
    418	24007200
    419	19205760
    420	19205760
    421	19205760
    422	14404320
    423	19205760
    424	14404320
    425	24007200
    426	38411520
    427	14404320
    428	28808640
    429	14404320
    430	14404320
    431	19205760
    432	19205760
    434	24007200
    435	24007200
    436	19205760
    437	24007200
    438	19205760
    439	24007200
    440	28808640
    441	24007200
    442	19205760
    443	19205760
    444	33610080
    445	14404320
    446	33610080
    447	19205760
    448	43212960
    449	24007200
    450	19205760
    451	4801440
    452	24007200
    453	9602880
    454	4801440
    455	19205760
    456	9602880
    457	14404320
    458	14404320
    459	24007200
    460	9602880
    461	9602880
    462	14404320
    463	9602880
    464	4801440
    465	14404320
    466	4801440
    467	4801440
    468	24007200
    469	14404320
    470	9602880
    471	9602880
    472	9602880
    473	9602880
    474	24007200
    475	4801440
    476	19205760
    477	4801440
    478	14404320
    479	4801440
    480	19205760
    481	14404320
    482	4801440
    483	9602880
    484	4801440
    485	9602880
    486	24007200
    488	28808640
    490	19205760
    492	4801440
    493	9602880
    494	4801440
    495	9602880
    496	14404320
    498	9602880
    499	28808640
    500	24007200
    501	4801440
    502	9602880
    503	24007200
    505	9602880
    506	9602880
    507	19205760
    508	4801440
    509	14404320
    510	9602880
    511	14404320
    512	4801440
    513	9602880
    514	4801440
    515	28808640
    516	19205760
    517	14404320
    518	14404320
    519	14404320
    520	9602880
    521	9602880
    523	19205760
    525	14404320
    526	9602880
    527	28808640
    529	9602880
    530	4801440
    531	9602880
    533	14404320
    534	4801440
    535	14404320
    536	14404320
    537	4801440
    539	19205760
    540	4801440
    542	9602880
    545	9602880
    549	4801440
    550	9602880
    555	4801440
    558	4801440
    562	4801440
    565	4801440
    570	9602880
    571	4801440
    577	4801440
    578	4801440
    593	4801440
    595	4801440
    597	4801440
    604	4801440
    605	9602880
    615	4801440
    616	4801440
    625	4801440
    637	4801440
    640	4801440
    641	4801440
    645	4801440
    655	4801440
    661	14404320
    670	4801440
    675	4801440
    678	4801440
    693	4801440
    707	4801440
    708	4801440
    711	4801440
    722	4801440
    729	4801440
    730	4801440
    742	4801440
    751	4801440
    753	4801440
    766	4801440
    767	4801440
    769	4801440
    777	4801440
    784	4801440
    785	9602880
    787	4801440
    797	4801440
    822	4801440
    843	4801440
    870	4801440
    890	4801440
    901	4801440
    910	4801440
    926	4801440
    956	4801440
    966	4801440
    1000	4801440
    1030	4801440
    1034	4801440
    1039	4801440
    1059	4801440
    1070	4801440
    1072	4801440
    1088	4801440
    1095	4801440
    1149	4801440
    1173	4801440
    1176	4801440
    1209	4801440
    1211	4801440
    1268	4801440
    1273	4801440
    1293	4801440
    1321	4801440
    1352	4801440
    1354	4801440
    1356	4801440
    1421	4801440
    1434	4801440
    1500	4801440
    1504	4801440
    1525	4801440
    1562	4801440
    1573	4801440
    1707	4801440
"""

friendster_t192_latency_mem_str = """
    Latency	Loads
    6	31002898080
    7	397213528320
    8	31170948480
    9	17866158240
    11	52815840
    12	3116134560
    13	777833280
    14	1690106880
    15	3697108800
    16	3351405120
    17	869060640
    18	547364160
    19	398519520
    20	499349760
    21	297689280
    22	398519520
    23	624187200
    24	441732480
    25	441732480
    26	240072000
    27	182454720
    28	187256160
    29	134440320
    30	76823040
    31	91227360
    32	110433120
    33	115234560
    34	48014400
    35	33610080
    36	86425920
    37	48014400
    38	67220160
    39	72021600
    40	76823040
    41	62418720
    42	91227360
    43	57617280
    44	33610080
    45	33610080
    46	24007200
    47	48014400
    48	28808640
    49	38411520
    50	48014400
    51	43212960
    52	14404320
    53	43212960
    54	43212960
    55	28808640
    56	28808640
    57	33610080
    58	38411520
    59	52815840
    60	14404320
    61	48014400
    62	62418720
    63	43212960
    64	62418720
    65	57617280
    66	62418720
    67	52815840
    68	52815840
    69	43212960
    70	43212960
    71	57617280
    72	43212960
    73	19205760
    74	48014400
    75	24007200
    76	28808640
    77	38411520
    78	38411520
    79	48014400
    80	43212960
    81	9602880
    82	14404320
    83	43212960
    85	28808640
    86	14404320
    87	28808640
    88	43212960
    89	43212960
    90	19205760
    91	28808640
    92	28808640
    93	28808640
    94	24007200
    95	19205760
    96	43212960
    97	33610080
    98	9602880
    99	38411520
    100	38411520
    101	19205760
    102	62418720
    103	48014400
    104	28808640
    105	43212960
    106	9602880
    107	19205760
    108	19205760
    109	24007200
    110	38411520
    111	9602880
    112	24007200
    113	19205760
    114	28808640
    115	14404320
    116	19205760
    117	19205760
    118	14404320
    119	9602880
    120	28808640
    121	14404320
    122	14404320
    123	19205760
    124	24007200
    125	19205760
    126	4801440
    127	19205760
    128	4801440
    129	14404320
    130	9602880
    133	14404320
    134	4801440
    135	9602880
    136	4801440
    137	9602880
    138	14404320
    141	9602880
    143	4801440
    144	4801440
    146	14404320
    147	9602880
    149	9602880
    150	4801440
    151	4801440
    152	19205760
    154	4801440
    155	4801440
    156	9602880
    158	9602880
    159	4801440
    160	9602880
    161	4801440
    163	9602880
    164	4801440
    165	9602880
    166	9602880
    167	14404320
    171	14404320
    172	14404320
    173	9602880
    174	9602880
    176	19205760
    177	9602880
    178	4801440
    179	4801440
    180	4801440
    181	4801440
    184	9602880
    185	4801440
    187	9602880
    189	4801440
    190	9602880
    191	4801440
    192	19205760
    193	9602880
    194	4801440
    196	14404320
    197	14404320
    199	4801440
    200	4801440
    201	9602880
    202	9602880
    205	4801440
    207	4801440
    208	4801440
    211	19205760
    214	4801440
    217	19205760
    218	4801440
    219	4801440
    220	4801440
    221	4801440
    222	4801440
    225	4801440
    226	19205760
    227	4801440
    228	9602880
    230	4801440
    231	19205760
    232	14404320
    233	4801440
    234	4801440
    235	19205760
    236	14404320
    238	9602880
    239	9602880
    240	4801440
    241	4801440
    242	9602880
    243	4801440
    244	24007200
    245	24007200
    246	14404320
    247	28808640
    248	24007200
    249	19205760
    250	28808640
    251	52815840
    252	28808640
    253	24007200
    254	43212960
    255	14404320
    256	28808640
    257	38411520
    258	62418720
    259	28808640
    260	24007200
    261	43212960
    262	24007200
    263	33610080
    264	28808640
    265	43212960
    266	33610080
    267	14404320
    268	48014400
    269	62418720
    270	48014400
    271	38411520
    272	43212960
    273	24007200
    274	24007200
    275	19205760
    276	33610080
    277	43212960
    278	33610080
    279	38411520
    280	14404320
    281	33610080
    282	43212960
    283	28808640
    284	33610080
    285	38411520
    286	33610080
    287	24007200
    288	19205760
    289	24007200
    290	28808640
    291	33610080
    292	24007200
    293	14404320
    294	38411520
    295	43212960
    296	19205760
    297	28808640
    298	9602880
    299	28808640
    300	9602880
    301	24007200
    302	48014400
    303	14404320
    304	19205760
    305	52815840
    306	24007200
    307	24007200
    308	24007200
    309	38411520
    310	19205760
    311	14404320
    312	24007200
    313	4801440
    314	33610080
    315	9602880
    316	4801440
    317	24007200
    318	19205760
    319	9602880
    320	9602880
    321	14404320
    322	24007200
    324	14404320
    325	4801440
    326	4801440
    327	9602880
    328	14404320
    330	4801440
    331	4801440
    332	4801440
    334	14404320
    335	4801440
    337	4801440
    338	4801440
    339	9602880
    341	9602880
    343	4801440
    345	9602880
    346	4801440
    347	4801440
    348	4801440
    349	4801440
    351	19205760
    355	9602880
    356	4801440
    357	4801440
    358	14404320
    360	4801440
    361	4801440
    362	9602880
    363	4801440
    364	9602880
    365	4801440
    367	4801440
    369	9602880
    371	14404320
    372	9602880
    376	9602880
    377	9602880
    378	4801440
    379	9602880
    380	4801440
    381	19205760
    382	4801440
    383	9602880
    387	4801440
    390	4801440
    392	9602880
    394	9602880
    397	9602880
    398	4801440
    399	9602880
    400	9602880
    402	4801440
    405	4801440
    406	19205760
    407	4801440
    408	4801440
    411	14404320
    414	4801440
    415	4801440
    418	4801440
    419	4801440
    420	19205760
    421	9602880
    422	4801440
    423	19205760
    425	4801440
    428	9602880
    429	28808640
    430	14404320
    431	9602880
    433	14404320
    434	9602880
    436	14404320
    437	4801440
    438	4801440
    439	4801440
    440	14404320
    441	19205760
    442	14404320
    443	14404320
    445	24007200
    446	33610080
    447	9602880
    448	19205760
    449	19205760
    450	19205760
    451	19205760
    452	14404320
    453	9602880
    454	14404320
    455	19205760
    456	19205760
    457	19205760
    458	9602880
    459	24007200
    460	33610080
    461	14404320
    462	28808640
    463	19205760
    464	14404320
    465	43212960
    466	28808640
    467	24007200
    468	19205760
    469	24007200
    470	19205760
    471	28808640
    472	14404320
    473	14404320
    474	14404320
    475	9602880
    476	14404320
    477	9602880
    478	19205760
    479	24007200
    480	38411520
    481	14404320
    482	14404320
    483	28808640
    484	19205760
    485	9602880
    486	9602880
    487	14404320
    488	19205760
    489	14404320
    490	24007200
    491	9602880
    492	14404320
    493	9602880
    494	14404320
    495	14404320
    496	4801440
    497	14404320
    498	4801440
    499	9602880
    500	9602880
    501	14404320
    502	14404320
    503	9602880
    504	4801440
    505	19205760
    506	14404320
    507	19205760
    508	9602880
    510	4801440
    511	4801440
    513	19205760
    514	14404320
    515	14404320
    516	24007200
    517	4801440
    518	4801440
    520	9602880
    521	14404320
    522	9602880
    523	14404320
    524	14404320
    525	4801440
    527	4801440
    529	9602880
    530	14404320
    531	14404320
    533	4801440
    534	19205760
    535	9602880
    536	9602880
    537	14404320
    538	19205760
    539	14404320
    540	24007200
    541	9602880
    542	14404320
    543	14404320
    544	4801440
    545	9602880
    546	9602880
    547	9602880
    548	4801440
    549	19205760
    550	19205760
    551	4801440
    552	14404320
    553	4801440
    554	14404320
    555	4801440
    556	9602880
    558	14404320
    559	4801440
    560	4801440
    563	9602880
    565	24007200
    566	14404320
    567	14404320
    570	9602880
    571	4801440
    572	9602880
    574	9602880
    576	9602880
    579	4801440
    581	4801440
    585	4801440
    588	9602880
    589	9602880
    592	14404320
    593	9602880
    594	4801440
    597	4801440
    607	4801440
    612	4801440
    626	4801440
    629	4801440
    630	9602880
    633	4801440
    635	4801440
    652	4801440
    668	4801440
    671	4801440
    678	4801440
    693	4801440
    698	4801440
    699	4801440
    709	4801440
    715	4801440
    727	4801440
    728	4801440
    737	9602880
    748	9602880
    759	4801440
    777	4801440
    788	4801440
    806	4801440
    814	4801440
    817	4801440
    823	4801440
    824	4801440
    830	4801440
    834	4801440
    837	4801440
    863	4801440
    869	4801440
    873	4801440
    892	4801440
    914	4801440
    920	4801440
    950	4801440
    953	4801440
    981	4801440
    985	4801440
    996	4801440
    1000	4801440
    1017	4801440
    1032	4801440
    1102	9602880
    1155	4801440
    1191	9602880
    1215	4801440
    1223	4801440
    1225	4801440
    1226	4801440
    1241	4801440
    1250	4801440
    1255	4801440
    1269	4801440
    1288	4801440
    1311	4801440
    1391	4801440
    1438	4801440
    1470	4801440
    1492	4801440
    1528	4801440
    1592	4801440
    1855	4801440
"""


#----------------------------------------------------------------------------
# moliere2016, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

moliere2016_t192_latency_dram_str = """
    Latency	Loads
    6	6184254720
    7	92576564640
    8	7101329760
    9	4234870080
    11	14404320
    12	840252000
    13	235270560
    14	451335360
    15	859457760
    16	1694908320
    17	360108000
    18	268880640
    19	163248960
    20	100830240
    21	110433120
    22	211263360
    23	192057600
    24	216064800
    25	244873440
    26	52815840
    27	67220160
    28	76823040
    29	43212960
    30	100830240
    31	24007200
    32	24007200
    33	43212960
    34	52815840
    35	9602880
    36	4801440
    37	28808640
    38	9602880
    39	24007200
    40	19205760
    41	19205760
    42	9602880
    43	19205760
    44	19205760
    45	9602880
    46	19205760
    47	4801440
    48	9602880
    49	4801440
    50	24007200
    51	28808640
    52	14404320
    53	9602880
    54	19205760
    55	24007200
    56	4801440
    57	9602880
    58	9602880
    59	19205760
    60	9602880
    61	24007200
    62	19205760
    64	28808640
    65	14404320
    66	9602880
    67	14404320
    68	33610080
    69	9602880
    70	19205760
    71	19205760
    72	19205760
    73	24007200
    74	24007200
    75	14404320
    76	24007200
    77	19205760
    78	4801440
    79	19205760
    80	24007200
    81	14404320
    82	14404320
    83	14404320
    84	9602880
    85	14404320
    86	19205760
    87	9602880
    88	19205760
    89	4801440
    90	14404320
    92	9602880
    94	9602880
    95	4801440
    96	4801440
    97	4801440
    98	24007200
    99	4801440
    100	9602880
    101	14404320
    102	14404320
    103	28808640
    105	4801440
    107	19205760
    108	4801440
    109	9602880
    110	4801440
    112	4801440
    113	4801440
    114	14404320
    116	4801440
    117	9602880
    118	4801440
    119	4801440
    120	4801440
    121	14404320
    123	4801440
    124	9602880
    125	4801440
    126	4801440
    128	9602880
    130	4801440
    133	14404320
    134	4801440
    137	4801440
    143	4801440
    145	4801440
    146	4801440
    148	4801440
    151	4801440
    152	9602880
    153	4801440
    154	9602880
    156	4801440
    165	4801440
    166	9602880
    169	4801440
    170	4801440
    172	4801440
    173	4801440
    175	4801440
    181	4801440
    183	14404320
    184	4801440
    187	4801440
    196	4801440
    197	4801440
    200	4801440
    203	9602880
    205	4801440
    206	4801440
    209	4801440
    212	9602880
    213	4801440
    214	9602880
    218	4801440
    219	4801440
    221	4801440
    222	4801440
    225	4801440
    226	4801440
    229	9602880
    231	4801440
    234	9602880
    235	9602880
    236	9602880
    238	14404320
    239	9602880
    241	9602880
    242	9602880
    244	4801440
    246	4801440
    248	4801440
    249	9602880
    250	4801440
    251	19205760
    252	4801440
    253	4801440
    254	9602880
    256	9602880
    257	4801440
    258	4801440
    259	9602880
    261	24007200
    262	4801440
    263	9602880
    264	4801440
    265	14404320
    266	9602880
    267	9602880
    269	14404320
    270	9602880
    271	9602880
    272	4801440
    273	14404320
    274	4801440
    276	4801440
    278	4801440
    279	4801440
    280	4801440
    281	4801440
    282	9602880
    283	9602880
    284	4801440
    286	9602880
    287	4801440
    289	9602880
    290	4801440
    291	9602880
    292	9602880
    295	4801440
    296	4801440
    298	14404320
    300	4801440
    301	4801440
    302	4801440
    303	9602880
    304	4801440
    305	4801440
    308	9602880
    309	4801440
    311	4801440
    312	9602880
    315	4801440
    320	4801440
    321	4801440
    322	4801440
    325	4801440
    327	9602880
    328	4801440
    330	4801440
    331	14404320
    334	4801440
    338	9602880
    340	4801440
    341	9602880
    342	4801440
    343	4801440
    345	4801440
    346	4801440
    347	4801440
    348	4801440
    349	4801440
    353	4801440
    355	9602880
    356	4801440
    359	4801440
    360	4801440
    368	4801440
    376	4801440
    377	4801440
    378	4801440
    380	4801440
    382	4801440
    386	4801440
    387	4801440
    388	4801440
    389	4801440
    391	4801440
    395	4801440
    396	4801440
    397	9602880
    404	4801440
    408	4801440
    411	4801440
    413	4801440
    414	4801440
    415	4801440
    416	4801440
    417	9602880
    418	9602880
    427	4801440
    429	14404320
    433	9602880
    434	4801440
    435	9602880
    436	4801440
    437	4801440
    439	4801440
    441	4801440
    444	4801440
    445	4801440
    446	4801440
    447	4801440
    448	4801440
    449	14404320
    450	4801440
    451	9602880
    452	4801440
    453	9602880
    455	4801440
    456	4801440
    457	4801440
    459	4801440
    460	4801440
    461	14404320
    462	4801440
    463	4801440
    464	9602880
    465	4801440
    467	4801440
    468	4801440
    470	4801440
    471	4801440
    473	4801440
    474	4801440
    476	4801440
    478	9602880
    479	4801440
    480	4801440
    481	4801440
    482	19205760
    484	14404320
    485	9602880
    486	4801440
    489	4801440
    494	4801440
    495	4801440
    496	9602880
    501	9602880
    504	9602880
    507	4801440
    508	4801440
    511	9602880
    513	14404320
    514	4801440
    515	14404320
    516	9602880
    517	4801440
    518	9602880
    519	4801440
    524	4801440
    527	4801440
    528	9602880
    529	4801440
    534	4801440
    537	4801440
    539	4801440
    542	9602880
    544	14404320
    545	4801440
    548	4801440
    551	4801440
    552	9602880
    553	9602880
    559	9602880
    563	4801440
    566	9602880
    568	4801440
    570	4801440
    571	4801440
    573	4801440
    576	4801440
    583	9602880
    584	4801440
    587	4801440
    588	9602880
    602	4801440
    606	4801440
    612	4801440
    616	4801440
    617	4801440
    618	4801440
    620	4801440
    626	4801440
    628	4801440
    633	4801440
    634	4801440
    637	4801440
    641	4801440
    648	4801440
    654	4801440
    662	4801440
    670	4801440
    671	4801440
    673	4801440
    679	4801440
    680	9602880
    684	4801440
    687	4801440
    691	4801440
    693	4801440
    700	9602880
    705	4801440
    709	4801440
    711	4801440
    712	4801440
    718	4801440
    719	4801440
    726	4801440
    733	4801440
    734	4801440
    738	4801440
    749	4801440
    753	4801440
    757	4801440
    765	4801440
    767	4801440
    770	4801440
    778	4801440
    785	4801440
    788	4801440
    790	4801440
    808	4801440
    837	4801440
    853	4801440
    858	4801440
    890	4801440
    895	4801440
    910	4801440
    930	4801440
    939	4801440
    951	4801440
    958	4801440
    962	4801440
    980	4801440
    991	4801440
    1009	4801440
    1031	4801440
    1057	4801440
    1071	4801440
    1072	4801440
    1074	4801440
    1085	4801440
    1100	4801440
    1114	4801440
    1133	4801440
    1146	4801440
    1208	4801440
    1216	4801440
    1264	4801440
    1284	4801440
    1285	4801440
    1345	4801440
    1376	4801440
    1424	4801440
    1454	4801440
    1483	4801440
    1550	4801440
    1675	4801440
    1680	4801440
    1723	4801440
    1758	4801440
    1841	4801440
    1875	4801440
    1903	4801440
    1926	4801440
"""


moliere2016_t192_latency_pdax_str = """
    Latency	Loads
    6	6832449120
    7	96374503680
    8	6443532480
    9	4167649920
    11	14404320
    12	710613120
    13	254476320
    14	350505120
    15	720216000
    16	1526857920
    17	278483520
    18	211263360
    19	182454720
    20	153646080
    21	96028800
    22	182454720
    23	220866240
    24	144043200
    25	182454720
    26	62418720
    27	86425920
    28	43212960
    29	28808640
    30	100830240
    31	38411520
    32	33610080
    33	38411520
    34	28808640
    35	9602880
    36	9602880
    37	4801440
    38	4801440
    39	24007200
    40	9602880
    41	9602880
    42	19205760
    43	4801440
    44	4801440
    45	4801440
    47	19205760
    48	9602880
    49	9602880
    50	19205760
    51	14404320
    52	28808640
    53	9602880
    55	24007200
    56	14404320
    57	19205760
    58	19205760
    59	9602880
    60	24007200
    61	48014400
    62	28808640
    63	38411520
    64	19205760
    65	28808640
    66	19205760
    67	14404320
    68	33610080
    70	28808640
    71	33610080
    72	24007200
    73	24007200
    74	14404320
    75	19205760
    76	9602880
    77	28808640
    78	9602880
    79	19205760
    80	19205760
    81	14404320
    82	19205760
    83	4801440
    84	9602880
    85	4801440
    86	19205760
    87	4801440
    88	19205760
    89	9602880
    90	14404320
    91	14404320
    92	14404320
    93	19205760
    94	9602880
    95	9602880
    96	9602880
    97	14404320
    98	14404320
    99	9602880
    100	14404320
    102	14404320
    103	4801440
    104	9602880
    106	9602880
    107	9602880
    109	9602880
    110	24007200
    111	4801440
    112	4801440
    113	4801440
    114	14404320
    115	4801440
    116	9602880
    119	9602880
    120	4801440
    121	9602880
    122	19205760
    124	4801440
    125	9602880
    126	4801440
    129	4801440
    131	9602880
    133	4801440
    136	4801440
    141	4801440
    143	4801440
    145	4801440
    146	9602880
    148	9602880
    149	4801440
    152	14404320
    153	9602880
    154	4801440
    155	4801440
    156	9602880
    157	14404320
    158	4801440
    159	4801440
    160	4801440
    165	4801440
    166	4801440
    167	14404320
    168	9602880
    169	4801440
    172	9602880
    174	4801440
    175	9602880
    176	4801440
    181	4801440
    187	4801440
    190	9602880
    191	4801440
    192	4801440
    193	4801440
    194	4801440
    195	4801440
    196	4801440
    205	4801440
    211	9602880
    215	4801440
    216	4801440
    219	4801440
    225	4801440
    226	9602880
    227	14404320
    229	4801440
    230	9602880
    231	24007200
    232	9602880
    233	4801440
    235	9602880
    236	14404320
    237	9602880
    238	14404320
    239	19205760
    240	14404320
    241	9602880
    242	9602880
    243	24007200
    244	4801440
    245	4801440
    246	14404320
    247	9602880
    248	14404320
    249	19205760
    250	9602880
    251	19205760
    252	4801440
    253	14404320
    254	14404320
    255	19205760
    256	9602880
    257	14404320
    258	14404320
    260	9602880
    261	14404320
    262	14404320
    263	9602880
    264	19205760
    265	9602880
    266	4801440
    267	9602880
    268	9602880
    270	4801440
    271	9602880
    272	14404320
    273	4801440
    274	24007200
    276	14404320
    279	19205760
    282	14404320
    283	9602880
    284	14404320
    285	4801440
    286	14404320
    289	9602880
    291	4801440
    293	14404320
    294	4801440
    297	4801440
    298	9602880
    299	4801440
    301	4801440
    302	4801440
    303	4801440
    305	4801440
    309	4801440
    310	9602880
    313	9602880
    314	4801440
    315	4801440
    316	4801440
    317	9602880
    318	14404320
    319	4801440
    323	9602880
    324	4801440
    326	9602880
    327	4801440
    331	4801440
    332	9602880
    334	14404320
    339	4801440
    344	4801440
    349	4801440
    351	14404320
    352	4801440
    353	9602880
    355	4801440
    356	4801440
    357	9602880
    358	4801440
    359	4801440
    360	4801440
    361	4801440
    364	4801440
    365	4801440
    366	4801440
    367	4801440
    373	19205760
    374	4801440
    377	4801440
    386	4801440
    390	4801440
    395	4801440
    396	4801440
    398	9602880
    399	9602880
    402	4801440
    403	9602880
    404	4801440
    406	4801440
    407	9602880
    408	9602880
    409	19205760
    412	4801440
    413	4801440
    414	4801440
    416	4801440
    417	9602880
    418	4801440
    421	4801440
    423	4801440
    425	4801440
    431	9602880
    432	4801440
    433	4801440
    434	4801440
    435	4801440
    437	9602880
    438	9602880
    439	9602880
    440	4801440
    441	9602880
    442	9602880
    443	4801440
    444	4801440
    445	4801440
    446	19205760
    448	4801440
    449	9602880
    450	4801440
    451	19205760
    452	4801440
    453	9602880
    454	9602880
    455	9602880
    456	4801440
    457	4801440
    459	14404320
    460	14404320
    461	9602880
    462	4801440
    463	9602880
    465	19205760
    466	14404320
    467	4801440
    469	14404320
    470	4801440
    473	9602880
    474	4801440
    475	4801440
    476	4801440
    478	4801440
    479	14404320
    480	14404320
    482	9602880
    487	4801440
    489	4801440
    495	4801440
    498	9602880
    500	4801440
    505	4801440
    508	4801440
    514	4801440
    516	9602880
    520	4801440
    521	4801440
    522	4801440
    529	4801440
    537	4801440
    540	4801440
    544	4801440
    547	4801440
    551	4801440
    553	4801440
    556	4801440
    558	4801440
    559	4801440
    560	4801440
    565	4801440
    567	4801440
    569	9602880
    571	4801440
    597	4801440
    598	9602880
    609	9602880
    616	4801440
    622	4801440
    625	4801440
    626	4801440
    632	9602880
    640	4801440
    641	4801440
    642	4801440
    649	4801440
    658	4801440
    660	4801440
    663	4801440
    666	4801440
    671	4801440
    687	4801440
    693	4801440
    700	4801440
    704	4801440
    708	4801440
    720	9602880
    721	4801440
    724	4801440
    746	9602880
    747	4801440
    753	4801440
    761	4801440
    784	4801440
    785	4801440
    798	4801440
    814	4801440
    821	4801440
    827	4801440
    830	4801440
    837	4801440
    849	4801440
    855	4801440
    868	4801440
    869	4801440
    870	4801440
    907	4801440
    940	4801440
    949	4801440
    966	4801440
    967	4801440
    982	4801440
    983	4801440
    990	9602880
    1029	4801440
    1058	4801440
    1075	4801440
    1078	4801440
    1086	4801440
    1143	4801440
    1153	4801440
    1175	4801440
    1183	4801440
    1185	4801440
    1250	4801440
    1260	4801440
    1306	4801440
    1307	4801440
    1329	4801440
    1336	4801440
    1357	4801440
    1410	4801440
    1517	4801440
    1549	4801440
    1579	4801440
    1581	4801440
    1658	4801440
    1878	4801440
    1950	4801440
"""

moliere2016_t192_latency_kdax_str = """
    Latency	Loads
    6	6770030400
    7	93940173600
    8	6688405920
    9	4767829920
    11	4801440
    12	758627520
    13	168050400
    14	254476320
    15	792237600
    16	1526857920
    17	220866240
    18	235270560
    19	144043200
    20	120036000
    21	76823040
    22	182454720
    23	168050400
    24	192057600
    25	297689280
    26	67220160
    27	105631680
    28	72021600
    29	57617280
    30	134440320
    31	28808640
    32	33610080
    33	14404320
    34	19205760
    35	19205760
    36	28808640
    37	14404320
    38	9602880
    39	14404320
    40	28808640
    41	19205760
    42	14404320
    43	9602880
    44	14404320
    45	38411520
    46	9602880
    47	9602880
    48	14404320
    49	19205760
    50	9602880
    51	19205760
    52	14404320
    53	4801440
    54	9602880
    55	9602880
    56	9602880
    57	28808640
    58	28808640
    59	9602880
    60	19205760
    61	43212960
    62	43212960
    63	33610080
    64	19205760
    65	28808640
    66	9602880
    67	19205760
    68	24007200
    69	33610080
    70	19205760
    71	28808640
    72	38411520
    73	14404320
    74	19205760
    75	9602880
    76	28808640
    77	9602880
    78	14404320
    79	4801440
    80	9602880
    81	14404320
    82	28808640
    83	4801440
    84	9602880
    85	14404320
    86	19205760
    87	24007200
    88	14404320
    89	14404320
    90	4801440
    91	19205760
    92	4801440
    93	9602880
    94	14404320
    95	4801440
    96	14404320
    97	9602880
    98	14404320
    99	14404320
    100	4801440
    101	9602880
    102	9602880
    104	4801440
    105	4801440
    106	9602880
    107	14404320
    108	4801440
    109	24007200
    110	4801440
    112	4801440
    113	4801440
    115	14404320
    116	4801440
    118	4801440
    119	4801440
    120	4801440
    121	4801440
    122	4801440
    128	4801440
    130	9602880
    133	4801440
    140	14404320
    141	4801440
    143	4801440
    144	4801440
    147	4801440
    148	4801440
    155	14404320
    159	4801440
    164	4801440
    166	4801440
    167	4801440
    168	4801440
    169	4801440
    171	4801440
    172	4801440
    173	4801440
    174	14404320
    177	4801440
    178	4801440
    180	9602880
    181	4801440
    183	9602880
    187	9602880
    191	4801440
    193	4801440
    194	4801440
    195	4801440
    197	4801440
    198	14404320
    204	4801440
    209	4801440
    211	4801440
    212	4801440
    217	4801440
    219	4801440
    220	14404320
    221	4801440
    222	4801440
    225	4801440
    227	4801440
    230	9602880
    232	4801440
    235	4801440
    236	9602880
    237	4801440
    238	9602880
    240	4801440
    241	9602880
    242	9602880
    243	4801440
    244	24007200
    245	24007200
    246	9602880
    247	4801440
    248	9602880
    249	9602880
    252	4801440
    253	24007200
    254	4801440
    256	28808640
    257	9602880
    258	4801440
    259	4801440
    260	9602880
    261	9602880
    262	14404320
    263	4801440
    264	9602880
    265	4801440
    267	9602880
    268	9602880
    269	9602880
    271	4801440
    272	14404320
    274	9602880
    276	14404320
    277	4801440
    278	9602880
    279	4801440
    281	4801440
    282	4801440
    283	9602880
    284	14404320
    286	4801440
    287	4801440
    288	4801440
    290	14404320
    291	4801440
    292	4801440
    293	4801440
    294	4801440
    295	9602880
    296	9602880
    298	4801440
    303	9602880
    309	4801440
    311	4801440
    312	9602880
    313	4801440
    315	4801440
    317	9602880
    318	9602880
    319	4801440
    320	4801440
    321	4801440
    323	9602880
    324	9602880
    325	4801440
    332	4801440
    334	4801440
    337	9602880
    341	9602880
    342	4801440
    344	4801440
    345	4801440
    346	4801440
    349	4801440
    351	4801440
    357	4801440
    358	4801440
    361	4801440
    362	9602880
    368	4801440
    370	4801440
    371	4801440
    373	4801440
    378	4801440
    380	4801440
    389	4801440
    390	4801440
    392	9602880
    393	4801440
    396	4801440
    397	4801440
    401	4801440
    405	4801440
    406	4801440
    407	14404320
    410	4801440
    411	4801440
    412	4801440
    413	9602880
    414	4801440
    415	9602880
    417	9602880
    418	4801440
    419	4801440
    420	4801440
    421	9602880
    422	4801440
    423	24007200
    424	4801440
    425	9602880
    427	4801440
    428	4801440
    429	4801440
    430	4801440
    431	14404320
    433	4801440
    435	9602880
    436	24007200
    437	14404320
    438	4801440
    440	4801440
    441	4801440
    442	4801440
    443	4801440
    444	4801440
    445	4801440
    447	14404320
    448	19205760
    449	4801440
    450	14404320
    451	9602880
    452	9602880
    453	4801440
    454	4801440
    455	9602880
    456	9602880
    458	4801440
    459	9602880
    460	9602880
    462	14404320
    463	19205760
    464	9602880
    465	4801440
    466	9602880
    467	19205760
    468	14404320
    469	9602880
    470	14404320
    472	9602880
    474	4801440
    477	4801440
    478	4801440
    481	4801440
    484	9602880
    488	4801440
    489	4801440
    490	4801440
    491	4801440
    492	9602880
    496	4801440
    497	9602880
    498	4801440
    499	4801440
    501	9602880
    503	9602880
    506	4801440
    508	4801440
    509	9602880
    511	4801440
    512	4801440
    516	4801440
    517	4801440
    518	4801440
    519	9602880
    520	4801440
    524	4801440
    525	4801440
    531	4801440
    533	9602880
    534	4801440
    540	9602880
    544	4801440
    545	14404320
    546	4801440
    550	4801440
    551	4801440
    554	4801440
    558	4801440
    561	9602880
    564	4801440
    567	4801440
    570	9602880
    571	4801440
    577	4801440
    581	4801440
    589	4801440
    594	4801440
    614	4801440
    624	4801440
    634	4801440
    641	4801440
    649	4801440
    676	4801440
    680	4801440
    728	4801440
    732	4801440
    750	4801440
    765	4801440
    801	4801440
    808	4801440
    865	4801440
    880	4801440
    916	4801440
    932	4801440
    936	4801440
    946	4801440
    985	4801440
    986	4801440
    999	4801440
    1022	4801440
    1030	4801440
    1051	4801440
    1082	4801440
    1094	4801440
    1105	4801440
    1241	4801440
    1262	4801440
    1394	4801440
    1524	4801440
    1682	4801440
    1709	4801440
    2084	4801440
    2510	4801440
"""

moliere2016_t192_latency_mem_str = """
    Latency	Loads
    6	6726817440
    7	94650786720
    8	6573171360
    9	4239671520
    11	9602880
    12	854656320
    13	206461920
    14	336100800
    15	792237600
    16	1176352800
    17	259277760
    18	220866240
    19	153646080
    20	120036000
    21	67220160
    22	216064800
    23	139241760
    24	172851840
    25	244873440
    26	67220160
    27	76823040
    28	48014400
    29	52815840
    30	129638880
    31	33610080
    32	24007200
    33	28808640
    34	9602880
    35	28808640
    36	24007200
    37	9602880
    38	9602880
    39	9602880
    40	33610080
    41	14404320
    42	14404320
    43	19205760
    44	4801440
    45	4801440
    46	14404320
    48	24007200
    49	14404320
    50	4801440
    51	19205760
    52	24007200
    53	14404320
    55	33610080
    56	14404320
    57	4801440
    58	14404320
    59	4801440
    60	28808640
    61	43212960
    62	33610080
    63	14404320
    64	14404320
    65	28808640
    66	9602880
    67	9602880
    68	14404320
    69	24007200
    70	28808640
    71	14404320
    72	38411520
    73	19205760
    74	14404320
    75	9602880
    76	9602880
    77	38411520
    78	24007200
    79	9602880
    80	4801440
    81	4801440
    82	19205760
    83	4801440
    84	9602880
    85	14404320
    86	9602880
    87	14404320
    88	4801440
    89	4801440
    90	24007200
    91	24007200
    92	9602880
    93	28808640
    94	4801440
    95	19205760
    96	4801440
    97	4801440
    98	33610080
    99	9602880
    100	9602880
    101	19205760
    102	9602880
    103	19205760
    104	4801440
    105	4801440
    106	4801440
    107	4801440
    108	4801440
    109	9602880
    110	4801440
    111	4801440
    112	9602880
    113	9602880
    116	9602880
    117	9602880
    118	9602880
    119	4801440
    120	4801440
    122	4801440
    123	9602880
    124	4801440
    125	4801440
    126	4801440
    127	4801440
    128	9602880
    130	4801440
    131	9602880
    132	4801440
    133	4801440
    135	4801440
    136	4801440
    138	4801440
    141	4801440
    142	4801440
    144	9602880
    148	4801440
    149	4801440
    150	9602880
    151	4801440
    152	4801440
    154	9602880
    155	4801440
    158	4801440
    160	14404320
    161	4801440
    164	4801440
    165	4801440
    167	9602880
    168	4801440
    169	9602880
    170	4801440
    171	14404320
    173	4801440
    175	4801440
    177	4801440
    182	4801440
    186	9602880
    192	9602880
    193	9602880
    194	4801440
    197	9602880
    199	4801440
    201	4801440
    206	9602880
    207	9602880
    208	9602880
    209	4801440
    214	4801440
    217	9602880
    223	4801440
    225	4801440
    226	4801440
    229	4801440
    233	4801440
    234	4801440
    235	9602880
    236	4801440
    241	9602880
    242	4801440
    244	4801440
    246	4801440
    247	19205760
    249	4801440
    250	9602880
    251	9602880
    252	9602880
    254	14404320
    255	4801440
    256	4801440
    258	14404320
    260	14404320
    261	4801440
    262	19205760
    263	19205760
    264	4801440
    265	9602880
    266	14404320
    267	14404320
    268	19205760
    270	19205760
    271	14404320
    272	24007200
    273	24007200
    274	28808640
    275	14404320
    276	24007200
    277	9602880
    278	14404320
    279	14404320
    280	4801440
    281	14404320
    282	4801440
    283	9602880
    284	4801440
    285	9602880
    286	4801440
    287	9602880
    288	4801440
    289	9602880
    290	9602880
    291	14404320
    293	4801440
    294	9602880
    295	4801440
    296	9602880
    297	4801440
    301	4801440
    302	4801440
    303	14404320
    304	4801440
    306	4801440
    308	4801440
    310	9602880
    311	14404320
    314	4801440
    317	4801440
    325	4801440
    326	4801440
    327	9602880
    334	4801440
    335	4801440
    336	4801440
    337	4801440
    339	4801440
    340	4801440
    341	4801440
    343	4801440
    345	9602880
    349	9602880
    353	4801440
    358	4801440
    361	4801440
    363	9602880
    368	4801440
    371	9602880
    372	4801440
    373	4801440
    376	4801440
    378	9602880
    380	4801440
    381	4801440
    382	4801440
    383	4801440
    390	4801440
    391	4801440
    392	4801440
    396	9602880
    399	4801440
    405	9602880
    406	4801440
    408	4801440
    409	4801440
    413	4801440
    414	4801440
    416	9602880
    417	4801440
    425	4801440
    426	9602880
    431	4801440
    432	4801440
    433	4801440
    434	4801440
    437	9602880
    438	4801440
    439	4801440
    441	9602880
    443	24007200
    444	9602880
    445	19205760
    447	4801440
    449	4801440
    450	4801440
    454	9602880
    455	9602880
    457	4801440
    460	14404320
    461	9602880
    462	9602880
    463	4801440
    464	9602880
    465	4801440
    466	4801440
    467	9602880
    469	19205760
    470	4801440
    471	14404320
    472	19205760
    473	4801440
    474	14404320
    475	4801440
    478	14404320
    479	4801440
    480	9602880
    482	14404320
    483	9602880
    486	4801440
    488	4801440
    489	4801440
    491	4801440
    492	14404320
    495	9602880
    496	9602880
    498	4801440
    500	4801440
    504	4801440
    505	4801440
    507	9602880
    508	4801440
    509	4801440
    511	4801440
    513	4801440
    514	4801440
    515	4801440
    516	9602880
    517	4801440
    518	4801440
    519	4801440
    521	9602880
    522	4801440
    523	4801440
    524	9602880
    525	9602880
    526	4801440
    527	4801440
    532	4801440
    535	9602880
    536	4801440
    542	4801440
    547	9602880
    548	4801440
    549	14404320
    557	4801440
    563	4801440
    564	9602880
    573	4801440
    577	4801440
    584	4801440
    585	4801440
    586	4801440
    587	4801440
    588	4801440
    589	4801440
    591	9602880
    595	4801440
    611	4801440
    613	4801440
    638	4801440
    654	4801440
    656	4801440
    659	4801440
    669	4801440
    674	4801440
    709	4801440
    716	4801440
    717	4801440
    718	4801440
    729	4801440
    745	4801440
    757	4801440
    777	4801440
    778	4801440
    809	4801440
    820	4801440
    821	4801440
    835	4801440
    860	4801440
    895	4801440
    896	4801440
    926	4801440
    955	4801440
    990	4801440
    1016	4801440
    1023	4801440
    1028	4801440
    1071	4801440
    1120	4801440
    1134	4801440
    1140	4801440
    1167	4801440
    1182	4801440
    1190	9602880
    1199	4801440
    1200	4801440
    1244	9602880
    1265	4801440
    1315	4801440
    1350	4801440
    1379	4801440
    1400	4801440
    1447	4801440
    1451	4801440
    1526	4801440
    1570	4801440
    1573	4801440
    1626	4801440
    1773	4801440
    1807	4801440
    1832	4801440
    1911	4801440
    2047	4801440
    2341	4801440
    2490	4801440
    2552	4801440
"""


#----------------------------------------------------------------------------
# clueweb12, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

clueweb12_t192_latency_mem_str = """
    Latency	Loads
    6	30018602880
    7	567318944640
    8	45450431040
    9	26091024960
    11	96028800
    12	6030608640
    13	1555666560
    14	3620285760
    15	4599779520
    16	16632188160
    17	2458337280
    18	1680504000
    19	1296388800
    20	845053440
    21	825847680
    22	979493760
    23	2890466880
    24	2131839360
    25	4638191040
    26	556967040
    27	2055016320
    28	835450560
    29	470541120
    30	1997399040
    31	451335360
    32	979493760
    33	249674880
    34	220866240
    35	115234560
    36	240072000
    37	124837440
    38	192057600
    39	192057600
    40	134440320
    41	172851840
    42	144043200
    43	105631680
    44	115234560
    45	364909440
    46	67220160
    47	105631680
    48	153646080
    49	105631680
    50	124837440
    51	268880640
    52	374512320
    53	86425920
    54	144043200
    55	96028800
    56	182454720
    57	115234560
    58	163248960
    59	172851840
    60	105631680
    61	220866240
    62	115234560
    63	105631680
    64	153646080
    65	182454720
    66	134440320
    67	134440320
    68	220866240
    69	67220160
    70	67220160
    71	115234560
    72	105631680
    73	67220160
    74	144043200
    75	182454720
    76	28808640
    77	86425920
    78	96028800
    79	57617280
    80	38411520
    81	76823040
    82	48014400
    83	115234560
    84	86425920
    85	96028800
    86	28808640
    87	38411520
    88	19205760
    89	76823040
    90	48014400
    91	48014400
    92	57617280
    93	67220160
    94	105631680
    95	76823040
    96	57617280
    97	76823040
    98	67220160
    99	38411520
    100	105631680
    101	76823040
    102	48014400
    103	19205760
    104	28808640
    105	48014400
    106	38411520
    107	19205760
    108	38411520
    109	38411520
    110	57617280
    111	9602880
    112	38411520
    113	19205760
    114	9602880
    115	9602880
    116	9602880
    117	19205760
    118	48014400
    120	9602880
    121	57617280
    122	38411520
    124	28808640
    125	9602880
    126	19205760
    127	48014400
    128	9602880
    129	19205760
    130	9602880
    131	28808640
    132	19205760
    133	9602880
    134	9602880
    135	9602880
    136	9602880
    137	9602880
    138	28808640
    139	38411520
    140	9602880
    141	28808640
    142	9602880
    143	9602880
    145	19205760
    147	9602880
    148	28808640
    149	9602880
    150	9602880
    151	9602880
    152	9602880
    153	19205760
    154	9602880
    155	28808640
    157	9602880
    159	28808640
    162	38411520
    163	19205760
    166	9602880
    170	9602880
    171	9602880
    172	9602880
    173	9602880
    174	9602880
    176	9602880
    177	19205760
    178	9602880
    179	19205760
    180	9602880
    182	28808640
    185	9602880
    188	19205760
    189	9602880
    190	9602880
    191	19205760
    192	9602880
    194	9602880
    197	9602880
    198	9602880
    199	19205760
    203	19205760
    206	19205760
    209	9602880
    210	19205760
    214	19205760
    215	9602880
    217	19205760
    218	9602880
    219	19205760
    220	19205760
    222	9602880
    223	9602880
    224	9602880
    225	9602880
    226	9602880
    230	9602880
    236	9602880
    238	19205760
    239	9602880
    240	9602880
    241	9602880
    243	9602880
    247	9602880
    250	9602880
    251	9602880
    253	9602880
    256	9602880
    257	9602880
    259	19205760
    260	9602880
    261	19205760
    263	9602880
    267	9602880
    268	9602880
    269	9602880
    270	9602880
    272	19205760
    274	9602880
    275	9602880
    276	9602880
    277	9602880
    278	9602880
    279	9602880
    280	9602880
    286	9602880
    287	9602880
    288	19205760
    290	9602880
    291	9602880
    294	19205760
    295	9602880
    296	9602880
    299	19205760
    302	9602880
    303	19205760
    304	9602880
    308	9602880
    309	19205760
    312	9602880
    313	9602880
    314	9602880
    316	9602880
    317	19205760
    318	9602880
    319	38411520
    320	9602880
    321	19205760
    322	9602880
    323	19205760
    325	19205760
    328	19205760
    330	9602880
    332	9602880
    333	28808640
    335	9602880
    336	19205760
    342	19205760
    346	28808640
    347	9602880
    348	19205760
    350	9602880
    351	9602880
    353	19205760
    354	9602880
    358	9602880
    360	9602880
    362	19205760
    363	9602880
    364	9602880
    365	9602880
    367	9602880
    370	9602880
    373	9602880
    375	19205760
    378	9602880
    389	9602880
    392	9602880
    397	9602880
    398	19205760
    399	9602880
    400	19205760
    401	9602880
    402	28808640
    407	19205760
    409	9602880
    411	9602880
    413	9602880
    414	9602880
    415	9602880
    420	9602880
    421	9602880
    424	9602880
    426	9602880
    427	9602880
    430	19205760
    435	9602880
    443	9602880
    446	9602880
    449	9602880
    451	9602880
    453	9602880
    455	9602880
    460	9602880
    462	19205760
    463	19205760
    465	9602880
    466	28808640
    472	19205760
    473	19205760
    475	9602880
    476	9602880
    477	9602880
    478	9602880
    479	9602880
    481	9602880
    483	9602880
    489	9602880
    490	9602880
    492	9602880
    497	9602880
    499	9602880
    500	9602880
    501	9602880
    502	19205760
    503	9602880
    505	9602880
    506	9602880
    507	9602880
    508	19205760
    510	9602880
    511	19205760
    512	9602880
    513	9602880
    515	9602880
    516	19205760
    517	9602880
    520	9602880
    526	9602880
    528	19205760
    532	9602880
    533	9602880
    539	19205760
    540	19205760
    541	9602880
    543	19205760
    544	19205760
    545	9602880
    546	9602880
    547	19205760
    548	9602880
    549	9602880
    551	19205760
    552	28808640
    553	9602880
    554	9602880
    555	28808640
    556	9602880
    557	19205760
    558	28808640
    559	9602880
    560	19205760
    562	9602880
    564	9602880
    565	19205760
    566	9602880
    567	9602880
    568	19205760
    570	19205760
    571	38411520
    572	9602880
    574	9602880
    575	9602880
    577	9602880
    578	19205760
    579	19205760
    580	9602880
    582	19205760
    586	19205760
    587	9602880
    588	9602880
    589	9602880
    590	9602880
    593	9602880
    594	19205760
    595	9602880
    596	19205760
    598	9602880
    599	9602880
    600	9602880
    601	28808640
    602	9602880
    603	19205760
    604	9602880
    606	9602880
    608	9602880
    609	9602880
    610	9602880
    611	9602880
    613	9602880
    614	19205760
    615	9602880
    616	9602880
    617	9602880
    618	19205760
    621	28808640
    622	9602880
    623	28808640
    624	9602880
    626	19205760
    627	9602880
    628	9602880
    629	9602880
    630	9602880
    633	9602880
    634	9602880
    638	9602880
    640	9602880
    641	9602880
    642	9602880
    643	9602880
    644	9602880
    645	9602880
    647	9602880
    648	9602880
    650	28808640
    651	9602880
    652	9602880
    654	9602880
    661	9602880
    662	9602880
    674	9602880
    679	9602880
    680	9602880
    683	28808640
    684	9602880
    686	9602880
    690	9602880
    692	19205760
    694	9602880
    696	9602880
    704	9602880
    705	9602880
    706	9602880
    711	9602880
    715	9602880
    717	9602880
    723	19205760
    726	9602880
    730	9602880
    735	9602880
    742	9602880
    745	9602880
    746	9602880
    747	9602880
    749	28808640
    750	9602880
    751	28808640
    753	9602880
    759	19205760
    774	9602880
    781	9602880
    783	9602880
    784	9602880
    792	28808640
    795	19205760
    798	9602880
    803	9602880
    805	9602880
    812	9602880
    814	9602880
    815	9602880
    816	19205760
    825	9602880
    830	19205760
    841	9602880
    842	9602880
    844	9602880
    863	19205760
    864	9602880
    866	9602880
    869	9602880
    873	9602880
    878	19205760
    887	28808640
    890	9602880
    898	28808640
    899	9602880
    900	9602880
    904	9602880
    910	19205760
    916	9602880
    920	19205760
    924	9602880
    929	9602880
    934	9602880
    935	9602880
    947	9602880
    949	9602880
    951	9602880
    952	9602880
    957	9602880
    958	9602880
    959	9602880
    962	9602880
    972	9602880
    979	19205760
    980	9602880
    981	9602880
    991	9602880
    994	9602880
    1010	9602880
    1012	9602880
    1016	9602880
    1017	9602880
    1018	9602880
    1023	9602880
    1027	9602880
    1029	19205760
    1032	9602880
    1034	9602880
    1046	9602880
    1052	9602880
    1053	9602880
    1064	9602880
    1067	9602880
    1068	9602880
    1072	9602880
    1078	9602880
    1082	28808640
    1088	9602880
    1089	9602880
    1092	9602880
    1098	9602880
    1099	9602880
    1100	9602880
    1108	9602880
    1111	9602880
    1122	9602880
    1127	9602880
    1128	9602880
    1130	19205760
    1134	9602880
    1137	9602880
    1148	28808640
    1155	9602880
    1170	9602880
    1175	9602880
    1186	9602880
    1187	9602880
    1196	19205760
    1200	9602880
    1210	9602880
    1214	9602880
    1220	9602880
    1232	9602880
    1242	9602880
    1270	19205760
    1283	9602880
    1291	9602880
    1292	9602880
    1293	9602880
    1296	9602880
    1315	9602880
    1352	9602880
    1367	9602880
    1374	9602880
    1377	9602880
    1386	9602880
    1387	9602880
    1403	9602880
    1425	9602880
    1431	9602880
    1455	9602880
    1457	9602880
    1464	9602880
    1466	9602880
    1474	9602880
    1499	9602880
    1513	9602880
    1523	9602880
    1525	9602880
    1526	9602880
    1535	9602880
    1537	9602880
    1538	9602880
    1576	9602880
    1580	9602880
    1610	9602880
    1611	9602880
    1616	9602880
    1623	9602880
    1625	9602880
    1677	9602880
    1691	9602880
    1694	9602880
    1707	9602880
    1709	9602880
    1712	9602880
    1729	9602880
    1733	9602880
    1744	9602880
    1758	19205760
    1767	9602880
    1775	9602880
    1781	19205760
    1792	9602880
    1796	9602880
    1813	9602880
    1819	9602880
    1852	9602880
    1867	9602880
    1873	19205760
    1880	9602880
    1886	9602880
    1887	9602880
    1889	9602880
    1902	9602880
    1917	9602880
    1919	9602880
    1939	9602880
    1945	9602880
    1948	9602880
    1950	9602880
    1959	9602880
    1960	9602880
    1961	19205760
    1970	9602880
    1994	9602880
    1998	9602880
    2024	9602880
    2028	9602880
    2033	9602880
    2054	9602880
    2086	9602880
    2090	9602880
    2098	9602880
    2109	9602880
    2115	9602880
    2153	9602880
    2155	9602880
    2158	9602880
    2160	9602880
    2230	9602880
    2237	9602880
    2241	9602880
    2257	9602880
    2269	9602880
    2294	9602880
    2307	9602880
    2331	9602880
    2356	9602880
    2410	9602880
    2417	9602880
    2426	9602880
    2455	9602880
    2473	9602880
    2489	9602880
    2504	9602880
    2548	9602880
    2558	9602880
    2560	9602880
    2572	9602880
    2597	9602880
    2610	9602880
    2615	9602880
    2646	9602880
    2648	9602880
    2667	9602880
    2670	9602880
    2681	9602880
    2712	9602880
    2724	9602880
    2728	9602880
    2785	9602880
    2798	9602880
    2818	9602880
    2836	9602880
    2841	9602880
    2869	9602880
    2881	9602880
    2927	9602880
    2938	9602880
    3062	9602880
    3066	9602880
    3094	9602880
    3132	9602880
    3280	9602880
    3325	9602880
    3326	9602880
    3345	9602880
    3363	9602880
    3367	9602880
    3398	9602880
    3400	9602880
    3411	9602880
    3434	9602880
    3524	9602880
    3558	9602880
    3615	9602880
    3859	9602880
    3962	9602880
    4037	9602880
    4051	9602880
    4063	9602880
"""

clueweb12_t192_latency_kdax_str = """
    Latency	Loads
    2	9602880
    6	30335497920
    7	557648844480
    8	45018301440
    9	26369508480
    11	67220160
    12	5905771200
    13	1315594560
    14	3274582080
    15	4916674560
    16	18523955520
    17	2467940160
    18	1872561600
    19	1296388800
    20	941082240
    21	883464960
    22	902670720
    23	3389816640
    24	2333499840
    25	4676602560
    26	595378560
    27	2112633600
    28	921876480
    29	384115200
    30	1930178880
    31	460938240
    32	825847680
    33	211263360
    34	201660480
    35	134440320
    36	163248960
    37	182454720
    38	144043200
    39	124837440
    40	124837440
    41	134440320
    42	96028800
    43	153646080
    44	124837440
    45	345703680
    46	115234560
    47	57617280
    48	67220160
    49	115234560
    50	67220160
    51	259277760
    52	499349760
    53	134440320
    54	96028800
    55	134440320
    56	124837440
    57	48014400
    58	172851840
    59	201660480
    60	76823040
    61	268880640
    62	76823040
    63	115234560
    64	67220160
    65	220866240
    66	192057600
    67	249674880
    68	288086400
    69	134440320
    70	76823040
    71	96028800
    72	153646080
    73	38411520
    74	67220160
    75	96028800
    76	86425920
    77	48014400
    78	96028800
    79	48014400
    80	28808640
    81	76823040
    82	38411520
    83	38411520
    84	134440320
    85	57617280
    86	76823040
    87	48014400
    88	38411520
    89	9602880
    90	67220160
    91	28808640
    92	57617280
    93	57617280
    94	76823040
    95	48014400
    96	67220160
    97	67220160
    98	48014400
    99	19205760
    100	38411520
    101	9602880
    102	28808640
    103	38411520
    104	28808640
    105	28808640
    106	48014400
    107	38411520
    108	48014400
    109	38411520
    110	76823040
    111	57617280
    112	38411520
    113	9602880
    114	38411520
    115	28808640
    116	28808640
    117	9602880
    118	67220160
    119	38411520
    120	48014400
    121	48014400
    122	9602880
    123	48014400
    124	19205760
    126	19205760
    127	19205760
    128	48014400
    129	9602880
    131	9602880
    132	38411520
    133	9602880
    134	19205760
    135	9602880
    136	19205760
    137	19205760
    138	9602880
    139	19205760
    141	9602880
    143	19205760
    145	19205760
    146	9602880
    148	28808640
    150	9602880
    151	19205760
    154	9602880
    155	9602880
    157	28808640
    159	19205760
    160	9602880
    161	38411520
    162	9602880
    163	9602880
    164	28808640
    165	28808640
    166	19205760
    168	19205760
    169	19205760
    170	9602880
    172	28808640
    173	9602880
    174	19205760
    175	9602880
    176	9602880
    177	19205760
    178	9602880
    179	9602880
    180	9602880
    182	28808640
    183	9602880
    184	19205760
    185	9602880
    186	9602880
    188	9602880
    189	9602880
    190	28808640
    191	28808640
    192	19205760
    193	9602880
    195	9602880
    198	19205760
    199	9602880
    201	9602880
    203	19205760
    206	9602880
    207	9602880
    208	19205760
    212	9602880
    215	19205760
    220	9602880
    222	28808640
    223	19205760
    225	9602880
    227	19205760
    231	9602880
    232	9602880
    233	9602880
    234	19205760
    235	19205760
    236	28808640
    238	19205760
    239	9602880
    240	9602880
    241	19205760
    242	19205760
    244	9602880
    245	19205760
    246	9602880
    247	19205760
    249	9602880
    250	9602880
    253	9602880
    257	38411520
    262	9602880
    263	9602880
    264	9602880
    265	9602880
    267	9602880
    270	9602880
    272	9602880
    273	9602880
    274	9602880
    275	19205760
    276	19205760
    277	9602880
    278	19205760
    279	19205760
    281	9602880
    283	19205760
    286	28808640
    287	19205760
    289	19205760
    290	19205760
    291	9602880
    294	9602880
    295	9602880
    296	9602880
    298	9602880
    299	19205760
    300	19205760
    302	28808640
    303	9602880
    305	9602880
    306	19205760
    308	38411520
    310	9602880
    312	9602880
    313	9602880
    314	19205760
    316	19205760
    319	9602880
    320	9602880
    322	9602880
    323	9602880
    324	19205760
    326	9602880
    328	9602880
    329	19205760
    330	19205760
    332	9602880
    333	9602880
    335	28808640
    336	28808640
    337	9602880
    339	9602880
    340	9602880
    344	9602880
    345	19205760
    348	9602880
    349	19205760
    350	9602880
    354	9602880
    357	9602880
    358	9602880
    359	9602880
    360	9602880
    362	9602880
    365	9602880
    366	19205760
    368	28808640
    371	9602880
    374	19205760
    375	19205760
    379	9602880
    381	28808640
    383	9602880
    384	9602880
    385	9602880
    386	9602880
    387	9602880
    388	19205760
    389	9602880
    397	19205760
    402	19205760
    403	19205760
    406	9602880
    407	9602880
    408	9602880
    409	9602880
    410	9602880
    411	9602880
    413	9602880
    415	9602880
    416	9602880
    419	9602880
    423	19205760
    425	9602880
    426	9602880
    427	9602880
    429	9602880
    436	9602880
    440	9602880
    442	9602880
    443	9602880
    444	9602880
    447	9602880
    449	9602880
    451	9602880
    453	9602880
    454	9602880
    456	9602880
    457	19205760
    458	19205760
    460	9602880
    463	28808640
    468	19205760
    475	9602880
    479	9602880
    480	9602880
    481	9602880
    484	9602880
    486	9602880
    487	19205760
    489	9602880
    495	9602880
    497	9602880
    499	9602880
    504	9602880
    505	9602880
    506	9602880
    511	9602880
    513	9602880
    514	9602880
    516	9602880
    518	9602880
    521	9602880
    533	9602880
    535	9602880
    539	9602880
    542	9602880
    544	9602880
    547	9602880
    548	9602880
    555	9602880
    559	9602880
    560	9602880
    561	9602880
    562	9602880
    565	9602880
    568	9602880
    572	19205760
    573	9602880
    574	9602880
    579	9602880
    583	9602880
    584	9602880
    587	9602880
    588	9602880
    592	9602880
    596	9602880
    597	9602880
    599	9602880
    604	9602880
    606	9602880
    608	9602880
    612	9602880
    613	9602880
    614	9602880
    616	9602880
    617	9602880
    618	9602880
    626	9602880
    632	9602880
    633	19205760
    635	19205760
    638	9602880
    643	9602880
    649	19205760
    654	9602880
    655	9602880
    670	9602880
    677	28808640
    678	9602880
    682	9602880
    685	9602880
    691	9602880
    695	9602880
    698	9602880
    701	19205760
    707	9602880
    715	9602880
    716	9602880
    717	9602880
    733	9602880
    737	9602880
    739	9602880
    750	9602880
    757	9602880
    759	9602880
    766	19205760
    775	9602880
    776	9602880
    779	19205760
    781	9602880
    796	9602880
    800	9602880
    810	19205760
    818	19205760
    821	9602880
    828	9602880
    830	9602880
    831	9602880
    844	9602880
    846	9602880
    849	9602880
    861	9602880
    867	9602880
    869	9602880
    884	9602880
    888	9602880
    889	9602880
    899	9602880
    900	9602880
    906	9602880
    911	9602880
    933	9602880
    935	9602880
    938	9602880
    941	9602880
    954	9602880
    960	9602880
    965	9602880
    972	9602880
    995	9602880
    1010	9602880
    1021	19205760
    1033	9602880
    1038	9602880
    1052	9602880
    1065	28808640
    1072	9602880
    1085	9602880
    1097	9602880
    1100	9602880
    1102	9602880
    1110	9602880
    1113	9602880
    1125	9602880
    1128	9602880
    1129	9602880
    1131	9602880
    1139	9602880
    1146	9602880
    1149	19205760
    1151	9602880
    1160	9602880
    1161	9602880
    1163	9602880
    1167	9602880
    1173	9602880
    1174	9602880
    1176	9602880
    1178	9602880
    1183	9602880
    1187	9602880
    1194	9602880
    1195	9602880
    1198	9602880
    1201	9602880
    1202	9602880
    1203	9602880
    1205	9602880
    1208	19205760
    1211	9602880
    1215	9602880
    1221	9602880
    1223	9602880
    1237	9602880
    1245	9602880
    1247	19205760
    1249	9602880
    1253	19205760
    1266	9602880
    1270	9602880
    1274	9602880
    1279	9602880
    1280	9602880
    1283	9602880
    1284	9602880
    1290	9602880
    1295	9602880
    1297	9602880
    1299	9602880
    1300	19205760
    1307	9602880
    1311	9602880
    1318	9602880
    1323	9602880
    1325	9602880
    1326	9602880
    1327	19205760
    1329	9602880
    1331	9602880
    1333	9602880
    1334	9602880
    1344	9602880
    1356	9602880
    1360	9602880
    1361	9602880
    1367	19205760
    1368	9602880
    1384	9602880
    1385	9602880
    1388	9602880
    1391	9602880
    1402	28808640
    1407	9602880
    1410	19205760
    1411	9602880
    1420	9602880
    1423	9602880
    1428	9602880
    1436	9602880
    1441	9602880
    1442	9602880
    1453	9602880
    1454	9602880
    1474	9602880
    1478	9602880
    1483	9602880
    1486	9602880
    1490	9602880
    1496	9602880
    1503	9602880
    1517	19205760
    1519	9602880
    1522	9602880
    1523	9602880
    1534	9602880
    1543	9602880
    1552	9602880
    1553	9602880
    1554	9602880
    1558	9602880
    1564	9602880
    1565	9602880
    1572	9602880
    1593	9602880
    1604	9602880
    1611	9602880
    1617	9602880
    1619	9602880
    1625	9602880
    1638	9602880
    1657	9602880
    1665	9602880
    1670	9602880
    1682	19205760
    1685	9602880
    1686	9602880
    1692	9602880
    1693	9602880
    1712	9602880
    1713	9602880
    1718	9602880
    1723	19205760
    1734	9602880
    1750	9602880
    1769	9602880
    1783	9602880
    1802	9602880
    1830	9602880
    1853	9602880
    1892	9602880
    1921	9602880
    1927	9602880
    1944	9602880
    1948	9602880
    1965	9602880
    1966	9602880
    1982	9602880
    1998	9602880
    2020	9602880
    2032	9602880
    2034	9602880
    2041	9602880
    2048	9602880
    2049	9602880
    2094	9602880
    2102	9602880
    2103	9602880
    2112	9602880
    2115	9602880
    2120	9602880
    2126	9602880
    2163	9602880
    2174	9602880
    2180	9602880
    2194	9602880
    2197	9602880
    2207	9602880
    2226	9602880
    2230	9602880
    2232	19205760
    2256	9602880
    2262	9602880
    2265	9602880
    2355	9602880
    2364	9602880
    2380	9602880
    2396	9602880
    2477	9602880
    2505	9602880
    2510	9602880
    2515	9602880
    2538	9602880
    2570	9602880
    2579	9602880
    2625	9602880
    2680	9602880
    2697	9602880
    2717	9602880
    2720	9602880
    2744	9602880
    2769	9602880
    2775	9602880
    2779	9602880
    2800	9602880
    2823	9602880
    2828	9602880
    2852	9602880
    2946	9602880
    2963	9602880
    3006	9602880
    3070	9602880
    3112	9602880
    3131	9602880
    3140	9602880
    3199	9602880
    3201	9602880
    3228	9602880
    3235	9602880
    3257	9602880
    3279	9602880
    3315	9602880
    3319	9602880
    3344	9602880
    3345	9602880
    3381	9602880
    3414	9602880
    3443	9602880
    3477	9602880
    3585	9602880
    3587	9602880
    3638	9602880
    3677	9602880
    3834	9602880
    3835	9602880
    3849	9602880
    3903	9602880
    3930	9602880
    3943	9602880
    3975	9602880
    3995	9602880
    4070	9602880
"""


#----------------------------------------------------------------------------
# uk2014, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

uk2014_t192_latency_mem_str = """
    Latency	Loads
    6	28069218240
    7	605336746560
    8	52105226880
    9	27176150400
    11	96028800
    12	6184254720
    13	1267580160
    14	3312993600
    15	5195158080
    16	14116233600
    17	2439131520
    18	2016604800
    19	2362308480
    20	1161948480
    21	835450560
    22	1152345600
    23	2352705600
    24	3024907200
    25	1776532800
    26	566569920
    27	643392960
    28	604981440
    29	230469120
    30	307292160
    31	288086400
    32	432129600
    33	230469120
    34	278483520
    35	182454720
    36	134440320
    37	134440320
    38	172851840
    39	211263360
    40	211263360
    41	163248960
    42	96028800
    43	163248960
    44	105631680
    45	48014400
    46	67220160
    47	124837440
    48	124837440
    49	57617280
    50	57617280
    51	57617280
    52	86425920
    53	86425920
    54	57617280
    55	28808640
    56	105631680
    57	76823040
    58	57617280
    59	86425920
    60	28808640
    61	76823040
    62	57617280
    63	38411520
    64	48014400
    65	48014400
    66	48014400
    67	57617280
    68	48014400
    69	48014400
    70	48014400
    71	28808640
    72	48014400
    73	9602880
    74	57617280
    75	67220160
    76	48014400
    77	67220160
    78	57617280
    79	57617280
    80	67220160
    81	76823040
    82	48014400
    83	19205760
    84	38411520
    85	57617280
    86	28808640
    87	19205760
    88	28808640
    89	48014400
    90	38411520
    91	38411520
    92	28808640
    93	19205760
    94	57617280
    95	38411520
    96	19205760
    97	28808640
    98	38411520
    99	28808640
    100	9602880
    101	9602880
    102	38411520
    103	19205760
    104	38411520
    105	38411520
    108	19205760
    109	9602880
    110	19205760
    111	9602880
    112	9602880
    113	28808640
    116	19205760
    117	38411520
    118	38411520
    120	19205760
    121	28808640
    122	19205760
    125	9602880
    126	38411520
    127	9602880
    128	19205760
    131	9602880
    132	9602880
    133	9602880
    134	9602880
    135	19205760
    136	28808640
    138	9602880
    139	9602880
    141	9602880
    142	9602880
    145	9602880
    146	19205760
    147	19205760
    148	9602880
    152	9602880
    153	28808640
    155	9602880
    156	9602880
    158	9602880
    160	9602880
    167	9602880
    168	9602880
    169	19205760
    170	9602880
    172	9602880
    175	38411520
    176	9602880
    177	9602880
    178	9602880
    179	9602880
    180	9602880
    181	9602880
    182	9602880
    185	9602880
    196	9602880
    197	28808640
    198	9602880
    200	9602880
    202	9602880
    204	28808640
    205	9602880
    212	28808640
    222	9602880
    227	9602880
    232	9602880
    236	9602880
    239	9602880
    241	9602880
    242	19205760
    245	9602880
    249	9602880
    255	9602880
    257	9602880
    260	9602880
    264	9602880
    266	9602880
    271	9602880
    273	9602880
    274	19205760
    275	9602880
    277	9602880
    284	9602880
    285	9602880
    286	9602880
    288	9602880
    289	9602880
    293	19205760
    304	9602880
    307	9602880
    309	9602880
    310	9602880
    311	9602880
    313	19205760
    317	9602880
    318	9602880
    319	9602880
    320	19205760
    321	9602880
    327	9602880
    329	9602880
    332	28808640
    341	9602880
    342	19205760
    345	9602880
    348	9602880
    352	9602880
    353	9602880
    354	9602880
    356	9602880
    361	9602880
    366	9602880
    378	9602880
    381	19205760
    382	9602880
    383	9602880
    389	19205760
    393	19205760
    397	9602880
    401	9602880
    402	19205760
    410	9602880
    411	9602880
    419	9602880
    420	9602880
    426	9602880
    437	9602880
    442	9602880
    447	9602880
    448	9602880
    450	19205760
    454	9602880
    455	9602880
    468	9602880
    469	9602880
    476	19205760
    481	19205760
    483	9602880
    490	9602880
    503	9602880
    504	9602880
    507	9602880
    521	9602880
    525	19205760
    533	9602880
    538	9602880
    543	9602880
    547	9602880
    556	9602880
    560	9602880
    563	9602880
    572	9602880
    573	9602880
    575	9602880
    583	9602880
    584	9602880
    590	9602880
    591	9602880
    592	9602880
    602	9602880
    606	19205760
    610	19205760
    618	9602880
    623	9602880
    626	9602880
    641	19205760
    645	9602880
    646	9602880
    655	19205760
    658	9602880
    659	9602880
    662	9602880
    665	9602880
    686	9602880
    689	9602880
    691	19205760
    696	9602880
    698	9602880
    707	9602880
    711	9602880
    718	9602880
    719	9602880
    723	9602880
    725	9602880
    733	9602880
    738	19205760
    739	9602880
    740	9602880
    742	9602880
    750	9602880
    752	9602880
    762	9602880
    763	9602880
    766	9602880
    772	9602880
    784	9602880
    786	9602880
    791	9602880
    793	19205760
    794	9602880
    798	9602880
    811	9602880
    814	9602880
    816	9602880
    817	9602880
    836	9602880
    837	9602880
    840	9602880
    861	9602880
    872	9602880
    875	9602880
    887	9602880
    893	9602880
    918	19205760
    923	9602880
    932	9602880
    939	9602880
    940	9602880
    943	9602880
    947	19205760
    948	9602880
    953	9602880
    954	9602880
    975	9602880
    980	9602880
    987	9602880
    993	9602880
    997	9602880
    999	9602880
    1006	9602880
    1007	9602880
    1014	9602880
    1018	9602880
    1020	9602880
    1024	9602880
    1041	9602880
    1047	9602880
    1048	9602880
    1054	9602880
    1066	9602880
    1068	9602880
    1081	9602880
    1088	9602880
    1097	9602880
    1098	9602880
    1130	9602880
    1156	9602880
    1163	9602880
    1165	9602880
    1177	9602880
    1179	9602880
    1181	9602880
    1191	9602880
    1199	9602880
    1201	9602880
    1204	9602880
    1211	9602880
    1233	9602880
    1239	9602880
    1242	9602880
    1250	9602880
    1293	19205760
    1303	9602880
    1320	9602880
    1340	9602880
    1349	9602880
    1380	9602880
    1386	9602880
    1392	9602880
    1403	9602880
    1407	9602880
    1414	9602880
    1425	9602880
    1433	9602880
    1448	9602880
    1461	9602880
    1479	9602880
    1482	9602880
    1486	9602880
    1503	9602880
    1511	19205760
    1514	9602880
    1515	19205760
    1530	19205760
    1542	9602880
    1551	9602880
    1555	9602880
    1560	9602880
    1563	9602880
    1570	19205760
    1580	9602880
    1593	9602880
    1599	9602880
    1604	9602880
    1625	19205760
    1629	9602880
    1630	9602880
    1651	9602880
    1655	9602880
    1673	9602880
    1677	9602880
    1690	9602880
    1701	19205760
    1705	9602880
    1716	9602880
    1718	9602880
    1776	9602880
    1777	9602880
    1778	9602880
    1794	9602880
    1797	9602880
    1798	28808640
    1799	9602880
    1811	9602880
    1831	9602880
    1842	9602880
    1845	9602880
    1863	9602880
    1893	9602880
    1895	9602880
    1913	9602880
    1927	9602880
    1928	9602880
    1933	9602880
    1954	9602880
    1959	9602880
    1996	9602880
    2010	9602880
    2040	9602880
    2043	9602880
    2051	9602880
    2055	9602880
    2061	9602880
    2072	19205760
    2125	9602880
    2126	9602880
    2132	9602880
    2146	9602880
    2150	9602880
    2167	9602880
    2179	9602880
    2222	9602880
    2225	9602880
    2233	9602880
    2234	9602880
    2262	19205760
    2273	9602880
    2279	9602880
    2288	9602880
    2302	19205760
    2314	9602880
    2319	9602880
    2368	9602880
    2403	9602880
    2421	9602880
    2424	9602880
    2433	9602880
    2434	9602880
    2463	9602880
    2495	9602880
    2499	9602880
    2522	9602880
    2549	9602880
    2574	9602880
    2581	9602880
    2596	9602880
    2631	19205760
    2638	9602880
    2652	9602880
    2660	9602880
    2670	9602880
    2711	9602880
    2736	9602880
    2749	19205760
    2752	9602880
    2765	9602880
    2769	9602880
    2777	9602880
    2796	9602880
    2805	9602880
    2809	9602880
    2812	9602880
    2851	9602880
    2867	9602880
    2883	9602880
    2913	9602880
    2922	9602880
    2949	9602880
    2953	9602880
    2997	9602880
    3030	9602880
    3039	9602880
    3081	9602880
    3087	9602880
    3118	9602880
    3141	9602880
    3168	9602880
    3215	9602880
    3240	9602880
    3265	9602880
    3271	9602880
    3281	9602880
    3293	9602880
    3312	9602880
    3324	9602880
    3370	9602880
    3385	9602880
    3386	9602880
    3458	9602880
    3469	9602880
    3470	9602880
    3472	9602880
    3491	9602880
    3508	9602880
    3549	9602880
    3550	9602880
    3626	9602880
    3648	9602880
    3661	9602880
    3667	9602880
    3937	9602880
    3997	9602880
"""

uk2014_t192_latency_kdax_str = """
    Latency	Loads
    6	28174849920
    7	601226713920
    8	53996994240
    9	27886763520
    11	86425920
    12	5540861760
    13	1584475200
    14	2900069760
    15	4993497600
    16	16228867200
    17	2967289920
    18	2026207680
    19	2026207680
    20	1181154240
    21	883464960
    22	1046713920
    23	2179853760
    24	3159347520
    25	2103030720
    26	537761280
    27	604981440
    28	691407360
    29	422526720
    30	307292160
    31	393718080
    32	489746880
    33	297689280
    34	153646080
    35	134440320
    36	182454720
    37	144043200
    38	124837440
    39	182454720
    40	134440320
    41	144043200
    42	163248960
    43	115234560
    44	96028800
    45	76823040
    46	96028800
    47	124837440
    48	48014400
    49	76823040
    50	9602880
    51	67220160
    52	19205760
    53	96028800
    54	96028800
    55	86425920
    56	76823040
    57	9602880
    58	19205760
    59	57617280
    60	28808640
    61	48014400
    62	57617280
    63	9602880
    64	67220160
    65	28808640
    66	57617280
    67	19205760
    68	67220160
    69	67220160
    70	86425920
    71	48014400
    72	76823040
    73	38411520
    74	9602880
    75	57617280
    76	9602880
    77	28808640
    78	38411520
    79	38411520
    80	19205760
    81	48014400
    82	38411520
    83	48014400
    84	28808640
    85	48014400
    86	28808640
    87	28808640
    88	19205760
    89	38411520
    90	38411520
    91	19205760
    92	38411520
    93	28808640
    94	76823040
    95	86425920
    96	38411520
    97	28808640
    98	9602880
    99	48014400
    100	38411520
    101	28808640
    102	28808640
    103	9602880
    104	38411520
    105	28808640
    106	28808640
    107	19205760
    108	28808640
    109	48014400
    110	9602880
    111	19205760
    112	19205760
    113	19205760
    114	48014400
    115	19205760
    116	9602880
    117	9602880
    119	38411520
    120	19205760
    121	9602880
    122	9602880
    123	9602880
    124	19205760
    125	48014400
    126	9602880
    127	38411520
    128	19205760
    129	9602880
    130	19205760
    131	9602880
    132	28808640
    133	28808640
    134	28808640
    138	9602880
    139	9602880
    140	19205760
    141	19205760
    142	9602880
    143	19205760
    147	9602880
    148	9602880
    149	9602880
    151	19205760
    152	9602880
    153	19205760
    154	9602880
    156	9602880
    160	9602880
    161	9602880
    162	9602880
    163	9602880
    166	9602880
    168	28808640
    169	19205760
    171	9602880
    173	9602880
    180	9602880
    186	9602880
    188	28808640
    194	19205760
    195	9602880
    196	9602880
    198	9602880
    200	9602880
    202	9602880
    209	9602880
    210	9602880
    213	9602880
    216	9602880
    220	9602880
    225	19205760
    227	9602880
    228	9602880
    230	9602880
    231	9602880
    233	9602880
    235	9602880
    242	9602880
    245	9602880
    247	9602880
    248	19205760
    251	9602880
    253	19205760
    254	9602880
    259	9602880
    264	9602880
    266	9602880
    275	9602880
    277	9602880
    278	28808640
    282	9602880
    287	9602880
    291	9602880
    292	9602880
    294	9602880
    295	9602880
    299	9602880
    304	9602880
    309	9602880
    311	9602880
    313	9602880
    318	9602880
    323	9602880
    325	9602880
    327	9602880
    328	9602880
    331	9602880
    332	9602880
    334	9602880
    337	9602880
    338	9602880
    340	9602880
    344	9602880
    351	9602880
    356	9602880
    360	9602880
    364	9602880
    366	9602880
    369	9602880
    370	9602880
    375	9602880
    388	9602880
    391	19205760
    393	9602880
    395	9602880
    400	9602880
    403	9602880
    405	9602880
    408	9602880
    409	28808640
    411	9602880
    412	9602880
    413	9602880
    415	9602880
    417	9602880
    418	9602880
    420	9602880
    421	9602880
    422	9602880
    423	9602880
    425	9602880
    427	9602880
    436	19205760
    439	9602880
    442	9602880
    448	9602880
    453	9602880
    454	9602880
    460	9602880
    461	9602880
    473	9602880
    482	9602880
    488	9602880
    493	9602880
    496	9602880
    499	9602880
    506	9602880
    509	9602880
    512	9602880
    513	9602880
    514	9602880
    522	9602880
    525	19205760
    539	9602880
    550	9602880
    552	9602880
    563	9602880
    564	9602880
    566	9602880
    567	9602880
    568	9602880
    579	9602880
    582	9602880
    586	9602880
    589	19205760
    612	9602880
    613	9602880
    620	9602880
    634	9602880
    637	9602880
    647	9602880
    654	9602880
    673	9602880
    677	9602880
    681	9602880
    683	9602880
    699	9602880
    704	9602880
    711	9602880
    721	9602880
    722	9602880
    729	9602880
    735	19205760
    739	9602880
    747	9602880
    755	9602880
    760	9602880
    767	9602880
    774	19205760
    775	9602880
    790	9602880
    798	9602880
    805	9602880
    808	9602880
    810	9602880
    824	9602880
    831	9602880
    836	9602880
    841	9602880
    844	19205760
    845	9602880
    850	19205760
    854	9602880
    864	9602880
    866	9602880
    868	9602880
    892	9602880
    897	9602880
    908	19205760
    910	9602880
    912	9602880
    914	9602880
    924	19205760
    932	9602880
    935	9602880
    938	19205760
    941	19205760
    943	19205760
    944	9602880
    965	9602880
    974	9602880
    975	19205760
    978	9602880
    984	9602880
    987	9602880
    990	9602880
    1015	9602880
    1022	9602880
    1027	9602880
    1029	9602880
    1050	9602880
    1068	9602880
    1069	9602880
    1070	9602880
    1080	9602880
    1097	9602880
    1102	9602880
    1146	9602880
    1153	19205760
    1157	9602880
    1174	9602880
    1179	9602880
    1202	9602880
    1205	9602880
    1218	9602880
    1221	9602880
    1227	9602880
    1228	9602880
    1230	9602880
    1259	9602880
    1260	9602880
    1286	9602880
    1299	9602880
    1302	19205760
    1315	9602880
    1347	9602880
    1355	19205760
    1358	9602880
    1376	9602880
    1385	9602880
    1389	9602880
    1395	9602880
    1396	9602880
    1399	9602880
    1403	9602880
    1407	9602880
    1418	9602880
    1431	9602880
    1457	9602880
    1473	9602880
    1478	9602880
    1481	9602880
    1488	9602880
    1495	9602880
    1520	9602880
    1522	9602880
    1542	9602880
    1544	9602880
    1545	9602880
    1550	9602880
    1551	19205760
    1563	9602880
    1566	9602880
    1575	9602880
    1581	9602880
    1586	9602880
    1594	9602880
    1603	9602880
    1617	9602880
    1622	9602880
    1629	19205760
    1640	9602880
    1647	9602880
    1651	9602880
    1663	9602880
    1665	9602880
    1691	9602880
    1711	9602880
    1742	9602880
    1747	9602880
    1753	9602880
    1775	9602880
    1787	9602880
    1788	9602880
    1794	9602880
    1795	9602880
    1844	9602880
    1865	9602880
    1881	9602880
    1887	9602880
    1895	9602880
    1899	9602880
    1906	9602880
    1923	9602880
    1937	9602880
    1946	9602880
    1968	9602880
    1999	9602880
    2013	9602880
    2021	9602880
    2023	9602880
    2028	9602880
    2039	9602880
    2061	9602880
    2087	9602880
    2092	9602880
    2096	9602880
    2114	19205760
    2123	9602880
    2126	9602880
    2154	9602880
    2165	19205760
    2167	9602880
    2172	9602880
    2193	19205760
    2201	9602880
    2209	9602880
    2229	9602880
    2238	9602880
    2283	9602880
    2311	9602880
    2317	9602880
    2319	9602880
    2328	9602880
    2343	9602880
    2357	9602880
    2379	9602880
    2396	9602880
    2418	9602880
    2432	9602880
    2438	9602880
    2452	9602880
    2464	9602880
    2506	9602880
    2508	9602880
    2512	9602880
    2519	9602880
    2529	9602880
    2531	9602880
    2573	9602880
    2576	9602880
    2621	9602880
    2640	9602880
    2660	9602880
    2684	9602880
    2692	9602880
    2703	9602880
    2710	9602880
    2767	9602880
    2808	9602880
    2827	9602880
    2841	9602880
    2977	9602880
    2988	9602880
    3010	9602880
    3052	9602880
    3067	9602880
    3122	9602880
    3200	9602880
    3295	9602880
    3304	9602880
    3326	9602880
    3341	9602880
    3347	9602880
    3396	9602880
    3597	9602880
    3648	9602880
    3661	9602880
    3794	9602880
    3801	9602880
    3828	9602880
    3859	9602880
    3932	9602880
    3959	9602880
    4038	9602880
    4047	9602880
    4075	9602880
"""


#----------------------------------------------------------------------------
# XXX, 192 threads, Load Latency (cycles)
#----------------------------------------------------------------------------

XXX_t192_latency_dram_str = """
    Latency	Loads
"""

XXX_t192_latency_mem_str = """
    Latency	Loads
"""

XXX_t192_latency_kdax_str = """
    Latency	Loads
"""

XXX_t192_latency_pdax_str = """
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



def plot_scaling(dfrm, graph_nm, axes, y_metric, plt_sty, mrk_sty, ln_sty, nm_j):
    dfrm_me = dfrm.xs(graph_nm, level='graph')

    dfrm_me = dfrm_me.dropna(axis='rows', subset=[y_metric])
    #print(dfrm_me)

    plt_sty = plot_align_palette(dfrm_me.index.get_level_values('mode').values, plt_sty)
    
    ax = seaborn.lineplot(data=dfrm_me, x='threads', y=y_metric,
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

    #print("bw_dfrm_hist\n", bw_dfrm_hist)
    #print("bw_dfrm_wide\n", bw_dfrm_wide)

    plt_sty = plot_align_palette(bw_dfrm_hist.columns, plt_sty)

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


def plot_align_palette(modeL, plt_sty):
    # if no dram values, adjust plt_sty

    if ('dram' in modeL):
        return plt_sty
    else:
        modeS = set(modeL)
        plt = seaborn.color_palette(plt_sty, n_colors= (len(modeS) + 1))
        plt.pop(0)
        return plt


#****************************************************************************
#
#****************************************************************************


def makeRelTime(dfrm, row_srcL, col_src, col_dst):
    col_dat = []

    for (graph, thrd, ty) in dfrm.index:
        #print("{}: {}/{}/{}".format(makeRelTime.__name__,graph, thrd, ty))
        v = dfrm.at[(graph, thrd, ty), col_src]

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

fig1, axes1L = pyplt.subplots(nrows=2, ncols=3, figsize=(9, 4.0))

fig2, axes2L = pyplt.subplots(nrows=1, ncols=4, figsize=(14, 2.5))

fig2x, axes2xA = pyplt.subplots(nrows=2, ncols=4, figsize=(14, 5.5),
                                gridspec_kw={'height_ratios': [4.0, 3.5]})

fig3, axes3L = pyplt.subplots(nrows=1, ncols=5, figsize=(14, 2.5))


ln_sty1 = '-' # ':' # --
ln_sty2 = '--' # ':' # 
mrk_sty1 = 'o' # --
mrk_sty2 = 'x' # --

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
    plot_modes(mode_dfrm, axes1L[0][nm_i], nm_i, ttl, plt_sty1, mrk_sty1, ln_sty1)
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
    plot_modes(mode_dfrm, axes1L[1][nm_i], nm_i, ttl, plt_sty1, mrk_sty1, ln_sty1)
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

plot_scaling(time_dfrm_grp, nm, axes2L[nm_j], col_src, plt_sty1, mrk_sty1, ln_sty1, nm_j)

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

plot_bw_lat(axes2xA[0,nm_j], axes2xA[1,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)


#-------------------------------------------------------
# 
#-------------------------------------------------------

nm = 'moliere2016'
nm_j = 1

plot_scaling(time_dfrm_grp, nm, axes2L[nm_j], col_src, plt_sty1, mrk_sty1, ln_sty1, nm_j)

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

plot_bw_lat(axes2xA[0,nm_j], axes2xA[1,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)

#-------------------------------------------------------
# 
#-------------------------------------------------------

nm = 'clueweb12'
nm_j = 2

bw_data_nmL =  ['mem', 'kdax', 'kdax'] # 'mem',
lat_data_nmL =  ['mem', 'kdax']


plot_scaling(time_dfrm_grp, nm, axes2L[nm_j], col_src, plt_sty1, mrk_sty1, ln_sty1, nm_j)

bw_data_strL = [ clueweb12_t192_dramBw_mem_str,
                 #clueweb12_t192_pmemBw_mem_str,
                 
                 clueweb12_t192_dramBw_kdax_str,
                 clueweb12_t192_pmemBw_kdax_str ]

lat_data_strL = [ clueweb12_t192_latency_mem_str,
                  clueweb12_t192_latency_kdax_str ]

plot_bw_lat(axes2xA[0,nm_j], axes2xA[1,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)

#-------------------------------------------------------
# 
#-------------------------------------------------------

nm = 'uk2014'
nm_j = 3


plot_scaling(time_dfrm_grp, nm, axes2L[nm_j], col_src, plt_sty1, mrk_sty1, ln_sty1, nm_j)

bw_data_strL = [ uk2014_t192_dramBw_mem_str,
                 #uk2014_t192_pmemBw_mem_str,

                 uk2014_t192_dramBw_kdax_str,
                 uk2014_t192_pmemBw_kdax_str ]


lat_data_strL = [ uk2014_t192_latency_mem_str,
                  uk2014_t192_latency_kdax_str ]


plot_bw_lat(axes2xA[0,nm_j], axes2xA[1,nm_j], bw_data_strL, lat_data_strL, nm, bw_data_nmL, lat_data_nmL, plt_sty2, nm_j)


#----------------------------------------------------------------------------
# Ripples: Per-graph Scaling
#----------------------------------------------------------------------------

nmL = [ 'slash', 'twitter', 'talk', 'pokec', 'topcats' ]

nm_i = 0
for nm in nmL:
    plot_scaling(time_dfrm_rip, nm, axes3L[nm_i], col_src, plt_sty1, mrk_sty1, ln_sty1, nm_i)
    nm_i += 1


#----------------------------------------------------------------------------

adjustH1 = { 'left':0.05, 'right':0.99, 'bottom':0.08, 'top':0.92,
             'wspace':0.20, 'hspace':0.45 }

adjustH2 = { 'left':0.05, 'right':0.99, 'bottom':0.03, 'top':0.97,
             'wspace':0.18, 'hspace':0.15 }

fig1.subplots_adjust(**adjustH1)
fig2.subplots_adjust(**adjustH2)
fig3.subplots_adjust(**adjustH2)

fig1.savefig('chart-teaser.pdf', bbox_inches='tight')
fig2.savefig('chart-grappolo-scaling.pdf', bbox_inches='tight')
#fig2x.savefig('chart-2x.pdf', bbox_inches='tight')
fig3.savefig('chart-ripples-scaling.pdf', bbox_inches='tight')

#seaborn.plt.show()
pyplt.show()
