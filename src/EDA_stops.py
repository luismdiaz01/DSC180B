# Import libraries/modules
import sys
import json
import shutil
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Global constants
DIVS = ['MISSION', 'WEST LA','SEVENTY-SEVENTH', 'NORTH EAST', 'TOPANGA', 'WEST VALLEY','OLYMPIC', 'SOUTH EAST', 'SOUTH WEST', 
 'FOOTHILL','NEWTON', 'RAMPART', 'HOLLYWOOD', 'NORTH HOLLYWOOD', 'WILSHIRE','DEVONSHIRE', 'VAN NUYS','CENTRAL', 'PACIFIC', 
 'HOLLENBECK', 'HARBOR']

# Main driver functions
def generate_viz(inpath='data/cleaned/stops-processed.csv', outpath='viz/EDA/Stops', **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    df = pd.read_csv(inpath)
    describe_null(outpath)
    stops_by_year(df, outpath)
    stops_by_offdiv(df, outpath)
    stops_by_offdiv_year(df, outpath)
    stops_race(df, outpath)
    stops_post(df, outpath)

# Helper methods
def describe_null(outpath, rawpath='data/raw/stops.csv', cleanpath='data/cleaned/stops-processed.csv', **kwargs):
    raw_data = pd.read_csv(rawpath)
    if 'test_data' in rawpath:
        raw_data.drop(columns=['Unnamed: 0'], inplace=True)
    clean_data = pd.read_csv(cleanpath)
    print('Generating null proportions.')
    raw_data.isna().mean().round(5).to_frame().reset_index().rename(columns={0:'Proportion of Null Values', 'index':'Column Name'}).to_csv(os.path.join(outpath, 'nulls_stops_raw.csv'), index=False)
    clean_data.isna().mean().round(5).to_frame().reset_index().rename(columns={0:'Proportion of Null Values', 'index':'Column Name'}).to_csv(os.path.join(outpath, 'nulls_stops_clean.csv'), index=False)
    print('Complete')
    
def stops_by_year(df, outpath):
    print('Plotting stops per year.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[(df.Year != 2020) & (df['Division Description 1'].isin(DIVS))].groupby('Year').size().plot(kind='barh', ax=ax)
    plt.title('Stops by Year')
    plt.xlabel('Number of Stops')
    plt.ylabel('Year')
    plt.savefig(os.path.join(outpath, 'stops_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv(df, outpath):
    print('Plotting stops per officer division.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[(df.Year != 2020) & (df['Division Description 1'].isin(DIVS))].groupby('Division Description 1').size().plot(kind='barh', ax=ax)
    plt.title('Stops per Division 2010-2019')
    plt.xlabel('Number of Stops')
    plt.ylabel('Division')
    plt.savefig(os.path.join(outpath, 'stops_by_area.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv_year(df, outpath):
    print('Plotting stops per division per year.')
    stops_by_area_year = df.loc[(df.Year != 2020) & (df['Division Description 1'].isin(DIVS))].groupby(['Year', 'Division Description 1']).size().unstack().T
    fig=plt.figure(figsize=(10,80))
    fig.tight_layout()
    columns = 1
    rows = 15
    for idx, col in enumerate(stops_by_area_year.columns):
        fig.add_subplot(rows, columns, idx+1)
        plt.barh(stops_by_area_year.index, stops_by_area_year[col])
        plt.title('Number of Stops in {}'.format(col))
        plt.xlabel('Number of Stops')
        plt.ylabel('Division')
    plt.savefig(os.path.join(outpath, 'stops_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_race(df, outpath):
    print('Plotting distribution of stops Races.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    distr = df.loc[(df.Year != 2020) & (df['Division Description 1'].isin(DIVS))]['Descent Description'].value_counts(normalize=True)
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
    df.loc[(df.Year != 2020) & (df['Division Description 1'].isin(DIVS))]['Post Stop Activity Indicator'].value_counts(normalize=True).plot(kind='barh', ax=ax)
    plt.title('Distribution of Stops with Further Actions (2010-2019)')
    plt.xlabel('Proportion')
    plt.ylabel('Post Stop')
    plt.savefig(os.path.join(outpath, 'ps_distr.png'), bbox_inches='tight')
    print('Complete.')
