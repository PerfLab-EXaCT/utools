#!/usr/bin/env python

import os

import pandas

#****************************************************************************

class VtuneCSV():
    """
    Pass a list of strings containing paths to CSV files.
    If each file name contains only integers
      - These files will be aranged in ascending order based on filename
    else:
      - These files will be aranged in the order they're passed in through CLI
    """

    labelL = None
    data = None

    data_idx_nm = 'Function' # rows are labeled by this column

    def __init__ (self, csv_pathL, metricL = None):
        self.data = pandas.DataFrame()
        self.labelL = []
        
        if (not isinstance(csv_pathL, list)):
            csv_pathL = [csv_pathL]

        #self.labelL = [os.path.basename(x).strip(".csv") for x in csv_pathL]

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------
        for csv_fnm in csv_pathL:
            self.add_csv(csv_fnm, metricL)


    def __str__(self):
        return ""


    def add_csv(self, csv_fnm, metricL):
        print(("*** File %s" % csv_fnm))

        dfrm = pandas.read_csv(csv_fnm, error_bad_lines = False)

        #idx_col = dfrm.columns[0]
        dfrm = dfrm.set_index(self.data_idx_nm)

        label = os.path.basename(csv_fnm).strip(".csv")
        self.labelL.append(label)

        #dfrm = self.remove_empty_cols(dfrm)
        dfrm = dfrm.dropna(axis = 1, how = "all")


        #-------------------------------------------------------
        # Normalize
        #-------------------------------------------------------

        #if ('[Unknown stack frame(s)]') in dfrm:
        #    dfrm = dfrm.drop('[Unknown stack frame(s)]')
        #dfrm = dfrm.rename(lambda x: x.strip(" []").replace("Loop at line ", ""))

        dfrm = dfrm.groupby(dfrm.index, sort = False).first()

        if (metricL):
            dfrm = dfrm[metricL]

        if (self.data.empty):
            self.data = dfrm
        else:
            self.data = pandas.concat([self.data, dfrm], axis=1)

        return self.data

    
    def info(self):
        index_list = list(self.data.index)
        column_list = list(self.data.columns)
    
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


    def get_frame(self, metricL, function = None):
        dfrm = pandas.DataFrame()

        for x in self.dataL:
            print(x[metricL])
            dfrm = pandas.concat([ dfrm, x[metricL] ], axis=1)

        # ???
        if (function):
            dfrm = dfrm.loc[function]
            if len(self.dataL) > 1:
                dfrm.columns = [metricL]
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

    import sys

    assert(len(sys.argv) > 1)
    csv_pathL = sys.argv[1:]
    
    csv = VtuneCSV(csv_pathL)
    #csv.info()

    csv = VtuneCSV(csv_pathL, ['CPU Time', 'CPI Rate'])
    #csv.info()

    print(csv.data)
