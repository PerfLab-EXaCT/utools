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

#****************************************************************************
#
#****************************************************************************

class VTuneCSV():
    """
    Create a hash of DataFrames that have rows indexed by 'data_index_nm'.
    The grouping for each DataFrame is controlled with <group_by>.

    <csv_pathL>: List of paths to CSV data files

    <group_by>: How to create the columns for each DataFrame
      'csv':    For each column c:   [ indexL x CSV-file[c] ]
      'metric': For each CSV-file f: [ indexL x f[columnL] ]

    <indexL>:  From 'data_index_nm', select only rows (functions) in 'indexL'
    <columnL>: From each CSV, select only columns (metrics) in 'columnL'
    """

    dataH = None
    dataL = None
    group_by = None

    data_index_nm = 'Function' # rows are labeled by this column

    data_col_sep = '/'

    def __init__ (self,
                  csv_pathL,
                  group_by = 'csv',
                  indexL = None,
                  columnL = None):

        self.dataH = { }
        self.dataL = [ ]
        self.group_by = group_by

        if (not isinstance(csv_pathL, list)):
            csv_pathL = [csv_pathL]

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------

        for csv_fnm in csv_pathL:
            self.add_csv(csv_fnm, indexL, columnL)

        if (self.group_by == 'csv'):
            for key, dfrm in self.dataH.items():
                #dfrm.sort_index(axis=1, inplace = True)
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
            msg += ("*** %s ***\n%s\n") % (kv[0], kv[1])

        #for x, y in self.dataH.items():
        #    msg += ("*** %s ***\n%s\n") % (x, y)

        return msg

    
    def add_csv(self, csv_fnm, indexL, columnL):
        print(("*** %s: '%s'" % (type(self).__name__, csv_fnm)))

        if (not os.path.exists(csv_fnm)):
            print(("Skipping non-existent file: '%s'" % csv_fnm))
            return

        csv_nm = os.path.basename(csv_fnm).strip(".csv")

        dfrm = pandas.read_csv(csv_fnm, error_bad_lines = False)

        dfrm = dfrm.set_index(self.data_index_nm)

        columnL_me = columnL
        if (not columnL_me):
            columnL_me = dfrm.columns

        #-------------------------------------------------------
        # Initialize data frames for 'csv'
        #-------------------------------------------------------

        if (self.group_by == 'csv'):
            if (not self.dataH):
                for x in columnL_me:
                    self.dataH[x] = pandas.DataFrame()
        
        #-------------------------------------------------------
        # Normalize
        #-------------------------------------------------------
        
        #dfrm = self.remove_empty_cols(dfrm)
        dfrm = dfrm.dropna(axis = 1, how = "all")

        #if ('[Unknown stack frame(s)]') in dfrm:
        #    dfrm = dfrm.drop('[Unknown stack frame(s)]')
        #dfrm = dfrm.rename(lambda x: x.strip(" []").replace("Loop at line ", ""))

        dfrm = dfrm.groupby(dfrm.index, sort = False).first()

        #-------------------------------------------------------
        # Select columns
        #-------------------------------------------------------

        if (len(columnL_me) < len(dfrm.columns)):
            dfrm = dfrm[columnL_me]

        if (self.group_by == 'csv'):
            if (len(dfrm.columns) == 1):
                dfrm.columns = [ csv_nm ]
            else:
                dfrm.columns = [(csv_nm + self.data_col_sep + x) for x in dfrm.columns]

        #-------------------------------------------------------
        # Add "%" column
        #-------------------------------------------------------
        # FIXME:

        #-------------------------------------------------------
        # Select rows
        #-------------------------------------------------------
        if (indexL):
            if (indexL[0] == '<total>'):
                sys.exit("FIXME!")
            else:
                dfrm = dfrm.loc[indexL]

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------

        if (self.group_by == 'csv'):
            for key, dfrmX in self.dataH.items():
                if (dfrmX.empty):
                    self.dataH[key] = dfrm
                else:
                    self.dataH[key] = pandas.concat([dfrmX, dfrm], axis=1)
        elif (self.group_by == 'metric'):
            self.dataH[csv_nm] = dfrm
        else:
            sys.exit("Bad group_by! %s" % self.group_by)

        return dfrm

    
    def info(self):
        #dfrm0 = next(iter(self.dataH.values()))
        (title, dfrm0) = self.dataL[0]
        
        print("************************************************")
        print("%s: Loops/Functions" % title)
        print("************************************************")
        for x in dfrm0.index:
            print("  '%s'" % x)

        print("************************************************")
        print("%s: Metrics" % title)
        print("************************************************")
        for x in dfrm0.columns:
            print("  '%s'" % x)
   

    def remove_empty_cols(self, dfrm):
        empties = (dfrm.iloc[:,:].sum() != 0)
        dfrm = dfrm.iloc[:, list(empties)]
        return dfrm


def my_sort_keyval(kv):
    key = kv[0]
    return my_sort_key(key)

def my_sort_key(key):
    assert(isinstance(key, str))

    splitL = key.split(VTuneCSV.data_col_sep)
    
    try:
        return int(splitL[0])
    except (ValueError, TypeError):
        return splitL[0]


#****************************************************************************

if __name__ == "__main__":

    assert(len(sys.argv) > 1)
    csv_pathL = sys.argv[1:]
    
    csv1 = VTuneCSV(csv_pathL, group_by = 'csv')
    csv2 = VTuneCSV(csv_pathL, group_by = 'metric')

    csv1.info()

    print(csv1)
    print(csv2)
