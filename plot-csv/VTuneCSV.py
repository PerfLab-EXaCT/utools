#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys

#import traceback
#import inspect

import re

# https://pandas.pydata.org
import pandas
import numpy

#import matplotlib.pyplot as pyplt

plot_stats_cutoff = 50

# FIXME:
# - index should be 'Function (Full)'
# - avoid dropping duplicates

MergeRows_nosum_metricPat = r'%|Average' # Latency, Bound, # respect case
MergeRows_sum_metricPat = r'Hardware Event Count'

#****************************************************************************
#
#****************************************************************************

class VTuneCSV:
    """
    Create a hash of DataFrames that have rows indexed by 'data_index_nm'.
    The grouping for each DataFrame is controlled with <group_by>.

    <csv_pathL>: List of paths to CSV data files

    <group_by>: How to create the columns for each DataFrame
      'metric': For each CSV-file f: [ indexL x f[columnL] ]
      'csv':    For each column c:   [ indexL x CSV-file[c] ]

    <indexL>:  From 'data_index_nm', select only rows (functions) in 'indexL'
               'None' means '<all>'

    <columnL>: From each CSV, select only columns (metrics) in 'columnL'
               For 'metric', 'None' means '<all>'
               For 'csv',    'None' means '<each>', i.e., one column/csv
                             '[]' means '<all>', i.e., all columns/csv

    <makeColL>: Make new columns. List of (col-source, col-dest, make-fn),
                where 'make-fn' is a function with the signature of
                'makeCol_pctOfColTotal(df, col-source)' (below).
    """

    NM = "" #VTuneCSV.__name__

    dataH = None
    dataL = None
    group_by = None

    index_name = None # rows are labeled by this column

    COL_SEP = '/'

    metric_id = 'Function'
    metric_id_x = [ 'Function (Full)',
                    'Module',
                    'Source File',
                    'Start Address' ]
    metric_mn = '[mean]'
    metric_sm = '[sum]'

    def __init__ (self,
                  csv_pathL,
                  group_by = 'metric',
                  indexL = None,
                  columnL = None,
                  makeColL = None):

        VTuneCSV.NM = type(self).__name__
    
        self.dataH = { }
        self.dataL = [ ]
        self.group_by = group_by

        if (not isinstance(csv_pathL, list)):
            csv_pathL = [csv_pathL]

        if (makeColL == None):
            makeColL = []
        elif (not isinstance(makeColL, list)):
            makeColL = [makeColL]

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------

        for csv_fnm in csv_pathL:
            self.add_csv(csv_fnm, indexL, columnL, makeColL)

        #-------------------------------------------------------
        # finalize grouping
        #-------------------------------------------------------

        if (self.group_by == 'csv'):
            for key, dfrm in self.dataH.items():
                # col_srt = sorted(dfrm.columns, key = lambda x : my_sort_key(x))
                # self.dataH[key] = dfrm[col_srt]
                pass                
                #dfrm.sort_index(axis=1, inplace = True)

            self.dataL = list(self.dataH.items())

        elif (self.group_by == 'metric'):
            self.dataL = sorted(self.dataH.items(),
                                key = lambda kv : my_sort_keyval(kv))
        else:
            sys.exit("Bad group_by! %s" % self.group_by)


    def __str__(self):
        msg = ""

        for kv in self.dataL:
            msg += ("*** %s: %s (index: %s) ***\n%s\n") % (VTuneCSV.NM, kv[0], self.index_name, kv[1])

        #for x, y in self.dataH.items():
        #    msg += ("*** %s ***\n%s\n") % (x, y)

        return msg


    def info(self):
        #dfrm0 = next(iter(self.dataH.values()))
        (title, dfrm0) = self.dataL[0]

        print("************************************************")
        print("%s: Columns" % title)
        print("************************************************")
        dfrm0.info()
        print("------------------------------------------------")
        for x in dfrm0.columns:
            print("  '%s'" % x)
        
        print("************************************************")
        print("%s: Loops/Functions" % title)
        print("************************************************")
        for x in dfrm0.index:
            print("  '%s'" % x)


    
    def add_csv(self, csv_fnm, indexL, columnL, makeColL):
        if (not os.path.exists(csv_fnm)):
            MSG.warn(("Skipping non-existent file '%s'" % (csv_fnm)))
            return

        csv_nm = re.sub('\.csv$', '', os.path.basename(csv_fnm))

        MSG.msg("Reading '{}'".format(csv_fnm))
        
        dfrm = pandas.read_csv(csv_fnm, error_bad_lines = False)

        #-------------------------------------------------------
        # Set Index
        #-------------------------------------------------------

        if (dfrm.columns.isin( [VTuneCSV.metric_id] ).any()):
            self.index_name = VTuneCSV.metric_id
        else:
            self.index_name = dfrm.columns[0]
            
        dfrm.set_index(self.index_name, inplace = True)

        #-------------------------------------------------------
        # Sometimes index is not unique, so we want to merge rows.
        #
        # If the metrics are ratios that we cannot sum, drop
        # duplicates and warn.
        #
        # FIXME: try using 'Function (Full)' as index
        #-------------------------------------------------------
        #do_sum_fn = lambda x: re.search(MergeRows_sum_metricPat, x)
        #do_sum = all(map(do_sum_fn, dfrm.columns))
        
        no_sum_fn = lambda x: re.search(MergeRows_nosum_metricPat, x)
        no_sum = any(map(no_sum_fn, dfrm.columns))

        if (not no_sum):
            # merge rows with sum
            dfrm = dfrm.groupby(dfrm.index, sort = False).sum()
        else:
            # Remove duplicates
            dup = dfrm.index.duplicated()
            if (dup.any()):
                MSG.warn("Dropping duplicates '{}'".format(csv_fnm))
                #print(dfrm[dup])

            dfrm = dfrm[ ~dfrm.index.duplicated(keep='first') ]
            #dfrm = dfrm[ dfrm.index.drop_duplicates(keep='first') ]

        #-------------------------------------------------------
        # Normalize
        #-------------------------------------------------------

        # Drop non-numerical columns (incorporate into id?)
        if (dfrm.columns.isin(VTuneCSV.metric_id_x).any()):
            dfrm.drop(VTuneCSV.metric_id_x, axis=1, inplace=True)
        
        #if ('[Unknown stack frame(s)]') in dfrm:
        #    dfrm = dfrm.drop('[Unknown stack frame(s)]')
        #dfrm = dfrm.rename(lambda x: x.strip(" []").replace("Loop at line ", ""))
        
        #-------------------------------------------------------
        
        #dfrm = self.remove_empty_cols(dfrm)
        dfrm = dfrm.dropna(axis = 1, how = 'all')
        
        
        #-------------------------------------------------------
        # Make new columns
        #-------------------------------------------------------
        # Works for
        # - group_by 'csv' when no colL is specified

        for makeTuple in makeColL:
            col_src = makeTuple[0]
            col_dst = makeTuple[1]
            mkcol_fn = makeTuple[2]

            col_src_i = dfrm.columns.get_loc(col_src)
            # except: sys.exit("Cannot find column '%s'" % col)

            col_dst_i = col_src_i + 1

            dfrm_dst = mkcol_fn(dfrm, col_src)

            dfrm.insert(loc = col_dst_i, column = col_dst, value = dfrm_dst)


        #-------------------------------------------------------
        # Initialize DataFrames for group_by 'csv'
        #-------------------------------------------------------

        if (self.group_by == 'csv'):

            if (columnL == None):
                colL = dfrm.columns
            elif (len(columnL) == 0):
                colL = [ '<all>' ]
            else:
                colL = columnL

            # Ensure we have each column in 'colL'
            for x in colL:
                if (not x in self.dataH):
                    self.dataH[x] = pandas.DataFrame()


        #-------------------------------------------------------
        # Select rows
        #-------------------------------------------------------
        if (indexL):
            if (indexL[0] == '<total>'):
                sys.exit("FIXME!")
            else:
                dfrm = dfrm.loc[indexL]

        #-------------------------------------------------------
        # Select columns
        #-------------------------------------------------------

        if (self.group_by == 'metric'):
            if (columnL):
                dfrm = dfrm[columnL]

        #-------------------------------------------------------
        # Select columns for final DataFrame
        #-------------------------------------------------------

        if (self.group_by == 'csv'):
            for key0, dfrm0 in self.dataH.items():
                if (key0 == '<all>'):
                    dfrm_new = dfrm
                    dfrm_new.columns = [(csv_nm + self.COL_SEP + x) for x in dfrm.columns]
                else:
                    if (dfrm.columns.isin([key0]).any()):
                        dfrm_new = dfrm[ [key0] ]
                    else:
                        dfrm_new = pandas.DataFrame(numpy.NAN, index=dfrm.index, columns=[key0])

                    dfrm_new.columns = [ csv_nm ]
                
                if (dfrm0.empty):
                    self.dataH[key0] = dfrm_new
                else:
                    self.dataH[key0] = pandas.concat([dfrm0, dfrm_new], axis=1) # pandas.join()
        elif (self.group_by == 'metric'):
            self.dataH[csv_nm] = dfrm
        else:
            sys.exit("Bad group_by! %s" % self.group_by)

        return dfrm
   

    def remove_empty_cols(self, dfrm):
        empties = (dfrm.iloc[:,:].sum() != 0)
        dfrm = dfrm.iloc[:, list(empties)]
        return dfrm


    def plot(self, kind, xlabel = ''):
        import matplotlib.pyplot as pyplt
        
        # if (dfrm.group_by == 'csv'):
        #     xlabel = 'CSV names'
        # elif (dfrm.group_by == 'metric'):
        # else:
        #     sys.exit("Bad group_by! %s" % dfrm.group_by)

        (t, dfrm0) = self.dataL[0]
        dfrm0_ncol = len(dfrm0.columns)
        #dfrm0_nrow = len(dfrm0.columns)

        n_axes = len(self.dataL)
        w_axis = (0.5 * dfrm0_ncol + 1.0)
        w_fig = 2.2 + w_axis + (n_axes - 1) * w_axis

        (fig, axesL) = pyplt.subplots(nrows=1, ncols=n_axes, figsize=(w_fig, 19))

        # Need to test commented code when n_axes == 1
        assert(n_axes > 1)
        #if (not isinstance(axesL, numpy.array)):
        #    axesL = numpy.array([axesL]) # true when n_axes == 1

        for i in range(n_axes):
        #for kv in self.dataL:
            kv = self.dataL[i]
            title = kv[0]
            dfrm = kv[1]

            dfrm = dfrm.rename(index = (lambda x: x[0:30]))

            dfrm = make_stats(dfrm)

            axes = axesL[i]

            if (kind == 'heat'):
                do_yticks = True if (i == 0) else False
                plot_heat(dfrm, axes, title, do_yticks)
            else:
                dfrm_plot = dfrm.transpose()

                dfrm_plot.plot(kind = kind, ax=axes)
 
                axes.set_xticklabels(axes.get_xticklabels(), rotation='vertical')
                axes.set_xlabel(xlabel)

                axes.set_ylabel(title)

        adjustH = { 'left':0.09, 'right':1.0, 'bottom':0.08, 'top':0.99,
                    'wspace':0.01, 'hspace':0.00 }
        fig.subplots_adjust(**adjustH)
        #fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.1)

        pyplt.show()
        return (fig, axesL)

