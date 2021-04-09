#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys
#import argparse # https://docs.python.org/3/library/argparse.html

import copy

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

from dataclasses import dataclass


#****************************************************************************

# FIXME:
# - Better weighted average for averaging function rows

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

@dataclass
class PlotData:
    is_group_beg:  bool
    group_nm:      str
    dfrm_col_grpL: tuple
    dfrm:          pandas.DataFrame()


#****************************************************************************
#
#****************************************************************************

def main():

    #seaborn.set_style({'font.family': 'serif'})
    #seaborn.set(font='Times New Roman') # Cambria not available

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
        ('Memory Bound:L2 Bound(%)', 'L2/1 Bound (%)', vtcsv.makeCol_Sum('Memory Bound:L1 Bound(%)') ),
        ('Stores',   'Stores (%)',   vtcsv.makeCol_pctOfOther('Loads') ),
    ]

    makeColL_g2 = [
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_MEM_ANY', 'All Mem Stalls', vtcsv.makeCol_Sum('Hardware Event Count:EXE_ACTIVITY.BOUND_ON_STORES') ),
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L2_MISS', 'L3 Stalls', vtcsv.makeCol_Diff('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L3_MISS') ),
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L1D_MISS', 'L2 Stalls', vtcsv.makeCol_Diff('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L2_MISS') ), # ???
        ('Hardware Event Count:CYCLE_ACTIVITY.STALLS_MEM_ANY', 'L1 Stalls', vtcsv.makeCol_Diff('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L1D_MISS') ),
        ('L3 Stalls', 'Cache Stalls', vtcsv.makeCol_Sum(['L1 Stalls', 'L2 Stalls']) ), # L3...L1

        ('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.LOCAL_DRAM_PS', '$L$DRAM+PMM Ld', vtcsv.makeCol_Sum('Hardware Event Count:MEM_LOAD_RETIRED.LOCAL_PMM_PS') ),
        ('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.REMOTE_DRAM_PS', '$R$DRAM+PMM Ld', vtcsv.makeCol_Sum('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.REMOTE_PMM_PS') ),

        ('Hardware Event Count:MEM_LOAD_RETIRED.L1_HIT_PS', 'L1...L3 Hits', vtcsv.makeCol_Sum(['Hardware Event Count:MEM_LOAD_RETIRED.L2_HIT_PS', 'Hardware Event Count:MEM_LOAD_RETIRED.L3_HIT_PS']) ),

        ('Hardware Event Count:MEM_LOAD_RETIRED.LOCAL_PMM_PS', 'DRAM+PMM', vtcsv.makeCol_Sum(['Hardware Event Count:OCR.ALL_READS.L3_MISS_LOCAL_DRAM.ANY_SNOOP', 'Hardware Event Count:OCR.ALL_READS.L3_MISS_REMOTE_HOP1_DRAM.ANY_SNOOP', 'Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.REMOTE_PMM_PS']) ),
    ]
    
    makeColL_r1 = [
        ('CPU Time', 'CPU Time (s)', makeCol_wallclock(64) ),
        makeColL_g1[1],
        makeColL_g1[2],
        #('Memory Bound:L2 Bound(%)',  'L2/1 Bound (%)', makeCol_L2xBound('Memory Bound:L1 Bound(%)') ),
        #('Stores',   'Stores (%)',   vtcsv.makeCol_pctOfOther('Loads') ),
    ]

    makeColL_r2 = copy.deepcopy(makeColL_g2)
    makeColL_r2.pop() # remove 'DRAM+PMM'
    
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
    
    global metricLf_g
    metricLf_g = [
        #------------------------
        # hotspots
        #------------------------
        [(makeColL_g1[0][1] ,),  # ('CPU Time'),
         ],

        #('Average Latency (cycles)',    'Latency (cycles)'),
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

        #------------------------
        # stalls
        #------------------------
        #(makeColL_g2[0][1] ,), # 'All Mem Stalls'

        [('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L3_MISS', 'Mem Stalls'),
         #(makeColL_g2[1][1] ,), # 'L3 Stalls'
         #(makeColL_g2[2][1] ,), # 'L2 Stalls'
         #(makeColL_g2[3][1] ,), # 'L1 Stalls'
         (makeColL_g2[4][1] ,),  # 'Cache Stalls'
         #(makeColL_g2[7][1] ,),  # 'L1...L3 Hits'
         ('Hardware Event Count:OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO',  'RFO Cycles'),
         ],

        #------------------------
        # hw-events
        #------------------------
        [('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.LOCAL_DRAM_PS', '$L$DRAM Ld'),
         ('Hardware Event Count:MEM_LOAD_RETIRED.LOCAL_PMM_PS', '$L$PMM Ld'),
         #(makeColL_g2[5][1] ,), # '$L$DRAM+PMM Ld'
         #('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.REMOTE_DRAM_PS', 'Rmt DRAM'),
         (makeColL_g2[6][1] ,), # '$R$DRAM+PMM Ld'

         #(makeColL_g2[8][1] ,),  # 'DRAM+PMM'
         
         #('Hardware Event Count:MEM_LOAD_RETIRED.L1_HIT_PS',  'L1 Hit'),
         #('Hardware Event Count:MEM_LOAD_RETIRED.L2_HIT_PS',  'L2 Hit'),
         #('Hardware Event Count:MEM_LOAD_RETIRED.L3_HIT_PS',  'L3 Hit'),
         #('Hardware Event Count:MEM_LOAD_RETIRED.L3_MISS_PS', 'L3 Miss'),
         ]
        
        #('Hardware Event Count:EXE_ACTIVITY.BOUND_ON_STORES',  'Store Stalls'),
    ]

    global metricLf_g2
    metricLf_g2 = copy.deepcopy(metricLf_g)
    grp0 = metricLf_g2[-1] # end group
    m0 = grp0.pop() # remove end metric
    m1 = grp0.pop() # remove end metric+1
    grp0.append(m0) # recover end metric


    global metricLf_r
    metricLf_r = [ # metricL1.copy()
        #------------------------
        # hotspots
        #------------------------
        [(makeColL_r1[0][1] ,),  #('CPU Time'),
         ],

        #
        #('Average Latency (cycles)',    'Latency (cycles)'),
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

        #------------------------
        # stalls
        #------------------------
        #(makeColL_g2[0][1] ,), # All Mem Stalls'

        [('Hardware Event Count:CYCLE_ACTIVITY.STALLS_L3_MISS', 'Mem Stalls'),
         #(makeColL_g2[1][1] ,), # 'L3 Stalls'
         #(makeColL_g2[2][1] ,), # 'L2 Stalls'
         #(makeColL_g2[3][1] ,), # 'L1 Stalls'
         (makeColL_g2[4][1] ,),  # 'Cache Stalls'
         ('Hardware Event Count:OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO',  'RFO Cycles'),
         ],

        #------------------------
        # hw-events
        #------------------------
        [#('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.LOCAL_DRAM_PS',  '$L$DRAM Ld'),
         #('Hardware Event Count:MEM_LOAD_RETIRED.LOCAL_PMM_PS',           '$L$PMM Ld'),

         #('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.REMOTE_DRAM_PS', '$R$DRAM Ld'),
         #('Hardware Event Count:MEM_LOAD_L3_MISS_RETIRED.REMOTE_PMM_PS',  '$R$PMM Ld'),

         (makeColL_g2[5][1] ,), # '$L$DRAM+PMM Ld'
         (makeColL_g2[6][1] ,), # '$R$DRAM+PMM Ld'
         ]
        
        #('Hardware Event Count:EXE_ACTIVITY.BOUND_ON_STORES',  'Store Stalls'),
    ]

    
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

    graph_sfx = ['-t192-dram', '-t192-dram2', '-t192-mem', '-t192-kdax'] # '-t192-mem2', '-t192-pdax'

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

    graph_sfx = ['-t192-mem', '-t192-mem2', '-t192-kdax', '-t192-kdax2']

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
    vt_f = vtcsv.VTuneCSV(pathL_f1, group_by = 'csv', makeColL = makeColL1)
    vt_f1 = vtcsv.VTuneCSV(pathL_f2, group_by = 'csv', makeColL = makeColL2)

    vt_f.merge(vt_f1)
    

    adjHx = { 'left':0.05, 'right':0.99, 'bottom':0.10, 'top':0.75,
              'wspace':0.15, 'hspace':0.0 }

    plotHp = {'w':2.6, 'h':1.7, 'title':1, 'ctitle':1, 'ctitle_bot':1}
    adjHp = { 'left':0.15, 'right':0.95, 'bottom':0.15, 'top':0.85,
              'wspace':0.10, 'hspace':0.0 }

    fig_p1 = plot_pkg(vt_p, graphL, [metricLp[0]], {**plotHp}, adjHp)
    fig_p2 = plot_pkg(vt_p, graphL, [metricLp[1]], {**plotHp}, adjHp)
    fig_px = plot_pkg(vt_p, graphL, metricLx, {'w':3.0, 'h':1.8}, adjHx)

    plotHf = {'w':4.5, 'h':1.5, 'title':0, 'ctitle':0, 'ctitle_bot':0}
    adjHf = { 'left':0.15, 'right':0.98, 'bottom':0.15, 'top':0.85,
              'wspace':0.05, 'hspace':0.0 } # 'ytitle'

    fig_f1 = plot_fn(vt_f, graphL1, funcH, metricLf_g2, {**plotHf, 'ctitle':1}, adjHf)
    fig_f2 = plot_fn(vt_f, graphL2, funcH, metricLf_g2, {**plotHf, 'ctitle_bot':1}, adjHf)
    fig_f3 = plot_fn(vt_f, graphL3, funcH, metricLf_g, {**plotHf, 'ctitle':1, 'h':1.4, 'txt_rot':0}, adjHf)
    fig_f4 = plot_fn(vt_f, graphL4, funcH, metricLf_g, {**plotHf, 'h':1.4, 'ctitle_bot':1, 'txt_rot':0}, adjHf)

    fig_fx = plot_fn(vt_f, graphL, funcH, metricLx, {'w':3.2, 'h':2.7, 'ctitle_bot':1}, adjHx)

    #fig_f1 = plot_fn(vt_f, graphL, funcH, [metricL1[0]], {'w':3.2, 'h':2.7, 'ctitle_bot':False}, adjH)

    fig_p1.savefig('chart-grappolo-pkg1.pdf', bbox_inches='tight')
    fig_p2.savefig('chart-grappolo-pkg2.pdf', bbox_inches='tight')

    fig_f1.savefig('chart-grappolo-fn1.pdf', bbox_inches='tight')
    fig_f2.savefig('chart-grappolo-fn2.pdf', bbox_inches='tight')
    fig_f3.savefig('chart-grappolo-fn3.pdf', bbox_inches='tight')
    fig_f4.savefig('chart-grappolo-fn4.pdf', bbox_inches='tight')

    

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
                 '.imm-kdax2.T64',
                 '.imm-kdax.T64',
                 '.imm-kdax3.T64']

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
    vt_f = vtcsv.VTuneCSV(pathL_f1, group_by = 'csv', makeColL = makeColL1)
    vt_f1 = vtcsv.VTuneCSV(pathL_f2, group_by = 'csv', makeColL = makeColL2)

    vt_f.merge(vt_f1)
    
    adjHx = { 'left':0.05, 'right':0.99, 'bottom':0.15, 'top':0.75,
              'wspace':0.15, 'hspace':0.0 }

    plotHp = {'w':2.7, 'h':1.6, 'title':1, 'ctitle':1, 'ctitle_bot':1}
    adjHp = { 'left':0.15, 'right':0.95, 'bottom':0.15, 'top':0.85,
              'wspace':0.10, 'hspace':0.0 }

    fig_p1 = plot_pkg(vt_p, graphL, [metricLp[0]], {**plotHp}, adjHp)
    fig_p2 = plot_pkg(vt_p, graphL, [metricLp[1]], {**plotHp}, adjHp)
    fig_px = plot_pkg(vt_p, graphL, metricLx, {'w':2.6, 'h':1.6}, adjHx)


    plotHf = {'w':5.3, 'h':2.0, 'title':0, 'ctitle':0, 'ctitle_bot':0}
    adjHf = { 'left':0.15, 'right':0.98, 'bottom':0.15, 'top':0.90,
              'wspace':0.05, 'hspace':0.0 } # 'ytitle'

    fig_f1 = plot_fn(vt_f, graphL1, funcH, metricLf_r, {**plotHf, 'ctitle':1}, adjHf)
    fig_f2 = plot_fn(vt_f, graphL2, funcH, metricLf_r, {**plotHf, 'ctitle':1}, adjHf)
    fig_f3 = plot_fn(vt_f, graphL3, funcH, metricLf_r, {**plotHf, 'title':1}, adjHf)
    fig_f4 = plot_fn(vt_f, graphL4, funcH, metricLf_r, {**plotHf, 'ctitle':1, 'ctitle_bot':1}, adjHf)
    fig_f5 = plot_fn(vt_f, graphL5, funcH, metricLf_r, {**plotHf, 'ctitle_bot':1, 'h':1.8, 'txt_rot':0}, adjHf)

    # fig_f1 = plot_fn(vt_f, graphL, funcH, [metricL1[0]], {'w':3.2, 'h':2.7, 'ctitle_bot':False}, adjH)

    fig_fx = plot_fn(vt_f, graphL, funcH, metricLx, {'w':2.7, 'h':2.3, 'ctitle_bot':1}, adjHx)
    
    fig_p1.savefig('chart-ripples-pkg1.pdf', bbox_inches='tight')
    fig_p2.savefig('chart-ripples-pkg2.pdf', bbox_inches='tight')

    fig_f1.savefig('chart-ripples-fn1.pdf', bbox_inches='tight')
    fig_f2.savefig('chart-ripples-fn2.pdf', bbox_inches='tight')
    fig_f3.savefig('chart-ripples-fn3.pdf', bbox_inches='tight')
    fig_f4.savefig('chart-ripples-fn4.pdf', bbox_inches='tight')
    fig_f5.savefig('chart-ripples-fn5.pdf', bbox_inches='tight')

    

