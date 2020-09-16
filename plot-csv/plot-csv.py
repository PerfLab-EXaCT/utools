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
    # grappolo-pmem-dax
    #-------------------------------------------------------

    # './grappolo-vtune-profile-orkut-appdirect-dram-pkg.csv'
    # './grappolo-vtune-profile-orkut-appdirect-pmem-pkg.csv'
    # './grappolo-vtune-profile-friendster-appdirect-dram-pkg.csv'
    # './grappolo-vtune-profile-friendster-appdirect-pmem-pkg.csv'
    # './grappolo-vtune-profile-moliere2016-appdirect-dram-pkg.csv'
    # './grappolo-vtune-profile-moliere2016-appdirect-pmem-pkg.csv'

    # './grappolo-vtune-profile-friendster-appdirect-dram-fn.csv'
    # './grappolo-vtune-profile-friendster-appdirect-pmem-fn.csv'
    # './grappolo-vtune-profile-moliere2016-appdirect-dram-fn.csv'
    # './grappolo-vtune-profile-moliere2016-appdirect-pmem-fn.csv'
    # './grappolo-vtune-profile-orkut-appdirect-dram-fn.csv'
    # './grappolo-vtune-profile-orkut-appdirect-pmem-fn.csv'

    graphL = ['orkut', 'friendster', 'moliere2016']
    
    path_pfx = './grappolo-pmem-dax/grappolo-vtune-profile-'

    pathL1 = [
        [path_pfx + x + '-appdirect-dram-pkg.csv',
         path_pfx + x + '-appdirect-pmem-pkg.csv'] for x in graphL ]

    pathL1 = [x for pair in pathL1 for x in pair ] # flatten

    pathL2 = [
        [path_pfx + x + '-appdirect-dram-fn.csv',
         path_pfx + x + '-appdirect-pmem-fn.csv'] for x in graphL ]

    pathL2 = [x for pair in pathL2 for x in pair ] # flatten

    
    #-------------------------------------------------------
    # grappolo-kmem-dax
    #-------------------------------------------------------

    # grappolo-vtune-profile-friendster-appdirect-pmem-pkg.csv
    # grappolo-vtune-profile-clueweb12-appdirect-pmem-pkg.csv
    # grappolo-vtune-profile-uk2014-appdirect-pmem-pkg.csv

    # grappolo-vtune-profile-friendster-appdirect-pmem-fn.csv
    # grappolo-vtune-profile-clueweb12-appdirect-pmem-fn.csv
    # grappolo-vtune-profile-uk2014-appdirect-pmem-fn.csv


    graphL_k = ['friendster', 'clueweb12', 'uk2014']

    path_pfx_k = './grappolo-kmem-dax/grappolo-vtune-profile-'

    pathL3 = [path_pfx_k + x + '-appdirect-pmem-pkg.csv' for x in graphL_k ]

    pathL4 = [path_pfx_k + x + '-appdirect-pmem-fn.csv' for x in graphL_k ]

    
    #-------------------------------------------------------

    metricL1 = [
        #('CPU Time', ''),
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #('Memory Bound(%)', ''), ''),
        ('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        ('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        ('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        ('Memory Bound:Store Bound(%)', 'Store Bound (%)')
        #('Memory Bound:Persistent Memory Bound(%)', 'PMem Bound (%)')
        ]

    makeColL = [ ('CPU Time', 'CPU Time (%)', 'percent') ]
    metricL1b = [
        (makeColL[0][1], ''),
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #('Memory Bound(%)', ''), ''),
        ('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        ('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        ('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        #('Memory Bound:Store Bound(%)', 'Store Bound (%)')
        #('Memory Bound:Persistent Memory Bound(%)', 'PMem Bound (%)')
        ]
    
    metricL2 = [
        ('Loads', ''),
        ('Stores', ''),
        #('LLC Miss Count', 'LLC Miss'),
        ('LLC Miss Count:Remote DRAM Access Count', 'LLC Miss:Remote DRAM'),
        ('LLC Miss Count:Local DRAM Access Count',  'LLC Miss:Local DRAM'),
        #('LLC Miss Count:Local Persistent Memory Access Count', 'LLC Miss:Local PMem'),
        #('LLC Miss Count:Remote Persistent Memory Access Count', 'LLC Miss:Remote PMem'),
        ('LLC Miss Count:Remote Cache Access Count', 'LLC Miss:Remote Cache')
        ]
    
    
    #-------------------------------------------------------
    # pmem-dax
    #-------------------------------------------------------

    vt1 = vtcsv.VTuneCSV(pathL1, group_by = 'csv')
    vt2 = vtcsv.VTuneCSV(pathL2, group_by = 'csv', makeColL = makeColL)
    
    (fig1a, fig1b) = plot_pkg(vt1, graphL, metricL1, metricL2)
    (fig2a, fig2b) = plot_fn (vt2, graphL, metricL1b, metricL2)

    fig1a.savefig("chart-grappolo-pdax-pkg-metric1.pdf", bbox_inches='tight')
    fig1b.savefig("chart-grappolo-pdax-pkg-metric2.pdf", bbox_inches='tight')

    fig2a.savefig("chart-grappolo-pdax-fn-metric1.pdf", bbox_inches='tight')
    fig2b.savefig("chart-grappolo-pdax-fn-metric2.pdf", bbox_inches='tight')

    #-------------------------------------------------------
    # kmem-dax
    #-------------------------------------------------------

    vt3 = vtcsv.VTuneCSV(pathL3, group_by = 'csv')
    vt4 = vtcsv.VTuneCSV(pathL4, group_by = 'csv', makeColL = makeColL)
    
    (fig3a, fig3b) = plot_pkg(vt3, graphL_k, metricL1, metricL2)
    (fig4a, fig4b) = plot_fn (vt4, graphL_k, metricL1b, metricL2)

    fig3a.savefig("chart-grappolo-kdax-pkg-metric1.pdf", bbox_inches='tight')
    fig3b.savefig("chart-grappolo-kdax-pkg-metric2.pdf", bbox_inches='tight')

    fig4a.savefig("chart-grappolo-kdax-fn-metric1.pdf", bbox_inches='tight')
    fig4b.savefig("chart-grappolo-kdax-fn-metric2.pdf", bbox_inches='tight')

    pyplt.show()

    
#****************************************************************************

def plot_pkg(vt, graphL, metricL1, metricL2):

    # Massage 'vt' in-place
    # for kv in vt.dataL:
    #     dfrm = kv[1]
    #     dfrm.sort_index(axis=0, ascending=True, inplace=True)
    #     dfrm.rename(index = (lambda x: x.replace("package_", "")), inplace=True)
    #     dfrm.rename(columns = (lambda x: rename_col(x, graphL)), inplace=True)

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    num_metric1 = len(metricL1)
    fig1, axesL1 = pyplt.subplots(nrows=1, ncols=(num_metric1), figsize=(3.3*num_metric1,1.8))
    plot_row(vt, fig1, axesL1, metricL1, dfrm_pkg_xform(graphL), 'Socket', graphL)

    num_metric2 = len(metricL2)
    fig2, axesL2 = pyplt.subplots(nrows=1, ncols=(num_metric2), figsize=(3.5*num_metric2,1.8))
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

def plot_fn(vt, graphL, metricL1, metricL2):

    functionH = collections.OrderedDict( [
        ('buildLocalMapCounter', 'blmc'),
        ('std::_Rb_tree_insert_and_rebalance', 'blmc->map'),
        ('max', 'max'),
        ('_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>', 'omp'),
        ('plm_analyzeClusters$omp$parallel_for@64', 'plm'),
        ('_int_malloc', 'malloc'),
        ('__GI___libc_malloc', 'malloc2'),
        #('__gnu_cxx::new_allocator<double>::construct<double, double const&>', 'new'),
        ('_int_free',   'free')
    ] )

    #functionL = list(functionH.items())

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    num_metric1 = len(metricL1)
    fig1, axesL1 = pyplt.subplots(nrows=1, ncols=(num_metric1), figsize=(3.3*num_metric1,2.7))
    plot_row(vt, fig1, axesL1, metricL1, dfrm_fn_xform(functionH, graphL), 'Functions', graphL)

    num_metric2 = len(metricL2)
    fig2, axesL2 = pyplt.subplots(nrows=1, ncols=(num_metric2), figsize=(3.4*num_metric2,2.7))
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
    #fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
    

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
        skip_x2 = int(n_x1 / n_x2)

        axes2 = axes.twiny() # twin y
        axes2_ticks = [ (x/n_x1) for x in list(range(1, n_x1, skip_x2)) ]
        axes2.set_xticks(axes2_ticks)
        axes2.set_xticklabels(xticks2L, rotation=0, ha='center')
    
    return axes

#****************************************************************************


def rename_col(x, graphL):
    x0 = x

    for g in graphL: x0 = x0.replace(g, "")
    
    x0 = x0.replace("grappolo-vtune-profile--appdirect-", "") # not a typo!
    x0 = x0.replace("-pkg", "")
    x0 = x0.replace("-fn", "")
    
    return x0


#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
