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
    # 
    #-------------------------------------------------------

    graphL = ['orkut', 'friendster', 'moliere2016']
    
    #-------------------------------------------------------

    # './data/grappolo-vtune-profile-orkut-optane-appdirect-dram-pkg.csv',
    # './data/grappolo-vtune-profile-orkut-optane-appdirect-pmem-pkg.csv',
    # './data/grappolo-vtune-profile-friendster-optane-appdirect-dram-pkg.csv',
    # './data/grappolo-vtune-profile-friendster-optane-appdirect-pmem-pkg.csv',
    # './data/grappolo-vtune-profile-moliere2016-optane-appdirect-dram-pkg.csv',
    # './data/grappolo-vtune-profile-moliere2016-optane-appdirect-pmem-pkg.csv'

    # './data/grappolo-vtune-profile-friendster-optane-appdirect-dram-fn.csv',
    # './data/grappolo-vtune-profile-friendster-optane-appdirect-pmem-fn.csv',
    # './data/grappolo-vtune-profile-moliere2016-optane-appdirect-dram-fn.csv',
    # './data/grappolo-vtune-profile-moliere2016-optane-appdirect-pmem-fn.csv',
    # './data/grappolo-vtune-profile-orkut-optane-appdirect-dram-fn.csv',
    # './data/grappolo-vtune-profile-orkut-optane-appdirect-pmem-fn.csv'

    path_pfx = './data/grappolo-vtune-profile-'

    pathL1 = [
        [path_pfx + y + '-optane-appdirect-dram-pkg.csv',
         path_pfx + y + '-optane-appdirect-pmem-pkg.csv'] for y in graphL ]

    pathL1 = [x for pair in pathL1 for x in pair ]

    pathL2 = [
        [path_pfx + y + '-optane-appdirect-dram-fn.csv',
         path_pfx + y + '-optane-appdirect-pmem-fn.csv'] for y in graphL ]

    pathL2 = [x for pair in pathL2 for x in pair ]

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

    metricL1b = [
        ('CPU Time', ''), # FIXME: need percent
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
    # 
    #-------------------------------------------------------

    vt1 = vtcsv.VTuneCSV(pathL1, group_by = 'csv')
    vt2 = vtcsv.VTuneCSV(pathL2, group_by = 'csv')
    
    (fig1a, fig1b) = plot_pkg(vt1, graphL, metricL1, metricL2)
    (fig2a, fig2b) = plot_fn (vt2, graphL, metricL1b, metricL2)

    fig1a.savefig("chart-grappolo-pkg-metric1.pdf", bbox_inches='tight')
    fig1b.savefig("chart-grappolo-pkg-metric2.pdf", bbox_inches='tight')

    fig2a.savefig("chart-grappolo-fn-metric1.pdf", bbox_inches='tight')
    fig2b.savefig("chart-grappolo-fn-metric2.pdf", bbox_inches='tight')

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
    fig1, axesL1 = pyplt.subplots(nrows=1, ncols=(num_metric1), figsize=(3.2*num_metric1,2.9))
    plot_row(vt, axesL1, metricL1, dfrm_pkg_xform(graphL), 'Socket', graphL)
    #pyplt.subplots_adjust(wspace=0.0)
    fig1.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)

    num_metric2 = len(metricL2)
    fig2, axesL2 = pyplt.subplots(nrows=1, ncols=(num_metric2), figsize=(3.3*num_metric2,2.9))
    plot_row(vt, axesL2, metricL2, dfrm_pkg_xform(graphL), 'Socket', graphL)
    #pyplt.subplots_adjust(wspace=0.0)
    fig2.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)

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
        ('plm_analyzeClusters$omp$parallel_for@64', 'plm'),
        ('max', 'max'),
        ('_int_malloc', 'malloc'),
        ('__GI___libc_malloc', 'malloc2'),
        ('__gnu_cxx::new_allocator<double>::construct<double, double const&>', 'new'),
        ('_int_free',   'free'),
        ('_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>', 'omp')
    ] )

    #functionL = list(functionH.items())

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    num_metric1 = len(metricL1)
    fig1, axesL1 = pyplt.subplots(nrows=1, ncols=(num_metric1), figsize=(3.4*num_metric1,3.2))
    plot_row(vt, axesL1, metricL1, dfrm_fn_xform(functionH, graphL), 'Functions', graphL)
    #pyplt.subplots_adjust(wspace=0.0)
    fig1.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)

    num_metric2 = len(metricL2)
    fig2, axesL2 = pyplt.subplots(nrows=1, ncols=(num_metric2), figsize=(3.5*num_metric2,3.2))
    plot_row(vt, axesL2, metricL2, dfrm_fn_xform(functionH, graphL), 'Functions', graphL)
    #pyplt.subplots_adjust(wspace=0.0)
    fig2.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)

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

def plot_row(vt, axesL, metricL, dfrm_xformF, ytitle_txt, graphL):
    num_metric = len(metricL)
    for i in range(num_metric):
        axes = axesL[i]

        axes.margins(tight=True)

        metricPair = metricL[i]
        ytitle = ytitle_txt if (i == 0) else None

        dfrm = vt.dataH[metricPair[0]]

        dfrm = dfrm_xformF(dfrm)

        axes1 = plot(dfrm, axes, metricPair, ytitle, graphL)
    

def plot(dfrm, axes, metricPair, ytitle, graphL):

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
        txt_sz = txt_sz_heatmap - 1
        txt_rot = 45

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
        axes.text(1.05, 0.995, (r'$\times10^{%s}$' % dfrm_scale_exp),
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

    axes2 = axes.twiny() # twin y
    axes2_ticks = [ x/6 for x in list(range(1, len(dfrm.columns), 2)) ]
    axes2.set_xticks(axes2_ticks)
    axes2.set_xticklabels(graphL, rotation=0, ha='center')
    
    return axes

#****************************************************************************

    
def rename_col(x, graphL):
    x0 = x

    for g in graphL: x0 = x0.replace(g, "")
    
    x0 = x0.replace("grappolo-vtune-profile--optane-appdirect-", "")
    x0 = x0.replace("-pkg", "")
    x0 = x0.replace("-fn", "")
    
    return x0


#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