#****************************************************************************

def plot_pkg(vt, graph_grpL, metricL, plotH, adjustH):

    dataL = plotL_selectNcfg(vt, 'Socket', metricL, graph_grpL, plotH,
                             dfrm_pkg_xform(graph_grpL))
    fig, axesL = plotL_do(dataL, plotH)
    plotL_adj(fig, adjustH)

    return fig


def dfrm_pkg_xform(graph_grpL):

    def dfrm_pkg_xform1(dfrm, graph_grp, metric):
        # 'dfrm': frame with down-selected columns
        # 'metric' is *original/full* metric name
        
        # 1. Reorder/rename rows
        dfrm.rename(columns = (lambda x: rename_col(x, graph_grpL)), inplace=True)

        # 2. Reorder/rename rows
        dfrm.sort_index(axis=0, ascending=True, inplace=True)
        dfrm.rename(index = (lambda x: x.replace('package_', '')), inplace=True)
        
        return dfrm

    return dfrm_pkg_xform1
    

#****************************************************************************

def plot_fn(vt, graph_grpL, functionH, metricL, plotH, adjustH):

    dataL = plotL_selectNcfg(vt, 'Functions', metricL, graph_grpL, plotH,
                             dfrm_fn_xform(vt, functionH, graph_grpL))
    fig, axesL = plotL_do(dataL, plotH)
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
        # 'dfrm': frame with down-selected columns
        # 'metric' is *original/full* metric name

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

