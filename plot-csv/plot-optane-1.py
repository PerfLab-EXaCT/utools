#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys
#import argparse

import collections

import pandas
import numpy
import math
import matplotlib.pyplot as pyplt
import seaborn

import VTuneCSV as vtcsv

#****************************************************************************

txt_sz_heatmap = 10
txt_sz_heatmap_scale = 10

do_view = 0

#****************************************************************************
#
#****************************************************************************

def main():
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    # cf. 1perf-projects.gitlab/graph-reorder/py-reorder/relayout/driver.py
    #parser = argparse.ArgumentParser()
    #args = vars(parser.parse_args())
    #csv_pathL.append(os.path.abspath(sys.argv[i]))
    
    #assert(len(sys.argv) > 1)
    #csv_pathL = sys.argv[1:]
    
    #-------------------------------------------------------
    # Medium graphs/All memory modes
    #-------------------------------------------------------

    graphL_med = ['orkut', 'friendster', 'moliere2016']

    # grappolo-orkut-appdirect-dram-pkg.csv
    # grappolo-orkut-appdirect-pdax-pkg.csv
    # grappolo-friendster-appdirect-dram-pkg.csv
    # grappolo-friendster-appdirect-pdax-pkg.csv
    # grappolo-moliere2016-appdirect-dram-pkg.csv
    # grappolo-moliere2016-appdirect-pdax-pkg.csv

    # grappolo-friendster-appdirect-dram-fn.csv
    # grappolo-friendster-appdirect-pdax-fn.csv
    # grappolo-moliere2016-appdirect-dram-fn.csv
    # grappolo-moliere2016-appdirect-pdax-fn.csv
    # grappolo-orkut-appdirect-dram-fn.csv
    # grappolo-orkut-appdirect-pdax-fn.csv

    #???
    # grappolo-friendster-appdirect-kdax-pkg.csv
    # grappolo-friendster-appdirect-kdax-fn.csv


    path_pfx = './1grappolo/grappolo-'

    pathL1 = [
        [path_pfx + x + '-appdirect-dram-pkg.csv',
         path_pfx + x + '-appdirect-pdax-pkg.csv',
         path_pfx + x + '-appdirect-kdax-pkg.csv'] for x in graphL_med ]

    pathL1 = [x for pair in pathL1 for x in pair ] # flatten

    pathL2 = [
        [path_pfx + x + '-appdirect-dram-fn.csv',
         path_pfx + x + '-appdirect-pdax-fn.csv',
         path_pfx + x + '-appdirect-kdax-fn.csv'] for x in graphL_med ]

    pathL2 = [x for pair in pathL2 for x in pair ] # flatten

    
    #-------------------------------------------------------
    # Big graphs/Big memory modes
    #-------------------------------------------------------

    graphL_big = ['clueweb12', 'uk2014']

    # grappolo-clueweb12-appdirect-kdax-pkg.csv
    # grappolo-uk2014-appdirect-kdax-pkg.csv

    # grappolo-clueweb12-appdirect-kdax-fn.csv
    # grappolo-uk2014-appdirect-kdax-fn.csv

    pathL3 = [path_pfx + x + '-appdirect-kdax-pkg.csv' for x in graphL_big ]

    pathL4 = [path_pfx + x + '-appdirect-kdax-fn.csv' for x in graphL_big ]

    
    #-------------------------------------------------------

    metricL1_p = [
        #('CPU Time', ''),
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #('Memory Bound(%)', ''), ''),
        ('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        ('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        ('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        #('Memory Bound:Store Bound(%)', 'Store Bound (%)')
        #('Memory Bound:Persistent Memory Bound(%)', 'Pdax Bound (%)')
        ]

    makeColL_f = [ ('CPU Time', 'CPU Time (%)', 'percent') ]
    metricL1_f = [
        (makeColL_f[0][1], ''),
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #('Memory Bound(%)', ''), ''),
        ('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        ('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        ('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        #('Memory Bound:Store Bound(%)', 'Store Bound (%)')
        #('Memory Bound:Persistent Memory Bound(%)', 'Pdax Bound (%)')
        ]
    
    metricL2 = [
        ('Loads', ''),
        ('Stores', ''),
        #('LLC Miss Count', 'LLC Miss'),
        ('LLC Miss Count:Remote DRAM Access Count', 'LLC Miss:Remote DRAM'),
        ('LLC Miss Count:Local DRAM Access Count',  'LLC Miss:Local DRAM'),
        #('LLC Miss Count:Local Persistent Memory Access Count', 'LLC Miss:Local Pdax'),
        #('LLC Miss Count:Remote Persistent Memory Access Count', 'LLC Miss:Remote Pdax'),
        ('LLC Miss Count:Remote Cache Access Count', 'LLC Miss:Remote Cache')
        ]
    
    
    #-------------------------------------------------------
    # Medium graphs
    #-------------------------------------------------------

    vt_Mp = vtcsv.VTuneCSV(pathL1, group_by = 'csv')
    vt_Mf = vtcsv.VTuneCSV(pathL2, group_by = 'csv', makeColL = makeColL_f)

    widthL_p = (3.4, 3.9, 1.8)
    widthL_f = (3.5, 3.9, 1.8) # h=2.7
    (fig_Mp1, fig_Mp2) = plot_pkg(vt_Mp, graphL_med, widthL_p, metricL1_p, metricL2)
    (fig_Mf1, fig_Mf2) = plot_fn (vt_Mf, graphL_med, widthL_f, metricL1_f, metricL2)

    fig_Mp1.savefig("chart-grappolo-med-pkg-metric1.pdf", bbox_inches='tight')
    #fig_Mp2.savefig("chart-grappolo-med-pkg-metric2.pdf", bbox_inches='tight')

    fig_Mf1.savefig("chart-grappolo-med-fn-metric1.pdf", bbox_inches='tight')
    #fig_Mf2.savefig("chart-grappolo-med-fn-metric2.pdf", bbox_inches='tight')

    #-------------------------------------------------------
    # Big graphs
    #-------------------------------------------------------

    vt_Bp = vtcsv.VTuneCSV(pathL3, group_by = 'csv')
    vt_Bf = vtcsv.VTuneCSV(pathL4, group_by = 'csv', makeColL = makeColL_f)

    widthL_p = (2.1, 2.1, 1.8)
    widthL_f = (2.3, 2.3, 1.8) # h=2.7
    (fig_Bp1, fig_Bp2) = plot_pkg(vt_Bp, graphL_big, widthL_p, metricL1_p, metricL2)
    (fig_Bf1, fig_Bf2) = plot_fn (vt_Bf, graphL_big, widthL_f, metricL1_f, metricL2)

    fig_Bp1.savefig("chart-grappolo-big-pkg-metric1.pdf", bbox_inches='tight')
    #fig_Bp2.savefig("chart-grappolo-big-pkg-metric2.pdf", bbox_inches='tight')

    fig_Bf1.savefig("chart-grappolo-big-fn-metric1.pdf", bbox_inches='tight')
    #fig_Bf2.savefig("chart-grappolo-big-fn-metric2.pdf", bbox_inches='tight')

    pyplt.show()

    
#****************************************************************************

def plot_pkg(vt, graphL, widthL, metricL1, metricL2):

    # Massage 'vt' in-place
    # for kv in vt.dataL:
    #     dfrm = kv[1]
    #     dfrm.sort_index(axis=0, ascending=True, inplace=True)
    #     dfrm.rename(index = (lambda x: x.replace("package_", "")), inplace=True)
    #     dfrm.rename(columns = (lambda x: rename_col(x, graphL)), inplace=True)

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    (w1, w2, h) = (widthL[0], widthL[1], widthL[2])
    
    num_metric1 = len(metricL1)
    fig1, axesL1 = pyplt.subplots(nrows=1, ncols=(num_metric1), figsize=(w1*num_metric1,h))
    plot_row(vt, fig1, axesL1, metricL1, dfrm_pkg_xform(graphL), 'Socket', graphL)

    num_metric2 = len(metricL2)
    fig2, axesL2 = pyplt.subplots(nrows=1, ncols=(num_metric2), figsize=(w2*num_metric2,h))
    plot_row(vt, fig2, axesL2, metricL2, dfrm_pkg_xform(graphL), 'Socket', graphL)

    return (fig1, fig2)


def dfrm_pkg_xform(graphL):
    def dfrm_pkg_xform1(dfrm):
        dfrm.sort_index(axis=0, ascending=True, inplace=True)
        dfrm.rename(index = (lambda x: x.replace("package_", "")), inplace=True)
        dfrm.rename(columns = (lambda x: rename_col(x, graphL)), inplace=True)
        return dfrm
    return dfrm_pkg_xform1
    

#****************************************************************************

def plot_fn(vt, graphL, widthL, metricL1, metricL2):

    functionH = collections.OrderedDict( [
        ('buildLocalMapCounter', 'blmc'),
        ('std::_Rb_tree_insert_and_rebalance', 'blmc->map'),
        ('max', 'max'),
        ('_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>', 'omp')
        #('plm_analyzeClusters$omp$parallel_for@64', 'plm'),
        #('_int_malloc', 'malloc'),
        #('__GI___libc_malloc', 'malloc2'),
        #('__gnu_cxx::new_allocator<double>::construct<double, double const&>', 'new'),
        #('_int_free',   'free')
    ] )

    #functionL = list(functionH.items())

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    (w1, w2, h) = (widthL[0], widthL[1], widthL[2])

    num_metric1 = len(metricL1)
    fig1, axesL1 = pyplt.subplots(nrows=1, ncols=(num_metric1), figsize=(w1*num_metric1,h))
    plot_row(vt, fig1, axesL1, metricL1, dfrm_fn_xform(functionH, graphL), 'Functions', graphL)

    num_metric2 = len(metricL2)
    fig2, axesL2 = pyplt.subplots(nrows=1, ncols=(num_metric2), figsize=(w2*num_metric2,h))
    plot_row(vt, fig2, axesL2, metricL2, dfrm_fn_xform(functionH, graphL), 'Functions', graphL)

    return (fig1, fig2)

    
def dfrm_fn_xform(functionH, graphL):
    def dfrm_fn_xform1(dfrm):
        functionLkey = functionH.keys()
        dfrm = dfrm.loc[functionLkey]
        dfrm.rename(index = functionH, inplace=True)
        dfrm.rename(columns = (lambda x: rename_col(x, graphL)), inplace=True)
        return dfrm
    return dfrm_fn_xform1

    
#****************************************************************************

def plot_row(vt, fig, axesL, metricL, dfrm_xformF, ytitle_txt, graphL):
    num_metric = len(metricL)
    for i in range(num_metric):
        axes = axesL[i]

        axes.margins(tight=True)

        metricPair = metricL[i]
        ytitle = ytitle_txt if (i == 0) else None

        dfrm = vt.dataH[metricPair[0]]

        dfrm = dfrm_xformF(dfrm)

        axes1 = plot(dfrm, axes, metricPair, ytitle, graphL)

    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.01, top=0.99,
                        wspace=0.02, hspace=0.0)
    if (do_view):
        fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
    

def plot(dfrm, axes, metricPair, ytitle, xticks2L = None):

    #-------------------------------------------------------
    # Scale data values for nice formattting
    #-------------------------------------------------------

    dfrm_scale_exp = None
    txt_fmt = '.2g'
    txt_sz = txt_sz_heatmap
    txt_rot = 0

    dfrm_max = numpy.max(dfrm.to_numpy())
    #dfrm_md = numpy.median(dfrm.to_numpy())
    if (dfrm_max > 100):
        dfrm_scale_exp = math.floor(math.log10(dfrm_max)) - 2
        dfrm_scale = math.pow(10, dfrm_scale_exp)
        dfrm = dfrm.applymap(lambda x: x / dfrm_scale)
        txt_fmt = '.3g'
        #txt_sz = txt_sz_heatmap + 1
        txt_rot = 40

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    do_y_lbl = True if (ytitle) else False
    
    axes = seaborn.heatmap(dfrm, ax=axes, annot=True,
                           cbar=True, cmap="RdBu_r",# coolwarm
                           fmt=txt_fmt,
                           yticklabels=do_y_lbl,
                           annot_kws={'size' : txt_sz,
                                      'rotation' : txt_rot } )

    if (dfrm_scale_exp):
        axes.text(1.06, 0.997, (r'$\times10^{%s}$' % dfrm_scale_exp),
                   transform=axes.transAxes, ha='left', va='bottom') # size=txt_sz_heatmap_scale

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    title_txt = metricPair[1] if (metricPair[1]) else metricPair[0]
    axes.set_title(title_txt)

    if (ytitle):
        axes.set_ylabel(ytitle)

    # correct x labels
    axes.set_xticklabels(dfrm.columns, rotation=15, ha='right')
    #for x in axes.get_xticklabels():
    #    x.set_rotation(0)

    #-------------------------------------------------------
    # Secondary X labels
    #-------------------------------------------------------
    if (xticks2L):
        n_x1 = len(dfrm.columns)
        n_x2 = len(xticks2L)
        x2_skip = int(n_x1 / n_x2)
        x2_beg = x2_skip / 2.0 # midpoint

        axes2 = axes.twiny() # twin y
        axes2_ticks = [ (x/n_x1) for x in list(numpy.arange(x2_beg, n_x1, x2_skip)) ]
        axes2.set_xticks(axes2_ticks)
        axes2.set_xticklabels(xticks2L, rotation=0, ha='center')
    
    return axes

#****************************************************************************


def rename_col(x, graphL):
    x0 = x

    for g in graphL: x0 = x0.replace(g, "")
    
    x0 = x0.replace("grappolo--appdirect-", "") # not a typo!
    x0 = x0.replace("-pkg", "")
    x0 = x0.replace("-fn", "")
    
    return x0


#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
