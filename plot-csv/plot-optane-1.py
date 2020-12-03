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

# Move this row merging ability to VTuneCSV
MergeRows_nosum_metricPat = vtcsv.MergeRows_nosum_metricPat
MergeRows_nosum_metricPat_st = r'stores (%)'

MergeRows_nosum_scaleMetric = 'CPU Time'
MergeRows_nosum_scaleMetric_st = 'Stores'

Txt_sz_title = 11.5
Txt_sz_ytitle = 13
Txt_sz_heatmap = 10
Txt_sz_heatmap_scale = 10
Fixed_cmap_w = 2

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

    makeColL_g1 = [
        ('CPU Time', 'CPU Time (s)', makeCol_wallclock(192) ),
        ('Memory Bound:L2 Bound(%)', 'L2/1 Bound (%)', makeCol_Sum('Memory Bound:L1 Bound(%)') ),
        ('Stores',   'Stores (%)',   vtcsv.makeCol_pctOfOther('Loads') ),
    ]

    makeColL_g2 = [
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_MEM_ANY', 'All Mem Stalls', makeCol_Sum('Hardware Event Count:EXE_ACTIVITY.BOUND_ON_STORES') ),
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L2_MISS', 'L3 Stalls', makeCol_Diff('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L3_MISS') ),
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L1D_MISS', 'L2 Stalls', makeCol_Diff('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L2_MISS') ),
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_MEM_ANY', 'L1 Stalls', makeCol_Diff('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L1D_MISS') ),
        ('L2 Stalls', 'L2/L1 Stalls', makeCol_Sum('L1 Stalls') ),
    ]
    
    makeColL_r1 = [
        ('CPU Time', 'CPU Time (s)', makeCol_wallclock(64) ),
        makeColL_g1[1],
        makeColL_g1[2],
        #('Memory Bound:L2 Bound(%)',  'L2/1 Bound (%)', makeCol_L2xBound('Memory Bound:L1 Bound(%)') ),
        #('Stores',   'Stores (%)',   vtcsv.makeCol_pctOfOther('Loads') ),
    ]

    makeColL_r2 = makeColL_g2.copy()

    #-------------------------------------------------------
    # Metrics: Locally map old -> new names
    #-------------------------------------------------------

    global metricLp
    metricLp = [
        #(makeColL_g1[0][1] ,),  #('CPU Time'),
        #
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #
        ('Memory Bound(%)',),
        #('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        #('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        #('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        #('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),

        #(makeColL_g1[1][1] ,),  #('Stores (%)',),
        #('Memory Bound:Store Bound(%)', 'Store Bound (%)'),
    ]
    
    global metricLf_g1
    metricLf_g1 = [
        (makeColL_g1[0][1] ,),  # ('CPU Time'),
        #
        ('Average Latency (cycles)',    'Latency (cycles)'),
        ##
        #('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        #('Memory Bound:Persistent Memory Bound(%)', 'Pmem Bound (%)'),
        ##('Memory Bound(%)',),
        #('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        #(makeColL_g1[1][1] ,),  #('L2/1 Bound (%)'),
        ##('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ##('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),

        ##(makeColL_g1[2][1] ,),  #('Stores (%)',),
        ##('Memory Bound:Store Bound(%)', 'Store Bound (%)'),
    ]

    global metricLf_g2
    metricLf_g2 = [
        #(makeColL_g2[0][1] ,), # ('All Mem Stalls'),
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L3_MISS', 'Mem Stalls'),
        (makeColL_g2[1][1] ,), # ('L3 Stalls'),
        (makeColL_g2[2][1] ,), # ('L2 Stalls'),
        (makeColL_g2[3][1] ,), # ('L1 Stalls'),
        #(makeColL_g2[4][1] ,), # ('L2/L1 Stalls'),
        #('Hardware Event Count:EXE_ACTIVITY.BOUND_ON_STORES',  'Store Stalls'),
    ]


    global metricLf_r1
    metricLf_r1 = [ # metricL1.copy()
        (makeColL_r1[0][1] ,),  #('CPU Time'),
        #
        ('Average Latency (cycles)',    'Latency (cycles)'),
        ##
        ##('Memory Bound(%)',),
        #('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        #('Memory Bound:Persistent Memory Bound(%)', 'Pmem Bound (%)'),
        ##('LLC Miss Count:Local DRAM Access Count',  'LLC Miss:Lcl DRAM'),
        ##('LLC Miss Count:Remote DRAM Access Count', 'LLC Miss:Rmt DRAM'),
        ##('LLC Miss Count:Local Persistent Memory Access Count', 'LLC Miss:Lcl PMEM'),
        ##('LLC Miss Count:Remote Persistent Memory Access Count', 'LLC Miss:Rmt PMEM'),
        #('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        #(makeColL_r1[1][1] ,),  #('L2/1 Bound (%)'),
        ##
        ##('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ##('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        ##
        ##(makeColL_r1[2][1] ,),  #('Stores (%)',),
    ]

    global metricLf_r2
    metricLf_r2 = metricLf_g2.copy()

    
    global metricLx
    metricLx = [
        ('Loads',),
        ('Stores',),

        ('LLC Miss Count', 'LLC Miss'),
        #('LLC Miss Count:Remote DRAM Access Count', 'LLC Miss:Remote DRAM'),
        #('LLC Miss Count:Local DRAM Access Count',  'LLC Miss:Local DRAM'),
        #('LLC Miss Count:Local Persistent Memory Access Count', 'LLC Miss:Local Pdax'),
        #('LLC Miss Count:Remote Persistent Memory Access Count', 'LLC Miss:Remote Pdax'),
        #('LLC Miss Count:Remote Cache Access Count', 'LLC Miss:Remote Cache'),
        ]

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    pyplt.rcParams.update({'figure.max_open_warning': 0})

    main_grappolo(makeColL_g1, makeColL_g2)
    main_ripples (makeColL_r1, makeColL_r2)

    pyplt.show()

    
