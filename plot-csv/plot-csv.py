#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys
#import argparse

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

    graphL = ['orkut', 'friendster', 'moliere2016']

    pathL1 = [
        [path_pfx + y + '-optane-appdirect-dram-pkg.csv',
         path_pfx + y + '-optane-appdirect-pmem-pkg.csv'] for y in graphL ]

    pathL1 = [x for pair in pathL1 for x in pair ]

    pathL2 = [
        [path_pfx + y + '-optane-appdirect-dram-fn.csv',
         path_pfx + y + '-optane-appdirect-pmem-fn.csv'] for y in graphL ]

    pathL2 = [x for pair in pathL2 for x in pair ]

    vt1 = vtcsv.VTuneCSV(pathL1, group_by = 'csv')
    vt2 = vtcsv.VTuneCSV(pathL2, group_by = 'csv')
    
    plot_pkg(vt1, graphL)
    pyplt.show()

    
    
#****************************************************************************

def plot_pkg(vt, graphL):
    colL1 = [
        #'CPU Time',
        #'Memory Bound(%)',
        'Average Latency (cycles)',
        'Memory Bound:L1 Bound(%)',
        'Memory Bound:L2 Bound(%)',
        'Memory Bound:L3 Bound(%)',
        'Memory Bound:DRAM Bound(%)',
        'Memory Bound:Store Bound(%)',
        #'Memory Bound:Persistent Memory Bound(%)',
        ]

    colL2 = [
        'Loads',
        'Stores',
        #'LLC Miss Count',
        'LLC Miss Count:Remote DRAM Access Count',
        'LLC Miss Count:Local DRAM Access Count',
        #'LLC Miss Count:Local Persistent Memory Access Count',
        #'LLC Miss Count:Remote Persistent Memory Access Count',
        'LLC Miss Count:Remote Cache Access Count'
    ]
   
    for kv in vt.dataL:
        dfrm = kv[1]
        dfrm.sort_index(axis=0, ascending=True, inplace=True)

        dfrm.rename(index = (lambda x: x.replace("package_", "")), inplace=True)
        dfrm.rename(columns = (lambda x: rename_col(x, graphL)), inplace=True)


    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    len_col1 = len(colL1)
    fig1, axesL1 = pyplt.subplots(nrows=1, ncols=(len_col1), figsize=(3.2*len_col1,3.0))

    for i in range(len_col1):
        axes = axesL1[i]
        metric = colL1[i]
        ytitle = 'Socket' if (i == 0) else None
        plot_pkg_doit(vt, axes, metric, graphL, ytitle)


    len_col2 = len(colL2)
    fig2, axesL2 = pyplt.subplots(nrows=1, ncols=(len_col2), figsize=(3.2*len_col2,3.0))
    
    for i in range(len_col2):
        axes = axesL2[i]
        metric = colL2[i]
        ytitle = 'Socket' if (i == 0) else None
        plot_pkg_doit(vt, axes, metric, graphL, ytitle)
        
    fig1.tight_layout()
    fig2.tight_layout()


def plot_pkg_doit(vt, axes, metric, graphL, ytitle):
    dfrm = vt.dataH[metric]

    axes1 = plot(dfrm, axes, metric, graphL)

    if (ytitle):
        axes1.set_ylabel(ytitle)

    pyplt.subplots_adjust(wspace = -0.05)



#****************************************************************************

def plot_fn(vt, graphL):
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------


    fnL = [ 'buildLocalMapCounter',
            'std::_Rb_tree_insert_and_rebalance',
            'max',
            '_int_free',
            '_int_malloc',
            '_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>',
            '__GI___libc_malloc',
            '__gnu_cxx::new_allocator<double>::construct<double, double const&>',
            'plm_analyzeClusters$omp$parallel_for@64' ]

    colL1 = [ 'Memory Bound:L1 Bound(%)',
              'Memory Bound:L2 Bound(%)',
              'Memory Bound:L3 Bound(%)',
              'Memory Bound:DRAM Bound(%)',
              'Memory Bound:Store Bound(%)',
              'Memory Bound:Persistent Memory Bound(%)'
    ]
    
    # col2 = [ 'Loads',
    #          'Stores',
    #          'LLC Miss Count']




#****************************************************************************

def plot(dfrm, axes, title, graphL): # txt_fmt, txt_sz, txt_rot
    # axes = pyplt.axes(label=title)

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

    axes = seaborn.heatmap(dfrm, ax=axes, annot=True, cmap="RdBu_r",# coolwarm
                           fmt=txt_fmt,
                           annot_kws={'size' : txt_sz,
                                      'rotation' : txt_rot } )

    axes.set_xticklabels(dfrm.columns, rotation=15, ha='right')
    #axes.set_xlabel('')

    axes2 = axes.twiny() # twin y
    axes2_ticks = [ x/6 for x in list(range(1, len(dfrm.columns), 2)) ]
    axes2.set_xticks(axes2_ticks)
    axes2.set_xticklabels(graphL, rotation=0, ha='center')

    if (dfrm_scale_exp):
        axes.text(1.04, 0.99, (r'$\times10^{%s}$' % dfrm_scale_exp),
                   transform=axes.transAxes, ha='left', va='bottom') # size=txt_sz_heatmap_scale

    axes.set_title(rename_metric(title))
    
    return axes


def rename_metric(x):
    x0 = x
    
    x0 = x0.replace("LLC Miss Count", "LLC Miss")
    x0 = x0.replace("Persistent Memory", "PMem")
    x0 = x0.replace("Count", "")
    x0 = x0.replace("Access", "")

    return x0

    
def rename_col(x, graphL):
    x0 = x

    for g in graphL: x0 = x0.replace(g, "")
    
    x0 = x0.replace("grappolo-vtune-profile--optane-appdirect-", "")
    x0 = x0.replace("-pkg", "")
    
    return x0


#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
