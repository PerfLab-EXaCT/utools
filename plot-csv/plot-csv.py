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

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    # 'CPU Time'
    # 'Memory Bound(%)'
    # 'Memory Bound:L1 Bound(%)'
    # 'Memory Bound:L2 Bound(%)'
    # 'Memory Bound:L3 Bound(%)'
    # 'Memory Bound:DRAM Bound(%)'
    # 'Memory Bound:Store Bound(%)'
    # 'Memory Bound:Persistent Memory Bound(%)'
    # 'Loads'
    # 'Stores'
    # 'LLC Miss Count'
    # 'LLC Miss Count:Local DRAM Access Count'
    # 'LLC Miss Count:Remote DRAM Access Count'
    # 'LLC Miss Count:Local Persistent Memory Access Count'
    # 'LLC Miss Count:Remote Persistent Memory Access Count'
    # 'LLC Miss Count:Remote Cache Access Count'
    # 'Average Latency (cycles)'

    
    pathL1 = [
        'grappolo-vtune-profile-friendster-optane-appdirect-dram-pkg.csv',
        'grappolo-vtune-profile-friendster-optane-appdirect-pmem-pkg.csv' ]

    csv1 = vtcsv.VTuneCSV(csv_pathL1, group_by = 'csv')

    pathL2 = [
        'grappolo-vtune-profile-friendster-optane-appdirect-dram-pkg.csv',
        'grappolo-vtune-profile-friendster-optane-appdirect-pmem-pkg.csv' ]

    csv2 = vtcsv.VTuneCSV(csv_pathL2, group_by = 'csv')
    
    

    pathL = [
        'grappolo-vtune-profile-friendster-optane-appdirect-dram-fn.csv',
        'grappolo-vtune-profile-friendster-optane-appdirect-pmem-fn.csv' ]


# grappolo-vtune-profile-moliere2016-optane-appdirect-dram-fn.csv
# grappolo-vtune-profile-moliere2016-optane-appdirect-dram-pkg.csv
# grappolo-vtune-profile-moliere2016-optane-appdirect-pmem-fn.csv
# grappolo-vtune-profile-moliere2016-optane-appdirect-pmem-pkg.csv
# grappolo-vtune-profile-orkut-optane-appdirect-dram-fn.csv
# grappolo-vtune-profile-orkut-optane-appdirect-dram-pkg.csv
# grappolo-vtune-profile-orkut-optane-appdirect-pmem-fn.csv
# grappolo-vtune-profile-orkut-optane-appdirect-pmem-pkg.csv
    
    csv_pathL = [ './data0/progression/108544.csv',
                  './data0/progression/1696.csv',
                  './data0/progression/1736704.csv',
                  './data0/progression/27136.csv',
                  './data0/progression/434176.csv',
                  './data0/progression/6784.csv',
                  './data0/progression/6946816.csv' ]

    fnL = [ 'buildLocalMapCounter',
            'std::_Rb_tree_insert_and_rebalance',
            'max',
            '_int_free',
            '_int_malloc',
            '_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>',
            '__GI___libc_malloc',
            '__gnu_cxx::new_allocator<double>::construct<double, double const&>',
            'plm_analyzeClusters$omp$parallel_for@64' ]

    colL = [ 'Memory Bound:L1 Bound(%)',
             'Memory Bound:L2 Bound(%)',
             'Memory Bound:L3 Bound(%)',
             'Memory Bound:DRAM Bound(%)',
             'Memory Bound:Store Bound(%)',
             'Memory Bound:Persistent Memory Bound(%)']

    col2 = [ 'Loads',
             'Stores',
             'LLC Miss Count']

    csv = vtcsv.VTuneCSV(csv_pathL, group_by = 'metric', indexL = fnL, columnL = colL)
    plot(kind='heat')
    plt.show()


#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())