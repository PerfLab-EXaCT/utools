#!/usr/bin/env python
# -*-Mode: python;-*-

# $Id$

#****************************************************************************
#
#****************************************************************************

import os
import sys
#import argparse

import pandas
import matplotlib.pyplot as plt
import seaborn as sns

import VTuneCSV as vtcsv

#****************************************************************************
#
#****************************************************************************

def main():
    #-------------------------------------------------------
    # 
    #-------------------------------------------------------

    #assert(len(sys.argv) > 1)
    #csv_pathL = sys.argv[1:]

    csv_pathL = [ './0data/progression/108544.csv',
                  './0data/progression/1696.csv',
                  './0data/progression/1736704.csv',
                  './0data/progression/27136.csv',
                  './0data/progression/434176.csv',
                  './0data/progression/6784.csv',
                  './0data/progression/6946816.csv' ]


    indexL1 = ['[Loop at line 4015 in gwce_new]',
               '[Loop at line 5354 in mom_eqs_new_nc]']
              #'[Loop at line 1939 in pjac]']
              #'[Outside any loop]',
              #'[Loop at line 3149 in timestep]' ]

    indexL2 = ['[Loop at line 4015 in gwce_new]',
               '[Loop at line 5354 in mom_eqs_new_nc]',
               '[Loop at line 1939 in pjac]',
               '[Outside any loop]',
               '[Loop at line 3149 in timestep]' ]

    columnL1 = ['CPU Time']
    columnL2 = ['CPU Time', 'CPI Rate']

    #-------------------------------------------------------
    # 
    #-------------------------------------------------------
    csv1 = vtcsv.VTuneCSV(csv_pathL, group_by = 'csv',
                          indexL = indexL2, columnL = columnL1)
    axes = csv1.plot(kind = 'line', xlabel='Elements')
    axes = csv1.plot(kind = 'bar',  xlabel='Elements')

    csv2 = vtcsv.VTuneCSV(csv_pathL, group_by = 'metric',
                          indexL = indexL2, columnL = columnL2)
    #csv2.plot(kind = 'line', xlabel='Metrics')
    #csv2.plot(kind = 'bar',  xlabel='Metrics')
    print(csv2)
    
    plt.show()


    #-------------------------------------------------------
    # 
    #-------------------------------------------------------
    plot_OLD(csv_pathL, kind = 'stack')

    plot_OLD(csv_pathL, kind = 'line', total_pct=True)

    plot_OLD(csv_pathL, kind = 'line', total_pct=False, indexL = ['total'])

    plot_OLD(csv_pathL, kind = 'line', total_pct=False, indexL = indexL1)

    plt.show()


#****************************************************************************

def plot_OLD(csv_pathL,
             total_pct = True,
             kind = "bar",
             index_cutoff = ('number', 5),
             indexL = []):
    """
    Plot either a line or a bar graph representing changes in where time
    is being spent with increasing MPI ranks
    index_cutoff = ('number', 5) or index_cutoff = ("percentage", 34)
    """

    #-------------------------------------------------------
    # Input parameters
    #-------------------------------------------------------

    # Metric is a data column label
    data_index_nm = 'Function' # rows will be labeled by this column name
    data_column = 'CPU Time'

    # FIXME: ugly
    percent_cutoff = index_cutoff[1]/100 # percentage of top consumer loops to display
    num_cutoff = index_cutoff[1] # number of loops to display

    data_column_pct = '% of Total'

    #-------------------------------------------------------
    # Populate
    #-------------------------------------------------------

    dfrm_all = pandas.DataFrame()
    labelL = []

    for csv_fnm in csv_pathL:
        #print(("*** File %s" % csv_fnm))

        labelL.append(os.path.basename(csv_fnm).strip(".csv"))

        dfrm0 = pandas.read_csv(csv_fnm, index_col = data_index_nm)
        
        dfrmX = dfrm0[ [data_column] ]
        #print(dfrm0)

        #-------------------------------------------------------
        # Add "%" column
        #-------------------------------------------------------
        data_column_sum = dfrmX[ [data_column] ].sum()[0]
        
        dfrmX.insert(loc = 1,
                    column = data_column_pct,
                    value = dfrmX[data_column] / data_column_sum * 100)
        #print(dfrmX)

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------
        
        other = pandas.DataFrame(index = ['Other Loops'], columns = dfrmX.columns)
        #print(other)
        
        if index_cutoff[0] == 'number':
            data_cutoff = dfrmX.iloc[0:num_cutoff, :]
            other.loc['Other Loops']  = dfrmX.iloc[num_cutoff:, :].sum()
        elif index_cutoff[0] == "percentage":
            data_cutoff = dfrmX[dfrmX[data_column]/data_column_sum > percent_cutoff]
            other.loc['Other Loops']= dfrmX[dfrmX[data_column]/data_column_sum < percent_cutoff].sum()
        else:
            sys.exit("Cutoff must be either 'number' or 'percentage'")

        data_cutoff = data_cutoff.append(other)

        if indexL != []:
            if (indexL[0] == 'total'):
                data_cutoff = pandas.DataFrame(dfrmX.sum())
                data_cutoff.columns = ['total']
                data_cutoff = data_cutoff.transpose()
            else:
                data_cutoff = dfrmX.loc[indexL]
                #data_cutoff = dfrmX.transpose().loc[indexL]


        if total_pct == True:
            slice_this = data_column_pct
        else:
            slice_this = data_column

        #data_cutoff.rename(lambda x: x.strip("[]").replace("Loop at line ", ""))

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------
        
        if (dfrm_all.empty): # Slice out only the % of times
            dfrm_all = data_cutoff[[slice_this]]
        else:
            print('--------------------')
            print(dfrm_all)
            print('--------------------')
            print(data_cutoff[slice_this])
            dfrm_all = pandas.concat([dfrm_all, data_cutoff[slice_this]], axis=1)

    #-------------------------------------------------------
    # Set/sort columns; Sort rows
    #-------------------------------------------------------

    dfrm_all.columns = labelL
    sorted_names = [int(idx) for idx in labelL]
    sorted_names.sort()
    sorted_names = [str(idx) for idx in sorted_names]
    dfrm_all = dfrm_all[sorted_names]

    # Make sure that the data starts with most expensive column first
    dfrm_all = dfrm_all.sort_values(by=sorted_names[0], ascending=False)

    #-------------------------------------------------------
    # Plot
    #-------------------------------------------------------
    
    plot_data = dfrm_all.transpose()
    if kind == 'stack':
        ax = plt.stackplot(list(range(len(sorted_names))),
                           [list(plot_data.iloc[:,a]) for a in range(len(plot_data.columns))],
                           labels=plot_data.columns)
        plt.legend(loc="lower right")
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

if (__name__ == "__main__"):
    sys.exit(main())
