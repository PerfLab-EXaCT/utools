#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys
#import argparse # https://docs.python.org/3/library/argparse.html

import re
import collections

import functools
import operator

import pandas
import numpy
import math

import matplotlib.pyplot as pyplt
import matplotlib.patches as patches
import seaborn

import VTuneCSV as vtcsv

#****************************************************************************

# FIXME:
# - when averaging function rows, should weight by cpu-time
# - metric grouping

#****************************************************************************

txt_sz_heatmap = 10
txt_sz_heatmap_scale = 10
fixed_cmap_w = 2

Do_view = 0 # resets 'subplots_adjust'
Do_rows = 1

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
    # Make new columns in 'vtcsv'
    #-------------------------------------------------------

    makeColL_g = [
        ('CPU Time', 'CPU Time (s)', makeCol_wallclock(192) ),
        ('Stores',   'Stores (%)',   vtcsv.makeCol_pctOfOther('Loads') ),
    ]

    makeColL_r = [
        ('CPU Time', 'CPU Time (s)', makeCol_wallclock(64) ),
        ('Stores',   'Stores (%)',   vtcsv.makeCol_pctOfOther('Loads') ),
        #makeColL_g[1],
    ]

    #-------------------------------------------------------
    # Metrics: Locally map old -> new names
    #-------------------------------------------------------

    global metricL1
    metricL1 = [ # metricL1.copy()
        (makeColL_g[0][1] ,),  #('CPU Time'),
        #
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #
        ('Memory Bound(%)',),
        ('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        ('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        ('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        #('Memory Bound:Store Bound(%)', 'Store Bound (%)'),
    ]

    global metricL2
    metricL2 = [
        #('Memory Bound:Persistent Memory Bound(%)', 'Pmem Bound (%)'),
        
        (makeColL_g[1][1] ,),  #('Stores (%)',),
        #('Loads',),
        #('Stores',),
        
        #('LLC Miss Count', 'LLC Miss'),
        ('LLC Miss Count:Remote DRAM Access Count', 'LLC Miss:Remote DRAM'),
        ('LLC Miss Count:Local DRAM Access Count',  'LLC Miss:Local DRAM'),
        #('LLC Miss Count:Local Persistent Memory Access Count', 'LLC Miss:Local Pdax'),
        #('LLC Miss Count:Remote Persistent Memory Access Count', 'LLC Miss:Remote Pdax'),
        ('LLC Miss Count:Remote Cache Access Count', 'LLC Miss:Remote Cache'),
        ]

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    main_grappolo(makeColL_g)
    main_ripples (makeColL_r)

    pyplt.show()

    
def main_grappolo(makeColL):

    path_pfx = './1grappolo/grappolo-'

    #-------------------------------------------------------
    # Medium graphs (192 threads)/All memory modes
    #-------------------------------------------------------

    # grappolo-<graph>-<type>-pkg.csv
    # grappolo-<graph>-<type>-fn.csv

    graphL_med = ['friendster',
                  'moliere2016']

    graph_sfx = ['-t192-dram',
                 '-t192-mem',
                 '-t192-kdax',
                 '-t192-pdax']

    pathL_Mp = [
        [ (path_pfx + grph + sfx + '-pkg.csv') for sfx in graph_sfx ]
        for grph in graphL_med ]

    pathL_Mp = flattenL(pathL_Mp)


    pathL_Mf = [
        [ (path_pfx + grph + sfx + '-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_med ]

    pathL_Mf = flattenL(pathL_Mf)

    
    #-------------------------------------------------------
    # Big graphs (192 threads)/Big memory modes
    #-------------------------------------------------------

    graphL_big = [ ('clueweb12', 'clueweb'),
                   ('uk2014', 'uk') ]

    graphL_0 = [ x[0] for x in graphL_big ]


    pathL_Bp = [
        [path_pfx + grph + '-t192-mem-pkg.csv',
         path_pfx + grph + '-t192-kdax-pkg.csv'] for grph in graphL_0 ]

    pathL_Bp = flattenL(pathL_Bp)
    
    pathL_Bf = [
        [path_pfx + grph + '-t192-mem-fn.csv',
         path_pfx + grph + '-t192-kdax-fn.csv'] for grph in graphL_0 ]

    pathL_Bf = flattenL(pathL_Bf)

    #-------------------------------------------------------

    graphL = [ graphL_med, graphL_big ]
    
    pathL_p = pathL_Mp + pathL_Bp

    pathL_f = pathL_Mf + pathL_Bf
    
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    functionH = collections.OrderedDict( [
        ('buildLocalMapCounter', 'blmc'),

        ('std::_Rb_tree_insert_and_rebalance', 'map'),

        ('max', 'max'),

        ('_int_free', 'mem'), # 'free'
        ('__GI___libc_malloc', 'mem'), # 'malloc2'
        ('_int_malloc', 'mem'), # 'malloc'
        ('malloc_consolidate', 'mem'),

        #('__gnu_cxx::new_allocator<double>::construct<double, double const&>', 'new'),

        ('parallelLouvianMethod$omp$parallel_for@237', 'plm'),
        ('plm_analyzeClusters$omp$parallel_for@64', 'plm'), # 'plm2'
        
        ('_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>', 'omp'),

        # OLD
        #('duplicateGivenGraph$omp$parallel_for@171', 'copy'),
        #('duplicateGivenGraph$omp$parallel_for@152', 'copy'),

        ('[vmlinux]', 'kernel'),
    ] )

    #functionL = list(functionH.items())

    
    #-------------------------------------------------------
    # graphs
    #-------------------------------------------------------

    vt_p = vtcsv.VTuneCSV(pathL_p, group_by = 'csv', makeColL = makeColL)
    vt_f = vtcsv.VTuneCSV(pathL_f, group_by = 'csv', makeColL = makeColL)

    adjustH = { 'left':0.05, 'right':0.95, 'bottom':0.10, 'top':0.80,
                'wspace':0.10, 'hspace':0.0 }

    fig_p1 = plot_pkg(vt_p, graphL, [metricL1[1]], adjustH, w=2.7, h=1.8)
    fig_p2 = plot_pkg(vt_p, graphL, [metricL1[2]], adjustH, w=2.7, h=1.8)
    fig_px = plot_pkg(vt_p, graphL, metricL2, adjustH, w=3.0, h=1.8)
    
    fig_f1 = plot_fn(vt_f, graphL, functionH, [metricL1[0]], adjustH, 3.2, 2.7)
    fig_f2 = plot_fn(vt_f, graphL, functionH, [metricL1[1]], adjustH, 3.2, 2.7)
    fig_f3 = plot_fn(vt_f, graphL, functionH, [metricL1[3]], adjustH, 3.2, 2.7)
    fig_f4 = plot_fn(vt_f, graphL, functionH, [metricL1[4]], adjustH, 3.2, 2.7)
    fig_f5 = plot_fn(vt_f, graphL, functionH, [metricL1[5]], adjustH, 3.2, 2.7)
    fig_f6 = plot_fn(vt_f, graphL, functionH, [metricL1[6]], adjustH, 3.2, 2.7)
    fig_f7 = plot_fn(vt_f, graphL, functionH, [metricL2[0]], adjustH, 3.2, 2.7)
    
    fig_fx = plot_fn(vt_f, graphL, functionH, metricL2, adjustH, 3.2, 2.7)

    fig_p1.savefig('chart-grappolo-pkg1.pdf', bbox_inches='tight')
    fig_p1.savefig('chart-grappolo-pkg2.pdf', bbox_inches='tight')

    fig_f1.savefig('chart-grappolo-fn1.pdf', bbox_inches='tight')
    fig_f2.savefig('chart-grappolo-fn2.pdf', bbox_inches='tight')
    fig_f3.savefig('chart-grappolo-fn3.pdf', bbox_inches='tight')
    fig_f4.savefig('chart-grappolo-fn4.pdf', bbox_inches='tight')
    fig_f5.savefig('chart-grappolo-fn5.pdf', bbox_inches='tight')
    fig_f6.savefig('chart-grappolo-fn6.pdf', bbox_inches='tight')
    fig_f7.savefig('chart-grappolo-fn7.pdf', bbox_inches='tight')



def main_ripples(makeColL):

    #-------------------------------------------------------
    # Ripples
    #-------------------------------------------------------

    path_pfx = './2ripples/'

    # <graph>.imm-<type>.T64.R0-pkg.csv
    # <graph>.imm-<type>.T64.R0-fn.csv

    graphL = [ [('soc-Slashdot0902', 'slash'),
                ('soc-twitter-combined', 'twitter'),
                ('wiki-talk', 'talk') ],
               [('soc-pokec-relationships', 'pokec'),
                ('wiki-topcats', 'topcats') ] ]

    graphL_0 = [ x[0] for x in flattenL(graphL) ]

    graph_sfx = ['.imm-dram.T64.R0',
                 '.imm-mem.T64.R0',
                 '.imm-kdax.T64.R0']


    pathL_p = [
        [ (path_pfx + grph + sfx + '-pkg.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]

    # [
    #     [path_pfx + x + '.imm-dram.T64.R0-pkg.csv',
    #      path_pfx + x + '.imm-kdax.T64.R0-pkg.csv'] for x in graphL_0 ]

    pathL_p = flattenL(pathL_p)

    pathL_f = [
        [ (path_pfx + grph + sfx + '-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]

    # [
    #     [path_pfx + x + '.imm-dram.T64.R0-fn.csv',
    #      path_pfx + x + '.imm-kdax.T64.R0-fn.csv'] for x in graphL_0 ]

    pathL_f = flattenL(pathL_f)

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    functionH = collections.OrderedDict( [
        ('ripples::AddRRRSet<ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>, trng::lcg64, ripples::independent_cascade_tag>', 'AddRRR'),

        ('ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>::neighbors', 'neigh'),

        # move_merge (int*) [FIX: SHARED]
        ('std::__move_merge<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),
        ('std::__move_merge<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),
        #
        # move_merge (it) 
        ('std::__move_merge<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),
        ('std::__move_merge<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),
        #
        ('std::__move_merge_adaptive_backward<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),
        ('std::__move_merge_adaptive_backward<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),
        #
        ('std::__move_merge_adaptive<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),
        ('std::__move_merge_adaptive<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'mv_mrg'),

        # operator++ [FIX: SHARED]
        ('__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>::operator++', 'op'),
        ('__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>::operator++', 'op'),
        #
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>', 'op'),
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>', 'op'),
        #
        ('__gnu_cxx::__ops::_Val_less_iter::operator()<unsigned int, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>', 'op'),
        ('__gnu_cxx::__ops::_Val_less_iter::operator()<unsigned int, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>', 'op'),
        # operator< 
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>', 'op'),
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>', 'op'),
        #
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, unsigned int*>', 'op'),
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, unsigned int*>', 'op'),
        #
        ('std::__unguarded_linear_insert<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Val_less_iter>', 'op'),
        ('std::__unguarded_linear_insert<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Val_less_iter>', 'op'),
        #
        ('std::__copy_move_backward<(bool)1, (bool)1, std::random_access_iterator_tag>::__copy_move_b<unsigned int>', 'op'),
        
        # [FIX: SHARED]
        ('trng::lcg64::step', 'trng'),
        ('trng::utility::u01xx_traits<float, (unsigned long)1, trng::lcg64>::addin', 'trng'),
        ('trng::utility::u01xx_traits<float, (unsigned long)1, trng::lcg64>::co', 'trng'),
        
        # [FIX: SHARED]
        ('ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>::Neighborhood::Neighborhood', 'xtra'), # 'neigh-hood'
        # push_back
        ('std::vector<unsigned int, std::allocator<unsigned int>>::push_back', 'xtra'), # 'push_back'
        ('std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>::push_back', 'xtra'), # 'push_back'
        # count
        ('ripples::CountOccurrencies<__gnu_cxx::__normal_iterator<std::vector<unsigned int, std::allocator<unsigned int>>*, std::vector<std::vector<unsigned int, std::allocator<unsigned int>>, std::allocator<std::vector<unsigned int, std::allocator<unsigned int>>>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>._omp_fn.12', 'xtra'), # 'count'
        ('ripples::CountOccurrencies<__gnu_cxx::__normal_iterator<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>*, std::vector<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>, std::allocator<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>._omp_fn.12', 'xtra'), # 'count'
        #
        ('std::allocator<unsigned int>::construct<unsigned int, unsigned int>', 'xtra'),
        ('libmemkind::static_kind::allocator<unsigned int>::construct<unsigned int, unsigned int>', 'xtra'),
        #
        ('std::allocator<unsigned int>::construct<unsigned int, unsigned int const&>', 'xtra'),
        ('libmemkind::static_kind::allocator<unsigned int>::construct<unsigned int, unsigned int const&>', 'xtra'),
        #
        ('std::__insertion_sort<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'xtra'),
        ('std::__insertion_sort<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'xtra'),
        #
        ('__memmove_avx_unaligned_erms', 'xtra'),
        ('std::vector<bool, std::allocator<bool>>::operator[]', 'xtra'),
        ('__GI___libc_malloc', 'xtra'),
        ('_int_free', 'xtra'),

        # DRAM
        # 'unlink_chunk'

        # omp [FIX: SHARED]
        ('func@0x1d6d0', 'omp'), # 'omp/lock'
        ('func@0x1d860', 'omp'), # 'omp/reduce'
        ('func@0xa7d0', 'omp'), # 

        ('[vmlinux]', 'kernel'),
    ] )


    #functionL = list(functionH.items())

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    vt_p = vtcsv.VTuneCSV(pathL_p, group_by = 'csv', makeColL = makeColL)
    vt_f = vtcsv.VTuneCSV(pathL_f, group_by = 'csv', makeColL = makeColL)

    adjustH = { 'left':0.05, 'right':0.95, 'bottom':0.10, 'top':0.80,
                'wspace':0.10, 'hspace':0.0 }

    fig_p1 = plot_pkg(vt_p, graphL, [metricL1[1]], adjustH, w=2.6, h=1.8)
    fig_p2 = plot_pkg(vt_p, graphL, [metricL1[2]], adjustH, w=2.6, h=1.8)
    fig_px = plot_pkg(vt_p, graphL, metricL2, adjustH, w=3.0, h=1.8)

    fig_f1 = plot_fn(vt_f, graphL, functionH, [metricL1[0]], adjustH, 3.2, 2.7)
    fig_f2 = plot_fn(vt_f, graphL, functionH, [metricL1[1]], adjustH, 3.2, 2.7)
    fig_f3 = plot_fn(vt_f, graphL, functionH, [metricL1[3]], adjustH, 3.2, 2.7)
    fig_f4 = plot_fn(vt_f, graphL, functionH, [metricL1[4]], adjustH, 3.2, 2.7)
    fig_f5 = plot_fn(vt_f, graphL, functionH, [metricL1[5]], adjustH, 3.2, 2.7)
    fig_f6 = plot_fn(vt_f, graphL, functionH, [metricL1[6]], adjustH, 3.2, 2.7)
    fig_f7 = plot_fn(vt_f, graphL, functionH, [metricL2[0]], adjustH, 3.2, 2.7)
    fig_fx = plot_fn(vt_f, graphL, functionH, metricL2, adjustH, 3.2, 2.7)
    
    fig_p1.savefig('chart-ripples-pkg1.pdf', bbox_inches='tight')
    fig_p1.savefig('chart-ripples-pkg2.pdf', bbox_inches='tight')

    fig_f1.savefig('chart-ripples-fn1.pdf', bbox_inches='tight')
    fig_f2.savefig('chart-ripples-fn2.pdf', bbox_inches='tight')
    fig_f3.savefig('chart-ripples-fn3.pdf', bbox_inches='tight')
    fig_f4.savefig('chart-ripples-fn4.pdf', bbox_inches='tight')
    fig_f5.savefig('chart-ripples-fn5.pdf', bbox_inches='tight')
    fig_f6.savefig('chart-ripples-fn6.pdf', bbox_inches='tight')
    fig_f7.savefig('chart-ripples-fn7.pdf', bbox_inches='tight')
    

#****************************************************************************

def plot_pkg(vt, graph_grpL, metricL, adjustH, w, h):

    fig, axesL = plotL_mk(vt, metricL, w, h, graph_grpL)
    plotL_do(vt, fig, axesL, metricL, dfrm_pkg_xform(graph_grpL), 'Socket', graph_grpL)
    plotL_adj(fig, adjustH)

    return fig


def dfrm_pkg_xform(graph_grpL):
    def dfrm_pkg_xform1(dfrm, metric):
        dfrm.sort_index(axis=0, ascending=True, inplace=True)
        dfrm.rename(index = (lambda x: x.replace('package_', '')), inplace=True)
        dfrm.rename(columns = (lambda x: rename_col(x, graph_grpL)), inplace=True)
        return dfrm
    return dfrm_pkg_xform1
    

#****************************************************************************

def plot_fn(vt, graph_grpL, functionH, metricL, adjustH, w, h):
    
    fig, axesL = plotL_mk(vt, metricL, w, h, graph_grpL)
    plotL_do(vt, fig, axesL, metricL, dfrm_fn_xform(functionH, graph_grpL), 'Functions', graph_grpL)
    plotL_adj(fig, adjustH)

    return fig

    
def dfrm_fn_xform(functionH, graph_grpL):
    def dfrm_fn_xform1(dfrm, metric):
        #functionH_key = functionH.keys()
        #dfrm = dfrm.loc[functionH_key]
        #dfrm.rename(index = functionH, inplace=True)
        #dfrm.rename(columns = (lambda x: rename_col(x, graph_grpL)), inplace=True)

        # N.B.: functionH can map multiple keys to same target function

        # 1. Unique target names from functionH, in original order
        functionHx = { x : None for x in functionH.values() }
        functionHx_keys = functionHx.keys()

        # 2. Rename columns
        dfrm.rename(columns = (lambda x: rename_col(x, graph_grpL)), inplace=True)

        # 3. Rename rows
        dfrm.rename(index = functionH, inplace=True)

        # 4. Select and merge rows with same target name
        if (metric.find('(%)') > 0):
            # FIXME: should be mean, weighted by cpu time
            rowL = [ dfrm.loc[ [fn] ].mean(axis=0).to_frame().transpose()
                     for fn in functionHx_keys ]
        else:
            rowL = [ dfrm.loc[ [fn] ].sum(axis=0).to_frame().transpose()
                     for fn in functionHx_keys ]
        #print(rowL)

        # Create row for everything else???: pandas.Index.difference
        
        dfrm1 = pandas.concat(rowL, axis=0)
        dfrm1.index = functionHx_keys
        #print(dfrm1)
        
        return dfrm1

    return dfrm_fn_xform1

    
#****************************************************************************

def plotL_mk(vt, metricL, w, h, graph_grpL):
    num_metric = len(metricL)

    grp_per_metric = len(graph_grpL)

    num_axes = num_metric * grp_per_metric
    #print("axes:", num_axes)

    # width_ratios are proportional to 'select_dfrm_col'
    widthL = plotL_mk_widths(vt, metricL, graph_grpL)
    #print("widthL:", widthL)

    if (Do_rows):
        fig, axesL = pyplt.subplots(nrows=1, ncols=(num_axes),
                                    figsize=(w * num_axes, h),
                                    gridspec_kw={'width_ratios': widthL})
    else:
        # FIXME: ncol = num_groups
        fig, axesL = pyplt.subplots(nrows=(num_axes), ncols=1,
                                    figsize=(w, h * num_axes),
                                    gridspec_kw={'width_ratios': widthL})

    return (fig, axesL)


def plotL_mk_widths(vt, metricL, graph_grpL):
    widthL = []

    grp_per_metric = len(graph_grpL)

    num_metric = len(metricL)
    for i_m in range(num_metric):
        for i_g in range(grp_per_metric):
            graph_grp = graph_grpL[i_g]

            metricPair = metricL[i_m]

            g_title_w = 0
            #g_title_w = 2 if (i_g == 0) else 0

            # find DataFrame for 'metricPair'
            try:
                dfrm = vt.dataH[metricPair[0]]
            except KeyError:
                vtcsv.MSG.warnx(("Skipping metric: '%s'" % metricPair[0]))
                widthL.append(1)
                continue

            n_col = find_fig_width(dfrm, graph_grp)
            widthL.append(g_title_w + n_col + fixed_cmap_w)

    return widthL


def plotL_do(vt, fig, axesL, metricL, dfrm_xformF, ytitle_txt, graph_grpL):

    grp_per_metric = len(graph_grpL)
    
    num_metric = len(metricL)
    for i_m in range(num_metric):

        for i_g in range(grp_per_metric):

            graph_grp = graph_grpL[i_g]
        
            axes_i = (i_m * grp_per_metric) + i_g

            axes = axesL[axes_i]

            metricPair = metricL[i_m]
            metric0 = metricPair[0]

            do_title = (i_g == 0)
            ytitle = ytitle_txt if (i_m == 0 and i_g == 0) else None

            # find DataFrame for 'metricPair'
            try:
                dfrm = vt.dataH[metric0]
            except KeyError:
                vtcsv.MSG.warnx(("Skipping metric: '%s'" % metric0))
                continue

            # select columns for 'graph_grp'
            dfrm = select_dfrm_col(dfrm, graph_grp)
            #print(dfrm)
            #sys.exit()

            dfrm = dfrm_xformF(dfrm, metric0)

            axes.margins(x=0.00, y=0.00)
            axes1 = plot(dfrm, axes, metricPair, do_title, ytitle, graph_grp)

            # # FIXME:
            # #print(axes1.get_tightbbox(fig.canvas.get_renderer()))
            # bbox = axes1.bbox.get_points()
            # #print(bbox)
            # bbox_w = bbox[1][0] - bbox[0][0]
            # bbox_h = bbox[1][1] - bbox[0][1]
            # axes1.add_patch(patches.Rectangle(xy=bbox[0], width=bbox_w, height=bbox_h, edgecolor='red', linewidth=2.0, fill=True, zorder=100))


def plotL_adj(fig, adjustH):

    fig.subplots_adjust(**adjustH)

    if (Do_view):
        # Changes 'subplots_adjust'!
        fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)


def plot(dfrm, axes, metricPair, do_title, ytitle, x_groupL = None):

    n_col = len(dfrm.columns)
    
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

    cbar_frac = 0.16 if (n_col <= 4) else 0.08
    cbar_pad  = 0.05 if (n_col <= 4) else 0.02
    
    axes = seaborn.heatmap(dfrm, ax=axes, annot=True,
                           cbar=True,
                           cmap='RdBu_r',# coolwarm
                           fmt=txt_fmt,
                           yticklabels=do_y_lbl,
                           annot_kws= {'size':txt_sz, 'rotation':txt_rot},
                           cbar_kws = dict(fraction=cbar_frac, pad=cbar_pad))
                           # use_gridspec=False location='right'


    # adjust colorbar
    cbar_ax = axes.collections[0].colorbar.ax # get_axes()
    cbar_ax.set_yticklabels(cbar_ax.get_yticklabels(), rotation=270, va='center')

    if (dfrm_scale_exp):
        axes.text(1.06, 0.997, (r'$\times10^{%s}$' % dfrm_scale_exp),
                   transform=axes.transAxes, ha='left', va='bottom') # size=txt_sz_heatmap_scale
    
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    do_ytitle = (not Do_rows) or ytitle
    
    if (do_ytitle):
        axes.set_ylabel(ytitle)

    if (do_title):
        title_txt = metricPair[1] if (len(metricPair) > 1) else metricPair[0]
        #x_pos = -0.4 if (do_ytitle) else -0.08
        axes.set_title(title_txt, ha='center') # va='center', rotation='vertical', x=x_pos, y=0.5

    # correct x-ticks and x-labels
    axes.set_xticks(numpy.arange(0.5, n_col))
    axes.set_xticklabels(dfrm.columns, rotation=20, ha='right')

    #for x in axes.get_xticklabels():
    #    x.set_rotation(0)

    #-------------------------------------------------------
    # Secondary x groups and labels (x_groupL)
    #-------------------------------------------------------
    if (x_groupL):
        # if x_groupL is a list of pairs, grab second item in each pair
        nmL = [ x[1] for x in x_groupL ] if (isinstance(x_groupL[0], tuple)) else x_groupL

        (x_beg, x_end) = axes.get_xlim()
        n_x = int(x_end) # n_col
        n_x2 = len(x_groupL)
        x2_skip = int(n_x / n_x2)
        x2_beg = x2_skip / 2.0 # midpoint

        g_beg = x2_skip
        axes.vlines(list(range(g_beg, n_x, x2_skip)), *axes.get_ylim(), colors='white', linewidths=1.0)

        axes2 = axes.twiny() # twin y
        axes2_ticks = [ (x/n_x) for x in list(numpy.arange(x2_beg, x_end, x2_skip)) ]
        axes2.set_xticks(axes2_ticks)
        axes2.set_xticklabels(nmL, rotation=0, ha='center')


    return axes

#****************************************************************************

def find_fig_width(dfrm, graphL):
    colL = dfrm.columns

    beg_i, beg_col = find_beg_col(colL, graphL)
    end_i, end_col = find_end_col(colL, graphL)

    return (end_i - beg_i) + 1


def select_dfrm_col(dfrm, graphL):
    colL = dfrm.columns

    beg_i, beg_col = find_beg_col(colL, graphL)
    end_i, end_col = find_end_col(colL, graphL) # beg_i + len(graphL)
    #print(beg_col, end_col)
    
    return dfrm.loc[:, beg_col : end_col]


def find_beg_col(columnL, graphL):
    for i_col in range(len(columnL)):
        for g in graphL:
            g_nm = g[0] if (isinstance(g, tuple)) else g
            col_nm = columnL[i_col]
            if (col_nm.find(g_nm) >= 0):
                return (i_col, col_nm)
    return (0, columnL[0])


def find_end_col(columnL, graphL):
    for i_col in reversed(range(len(columnL))):
        for g in graphL:
            g_nm = g[0] if (isinstance(g, tuple)) else g
            col_nm = columnL[i_col]
            if (col_nm.find(g_nm) >= 0):
                return (i_col, col_nm)
    return (len(columnL) - 1, columnL[-1])


def rename_col(x, graph_grpL):
    x0 = x

    graphL = flattenL(graph_grpL)
    
    for g_nm in graphL:
        g_nm = g_nm[0] if (isinstance(g_nm, tuple)) else g_nm
        x0 = x0.replace(g_nm, '')

    x0 = x0.replace('grappolo--', '') # not a typo!
    x0 = x0.replace('t192-', '')

    # ripples
    x0 = x0.replace('.imm-', '') # not a typo!
    x0 = re.sub('\.T\d+\.R0', '', x0) #x0 = x0.replace('.T64.R0', '')

    # both
    x0 = x0.replace('-pkg', '')
    x0 = x0.replace('-fn', '')
    
    return x0

#****************************************************************************

def makeCol_wallclock(n_threads):

    def mk_fn(dfrm, col_src):
        dfrm_dst = dfrm[col_src] / n_threads
        return dfrm_dst
        
    return mk_fn


def flattenL(L):
    #return [x for L_inner in L for x in L_inner ] # flatten
    return functools.reduce(operator.concat, L)

#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
