#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys

# https://pandas.pydata.org
import pandas

#import matplotlib.pyplot as pyplt


#****************************************************************************
#
#****************************************************************************

class VTuneCSV():
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

    <makeColL>: Make new columns. List of (source-col, new-col, 'percent')
                (TODO: abstract to function)
    """

    dataH = None
    dataL = None
    group_by = None

    index_name = None # rows are labeled by this column

    COL_SEP = '/'

    def __init__ (self,
                  csv_pathL,
                  group_by = 'metric',
                  indexL = None,
                  columnL = None,
                  makeColL = None):

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
                #dfrm.sort_index(axis=1, inplace = True)
                if (0):
                    # FIXME: To specific
                    col_srt = sorted(dfrm.columns, key = lambda x : my_sort_key(x))
                    self.dataH[key] = dfrm[col_srt]

            self.dataL = list(self.dataH.items())

        elif (self.group_by == 'metric'):
            self.dataL = sorted(self.dataH.items(),
                                key = lambda kv : my_sort_keyval(kv))
        else:
            sys.exit("Bad group_by! %s" % self.group_by)


    def __str__(self):
        msg = ""

        for kv in self.dataL:
            msg += ("*** %s: %s (index: %s) ***\n%s\n") % (type(self).__name__, kv[0], self.index_name, kv[1])

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
            print(("Skipping non-existent file: '%s'" % csv_fnm))
            return

        csv_nm = os.path.basename(csv_fnm).strip(".csv")

        dfrm = pandas.read_csv(csv_fnm, error_bad_lines = False)

        self.index_name = dfrm.columns[0]
        dfrm = dfrm.set_index(self.index_name)

        print(("*** %s: '%s' (%s)" % (type(self).__name__, csv_fnm, self.index_name)))

        #-------------------------------------------------------
        # Normalize
        #-------------------------------------------------------
        
        #dfrm = self.remove_empty_cols(dfrm)
        dfrm = dfrm.dropna(axis = 1, how = "all")

        #if ('[Unknown stack frame(s)]') in dfrm:
        #    dfrm = dfrm.drop('[Unknown stack frame(s)]')
        #dfrm = dfrm.rename(lambda x: x.strip(" []").replace("Loop at line ", ""))

        # Remove duplicates
        dfrm = dfrm.groupby(dfrm.index, sort = False).sum()

        #-------------------------------------------------------
        # Make new columns
        #-------------------------------------------------------
        # Works for
        # - group_by 'csv' when no colL is specified

        for makeTuple in makeColL:
            col_src = makeTuple[0]
            col_dst = makeTuple[1]
            col_ty =  makeTuple[2]

            col_src_i = dfrm.columns.get_loc(col_src)
            # except: sys.exit("Cannot find column '%s'" % col)

            col_dst_i = col_src_i + 1

            assert(col_ty == 'percent')
                
            col_sum = dfrm[col_src].sum()
            
            dfrm.insert(loc = col_dst_i,
                        column = col_dst,
                        value = dfrm[col_src] / col_sum * 100.0)


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

            if (not self.dataH):
                for x in colL:
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
                    dfrm_new = dfrm[[key0]]
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
        w_fig = 2.5 + w_axis + (n_axes - 1) * w_axis

        (fig, axesL) = pyplt.subplots(nrows=1, ncols=n_axes, figsize=(w_fig, 20))
        if (not isinstance(axesL, list)):
            axesL = [axesL] # true when n_axes == 1

        for i in range(len(self.dataL)):
        #for kv in self.dataL:
            kv = self.dataL[i]
            title = kv[0]
            dfrm = kv[1]

            dfrm = dfrm.rename(index = (lambda x: x[0:30]))

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

        fig.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.1)
        pyplt.show()
        return (fig, axesL)


def plot_heat(dfrm, axes, title, do_yticks):
    import seaborn

    axes = seaborn.heatmap(dfrm, ax=axes, annot=True,
                           cbar=True, cmap="RdBu_r", # coolwarm
                           yticklabels=do_yticks)

    if (len(dfrm.columns) == 1):
        axes.set_xticklabels([title], rotation=25, ha='right')
    else:
        axes.set_title(title)
        axes.set_xticklabels(dfrm.columns, rotation=25, ha='right')

    return axes

        
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
