import sys
import json
import shutil
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_viz(inpath='data/cleaned/crime-processed.csv', outpath='viz/EDA/Crime', **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    df = pd.read_csv(inpath)
    crimes_by_year(df, outpath)
    crimes_by_area(df, outpath)
    crimes_by_area_year(df, outpath)
    arrests_by_year(df, outpath)
    arrests_by_area_year(df, outpath)
    crime_types(df, outpath)
    crime_types_by_area(df, outpath)
    crime_types_by_area_year(df, outpath)

def crimes_by_year(df, outpath):
    print('Plotting crimes per year.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('Year').size().plot(kind='bar', ax=ax)
    plt.title('Crimes by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Crimes')
    plt.savefig(os.path.join(outpath, 'crimes_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def crimes_by_area(df, outpath):
    print('Plotting crimes per division.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('AREA NAME').size().plot(kind='bar', ax=ax)
    plt.title('Crimes per Division 2010-2019')
    plt.xlabel('Division')
    plt.ylabel('Number of Crimes')
    plt.savefig(os.path.join(outpath, 'crimes_by_area.png'), bbox_inches='tight')
    print('Complete.')
    
def crimes_by_area_year(df, outpath):
    print('Plotting crimes per division per year.')
    crimes_by_area_year = df.loc[df.Year != 2020].groupby(['Year', 'AREA NAME']).size().unstack().T
    fig=plt.figure(figsize=(22,60))
    fig.tight_layout()
    columns = 1
    rows = 10
    for idx, col in enumerate(crimes_by_area_year.columns):
        fig.add_subplot(rows, columns, idx+1)
        plt.bar(crimes_by_area_year.index, crimes_by_area_year[col])
        plt.title('Number of Crimes in {}'.format(col))
    plt.savefig(os.path.join(outpath, 'crimes_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def arrests_by_year(df, outpath):
    print('Plotting arrest rate over the years.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    df.loc[df.Year != 2020].groupby('Year')['Arrested'].mean().plot(ax=ax)
    plt.title('Arrest Rate wrt. Total Crimes (2010-2019)')
    plt.ylabel('Arrest Rate')
    plt.savefig(os.path.join(outpath, 'arrests_by_year.png'), bbox_inches='tight')
    print('Complete.')
    
def arrests_by_area_year(df, outpath):
    print('Plotting arrest rates per division per year.')
    arrest_by_area_year = df.loc[df.Year != 2020].groupby(['Year', 'AREA NAME'])['Arrested'].mean().unstack()
    fig=plt.figure(figsize=(20,30))
    fig.tight_layout()
    columns = 3
    rows = 7
    for idx, col in enumerate(arrest_by_area_year.columns):
        fig.add_subplot(rows, columns, idx+1)
        plt.plot(arrest_by_area_year[col])
        plt.title('Arrest Rate in {}'.format(col))
    plt.savefig(os.path.join(outpath, 'arrests_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
    
def crime_types(df, outpath):
    print('Plotting distribution of crimes.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    distr = df.loc[df.Year != 2020]['Crime Type'].value_counts(normalize=True)
    plt.pie(distr, labels=distr.index, autopct='%1.1f%%')
    ax.axis('equal')
    plt.title('Distribution of Crime Types (2010-2019)')
    plt.savefig(os.path.join(outpath, 'types_distr.png'), bbox_inches='tight')
    print('Complete.')
    
def crime_types_by_area(df, outpath):
    print('Plotting distribution of crimes per division.')
    distr_area = df.loc[df.Year != 2020].groupby('AREA NAME')['Crime Type'].value_counts(normalize=True).unstack()
    fig = plt.figure(figsize=(22, 8))
    ax = fig.add_subplot(1,1,1)
    stacked = plt.stackplot(distr_area.index, distr_area.T)
    legendProxies = []
    for stack in stacked:
        legendProxies.append(plt.Rectangle((0, 0), 1, 1, fc=stack.get_facecolor()[0]))
    plt.legend(legendProxies, distr_area.columns)
    plt.title('Distribution of Crime Types per Division (2010-2019)')
    plt.savefig(os.path.join(outpath, 'types_distr_by_area.png'), bbox_inches='tight')
    print('Complete.')
    
def crime_types_by_area_year(df, outpath):
    print('Plotting distribution of crimes per division per year.')
    foo = df.loc[df.Year != 2020].groupby(['Year', 'AREA NAME'])['Crime Type'].value_counts(normalize=True).unstack()
    fig=plt.figure(figsize=(22,60))
    fig.tight_layout()
    columns = 1
    rows = 10
    for idx, year in enumerate(range(2010,2020)):
        fig.add_subplot(rows, columns, idx+1)
        stacked = plt.stackplot(foo.loc[year].index, foo.loc[year].T)
        legendProxies = []
        for stack in stacked:
            legendProxies.append(plt.Rectangle((0, 0), 1, 1, fc=stack.get_facecolor()[0]))
        plt.legend(legendProxies, foo.loc[year].columns)
        plt.title('Distribution of Crime Types per Division in {}'.format(year))
    plt.savefig(os.path.join(outpath, 'types_distr_by_area_year.png'), bbox_inches='tight')
    print('Complete.')
