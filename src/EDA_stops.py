import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def generate_viz(inpath='data/cleaned/stops-processed.csv', outpath='viz/EDA/Stops', **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    df = pd.read_csv(inpath)
    stops_by_year(df, outpath)
    stops_by_offdiv(df, outpath)
    stops_by_offdiv_year(df, outpath)
    stops_race(df, outpath)
    stops_post(df, outpath)

def stops_by_year(df, outpath):
    print('Plotting stops per year.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('Year').size().plot(kind='barh', ax=ax)
    plt.title('Stops by Year')
    plt.xlabel('Number of Stops')
    plt.ylabel('Year')
    plt.savefig(os.path.join(outpath, 'stops_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv(df, outpath):
    print('Plotting stops per officer division.')
    fig = plt.figure(figsize=(10, 20))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('Division Description 1').size().plot(kind='barh', ax=ax)
    plt.title('Stops per Division 2010-2019')
    plt.xlabel('Number of Stops')
    plt.ylabel('Division')
    plt.savefig(os.path.join(outpath, 'stops_by_area.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv_year(df, outpath):
    print('Plotting stops per division per year.')
    stops_by_area_year = df.loc[df.Year != 2020].groupby(['Year', 'Division Description 1']).size().unstack().T
    fig=plt.figure(figsize=(10,250))
    fig.tight_layout()
    columns = 1
    rows = 15
    for idx, col in enumerate(stops_by_area_year.columns):
        fig.add_subplot(rows, columns, idx+1)
        plt.barh(stops_by_area_year.index, stops_by_area_year[col])
        plt.title('Number of Stops in {}'.format(col))
    plt.savefig(os.path.join(outpath, 'stops_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_race(df, outpath):
    print('Plotting distribution of stops Races.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    distr = df.loc[df.Year != 2020]['Descent Description'].value_counts(normalize=True)
    patches, texts = plt.pie(distr)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(distr.index, distr)]
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, distr),
                                          key=lambda x: x[2],
                                          reverse=True))
    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
    ax.axis('equal')
    plt.title('Distribution of Races (2010-2019)')
    plt.savefig(os.path.join(outpath, 'race_distr.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_post(df, outpath):
    print('Plotting distribution of post stops.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020]['Post Stop Activity Indicator'].value_counts(normalize=True).plot(kind='barh', ax=ax)
    plt.title('Distribution of Post Stops (2010-2019)')
    plt.xlabel('Proportion')
    plt.ylabel('Post Stop')
    plt.savefig(os.path.join(outpath, 'ps_distr.png'), bbox_inches='tight')
    print('Complete.')