def main_grappolo(makeColL1, makeColL2):

    path_pfx = './1grappolo/grappolo-'

    #-------------------------------------------------------
    # Grappolo, Medium graphs, 192 threads, *all* memory modes
    #-------------------------------------------------------

    # grappolo-<graph>-<type>-pkg.csv
    # grappolo-<graph>-<type>-fn.csv

    graphL1 = [ [ 'friendster' ] ]
    graphL2 = [ [ 'moliere2016' ] ]
    graphL3 = [ [ ('clueweb12', 'clueweb') ] ]
    graphL4 = [ [ ('uk2014', 'uk') ] ]
    
    graphL_med = [graphL1[0][0],  # 'friendster'
                  graphL2[0][0] ] # 'moliere2016'

    graph_sfx = ['-t192-dram', '-t192-mem', '-t192-kdax', '-t192-pdax']

    pathL_Mp = [
        [ (path_pfx + grph + sfx + '-hotspots-pkg.csv') for sfx in graph_sfx ]
        for grph in graphL_med ]
    pathL_Mp = flattenL(pathL_Mp)

    pathL_Mf1 = [
        [ (path_pfx + grph + sfx + '-hotspots-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_med ]
    pathL_Mf1 = flattenL(pathL_Mf1)

    pathL_Mf2 = [
        [ (path_pfx + grph + sfx + '-hw-events-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_med ]
    pathL_Mf2 = flattenL(pathL_Mf2)


    # (path_pfx + grph + sfx + '-hw-events-fn.csv')
    
    #-------------------------------------------------------
    # Grappolo, Big graphs, 192 threads, *big* memory modes
    #-------------------------------------------------------

    graphL_big = [ graphL3[0][0],  # ('clueweb12', 'clueweb'),
                   graphL4[0][0] ] # ('uk2014', 'uk')

    graphL_0 = [ x[0] for x in graphL_big ]

    graph_sfx = ['-t192-mem', '-t192-kdax']

    pathL_Bp = [
        [ (path_pfx + grph + sfx + '-hotspots-pkg.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]

    pathL_Bp = flattenL(pathL_Bp)
    
    pathL_Bf1 = [
        [ (path_pfx + grph + sfx + '-hotspots-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]
    pathL_Bf1 = flattenL(pathL_Bf1)

    pathL_Bf2 = [
        [ (path_pfx + grph + sfx + '-hw-events-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]
    pathL_Bf2 = flattenL(pathL_Bf2)

    #-------------------------------------------------------

    graphL = [ graphL_med, graphL_big ]
    
    pathL_p = pathL_Mp + pathL_Bp

    pathL_f1 = pathL_Mf1 + pathL_Bf1
    pathL_f2 = pathL_Mf2 + pathL_Bf2

    
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    funcH = collections.OrderedDict( [
        ('buildLocalMapCounter', 'cmty'),
        ('std::_Rb_tree_insert_and_rebalance', 'cmty'),
        ('max', 'cmty'),

        ('sumVertexDegree$omp$parallel_for@74', 'vtx°'),

        ('parallelLouvianMethod$omp$parallel_for@210', 'louv'),
        ('parallelLouvianMethod$omp$parallel_for@237', 'louv'),
        ('plm_analyzeClusters$omp$parallel_for@64', 'louv'),

        ('__GI___libc_malloc', 'mem'), # 'malloc2'
        ('_int_free', 'mem'), # 'free'
        ('_int_malloc', 'mem'), # 'malloc'
        ('malloc_consolidate', 'mem'),
        ('__gnu_cxx::new_allocator<double>::construct<double, double const&>', 'mem'),

        ('_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>', 'omp'),
        ('_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>', 'omp'),

        # OLD
        #('duplicateGivenGraph$omp$parallel_for@171', 'copy'),
        #('duplicateGivenGraph$omp$parallel_for@152', 'copy'),

        #('[vmlinux]', 'kernel'),
    ] )

    #functionL = list(funcH.items())

    
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    vt_p = vtcsv.VTuneCSV(pathL_p, group_by = 'csv', makeColL = makeColL1)
    vt_f1 = vtcsv.VTuneCSV(pathL_f1, group_by = 'csv', makeColL = makeColL1)
    vt_f2 = vtcsv.VTuneCSV(pathL_f2, group_by = 'csv', makeColL = makeColL2)

    adjHx = { 'left':0.05, 'right':0.99, 'bottom':0.10, 'top':0.75,
              'wspace':0.15, 'hspace':0.0 }

    plotHp = {'w':2.6, 'h':1.7, 'title':1, 'xtitle_top':1, 'xtitle_bot':1}
    adjHp = { 'left':0.15, 'right':0.95, 'bottom':0.15, 'top':0.85,
              'wspace':0.10, 'hspace':0.0 }

    fig_p1 = plot_pkg(vt_p, graphL, [metricLp[0]], {**plotHp}, adjHp)
    fig_p2 = plot_pkg(vt_p, graphL, [metricLp[1]], {**plotHp}, adjHp)
    fig_px = plot_pkg(vt_p, graphL, metricLx, {'w':3.0, 'h':1.8}, adjHx)

    plotHf = {'w':2.3, 'h':1.5, 'title':0, 'xtitle_top':0, 'xtitle_bot':0}
    adjHf = { 'left':0.15, 'right':0.98, 'bottom':0.15, 'top':0.85,
              'wspace':0.13, 'hspace':0.0 }

    fig_f1a = plot_fn(vt_f1, graphL1, funcH, metricLf_g1, {**plotHf, 'title':1}, adjHf)
    fig_f1b = plot_fn(vt_f2, graphL1, funcH, metricLf_g2, {**plotHf, 'title':1, 'ytitle':0}, adjHf)
    
    fig_f2a = plot_fn(vt_f1, graphL2, funcH, metricLf_g1, {**plotHf, 'xtitle_bot':1}, adjHf)
    fig_f2b = plot_fn(vt_f2, graphL2, funcH, metricLf_g2, {**plotHf, 'xtitle_bot':1, 'ytitle':0}, adjHf)
    
    fig_f3a = plot_fn(vt_f1, graphL3, funcH, metricLf_g1, {**plotHf, 'h':1.4, 'txt_rot':0}, adjHf)
    fig_f3b = plot_fn(vt_f2, graphL3, funcH, metricLf_g2, {**plotHf, 'h':1.4, 'txt_rot':0, 'ytitle':0}, adjHf)
    
    fig_f4a = plot_fn(vt_f1, graphL4, funcH, metricLf_g1, {**plotHf, 'h':1.4, 'xtitle_bot':1, 'txt_rot':0}, adjHf)
    fig_f4b = plot_fn(vt_f2, graphL4, funcH, metricLf_g2, {**plotHf, 'h':1.4, 'xtitle_bot':1, 'txt_rot':0, 'ytitle':0}, adjHf)

    fig_fx = plot_fn(vt_f1, graphL, funcH, metricLx, {'w':3.2, 'h':2.7, 'xtitle_bot':1}, adjHx)

    #fig_f1 = plot_fn(vt_f1, graphL, funcH, [metricL1[0]], {'w':3.2, 'h':2.7, 'xtitle_bot':False}, adjH)

    fig_p1.savefig('chart-grappolo-pkg1.pdf', bbox_inches='tight')
    fig_p2.savefig('chart-grappolo-pkg2.pdf', bbox_inches='tight')

    fig_f1a.savefig('chart-grappolo-fn1a.pdf', bbox_inches='tight')
    fig_f1b.savefig('chart-grappolo-fn1b.pdf', bbox_inches='tight')
    fig_f2a.savefig('chart-grappolo-fn2a.pdf', bbox_inches='tight')
    fig_f2b.savefig('chart-grappolo-fn2b.pdf', bbox_inches='tight')
    fig_f3a.savefig('chart-grappolo-fn3a.pdf', bbox_inches='tight')
    fig_f3b.savefig('chart-grappolo-fn3b.pdf', bbox_inches='tight')
    fig_f4a.savefig('chart-grappolo-fn4a.pdf', bbox_inches='tight')
    fig_f4b.savefig('chart-grappolo-fn4b.pdf', bbox_inches='tight')

    

def main_ripples(makeColL1, makeColL2):

    #-------------------------------------------------------
    # Ripples, 64 threads, all memory modes
    #-------------------------------------------------------

    path_pfx = './2ripples/'

    # <graph>.imm-<type>.T64-pkg.csv
    # <graph>.imm-<type>.T64-fn.csv

    graphL1 = [ [ ('soc-Slashdot0902', 'slash') ] ]
    graphL2 = [ [ ('soc-twitter-combined', 'twitter') ] ]
    graphL3 = [ [ ('wiki-talk', 'talk') ] ]
    graphL4 = [ [ ('soc-pokec-relationships', 'pokec') ] ]
    graphL5 = [ [ ('wiki-topcats', 'topcats') ] ]
    
    graphL = [ [ graphL1[0][0],   # 'slash'
                 graphL2[0][0],   # 'twitter'
                 graphL3[0][0] ], # 'talk'
               [ graphL4[0][0] ], # 'pokec'
               [ graphL5[0][0] ]  # 'topcats'
    ]

    graphL_0 = [ x[0] for x in flattenL(graphL) ]

    graph_sfx = ['.imm-dram.T64',
                 '.imm-mem.T64',
                 '.imm-kdax1.T64',
                 '.imm-kdax2.T64']

    # 'topcats' has no dram
    mykeep = lambda x: not ('topcats' in x and 'dram' in x)

    pathL_p = [
        [ (path_pfx + grph + sfx + '-hotspots-pkg.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]
    pathL_p = list(filter(mykeep, flattenL(pathL_p) )) 

    pathL_f1 = [
        [ (path_pfx + grph + sfx + '-hotspots-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]
    pathL_f1 = list(filter(mykeep, flattenL(pathL_f1) ))

    pathL_f2 = [
        [ (path_pfx + grph + sfx + '-hw-events-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_0 ]
    pathL_f2 = list(filter(mykeep, flattenL(pathL_f2) ))

    
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    funcH = collections.OrderedDict( [
        # --------------------------------------
        # 
        ('ripples::AddRRRSet<ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>, trng::lcg64, ripples::independent_cascade_tag>', 'rrr'),
        #
        ('ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>::neighbors', 'rrr'), # optane
        #
        ('ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>::Neighborhood::Neighborhood', 'rrr'), # 'neigh-hood'
        #
        ('std::vector<unsigned int, std::allocator<unsigned int>>::push_back', 'rrr'), # 'push_back'
        ('std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>::push_back', 'rrr'), # 'push_back'
        #
        ('std::__insertion_sort<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr'),
        ('std::__insertion_sort<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr'),
        
        # --------------------------------------
        # Optane? [SHARED]
        # 'count'
        ('ripples::CountOccurrencies<__gnu_cxx::__normal_iterator<std::vector<unsigned int, std::allocator<unsigned int>>*, std::vector<std::vector<unsigned int, std::allocator<unsigned int>>, std::allocator<std::vector<unsigned int, std::allocator<unsigned int>>>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>._omp_fn.12', 'count'), # 'count'
        ('ripples::CountOccurrencies<__gnu_cxx::__normal_iterator<std::vector<unsigned int, std::allocator<unsigned int>>*, std::vector<std::vector<unsigned int, std::allocator<unsigned int>>, std::allocator<std::vector<unsigned int, std::allocator<unsigned int>>>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>._omp_fn.13', 'count'), # 'count'
        ('ripples::CountOccurrencies<__gnu_cxx::__normal_iterator<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>*, std::vector<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>, std::allocator<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>._omp_fn.12', 'count'), # 'count'
        ('ripples::CountOccurrencies<__gnu_cxx::__normal_iterator<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>*, std::vector<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>, std::allocator<std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>._omp_fn.13', 'count'), # 'count'

        # --------------------------------------
        # move_merge (int*) [FIX: SHARED]
        ('std::__move_merge<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),
        ('std::__move_merge<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),

        #
        # move_merge (it) 
        ('std::__move_merge<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),
        ('std::__move_merge<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),
        #
        ('std::__move_merge_adaptive_backward<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),
        ('std::__move_merge_adaptive_backward<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),
        #
        ('std::__move_merge_adaptive<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),
        ('std::__move_merge_adaptive<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'rrr-mv'),
        #
        ('std::__copy_move_backward<(bool)1, (bool)1, std::random_access_iterator_tag>::__copy_move_b<unsigned int>', 'rrr-mv'),
        ('__memmove_avx_unaligned_erms', 'mem'),

        
        # --------------------------------------
        # operator++ 
        ('__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>::operator++', 'rrr-op'),
        ('__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>::operator++', 'rrr-op'),
        #
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>', 'rrr-op'),
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>', 'rrr-op'),
        #
        ('__gnu_cxx::__ops::_Val_less_iter::operator()<unsigned int, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>', 'rrr-op'),
        ('__gnu_cxx::__ops::_Val_less_iter::operator()<unsigned int, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>', 'rrr-op'),
        # operator< 
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>>', 'rrr-op'),
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>>', 'rrr-op'),
        #
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, unsigned int*>', 'rrr-op'),
        ('__gnu_cxx::__ops::_Iter_less_iter::operator()<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, unsigned int*>', 'rrr-op'),
        #
        ('std::__unguarded_linear_insert<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Val_less_iter>', 'rrr-op'),
        ('std::__unguarded_linear_insert<__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Val_less_iter>', 'rrr-op'),
        ('std::vector<bool, std::allocator<bool>>::operator[]', 'rrr-op'),
        

        # --------------------------------------                
        # Optane [SHARED]
        #
        ('std::allocator<unsigned int>::construct<unsigned int, unsigned int>', 'mem'),
        ('libmemkind::static_kind::allocator<unsigned int>::construct<unsigned int, unsigned int>', 'mem'),
        ('libmemkind::static_kind::allocator<unsigned int>::construct<unsigned int, unsigned int&>', 'mem'),
        #
        ('std::allocator<unsigned int>::construct<unsigned int, unsigned int const&>', 'mem'),
        ('libmemkind::static_kind::allocator<unsigned int>::construct<unsigned int, unsigned int const&>', 'mem'),
        #
        ('clear_page_erms', 'mem'),
        ('__GI___libc_malloc', 'mem'),
        ('_int_free', 'mem'),

                
        # --------------------------------------
        # DRAM [SHARED]
        # 
        ('trng::lcg64::step', 'rand'),
        ('trng::utility::u01xx_traits<float, (unsigned long)1, trng::lcg64>::addin', 'rand'),
        ('trng::utility::u01xx_traits<float, (unsigned long)1, trng::lcg64>::co', 'rand'),
        
        
        # --------------------------------------
        # DRAM
        # 'unlink_chunk'

        # --------------------------------------
        # omp [SHARED]
        ('func@0x1d6d0', 'omp'), # 'omp/lock'
        ('func@0x1d860', 'omp'), # 'omp/reduce'
        ('func@0xa7d0', 'omp'), # 

        # --------------------------------------
        #('[vmlinux]', 'kernel'),
    ] )


    #functionL = list(funcH.items())

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    vt_p = vtcsv.VTuneCSV(pathL_p, group_by = 'csv', makeColL = makeColL1)
    vt_f1 = vtcsv.VTuneCSV(pathL_f1, group_by = 'csv', makeColL = makeColL1)
    vt_f2 = vtcsv.VTuneCSV(pathL_f2, group_by = 'csv', makeColL = makeColL2)

    adjHx = { 'left':0.05, 'right':0.99, 'bottom':0.15, 'top':0.75,
              'wspace':0.15, 'hspace':0.0 }

    plotHp = {'w':2.7, 'h':1.6, 'title':1, 'xtitle_top':1, 'xtitle_bot':1}
    adjHp = { 'left':0.15, 'right':0.95, 'bottom':0.15, 'top':0.85,
              'wspace':0.10, 'hspace':0.0 }

    fig_p1 = plot_pkg(vt_p, graphL, [metricLp[0]], {**plotHp}, adjHp)
    fig_p2 = plot_pkg(vt_p, graphL, [metricLp[1]], {**plotHp}, adjHp)
    fig_px = plot_pkg(vt_p, graphL, metricLx, {'w':2.6, 'h':1.6}, adjHx)


    plotHf = {'w':2.3, 'h':2.0, 'title':0, 'xtitle_top':0, 'xtitle_bot':0}
    adjHf = { 'left':0.15, 'right':0.98, 'bottom':0.15, 'top':0.90,
              'wspace':0.13, 'hspace':0.0 }

    fig_f1a = plot_fn(vt_f1, graphL1, funcH, metricLf_r1, {**plotHf, 'title':1}, adjHf)
    fig_f1b = plot_fn(vt_f2, graphL1, funcH, metricLf_r2, {**plotHf, 'title':1, 'ytitle':0}, adjHf)

    fig_f2a = plot_fn(vt_f1, graphL2, funcH, metricLf_r1, {**plotHf, 'title':1}, adjHf)
    fig_f2b = plot_fn(vt_f2, graphL2, funcH, metricLf_r2, {**plotHf, 'title':1, 'ytitle':0}, adjHf)

    fig_f3a = plot_fn(vt_f1, graphL3, funcH, metricLf_r1, {**plotHf, 'title':1}, adjHf)
    fig_f3b = plot_fn(vt_f2, graphL3, funcH, metricLf_r2, {**plotHf, 'title':1, 'ytitle':0}, adjHf)

    fig_f4a = plot_fn(vt_f1, graphL4, funcH, metricLf_r1, {**plotHf, 'xtitle_bot':1}, adjHf)
    fig_f4b = plot_fn(vt_f2, graphL4, funcH, metricLf_r2, {**plotHf, 'xtitle_bot':1, 'ytitle':0}, adjHf)

    fig_f5a = plot_fn(vt_f1, graphL5, funcH, metricLf_r1, {**plotHf, 'xtitle_bot':1, 'h':1.8, 'txt_rot':0}, adjHf)
    fig_f5b = plot_fn(vt_f2, graphL5, funcH, metricLf_r2, {**plotHf, 'xtitle_bot':1, 'h':1.8, 'txt_rot':0, 'ytitle':0}, adjHf)

    # fig_f1 = plot_fn(vt_f1, graphL, funcH, [metricL1[0]], {'w':3.2, 'h':2.7, 'xtitle_bot':False}, adjH)

    fig_fx = plot_fn(vt_f1, graphL, funcH, metricLx, {'w':2.7, 'h':2.3, 'xtitle_bot':1}, adjHx)
    
    fig_p1.savefig('chart-ripples-pkg1.pdf', bbox_inches='tight')
    fig_p2.savefig('chart-ripples-pkg2.pdf', bbox_inches='tight')

    fig_f1a.savefig('chart-ripples-fn1a.pdf', bbox_inches='tight')
    fig_f1b.savefig('chart-ripples-fn1b.pdf', bbox_inches='tight')
    
    fig_f2a.savefig('chart-ripples-fn2a.pdf', bbox_inches='tight')
    fig_f2b.savefig('chart-ripples-fn2b.pdf', bbox_inches='tight')
    
    fig_f3a.savefig('chart-ripples-fn3a.pdf', bbox_inches='tight')
    fig_f3b.savefig('chart-ripples-fn3b.pdf', bbox_inches='tight')

    fig_f4a.savefig('chart-ripples-fn4a.pdf', bbox_inches='tight')
    fig_f4b.savefig('chart-ripples-fn4b.pdf', bbox_inches='tight')

    fig_f5a.savefig('chart-ripples-fn5a.pdf', bbox_inches='tight')
    fig_f5b.savefig('chart-ripples-fn5b.pdf', bbox_inches='tight')

    

#****************************************************************************

def plot_pkg(vt, graph_grpL, metricL, plotH, adjustH):
    plot_cfg(plotH, graph_grpL, metricL, 'Socket')

    w = plotH['w']
    h = plotH['h']

    fig, axesL = plotL_mk(vt, metricL, w, h, graph_grpL)
    plotL_do(vt, fig, axesL, metricL, dfrm_pkg_xform(graph_grpL), graph_grpL, plotH)
    plotL_adj(fig, adjustH)

    return fig


def dfrm_pkg_xform(graph_grpL):

    def dfrm_pkg_xform1(dfrm, graph_grp, metric):
        # 1. Reorder/rename rows
        dfrm.rename(columns = (lambda x: rename_col(x, graph_grpL)), inplace=True)

        # 2. Reorder/rename rows
        dfrm.sort_index(axis=0, ascending=True, inplace=True)
        dfrm.rename(index = (lambda x: x.replace('package_', '')), inplace=True)
        
        return dfrm

    return dfrm_pkg_xform1
    

#****************************************************************************

def plot_fn(vt, graph_grpL, functionH, metricL, plotH, adjustH):
    plot_cfg(plotH, graph_grpL, metricL, 'Functions')
    
    w = plotH['w']
    h = plotH['h']

    fig, axesL = plotL_mk(vt, metricL, w, h, graph_grpL)
    plotL_do(vt, fig, axesL, metricL, dfrm_fn_xform(vt, functionH, graph_grpL), graph_grpL, plotH)
    plotL_adj(fig, adjustH)

    return fig

    
def dfrm_fn_xform(vt, functionH, graph_grpL):
    
    # N.B.: functionH can map multiple keys to same target function
    # 0. Unique target names from functionH, in original order
    functionHx = { x : None for x in functionH.values() }
    functionHx_keys = functionHx.keys()

    # 0. Capture times for weights
    dfrm_time = None
    dfrm_st = None
    try:
        # Note: before 'MergeRows_nosum_scaleMetric' has been renamed!
        dfrm_time = vt.dataH[MergeRows_nosum_scaleMetric]
        dfrm_st =   vt.dataH[MergeRows_nosum_scaleMetric_st]
    except KeyError:
        pass

    
    def dfrm_fn_xform1(dfrm, graph_grp, metric):
        # 'metric' is *original* metric name

        # 1. Rename columns/rows
        dfrm = dfrm.rename(columns = (lambda x: rename_col(x, graph_grpL)))
        dfrm.rename(index = functionH, inplace=True)

        # 2. Select and merge rows with same target name
        if (re.search(MergeRows_nosum_metricPat, metric)):

            if (dfrm_time is None):
                vtcsv.MSG.err(("Cannot find metric: '%s'" % MergeRows_nosum_scaleMetric))
            if (dfrm_st is None):
                vtcsv.MSG.err(("Cannot find metric: '%s'" % MergeRows_nosum_scaleMetric_st))
                
            
            # 0. Select weighting column for 'graph_grp' (FIXME)
            df_tm = select_dfrm_col(dfrm_time, graph_grp) # copies dfrm slice
            if (re.search(MergeRows_nosum_metricPat_st, metric, re.IGNORECASE)):
                df_tm = select_dfrm_col(dfrm_st, graph_grp) # copies dfrm slice

            # 1. Rename columns/rows
            df_tm.rename(columns = (lambda x: rename_col(x, graph_grpL)), inplace=True)
            df_tm.rename(index = functionH, inplace=True)
            
            # Merge by weighted average
            rowL = []
            for fn in functionHx_keys:
                df_tm_fn = df_tm.loc[ [fn] ]
                df_tm_sm = df_tm_fn.sum(axis=0).to_frame().transpose()
                #print("df_tm_fn\n", df_tm_fn)
                #print("df_tm_sm\n", df_tm_sm)
                
                # time, weighted by metric percentage
                df_fn = dfrm.loc[ [fn] ]
                df_wtm_fn = df_tm_fn * (df_fn / 100.0)
                df_wtm_sm = df_wtm_fn.sum(axis=0).to_frame().transpose()
                #print("df_fn/{}\n".format(metric), df_fn)
                #print("df_wtm_fn\n", df_wtm_fn)
                #print("df_wtm_sm\n", df_wtm_sm)
                
                # New: percentage of weighted time
                df = 100.0 * df_wtm_sm / df_tm_sm
                #print("df/{}\n".format(metric), df)
                
                # if ( (df_fn > 100).any().any() ):
                    
                rowL.append(df)
        else:
            # Merge by sum
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

def plot_cfg(plotH, graph_grpL, metricL, ytitle):

    if (not ('title' in plotH)):
        plotH['title'] = True

    if (not ('ytitle' in plotH)):
        # If one graph group of length 1...
        if ((len(graph_grpL) == 1) and (len(graph_grpL[0]) == 1)):
            g_pair = graph_grpL[0][0]
            plotH['ytitle'] = g_pair[1] if (isinstance(g_pair, tuple)) else g_pair
        # If one metric
        elif (len(metricL) == 1):
            m_pair = metricL[0]
            plotH['ytitle'] = m_pair[1] if (len(m_pair) > 1) else m_pair[0]
        else:
            plotH['ytitle'] = ytitle

    if (not ('xtitle_top' in plotH)):
        plotH['xtitle_top'] = True

    if (not ('xtitle_top' in plotH)):
        plotH['xtitle_bot'] = True

    

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
                                    #squeeze=False,
                                    gridspec_kw={'width_ratios': widthL})
    else:
        # FIXME: ncol = num_groups
        fig, axesL = pyplt.subplots(nrows=(num_axes), ncols=1,
                                    figsize=(w, h * num_axes),
                                    #squeeze=False,
                                    gridspec_kw={'width_ratios': widthL})

    if (num_axes == 1): # squeeze=True
        axesL = numpy.array([axesL])

    return (fig, axesL)


def plotL_mk_widths(vt, metricL, graph_grpL):
    widthL = []

    grp_per_metric = len(graph_grpL)
    #print(grp_per_metric)

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
            widthL.append(g_title_w + n_col + Fixed_cmap_w)

    return widthL


def plotL_do(vt, fig, axesL, metricL, dfrm_xformF, graph_grpL, plotH):

    grp_per_metric = len(graph_grpL)
    
    num_metric = len(metricL)
    for i_m in range(num_metric):

        for i_g in range(grp_per_metric):

            graph_grp = graph_grpL[i_g]
            #print(graph_grp)
        
            axes_i = (i_m * grp_per_metric) + i_g

            axes = axesL[axes_i]

            metricPair = metricL[i_m]
            metric0 = metricPair[0]

            do_title = (plotH['title'] and i_g == 0)
            ytitle = plotH['ytitle'] if (i_m == 0 and i_g == 0) else None

            # find DataFrame for 'metricPair'
            try:
                dfrm = vt.dataH[metric0]
            except KeyError:
                vtcsv.MSG.warnx(("Skipping metric: '%s'" % metric0))
                continue

            # select columns for 'graph_grp'
            dfrm = select_dfrm_col(dfrm, graph_grp)
            #print(dfrm)

            dfrm = dfrm_xformF(dfrm, graph_grp, metric0)

            axes.margins(x=0.00, y=0.00)
            axes1 = plot(dfrm, axes, metricPair, do_title, ytitle, graph_grp, plotH)

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


def plot(dfrm, axes, metricPair, do_title, ytitle, x_groupL, plotH):

    n_col = len(dfrm.columns)
    
    #-------------------------------------------------------
    # Scale data values for nice formattting
    #-------------------------------------------------------

    dfrm_scale_exp = None
    txt_fmt = '.2g'
    txt_sz = Txt_sz_heatmap
    txt_rot = 0

    dfrm_max = numpy.max(dfrm.to_numpy())
    #dfrm_md = numpy.median(dfrm.to_numpy())
    if (dfrm_max > 100):
        dfrm_scale_exp = math.floor(math.log10(dfrm_max)) - 2
        dfrm_scale = math.pow(10, dfrm_scale_exp)
        dfrm = dfrm.applymap(lambda x: x / dfrm_scale)
        txt_fmt = '.3g'
        #txt_sz = Txt_sz_heatmap + 1
        txt_rot = plotH['txt_rot'] if ('txt_rot' in plotH) else 10

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
                   transform=axes.transAxes, ha='left', va='bottom') # size=Txt_sz_heatmap_scale
        
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    do_ytitle = (not Do_rows) or ytitle
    
    if (do_ytitle):
        axes.set_ylabel(ytitle, fontsize=Txt_sz_ytitle)

    if (do_title):
        title_txt = metricPair[1] if (len(metricPair) > 1) else metricPair[0]

        if (title_txt != ytitle):
            #x_pos = -0.4 if (do_ytitle) else -0.08
            axes.set_title(title_txt, ha='center', fontsize=Txt_sz_title) # va='center', rotation='vertical', x=x_pos, y=0.5


    # correct x-ticks and x-labels
    axes.set_xticks(numpy.arange(0.5, n_col))

    if ('xtitle_bot' in plotH and plotH['xtitle_bot']):
        # correct x-ticks and x-labels
        axes.set_xticklabels(dfrm.columns, rotation=20, ha='right')
    else:
        axes.set_xticklabels([])

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

        if ('xtitle_top' in plotH and plotH['xtitle_top']):
            axes2.set_xticklabels(nmL, rotation=0, ha='center')
        else:
            axes2.set_xticklabels([])


    return axes

#****************************************************************************

def find_fig_width(dfrm, graphL):
    matchL = find_matches(dfrm.columns, graphL)
    return len(matchL)


def select_dfrm_col(dfrm, graphL):
    matchL = find_matches(dfrm.columns, graphL)
    if (not matchL):
        vtcsv.MSG.warnx(("No metrics for '%s'" % graphL))

    return dfrm[matchL].copy()


def find_matches(columnL, graphL):
    matchL = []
    
    for g in graphL:
        g_nm = g[0] if (isinstance(g, tuple)) else g

        matchL += [col for col in columnL if g_nm in col]
        # col_nm.find(g_nm) >= 0)

    return matchL


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
    x0 = re.sub('\.T\d+', '', x0) #x0 = x0.replace('.T64', '')

    # both
    x0 = x0.replace('-hotspots-pkg', '')
    x0 = x0.replace('-hotspots-fn', '')
    x0 = x0.replace('-hw-events-fn', '')
    
    return x0

#****************************************************************************

def makeCol_wallclock(n_threads):

    def mk_fn(dfrm, col_src):
        dfrm_dst = dfrm[col_src] / n_threads
        return dfrm_dst
        
    return mk_fn


def makeCol_Sum(col_src2): # could be a list of source columns

    def mk_fn(dfrm, col_src):
        dfrm_dst = dfrm[col_src] + dfrm[col_src2]
        return dfrm_dst

    return mk_fn


def makeCol_Diff(col_src2, is_pos = True): # could be a list of source columns

    def mk_fn(dfrm, col_src):
        dfrm_dst = dfrm[col_src] - dfrm[col_src2]
        if (is_pos):
            dfrm_dst = dfrm_dst.apply(lambda x: max(x, 0))

        return dfrm_dst

    return mk_fn


def flattenL(L):
    #return [x for L_inner in L for x in L_inner ] # flatten

    islist = map(lambda x: isinstance(x, list), L)
    if (all(islist)):
        L1 = functools.reduce(operator.concat, L) # flatten
        return flattenL(L1)
    else:
        return L

#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