#****************************************************************************

def plot_heat(dfrm, axes, title, do_yticks):
    import seaborn

    df_mask = pandas.DataFrame(False, index=dfrm.index, columns=dfrm.columns)
    df_mask.loc[VTuneCSV.metric_mn] = True
    df_mask.loc[VTuneCSV.metric_sm] = True

    axes = seaborn.heatmap(dfrm, ax=axes, mask=df_mask, annot=True,
                           cbar=False, cmap="RdBu_r", # coolwarm
                           yticklabels = do_yticks)

    # show masked values (update font color to avoid white against white!)
    seaborn.heatmap(dfrm, ax=axes, mask=(~df_mask), annot=True,
                   cbar=False, alpha=0, annot_kws={'color':'black'},
                   yticklabels = do_yticks)

    if (not do_yticks):
        #axes.set_yticks([])
        axes.set_ylabel('')
    
    # correct x-ticks and x-labels
    axes.set_xticks(numpy.arange(0.5, len(dfrm.columns)))

    if (len(dfrm.columns) == 1):
        axes.set_xticklabels([title], rotation=10, ha='right')
    else:
        axes.set_title(title)
        axes.set_xticklabels(dfrm.columns, rotation=10, ha='right')

    return axes


def make_stats(dfrm):
    plot_stats_cutoff = 50

    if (len(dfrm.index) >= plot_stats_cutoff):
        dfrm1 = dfrm.iloc[0:plot_stats_cutoff, :].copy()
    else:
        dfrm1 = dfrm

    dfrm1.loc[VTuneCSV.metric_mn] = dfrm.mean(axis=0) # mean per column
    dfrm1.loc[VTuneCSV.metric_sm] = dfrm.sum(axis=0)  # sum per column
    
    return dfrm1


