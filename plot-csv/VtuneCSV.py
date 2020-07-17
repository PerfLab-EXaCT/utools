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

    csv_pathL = None
    data = None

    def __init__ (self, csv_pathL):
        self.dataL = []
        self.labelL = []
        
        data_idx_nm = 'Function' # rows will be labeled by this column name

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------

        if (not isinstance(csv_pathL, list)):
            csv_pathL = [csv_pathL]

        self.labelL = [os.path.basename(x).strip(".csv") for x in csv_pathL]

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------

        for csv_fnm in csv_pathL:
            dfrm = pandas.read_csv(csv_fnm, error_bad_lines = False)
            dfrm = self.remove_empty_cols(dfrm)
            dfrm = dfrm.dropna(axis = 1, how = "all")

            #idx_col = dfrm.columns[0]
            dfrm = dfrm.set_index(data_idx_nm)
            
            if (' [Unknown stack frame(s)]') in dfrm:
                dfrm = dfrm.drop(' [Unknown stack frame(s)]')

            #dfrm = dfrm.rename(lambda x: x.strip(" []").replace("Loop at line ", ""))
            
            dfrm = dfrm.groupby(dfrm.index, sort = False).first()

            self.dataL.append(dfrm)


    def __str__(self):
        return ""
 

    def info(self):
        index_list = list(self.dataL[0].index)
        column_list = list(self.dataL[0].columns)
    
        print("************************************************")
        print("Loops/Functions")
        print("************************************************")
        for x in index_list:
            print(x)

        print("************************************************")
        print("Metrics")
        print("************************************************")
        for x in column_list:
            print(x)
   

    def remove_empty_cols(self, dfrm):
        empties = (dfrm.iloc[:,:].sum() != 0)
        dfrm = dfrm.iloc[:, list(empties)]
        return dfrm


    def get_frame(self, function, metric):
        a= pandas.DataFrame()
        for td in self.data:
            a = pandas.concat([a, td[metric]])

        a = a.loc[function]
        if len(self.data) > 1:
            a.columns = [metric]
            a.index = self.labelL
            try:
                a.index = [int(idx) for idx in list(a.index)]
                a = a.sort_index(ascending=True)
                a.index = [str(idx) for idx in list(a.index)]
            except ValueError:
                a.index = self.labelL
        a.index.name = function
        return a


#****************************************************************************

if __name__ == "__main__":

    import sys

    assert(len(sys.argv) > 1)
    csv = VtuneCSV(sys.argv[1:])
    csv.info()
    #print(csv)

