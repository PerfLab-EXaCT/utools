#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys

import pandas

#****************************************************************************
#
#****************************************************************************

class VTuneCSV():
    """
    <csv_pathL>: list of paths for CSV files
    <indexL>: list of rows (functions) to select
    <columnL>: list of columns (metrics) to select

    FIXME:
    If each file name contains only integers
      - These files will be aranged in ascending order based on filename
    else:
      - These files will be aranged in the order they're passed in through CLI
    """

    labelL = None
    data = None

    data_index_nm = 'Function' # rows are labeled by this column

    def __init__ (self, csv_pathL, indexL = None, columnL = None):
        self.data = pandas.DataFrame() # []
        self.labelL = []

        if (not isinstance(csv_pathL, list)):
            csv_pathL = [csv_pathL]

        #self.labelL = [os.path.basename(x).strip(".csv") for x in csv_pathL]

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------

        for csv_fnm in csv_pathL:
            self.add_csv(csv_fnm, indexL, columnL)


    def __str__(self):
        return ""


    def add_csv(self, csv_fnm, indexL, columnL):
        print(("*** %s: '%s'" % (__name__, csv_fnm)))

        if (not os.path.exists(csv_fnm)):
            print(("Not found: '%s'" % csv_fnm))
            return

        dfrm = pandas.read_csv(csv_fnm, error_bad_lines = False)

        dfrm = dfrm.set_index(self.data_index_nm)

        label = os.path.basename(csv_fnm).strip(".csv")
        self.labelL.append(label)

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
        if (columnL):
            dfrm = dfrm[columnL]

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
        #self.data.append(dfrm)
        
        if (self.data.empty):
            self.data = dfrm
        else:
            self.data = pandas.concat([self.data, dfrm], axis=1)


        return self.data

    
    def info(self):
        if (isinstance(self.data, pandas.DataFrame)):
            index_list = list(self.data.index)
            column_list = list(self.data.columns)
        elif (isinstance(self.data, list)):
            index_list = list(self.data[0].index)
            column_list = list(self.data[0].columns)
        else:
            sys.exit("Bad type!")
        
    
        print("************************************************")
        print("Loops/Functions")
        print("************************************************")
        for x in index_list:
            print("  '%s'" % x)

        print("************************************************")
        print("Metrics")
        print("************************************************")
        for x in column_list:
            print("  '%s'" % x)
   

    def remove_empty_cols(self, dfrm):
        empties = (dfrm.iloc[:,:].sum() != 0)
        dfrm = dfrm.iloc[:, list(empties)]
        return dfrm


    def get_frame(self, columnL, function = None):
        # FIXME: Deprecated

        dfrm = pandas.DataFrame()

        for x in self.dataL:
            print(x[columnL])
            dfrm = pandas.concat([ dfrm, x[columnL] ], axis=1)

        # ???
        if (function):
            dfrm = dfrm.loc[function]
            if len(self.dataL) > 1:
                dfrm.columns = [columnL]
                dfrm.index = self.labelL
                try:
                    dfrm.index = [int(idx) for idx in list(dfrm.index)]
                    dfrm = dfrm.sort_index(ascending = True)
                    dfrm.index = [str(idx) for idx in list(dfrm.index)]
                except ValueError:
                    dfrm.index = self.labelL
            dfrm.index.name = function
        
        return dfrm


#****************************************************************************

if __name__ == "__main__":

    indexL = ['[Loop at line 4015 in gwce_new]',
              '[Loop at line 5354 in mom_eqs_new_nc]']
    columnL = ['CPU Time', 'CPI Rate']
    
    assert(len(sys.argv) > 1)
    csv_pathL = sys.argv[1:]
    
    csv = VTuneCSV(csv_pathL)
    #csv.info()

    csv = VTuneCSV(csv_pathL, columnL = columnL)
    #csv.info()

    csv = VTuneCSV(csv_pathL, indexL = indexL, columnL = columnL)

    print(csv.data)