#****************************************************************************
        
def my_sort_keyval(kv):
    key = kv[0]
    return my_sort_key(key)


def my_sort_key(key):
    assert(isinstance(key, str))

    splitL = key.split(VTuneCSV.COL_SEP)
    
    try:
        return int(splitL[0])
    except (ValueError, TypeError):
        return splitL[0]

    

#****************************************************************************
# makeCol_x: returns the new column
#****************************************************************************

def makeCol_pctOfColTotal(dfrm, col_src):
    col_sum = dfrm[col_src].sum()
    dfrm_dst = dfrm[col_src] / col_sum * 100.0
    return dfrm_dst


def makeCol_pctOfOther(col_src2): # could be a list of source columns

    def mk_fn(dfrm, col_src):
        dfrm_dst = 100.0 * dfrm[col_src] / (dfrm[col_src] + dfrm[col_src2])
        return dfrm_dst
        
    return mk_fn


#****************************************************************************
# 
#****************************************************************************

class MSG:
    # https://www.geeksforgeeks.org/print-colors-python-terminal/
    clr_bold  = '\033[01m'
    clr_red   = '\033[31m'
    clr_purpl = '\033[35m'

    clr_orang = '\033[33m'
    clr_blue  = '\033[34m'
    clr_purpl = '\033[35m'
    clr_cyan  = '\033[36m'
    # lightblue='\033[94m'

    clr_reset = '\033[0m'

    @staticmethod
    def msg(str):
        MSG.do('', VTuneCSV.NM, str)

    @staticmethod
    def warn(str):
        MSG.do(MSG.clr_bold + MSG.clr_purpl, VTuneCSV.NM + ' Warning', str)
    
    @staticmethod
    def warnx(str):
        MSG.do(MSG.clr_bold + MSG.clr_red, 'Warning', str)

    @staticmethod
    def err(str, code=1):
        MSG.do(MSG.clr_bold + MSG.clr_red, 'Error', str)
        exit(code)

    @staticmethod
    def do(color, info, str):
        try:
            # tbL = traceback.extract_stack(limit=3)
            # inspect.currentframe().f_back.f_back.f_code.co_name
            name = sys._getframe(2).f_code.co_name
        except (IndexError, TypeError, AttributeError): # something went wrong
            name = "<unknown>"

        print("{}{} [{}]: {}{}".format(color, info, name, str, MSG.clr_reset))


#****************************************************************************
#
#****************************************************************************

if __name__ == "__main__":
    assert(len(sys.argv) > 1)
    csv_pathL = sys.argv[1:]

    csv = VTuneCSV(csv_pathL, group_by = 'metric')
    csv.info()
    print(csv)

    csv2 = VTuneCSV(csv_pathL, group_by = 'csv') # columnL = []
    print(csv2)

    csv2.plot('heat')
    #csv2.plot('line')
