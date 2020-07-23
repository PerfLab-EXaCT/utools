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
import matplotlib.pyplot as plt
import seaborn as sns

import VTuneCSV as vtcsv

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

    graphL = ['orkut', 'friendster', 'moliere2016']

    pathL1 = [
        './data/grappolo-vtune-profile-orkut-optane-appdirect-dram-pkg.csv',
        './data/grappolo-vtune-profile-orkut-optane-appdirect-pmem-pkg.csv',
        './data/grappolo-vtune-profile-friendster-optane-appdirect-dram-pkg.csv',
        './data/grappolo-vtune-profile-friendster-optane-appdirect-pmem-pkg.csv',
        './data/grappolo-vtune-profile-moliere2016-optane-appdirect-dram-pkg.csv',
        './data/grappolo-vtune-profile-moliere2016-optane-appdirect-pmem-pkg.csv' ]


    pathL2 = [
        './data/grappolo-vtune-profile-friendster-optane-appdirect-dram-fn.csv',
        './data/grappolo-vtune-profile-friendster-optane-appdirect-pmem-fn.csv',
        './data/grappolo-vtune-profile-moliere2016-optane-appdirect-dram-fn.csv',
        './data/grappolo-vtune-profile-moliere2016-optane-appdirect-pmem-fn.csv',
        './data/grappolo-vtune-profile-orkut-optane-appdirect-dram-fn.csv',
        './data/grappolo-vtune-profile-orkut-optane-appdirect-pmem-fn.csv']

    vt1 = vtcsv.VTuneCSV(pathL1, group_by = 'csv')
    vt2 = vtcsv.VTuneCSV(pathL2, group_by = 'csv')
    
    plot_pkg(vt1, graphL)
    
    
#****************************************************************************

def plot_pkg(vt, graphL):
    colL1 = [
        #'CPU Time',
        #'Memory Bound(%)',
        'Memory Bound:L1 Bound(%)',
        'Memory Bound:L2 Bound(%)',
        'Memory Bound:L3 Bound(%)',
        'Memory Bound:DRAM Bound(%)',
        'Memory Bound:Store Bound(%)',
        #'Memory Bound:Persistent Memory Bound(%)',
        ]

    colL2 = [
        'Loads',
        #'Stores',
        'LLC Miss Count',
        'LLC Miss Count:Local DRAM Access Count',
        'LLC Miss Count:Remote DRAM Access Count',
        #'LLC Miss Count:Local Persistent Memory Access Count',
        #'LLC Miss Count:Remote Persistent Memory Access Count',
        'LLC Miss Count:Remote Cache Access Count',
        'Average Latency (cycles)'
    ]
   
    for kv in vt.dataL:
        dfrm = kv[1]
        dfrm.sort_index(axis=0, ascending=True, inplace=True)

        dfrm.rename(index = (lambda x: x.replace("package_", "")), inplace=True)
        dfrm.rename(columns = (lambda x: rename_col(x, graphL)), inplace=True)


    #-------------------------------------------------------
    # 
    #-------------------------------------------------------
        
    fig1, axesL1 = plt.subplots(nrows=1, ncols=(len(colL1)), figsize=(20.0,3.0))

    for i in range(len(colL1)):
        axes = axesL1[i]
        metric = colL1[i]
        plot_pkg_doit(vt, axes, metric, graphL)


    fig2, axesL2 = plt.subplots(nrows=1, ncols=(len(colL2)), figsize=(20.0,3.0))
    
    for i in range(len(colL2)):
        axes = axesL2[i]
        metric = colL2[i]
        plot_pkg_doit(vt, axes, metric, graphL)
        
    fig1.tight_layout()
    fig2.tight_layout()
    
    plt.show()


def plot_pkg_doit(vt, axes, metric, graphL):
        dfrm = vt.dataH[metric]
        axes1 = plot(dfrm, axes, metric, graphL, kind='heat')

        axes1.set_title(rename_metric(metric))
        axes1.set_ylabel('Socket')

        plt.subplots_adjust(wspace = 0.05)


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

def plot(dfrm, axes, name, graphL, kind):
    # axes = plt.axes(label=name)
    axes = sns.heatmap(dfrm, ax=axes, annot=True, cmap="RdBu_r") # coolwarm
    axes.set_xticklabels(dfrm.columns, rotation=15, ha='right')
    #axes.set_xlabel('')

    ax2 = axes.twiny() # twin y
    ax2_ticks = [ x/6 for x in list(range(1, len(dfrm.columns), 2)) ]
    ax2.set_xticks(ax2_ticks)
    ax2.set_xticklabels(graphL, rotation=0, ha='center')

    return axes


def rename_metric(x):
    x0 = x
    
    x0 = x0.replace("LLC Miss Count", "LLC Miss")
    x0 = x0.replace("Count", "")
    x0 = x0.replace("Access", "")

    return x0

    
def rename_col(x, graphL):
    x0 = x

    for g in graphL:
        x0 = x0.replace(g, "")
    
    x0 = x0.replace("grappolo-vtune-profile--optane-appdirect-", "")
    x0 = x0.replace("-pkg", "")
    
    return x0


#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
