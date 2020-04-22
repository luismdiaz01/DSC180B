import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def generate_viz(inpath='data/cleaned/stops-processed.csv', outpath='viz/EDA/Stops', **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    df = pd.read_csv(inpath)
    stops_by_year(df, outpath)
    stops_by_area(df, outpath)
    stops_by_offdiv(df, outpath)
    stops_by_offdiv_year(df, outpath)
    stops_race(df, outpath)
    stops_post(df, outpath)

def stops_by_year(df, outpath):
    print('Plotting stops per year.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('Year').size().plot(kind='bar', ax=ax)
    plt.title('Stops by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Stops')
    plt.savefig(os.path.join(outpath, 'stops_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_area(df, outpath):
    print('Plotting stops per reporting district.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('Officer 1 Division Number').size().plot(kind='bar', ax=ax)
    plt.title('Stops per Division 2010-2019')
    plt.xlabel('Division')
    plt.ylabel('Number of Stops')
    plt.savefig(os.path.join(outpath, 'stops_by_area.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv(df, outpath):
    print('Plotting stops per officer division.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('Reporting District').size().plot(kind='bar', ax=ax)
    plt.title('Stops per Division 2010-2019')
    plt.xlabel('Division')
    plt.ylabel('Number of Stops')
    plt.savefig(os.path.join(outpath, 'stops_by_area.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_by_offdiv_year(df, outpath):
    print('Plotting stops per division per year.')
    stops_by_area_year = df.loc[df.Year != 2020].groupby(['Year', 'Officer 1 Division Number']).size().unstack().T
    fig=plt.figure(figsize=(22,60))
    fig.tight_layout()
    columns = 1
    rows = 15
    for idx, col in enumerate(stops_by_area_year.columns):
        fig.add_subplot(rows, columns, idx+1)
        plt.bar(stops_by_area_year.index, stops_by_area_year[col])
        plt.title('Number of Stops in {}'.format(col))
    plt.savefig(os.path.join(outpath, 'stops_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_race(df, outpath):
    print('Plotting distribution of stops Races.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    distr = df.loc[df.Year != 2020]['Descent Code'].value_counts(normalize=True)
    plt.pie(distr, labels=distr.index, autopct='%1.1f%%')
    ax.axis('equal')
    plt.title('Distribution of Races (2010-2019)')
    plt.savefig(os.path.join(outpath, 'race_distr.png'), bbox_inches='tight')
    print('Complete.')
    
def stops_post(df, outpath):
    print('Plotting distribution of post stops.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020]['Post Stop Activity Indicator'].value_counts(normalize=True).plot(kind='bar', ax=ax)
    plt.title('Distribution of Post Stopss (2010-2019)')
    plt.xlabel('Post Stop')
    plt.ylabel('Proportion')
    plt.savefig(os.path.join(outpath, 'ps_distr.png'), bbox_inches='tight')
    print('Complete.')