def plotL_selectNcfg(vt, ytitle, metricL, graph_grpL, plotH, dfrm_xformF):
    """
    select-and-configure
    """

    dataL = []

    n_graph_grp = len(graph_grpL)

    # if one graph group of length 1, orders is graph then metrics
    do_graph_metric = (n_graph_grp == 1) and (len(graph_grpL[0]) == 1)

    plotL_title = None

    #-------------------------------------------------------
    # for each graph, show metrics
    #
    # * metricL: is a list of metric groups *
    #-------------------------------------------------------
    if (do_graph_metric):

        grph_grp0 = graph_grpL[0]
        grph_pr = grph_grp0[0]

        grph_nm = grph_pr[1] if (isinstance(grph_pr, tuple)) else grph_pr

        plotL_title = grph_nm

        for metric_grp in metricL:

            dfrm_colL = []
            dfrm_grp = None

            n_metric = len(metric_grp)
            for i_m in range(n_metric):
                
                is_m_grp_beg = (i_m == 0)

                metric_pair = metric_grp[i_m]
                m_nm_full = metric_pair[0]
                m_nm = metric_pair[1] if (len(metric_pair) > 1) else m_nm_full

                dfrm = select_data(vt, m_nm_full, grph_grp0, dfrm_xformF)

                dfrm_colL.append(m_nm)
                if (is_m_grp_beg):
                    dfrm_grp = dfrm
                else:
                    dfrm_grp = pandas.concat([dfrm_grp, dfrm], axis=1)

            dataL.append(PlotData(is_m_grp_beg, None, dfrm_colL, dfrm_grp))


    #-------------------------------------------------------
    # for each metric, show graphs
    #-------------------------------------------------------
    else:

        n_metric = len(metricL)
        
        metric_nm0 = None

        if (n_metric == 1):
            plotL_title = metric_nm0
        else:
            plotL_title = ytitle
        
        for i_m in range(n_metric):
            for i_g in range(n_graph_grp):

                is_grp_beg = (i_g == 0)
                
                metric_pair = metricL[i_m]
                m_nm_full = metric_pair[0]
                m_nm = metric_pair[1] if (len(metric_pair) > 1) else m_nm_full
                if (i_m == 0): metric_nm0 = m_nm

                grph_grp = graph_grpL[i_g] # graphL
                #print(grph_grp)

                dfrm = select_data(vt, m_nm_full, grph_grp, dfrm_xformF)

                dataL.append(PlotData(is_grp_beg, m_nm, grph_grp, dfrm))

                
    #-------------------------------------------------------
    # Configure plot options
    #-------------------------------------------------------

    # plot list title
    if (not ('ytitle' in plotH)):
        plotH['ytitle'] = plotL_title
    
    # DataFrame group title
    if (not ('title' in plotH)):
        plotH['title'] = True

    # DataFrame column titles (top)
    if (not ('ctitle' in plotH)):
        plotH['ctitle'] = True

    # DataFrame column titles (bottom)
    if (not ('ctitle_bot' in plotH)):
        plotH['ctitle_bot'] = True

            
    return dataL


