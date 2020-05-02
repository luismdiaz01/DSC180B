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

# Main driver functions
def generate_viz(inpath='data/cleaned/crime-processed.csv', outpath='viz/EDA/Crime', **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    df = pd.read_csv(inpath)
    describe_null(outpath)
    crimes_by_year(df, outpath)
    crimes_by_area_year(df, outpath)
    arrests_by_year(df, outpath)
    arrests_by_area_year(df, outpath)
    crime_sev(df, outpath)
    crime_tp(df, outpath)

# Helper methods
def describe_null(outpath, rawpath='data/raw/crime.csv', cleanpath='data/cleaned/crime-processed.csv', **kwargs):
    raw_data = pd.read_csv(rawpath)
    if 'test_data' in rawpath:
        raw_data.drop(columns=['Unnamed: 0'], inplace=True)
    clean_data = pd.read_csv(cleanpath)
    print('Generating null proportions.')
    raw_data.isna().mean().round(5).to_frame().reset_index().rename(columns={0:'Proportion of Null Values', 'index':'Column Name'}).to_csv(os.path.join(outpath, 'nulls_crime_raw.csv'), index=False)
    clean_data.isna().mean().round(5).to_frame().reset_index().rename(columns={0:'Proportion of Null Values', 'index':'Column Name'}).to_csv(os.path.join(outpath, 'nulls_crime_clean.csv'), index=False)
    print('Complete')

def crimes_by_year(df, outpath):
    print('Plotting crimes per year.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[(df.Year!=2020)].groupby(['PredPol Deployed','Year']).size().unstack().T.plot(kind='bar')
    plt.title('Number of Crimes by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Crimes')
    plt.savefig(os.path.join(outpath, 'crimes_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def crimes_by_area_year(df, outpath):
    print('Plotting crimes per division per year.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    heat = df.loc[(df.Year!=2020)].groupby(['Year','AREA NAME']).size().unstack().T
    sns.heatmap(heat, annot=False, xticklabels=True, yticklabels=True, ax=ax)
    plt.title('Number of crimes per Division (2010-2019)')
    plt.ylabel('Division')
    plt.savefig(os.path.join(outpath, 'crimes_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def arrests_by_year(df, outpath):
    print('Plotting arrest proportion over the years.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[(df.Year!=2020)].groupby(['PredPol Deployed','Year'])['Arrested'].mean().unstack().T.plot(kind='bar')
    plt.title('Proportion of Crimes Resulting in Arrests (2010-2019)')
    plt.ylabel('Proportion')
    plt.savefig(os.path.join(outpath, 'arrests_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def arrests_by_area_year(df, outpath):
    print('Plotting arrest proportion per division per year.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    heat = df.loc[(df.Year!=2020)].groupby(['Year','AREA NAME'])['Arrested'].mean().unstack().T
    sns.heatmap(heat, annot=False, xticklabels=True, yticklabels=True)
    plt.title('Proportion of Crimes Resulting in Arrests per Division')
    plt.savefig(os.path.join(outpath, 'arrests_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def crime_sev(df, outpath):
    print('Plotting distribution of crime charge.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('PredPol Deployed')['Crime Charge'].value_counts(normalize=True).unstack().T.plot(kind='barh', ax=ax)
    plt.xlabel('Proportion')
    plt.title('Distribution of Crime Charge (2010-2019)')
    plt.savefig(os.path.join(outpath, 'sev_distr.png'), bbox_inches='tight')
    print('Complete.')
    
def crime_tp(df, outpath):
    print('Plotting distribution of crime types.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('PredPol Deployed')['Crime Type'].value_counts(normalize=True).unstack().T.plot(kind='barh', ax=ax)
    plt.xlabel('Proportion')
    plt.title('Distribution of Crime Types (2010-2019)')
    plt.savefig(os.path.join(outpath, 'tp_distr.png'), bbox_inches='tight')
    print('Complete.')
