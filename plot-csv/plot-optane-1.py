#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys
#import argparse

import re
import collections

import functools
import operator

import pandas
import numpy
import math
import matplotlib.pyplot as pyplt
import seaborn

import VTuneCSV as vtcsv

#****************************************************************************

txt_sz_heatmap = 10
txt_sz_heatmap_scale = 10

Do_view = 1
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

    # makeColL_Gf = [ ('CPU Time', 'CPU Time (%)', vtcsv.makeCol_percent) ]
    # makeColL_Rf = makeColL_Gf

    makeColL_Gf = [ ('CPU Time', 'CPU Time (s)', makeCol_wallclock(192) ) ]
    makeColL_Rf = [ ('CPU Time', 'CPU Time (s)', makeCol_wallclock(64) ) ]
    assert(makeColL_Gf[0][1] == makeColL_Rf[0][1])

    #-------------------------------------------------------
    # Metrics: Locally map old -> new names
    #-------------------------------------------------------

    metricL1_p = [
        #('CPU Time'),
        #
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #
        ('Memory Bound(%)',),
        #('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        #('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        #('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        #('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        ('Memory Bound:Store Bound(%)', 'Store Bound (%)'),
        ]

    metricL1r_p = metricL1_p.copy()
    metricL1r_p.pop() # no 'Store Bound (%)'

    #-------------------------------------------------------
    
    metricL1_f = [
        #('CPU Time',),
        (makeColL_Gf[0][1] ,),
        #
        ('Average Latency (cycles)',    'Latency (cycles)'),
        #
        ]

    metricL2_f = [
        #('Memory Bound(%)',),
        ('Memory Bound:L1 Bound(%)',    'L1 Bound (%)'),
        ('Memory Bound:L2 Bound(%)',    'L2 Bound (%)'),
        ('Memory Bound:L3 Bound(%)',    'L3 Bound (%)'),
        ('Memory Bound:DRAM Bound(%)',  'DRAM Bound (%)'),
        ('Memory Bound:Store Bound(%)', 'Store Bound (%)'),
        ]

    metricL2r_f = metricL2_f.copy()
    metricL2r_f.pop() # no 'Store Bound (%)'

    #-------------------------------------------------------

    metricL3 = [
        #('Memory Bound:Persistent Memory Bound(%)', 'Pmem Bound (%)'),
        ('Loads',),
        ('Stores',),
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

    #main_grappolo(makeColL_Gf, metricL1_p, metricL1_f, metricL2_f, metricL3)
    main_ripples (makeColL_Rf, metricL1r_p, metricL1_f, metricL2r_f, metricL3)

    pyplt.show()

    
def main_grappolo(makeColL_f, metricL1_p, metricL1_f, metricL2_f, metricL3):

    path_pfx = './1grappolo/grappolo-'

    #-------------------------------------------------------
    # Medium graphs (192 threads)/All memory modes
    #-------------------------------------------------------

    # grappolo-<graph>-<type>-pkg.csv
    # grappolo-<graph>-<type>-fn.csv

    graphL_med = ['orkut', 'friendster', 'moliere2016']

    graph_sfx = ['-t192-dram',
                 '-t192-pdax',
                 '-t192-kdax',
                 '-t192-mem']

    pathL_Mp = [
        [ (path_pfx + grph + sfx + '-pkg.csv') for sfx in graph_sfx ]
        for grph in graphL_med ]

    pathL_Mp = flattenL(pathL_Mp)


    pathL_Mf = [
        [ (path_pfx + grph + sfx + '-fn.csv') for sfx in graph_sfx ]
        for grph in graphL_med ]

    pathL_Mf = flattenL(pathL_Mf)

    vtcsv.printRed("*** Warning: missing orkut-mem! ***")
    
    #-------------------------------------------------------
    # Big graphs (192 threads)/Big memory modes
    #-------------------------------------------------------

    graphL_big = ['clueweb12', 'uk2014']

    pathL_Bp = [
        [path_pfx + grph + '-t192-kdax-pkg.csv',
         path_pfx + grph + '-t192-mem-pkg.csv'] for grph in graphL_big ]

    pathL_Bp = flattenL(pathL_Bp)
    
    pathL_Bf = [
        [path_pfx + grph + '-t192-kdax-fn.csv',
         path_pfx + grph + '-t192-mem-fn.csv'] for grph in graphL_big ]

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
        ('parallelLouvianMethod$omp$parallel_for@237', 'plm'),
        ('std::_Rb_tree_insert_and_rebalance', 'blmc/map'),
        ('max', 'max'),
        ('_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>', 'omp'),
        ('duplicateGivenGraph$omp$parallel_for@171', 'copy'),
        ('[vmlinux]', 'kernel'),

        #('plm_analyzeClusters$omp$parallel_for@64', 'plm2'),
        #('_int_malloc', 'malloc'),
        #('__GI___libc_malloc', 'malloc2'),
        #('__gnu_cxx::new_allocator<double>::construct<double, double const&>', 'new'),
        #('_int_free',   'free'),
    ] )

    #functionL = list(functionH.items())

    
    #-------------------------------------------------------
    # Medium graphs
    #-------------------------------------------------------

    vt_p = vtcsv.VTuneCSV(pathL_p, group_by = 'csv')
    vt_f = vtcsv.VTuneCSV(pathL_f, group_by = 'csv', makeColL = makeColL_f)

    widthH_p = { 'width1':3.0, 'width2':3.0, 'height':1.8 }
    widthH_f = { 'width1':3.6, 'width2':3.3, 'height':2.7 } # h=2.7,1.8
    adjustH = { 'left':0.02, 'right':0.98, 'bottom':0.01, 'top':0.99,
                'wspace':0.00, 'hspace':0.0 }

    (fig_p1, fig_p2) = \
        plot_pkg(vt_p, graphL, metricL1_p, metricL3, widthH_p, adjustH, adjustH)
    (fig_f1, fig_f2, fig_f3) = \
        plot_fn (vt_f, graphL, functionH, metricL1_f, metricL2_f, metricL3, widthH_f, adjustH, adjustH)

    fig_p1.savefig('chart-grappolo-med-pkg-metrics.pdf', bbox_inches='tight')
    #fig_p2.savefig('chart-grappolo-med-pkg-metric2.pdf', bbox_inches='tight')

    fig_f1.savefig('chart-grappolo-med-fn-metrics.pdf', bbox_inches='tight')
    #fig_f2.savefig('chart-grappolo-med-fn-metric2.pdf', bbox_inches='tight')

    #-------------------------------------------------------
    # Big graphs
    #-------------------------------------------------------

    # vt_Bp = vtcsv.VTuneCSV(pathL_Bp, group_by = 'csv')
    # vt_Bf = vtcsv.VTuneCSV(pathL_Bf, group_by = 'csv', makeColL = makeColL_f)

    # widthH_p = {'width1':2.5, 'width2':2.6, 'height':1.8}
    # widthH_f = {'width1':2.5, 'width2':2.7, 'height':2.7} # h=2.7,1.8
    # adjustH['wspace'] = 0.10

    # (fig_Bp1, fig_Bp2) = plot_pkg(vt_Bp, [graphL_big], metricL1_p, metricL3,
    #                               widthH_p, adjustH, adjustH)
    # (fig_Bf1, fig_Bf2) = plot_fn (vt_Bf, [graphL_big], functionH,
    #                               metricL1_f, metricL3,
    #                               widthH_f, adjustH, adjustH)

    # fig_Bp1.savefig('chart-grappolo-big-pkg-metrics.pdf', bbox_inches='tight')
    # #fig_Bp2.savefig('chart-grappolo-big-pkg-metrics2.pdf', bbox_inches='tight')

    # fig_Bf1.savefig('chart-grappolo-big-fn-metrics.pdf', bbox_inches='tight')
    # #fig_Bf2.savefig('chart-grappolo-big-fn-metrics2.pdf', bbox_inches='tight')



