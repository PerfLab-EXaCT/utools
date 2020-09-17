#!/usr/bin/env python

import sys
import os

import pandas as pd
import matplotlib.pyplot as plt

#****************************************************************************

# Anything less than this %value will be grouped into "tiny loops" slice
percent_cutoff = 0.05

#****************************************************************************

def main():
    #assert(len(sys.argv) > 1)
    #csv_pathL = sys.argv[1:]

    csv_pathL = [ './0data/advanced-hotspots.csv',
                  './0data/progression/1696.csv' ]

    for path in csv_pathL:
        plot_pie(path)
        plt.show()

#****************************************************************************

def plot_pie(csv_path):
    """
    Plot a donut graph representing in which loops time is being spent
    """
    data = pd.read_csv(csv_path)
    
    time_total = data[['CPU Time']].sum()[0]
    
    data.insert(loc=2, column='% of Total', value=data['CPU Time']/time_total*100)
    data_cutoff = data[data['CPU Time']/time_total > percent_cutoff]

    other = data[data['CPU Time']/time_total < percent_cutoff].sum()
    other['Function'] = 'Tiny Loops'
    data_cutoff = data_cutoff.append(other, ignore_index=True).sort_values(by='CPU Time', ascending=False)
    func_times = data_cutoff[['Function', '% of Total']]
    labels=func_times['Function']
    labels_trim= labels.map(lambda x: x.strip("[]").replace("Loop at line ", ""))
    #pie = plt.pie(func_times['% of Total'], labels=labels_trim, autopct='%1.1f%%', startangle=90, labeldistance=0.8)
    pie = plt.pie(func_times['% of Total'], autopct='%1.1f%%', startangle=90, labeldistance=0.8)
    plt.legend(pie[0], labels_trim, loc="best")

    #draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.75,color='white', fc='white',linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)


#****************************************************************************

if (__name__ == "__main__"):
    sys.exit(main())
