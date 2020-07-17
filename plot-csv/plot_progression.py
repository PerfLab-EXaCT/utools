#!/usr/bin/env python

import os
import sys

import pandas
import matplotlib.pyplot as plt

from VtuneCSV import *

#****************************************************************************

def plot_progression(csv_pathL,
                     total_pct = True,
                     kind = "bar",
                     cutoff = ('number', 5),
                     target_functions = [],
                     target_data = []):
    """
    Plot either a line or a bar graph representing changes in where time
    is being spent with increasing MPI ranks
    cutoff = ('number', 5) or cutoff = ("percentage", 34)
    """

    # Input parameters: Metric is a data column label
    data_idx_nm = 'Function' # rows will be labeled by this column name
    data_tgt_col = 'CPU Time' # FIXME: should be a list

    # FIXME: ugly
    percent_cutoff = cutoff[1]/100 # percentage of top consumer loops to display
    num_cutoff = cutoff[1] # number of loops to display

    data_tgt_col_pct = '% of Total'
    
    dfrm_all = pandas.DataFrame()
    labelL = []

    # FIXME: replace with VtuneCSV...
    for csv_fnm in csv_pathL:
        print(("*** File %s" % csv_fnm))

        labelL.append(os.path.basename(csv_fnm).strip(".csv"))

        dfrm0 = pandas.read_csv(csv_fnm, index_col = data_idx_nm)
        
        dfrmX = dfrm0[ [data_tgt_col] ]
        #print(dfrm0)

        #-------------------------------------------------------
        # Add "%" column
        #-------------------------------------------------------
        data_tgt_col_sum = dfrmX[ [data_tgt_col] ].sum()[0]
        
        dfrmX.insert(loc = 1,
                    column = data_tgt_col_pct,
                    value = dfrmX[data_tgt_col] / data_tgt_col_sum * 100)
        print(dfrmX)

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------
        
        other = pandas.DataFrame(index = ['Other Loops'], columns = dfrmX.columns)
        print(other)
        
        if cutoff[0] == 'number':
            data_cutoff = dfrmX.iloc[0:num_cutoff, :]
            other.loc['Other Loops']  = dfrmX.iloc[num_cutoff:, :].sum()
        elif cutoff[0] == "percentage":
            data_cutoff = dfrmX[dfrmX[data_tgt_col]/data_tgt_col_sum > percent_cutoff]
            other.loc['Other Loops']= dfrmX[dfrmX[data_tgt_col]/data_tgt_col_sum < percent_cutoff].sum()
        else:
            sys.exit("Cutoff must be either 'number' or 'percentage'")

        data_cutoff = data_cutoff.append(other)

        if target_functions != []:
            if (target_functions[0] == 'total'):
                data_cutoff = pandas.DataFrame(dfrmX.sum())
                data_cutoff.columns = ['total']
                data_cutoff = data_cutoff.transpose()
            else:
                data_cutoff = dfrmX.loc[target_functions]
                #data_cutoff = dfrmX.transpose().loc[target_functions]


        if total_pct == True:
            slice_this = data_tgt_col_pct
        else:
            slice_this = data_tgt_col

        data_cutoff.rename(lambda x: x.strip("[]").replace("Loop at line ", ""))

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------
        
        if (dfrm_all.empty): # Slice out only the % of times
            dfrm_all = data_cutoff[[slice_this]]
        else:
            dfrm_all = pandas.concat([dfrm_all, data_cutoff[slice_this]], axis=1)

    dfrm_all.columns = labelL
    sorted_names = [int(idx) for idx in labelL]
    sorted_names.sort()
    sorted_names = [str(idx) for idx in sorted_names]
    dfrm_all = dfrm_all[sorted_names] # make sure data appears in increasing order

    # Make sure that the data starts with most expensive column first
    dfrm_all = dfrm_all.sort_values(sorted_names[0], ascending=False)

    plot_data = dfrm_all.transpose()
    if kind == "stack":
        #ax = plt.stackplot(range(len(sorted_names)), [list(plot_data.iloc[:,a]) for a in range(len(plot_data.columns))], labels=plot_data.columns)
        ax = plt.stackplot(list(range(len(sorted_names))), [list(plot_data.iloc[:,a]) for a in range(len(plot_data.columns))], labels=plot_data.columns)
        plt.legend(loc="lower right")
        #plt.xticks(range(len(sorted_names)), sorted_names, rotation='vertical')
        plt.xticks(list(range(len(sorted_names))), sorted_names, rotation='vertical')
        if total_pct == True:
            locs, labels = plt.yticks()
            plt.yticks(locs, ["%s%%" % a for a in locs])
            plt.ylim(0,100)
            plt.ylabel("% of Total Time")
        else:
            plt.ylabel("CPU Time(s)")
        plt.xlabel("Number of Elements")

    else:
        ax = plot_data.plot(kind=kind)
        ax.set_xticklabels(ax.get_xticklabels(), rotation='vertical')
        ax.set_xlabel("Number of Elements")
        if total_pct == True:
            ax.set_yticklabels(["%s%%" % pct for pct in ax.get_yticks()])
            ax.set_ylim(0, 75)
            ax.set_ylabel("% of Total Time")
        else:
            ax.set_ylabel("CPU Time(s)")


#****************************************************************************

csv_pathL = []
for i in range(1,len(sys.argv)):
    if (not os.path.exists(sys.argv[i])):
        print(("File %s not found" % sys.argv[i]))
        quit()
    csv_pathL.append(os.path.abspath(sys.argv[i]))


if __name__ == "__main__":

    assert(len(sys.argv) > 1)
    csv_pathL = sys.argv[1:]

    csv = VtuneCSV(csv_pathL)

    csv.info()

    #plot_pie(csv_pathL[0])

    #  target_functions = []
    
    plot_progression(csv_pathL, kind="stack")

    plot_progression(csv_pathL, kind="line", total_pct=True,
                     target_functions = [])

    plot_progression(csv_pathL, kind="line", total_pct=False,
                     target_functions = ['total'])

    fnL = ['[Loop at line 4015 in gwce_new]',
           '[Loop at line 5354 in mom_eqs_new_nc]']
    plot_progression(csv_pathL, kind="line", total_pct=False,
                     target_functions = fnL)

    #plot_progression(csv_pathL, kind="line", total_pct=False,
    #                 target_functions = ['Hardware Event Count:MEM_LOAD_RETIRED.L2_HIT_PS', 'Hardware Event Count:INST_RETIRED.ANY'])
    
    plt.show()