def plotL_do(dataL, plotH):
    """
    dataL: list of PlotData
    """

    fig, axesL = plotL_mkFig(dataL, plotH)

    for i_data in range(len(dataL)):

        data = dataL[i_data]
        axes = axesL[i_data]

        is_grp_beg = data.is_group_beg
        group_nm = data.group_nm
        col_grpL = data.dfrm_col_grpL
        dfrm = data.dfrm

        ytitle = plotH['ytitle'] if (i_data == 0) else None
        xtitle = group_nm if (plotH['title'] and is_grp_beg) else None

        axes.margins(x=0.00, y=0.00)
        axes1 = plot(dfrm, axes, ytitle, xtitle, col_grpL, plotH)


    return fig, axesL


def plotL_mkFig(dataL, plotH):

    n_axes = len(dataL)
    widthL = []

    for x in dataL:
        n_col = len(x.dfrm.columns)

        g_title_w = 0
        #g_title_w = 2 if (i_g == 0) else 0

        widthL.append(g_title_w + n_col + Fixed_cmap_w)

    #-----------------------------------

    w = plotH['w']
    h = plotH['h']

    if (Do_rows):
        fig, axesL = pyplt.subplots(nrows=1, ncols=(n_axes),
                                    figsize=(w * n_axes, h),
                                    #squeeze=False,
                                    gridspec_kw={'width_ratios': widthL})
    else:
        # FIXME: ncol = num_groups
        fig, axesL = pyplt.subplots(nrows=(n_axes), ncols=1,
                                    figsize=(w, h * n_axes),
                                    #squeeze=False,
                                    gridspec_kw={'width_ratios': widthL})

    if (n_axes == 1): # squeeze=True
        axesL = numpy.array([axesL])

    return (fig, axesL)