def main_ripples(makeColL_f, metricL1_p, metricL1_f, metricL2_f, metricL3):

    #-------------------------------------------------------
    # Ripples
    #-------------------------------------------------------

    path_pfx = './2ripples/'

    # <graph>.imm-<type>.T64.R0-pkg.csv
    # <graph>.imm-<type>.T64.R0-fn.csv

    graphL = [ [('soc-Slashdot0902', 'slash'),
                ('soc-twitter-combined', 'twitter'),
                ('wiki-talk', 'talk') ],
               [('wiki-topcats', 'topcats'),
                ('soc-pokec-relationships', 'pokec')] ]

    graphL_0 = [ x[0] for x in flattenL(graphL) ]

    graph_sfx = ['.imm-dram.T64.R0',
                 '.imm-kdax.T64.R0',
                 '.imm-mem.T64.R0']


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
        ('ripples::AddRRRSet<ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>, trng::lcg64, ripples::independent_cascade_tag>', 'AddRRRSet'),
        ('ripples::Graph<unsigned int, ripples::WeightedDestination<unsigned int, float>, ripples::BackwardDirection<unsigned int>>::neighbors', 'neighbors'),

        # move_merge
        ('std::__move_merge<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'move_merge'),
        ('std::__move_merge<unsigned int*, __gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>, __gnu_cxx::__ops::_Iter_less_iter>', 'move_merge'),

        # push_back
        ('std::vector<unsigned int, std::allocator<unsigned int>>::push_back', 'push_back'),
        ('std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>::push_back', 'push_back'),

        # operator++
        ('__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, std::allocator<unsigned int>>>::operator++', 'operator++'),
        ('__gnu_cxx::__normal_iterator<unsigned int*, std::vector<unsigned int, libmemkind::static_kind::allocator<unsigned int>>>::operator++', 'operator++'),

        ('trng::lcg64::step', 'trng::step'),

        ('func@0x1d6d0', 'omp/lock'),
        ('func@0x1d860', 'omp/reduce'),
        ('[vmlinux]', 'vmlinux')
    ] )


    #functionL = list(functionH.items())

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    vt_p = vtcsv.VTuneCSV(pathL_p, group_by = 'csv')
    vt_f = vtcsv.VTuneCSV(pathL_f, group_by = 'csv', makeColL = makeColL_f)

    widthH_p = { 'width1':3.0, 'width2':3.0, 'height':1.8 }
    widthH_f = { 'width1':3.5, 'width2':3.5, 'height':2.7 } # h=2.7,1.8
    adjustH = { 'left':0.02, 'right':0.98, 'bottom':0.01, 'top':0.99,
                'wspace':0.00, 'hspace':0.0 }

    (fig_p1, fig_p2) = \
        plot_pkg(vt_p, graphL, metricL1_p, metricL3, widthH_p, adjustH, adjustH)
    (fig_f1, fig_f2, fig_f3) = \
        plot_fn (vt_f, graphL, functionH, metricL1_f, metricL2_f, metricL3, widthH_f, adjustH, adjustH)

    fig_p1.savefig('chart-ripples-pkg-metrics.pdf', bbox_inches='tight')
    #fig_p2.savefig('chart-ripples-pkg-metrics2.pdf', bbox_inches='tight')

    fig_f1.savefig('chart-ripples-fn-metrics.pdf', bbox_inches='tight')
    #fig_f2.savefig('chart-ripples-fn-metrics2.pdf', bbox_inches='tight')
    

