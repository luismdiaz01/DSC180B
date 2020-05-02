# Import libraries/modules
import sys
import json
import shutil
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    stops_race(df, outpath, False)
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
    df.loc[(df.Year!=2020)].groupby(['Reassigned Officer','Year']).size().unstack().T.plot(kind='bar', ax=ax)
    plt.title('Stops by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Stops')
    plt.savefig(os.path.join(outpath, 'stops_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv(df, outpath):
    print('Plotting stops per division.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    stops_div = df.loc[(df.Year != 2020)].groupby(['Reassigned Officer','Stop Division']).size().unstack().T
    normalized = stops_div/stops_div.sum()
    normalized.plot(kind='barh', ax=ax)
    plt.title('Proportion of Stops per Division 2010-2019')
    plt.xlabel('Proportion')
    plt.ylabel('Stop Division')
    plt.savefig(os.path.join(outpath, 'stops_by_area.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv_year(df, outpath):
    print('Plotting stops per division per year.')
    fig = plt.figure(figsize=(10, 12))
    i = 1
    for j in [True, False]:
        ax = fig.add_subplot(2,1,i)
        stps_yr_div_false = df.loc[(df.Year != 2020)&(df['Reassigned Officer']==j)&(df.Year>=2013)].groupby(['Year','Stop Division']).size().unstack().T
        norm = stps_yr_div_false/stps_yr_div_false.sum()
        sns.heatmap(norm, annot=False, xticklabels=True, yticklabels=True, ax=ax)
        if j:
            plt.title('Proportion of Stops per Division by Reassigned Officers')
        else:
            plt.title('Proportion of Stops per Division by Non-Reassigned Officers')
        i+=1
    plt.savefig(os.path.join(outpath, 'stops_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_race(df, outpath, reassigned=True):
    print('Plotting distribution of stops Races.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    distr = df.loc[(df.Year != 2020)&(df['Reassigned Officer']==reassigned)&(df.Year>=2013)]['Descent Description'].value_counts(normalize=True)
    patches, texts = plt.pie(distr)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(distr.index, distr)]
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, distr),
                                          key=lambda x: x[2],
                                          reverse=True))
    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
    ax.axis('equal')
    plt.title('Racial Distribution of Stops by Reassigned Officers')
    if not reassigned:
        plt.title('Racial Distribution of Stops by Non-Reassigned Officers')
    plt.savefig(os.path.join(outpath, 'race_distr_{}.png'.format(reassigned)), bbox_inches='tight')
    print('Complete.')
    
def stops_post(df, outpath):
    print('Plotting distribution of post stops.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year!=2020].groupby('Reassigned Officer')['Post Stop Activity Indicator'].value_counts(normalize=True).unstack().T.plot(kind='bar', ax=ax)
    plt.title('Distribution of Stops with Further Actions (2010-2019)')
    plt.xlabel('Post Stop Activity Indicator')
    plt.ylabel('Proportion')
    plt.savefig(os.path.join(outpath, 'ps_distr.png'), bbox_inches='tight')
    print('Complete.')