def plotL_adj(fig, adjustH):

    fig.subplots_adjust(**adjustH)

    if (Do_view):
        # Changes 'subplots_adjust'!
        fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)


def plot(dfrm, axes, ytitle, xtitle, col_groupL, plotH):

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
        dfrm = dfrm.applymap( lambda x: round(x / dfrm_scale, 2) )
        txt_fmt = '.3g'
        #txt_sz = Txt_sz_heatmap + 1
        txt_rot = plotH['txt_rot'] if ('txt_rot' in plotH) else 10

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    do_y_lbl = True if (ytitle) else False

    cbar_frac = 0.16 if (n_col <= 4) else 0.08
    cbar_pad  = 0.05 if (n_col <= 4) else 0.02


    # vmin, vmax
    # fmt: cf. str.format() documentation (https://docs.python.org/3/library/string.html?highlight=string#formatspec)
    #  '.2%': percent with 2 decimal places

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

    # exponent over colorbar
    if (dfrm_scale_exp):
        axes.text(0.96, 0.997, (r'$\times10^{%s}$' % dfrm_scale_exp),
                   transform=axes.transAxes, ha='left', va='bottom') # size=Txt_sz_heatmap_scale
        
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    if (ytitle):
        axes.set_ylabel(ytitle, fontsize=Txt_sz_ytitle)

    if (xtitle):
        axes.set_title(xtitle, ha='center', fontsize=Txt_sz_title) # va='center', rotation='vertical', x=x_pos, y=0.5


    # correct x-ticks and x-labels
    axes.set_xticks(numpy.arange(0.5, n_col))

    if ('ctitle_bot' in plotH and plotH['ctitle_bot']):
        # correct x-ticks and x-labels
        axes.set_xticklabels(dfrm.columns, rotation=20, ha='right')
    else:
        axes.set_xticklabels([])

    #for x in axes.get_xticklabels():
    #    x.set_rotation(0)


    #-------------------------------------------------------
    # Secondary x groups and labels (col_groupL)
    #-------------------------------------------------------
    if (col_groupL):
        # if col_groupL is a list of pairs, grab second item in each pair
        nmL = [ x[1] for x in col_groupL ] if (isinstance(col_groupL[0], tuple)) else col_groupL

        (x_beg, x_end) = axes.get_xlim()
        n_x = int(x_end) # n_col
        n_x2 = len(col_groupL)
        x2_skip = int(n_x / n_x2)
        x2_beg = x2_skip / 2.0 # midpoint

        g_beg = x2_skip
        axes.vlines(list(range(g_beg, n_x, x2_skip)), *axes.get_ylim(), colors='white', linewidths=1.0)

        axes2 = axes.twiny() # twin y
        axes2_ticks = [ (x/n_x) for x in list(numpy.arange(x2_beg, x_end, x2_skip)) ]
        axes2.set_xticks(axes2_ticks)

        if ('ctitle' in plotH and plotH['ctitle']):
            axes2.set_xticklabels(nmL, rotation=0, ha='center')
        else:
            axes2.set_xticklabels([])


    return axes


#****************************************************************************

def select_data(vt, metric_nm_full, graphL, dfrm_xformF):
    """
    - graphL is a grph_grp
    """

    # find DataFrame for 'metric_nm_full'
    try:
        dfrm = vt.dataH[metric_nm_full]
    except KeyError:
        vtcsv.MSG.warnx("Skipping metric: '{}'".format(metric_nm_full))
        return pandas.DataFrame()

    # select columns for 'graphL'
    dfrm = select_dfrm_col(dfrm, graphL) # new copy
    #print(dfrm)

    dfrm = dfrm_xformF(dfrm, graphL, metric_nm_full)

    return dfrm

    
def select_dfrm_col(dfrm, graphL):
    """
    - graphL is a grph_grp
    - returns a *copy*
    """
    
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