#****************************************************************************

def plot_pkg(vt, graph_grpL, metricL1, metricL2, widthH, adjustH1, adjustH2):

    (w1, w2, h) = (widthH['width1'], widthH['width2'], widthH['height'])

    #-------------------------------------------------------
    
    graphL = flattenL(graph_grpL)
    #print(graphL)
    
    fig1, axesL1 = plotL_mk(vt, metricL1, w1, h, graph_grpL)
    plotL_do(vt, fig1, axesL1, metricL1, dfrm_pkg_xform(graph_grpL), 'Socket', graph_grpL)
    plotL_adj(fig1, adjustH1)

    #-------------------------------------------------------
    
    fig2, axesL2 = plotL_mk(vt, metricL2, w2, h, graph_grpL)
    plotL_do(vt, fig2, axesL2, metricL2, dfrm_pkg_xform(graph_grpL), 'Socket', graph_grpL)
    plotL_adj(fig2, adjustH2)

    return (fig1, fig2)


def dfrm_pkg_xform(graph_grpL):
    def dfrm_pkg_xform1(dfrm):
        dfrm.sort_index(axis=0, ascending=True, inplace=True)
        dfrm.rename(index = (lambda x: x.replace('package_', '')), inplace=True)
        dfrm.rename(columns = (lambda x: rename_col(x, graph_grpL)), inplace=True)
        return dfrm
    return dfrm_pkg_xform1
    

#****************************************************************************

def plot_fn(vt, graph_grpL, functionH, metricL1, metricL2, metricL3, widthH, adjustH1, adjustH2):
    (w1, w2, h) = (widthH['width1'], widthH['width2'], widthH['height'])
    
    #-------------------------------------------------------
    
    fig1, axesL1 = plotL_mk(vt, metricL1, w1, h, graph_grpL)
    plotL_do(vt, fig1, axesL1, metricL1, dfrm_fn_xform(functionH, graph_grpL), 'Functions', graph_grpL)
    plotL_adj(fig1, adjustH1)

    #-------------------------------------------------------
        
    # Percentage metrics
    graphL = [ flattenL(graph_grpL) ]
    
    fig2, axesL2 = plotL_mk(vt, metricL2, w2, h, graphL)
    plotL_do(vt, fig2, axesL2, metricL2, dfrm_fn_xform(functionH, graphL), 'Functions', graphL)
    plotL_adj(fig2, adjustH2)

    #-------------------------------------------------------
    
    fig3, axesL3 = plotL_mk(vt, metricL3, w2, h, graph_grpL)
    plotL_do(vt, fig3, axesL3, metricL3, dfrm_fn_xform(functionH, graph_grpL), 'Functions', graph_grpL)
    plotL_adj(fig3, adjustH2)

    return (fig1, fig2, fig3)

    
def dfrm_fn_xform(functionH, graph_grpL):
    def dfrm_fn_xform1(dfrm):
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
        rowL = [ dfrm.loc[ [fn] ].sum(axis=0).to_frame().transpose()
                 for fn in functionHx_keys ]
        #print(rowL)
        
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

            # find DataFrame for 'metricPair'
            try:
                dfrm = vt.dataH[metricPair[0]]
            except KeyError:
                vtcsv.printRed(("Warning: Skipping metric: '%s'" % metricPair[0]))
                widthL.append(1)
                continue

            n_col = find_fig_width(dfrm, graph_grp)
            widthL.append(n_col)

    return widthL


def plotL_do(vt, fig, axesL, metricL, dfrm_xformF, ytitle_txt, graph_grpL):

    grp_per_metric = len(graph_grpL)
    
    num_metric = len(metricL)
    for i_m in range(num_metric):

        for i_g in range(grp_per_metric):

            graph_grp = graph_grpL[i_g]
        
            axes_i = (i_m * grp_per_metric) + i_g

            axes = axesL[axes_i]

            axes.margins(tight=True)

            metricPair = metricL[i_m]
            ytitle = ytitle_txt if (i_m == 0 and i_g == 0) else None

            # find DataFrame for 'metricPair'
            try:
                dfrm = vt.dataH[metricPair[0]]
            except KeyError:
                vtcsv.printRed(("Warning: Skipping metric: '%s'" % metricPair[0]))
                continue

            # select columns for 'graph_grp'
            dfrm = select_dfrm_col(dfrm, graph_grp)
            #print(dfrm)
            #sys.exit()
            
            dfrm = dfrm_xformF(dfrm)

            axes1 = plot(dfrm, axes, metricPair, ytitle, graph_grp)


def plotL_adj(fig, adjustH):


    fig.subplots_adjust(**adjustH)

    if (Do_view):
        fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)


def plot(dfrm, axes, metricPair, ytitle, x_groupL = None):

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
                           cbar=True, cmap='RdBu_r',# coolwarm
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

    title_txt = metricPair[1] if (len(metricPair) > 1) else metricPair[0]
    axes.set_title(title_txt)

    if (ytitle):
        axes.set_ylabel(ytitle)

    # correct x labels
    try:
        axes.set_xticklabels(dfrm.columns, rotation=15, ha='right')
    except:
        print(ytitle, axes.get_xticklabels(), dfrm.columns)
        pass
    #for x in axes.get_xticklabels():
    #    x.set_rotation(0)

    #-------------------------------------------------------
    # Secondary x groups and labels (x_groupL)
    #-------------------------------------------------------
    if (x_groupL):
        # if x_groupL is a list of pairs, grab second item in each pair
        nmL = [ x[1] for x in x_groupL ] if (isinstance(x_groupL[0], tuple)) else x_groupL

        (x_beg, x_end) = axes.get_xlim()
        n_x = int(x_end) # len(dfrm.columns)
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

def find_fig_width(dfrm, graph_grpL):
    colL = dfrm.columns

    beg_i, beg_col = find_beg_col(colL, graph_grpL)
    end_i, end_col = find_end_col(colL, graph_grpL)

    return (end_i - beg_i) + 1


def select_dfrm_col(dfrm, graph_grpL):
    colL = dfrm.columns

    beg_i, beg_col = find_beg_col(colL, graph_grpL)
    end_i, end_col = find_end_col(colL, graph_grpL) # beg_i + len(graph_grpL)
    #print(beg_col, end_col)
    
    return dfrm.loc[:, beg_col : end_col]


def find_beg_col(columnL, graph_grpL):
    for i_col in range(len(columnL)):
        for g in graph_grpL:
            g_nm = g[0] if (isinstance(g, tuple)) else g
            col_nm = columnL[i_col]
            if (col_nm.find(g_nm) >= 0):
                return (i_col, col_nm)
    return (0, columnL[0])


def find_end_col(columnL, graph_grpL):
    for i_col in reversed(range(len(columnL))):
        for g in graph_grpL:
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
