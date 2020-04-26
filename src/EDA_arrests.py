# Import libraries/modules
import sys
import json
import shutil
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geospatial import *

# Global constants

# Main driver functions
def generate_viz(inpath='data/cleaned/arrests-processed.csv', outpath='viz/EDA/Arrests', **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    df = pd.read_csv(inpath)
    describe_null(outpath)
    census = get_census(read_gis())
    rate_by_race(df, census, outpath)
    rate_by_type(df, census, outpath)
    rate_by_charge(df, census, outpath)
    rate_by_race_pp(df, census, outpath)
    rate_by_type_pp(df, census, outpath)
    rate_by_charge_pp(df, census, outpath)

# Helper methods
def describe_null(outpath, rawpath='data/raw/arrests.csv', cleanpath='data/cleaned/arrests-processed.csv', **kwargs):
    raw_data = pd.read_csv(rawpath)
    if 'test_data' in rawpath:
        raw_data.drop(columns=['Unnamed: 0'], inplace=True)
    clean_data = pd.read_csv(cleanpath)
    print('Generating null proportions.')
    raw_data.isna().mean().round(5).to_frame().reset_index().rename(columns={0:'Proportion of Null Values', 'index':'Column Name'}).to_csv(os.path.join(outpath, 'nulls_arrests_raw.csv'), index=False)
    clean_data.isna().mean().round(5).to_frame().reset_index().rename(columns={0:'Proportion of Null Values', 'index':'Column Name'}).to_csv(os.path.join(outpath, 'nulls_arrests_clean.csv'), index=False)
    print('Complete')
    
def rate_by_race(df, census, outpath):
    print('Plotting arrest rates per race.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    rates = df.loc[df.Year!=2020].pivot_table(index=['Year'], columns='Descent Code', values='Total', aggfunc=sum)
    for col in rates:
        rates[col] /= census[col]
    rates.plot(ax=ax)
    plt.title('Arrest Rates by Race')
    plt.xlabel('Year')
    plt.ylabel('Rate')
    plt.savefig(os.path.join(outpath, 'rates_by_race.png'), bbox_inches='tight')
    print('Complete.')
    
def rate_by_type(df, census, outpath):
    print('Plotting arrest rates per crime type.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    AR_type = pd.DataFrame(df.groupby('Arrest Type Code').apply(lambda x: len(x)), columns=['Total Arrests by Type'])
    AR_type['Arrest Rates by Crime Type'] = AR_type['Total Arrests by Type'].apply(lambda x: x / census['Total'])
    AR_type.sort_values(by=['Arrest Rates by Crime Type'], ascending=True)['Arrest Rates by Crime Type'].plot(kind='barh', ax=ax)
    plt.title('Arrest Rates by Crime Type')
    plt.xlabel('Rate')
    plt.ylabel('Arrest Type')
    plt.savefig(os.path.join(outpath, 'rate_by_type.png'), bbox_inches='tight')
    print('Complete.')
    
def rate_by_charge(df, census, outpath):
    print('Plotting arrest rates per charge type.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    AR_type_2 = pd.DataFrame(df.groupby('Charge Group Description').apply(lambda x: len(x)), columns=['Total Arrests by Charge Group Description'])
    AR_type_2['Arrest Rates by Charge Group Description'] = AR_type_2['Total Arrests by Charge Group Description'].apply(lambda x: x / census['Total'])
    AR_type_2.sort_values(by=['Arrest Rates by Charge Group Description'], ascending=True)['Arrest Rates by Charge Group Description'].plot(kind='barh', ax=ax)
    plt.title('Arrest Rates by Charge')
    plt.xlabel('Rate')
    plt.ylabel('Charge')
    plt.savefig(os.path.join(outpath, 'rate_by_charge.png'), bbox_inches='tight')
    print('Complete.')
    
def get_gb(df, col):
    return df.groupby(['predPol Deployed', col])

def make_pivot(df, census, col, race=False):
    def arrest_rates():
        return lambda x: sum(x) / census['Total']

    return pd.pivot_table(df, values='Total', index=[col],
                    columns=['predPol Deployed'], aggfunc=arrest_rates())

def rate_by_race_pp(df, census, outpath):
    print('Plotting arrest rates per race.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    res = make_pivot(df, census, 'Descent Code', race=True)
    res.plot(kind='barh')
    plt.title('Arrest Rates by Race in PredPol/non-PredPol Areas')
    plt.xlabel('Rate')
    plt.ylabel('Race')
    plt.savefig(os.path.join(outpath, 'rate_by_race_pp.png'), bbox_inches='tight')
    print('Complete.')
    
def rate_by_type_pp(df, census, outpath):
    print('Plotting arrest rates per crime type.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    res = make_pivot(df, census, 'Arrest Type Code')
    res.plot(kind='barh')
    plt.title('Arrest Rates by Crime Type in PredPol/non-PredPol Areas')
    plt.xlabel('Rate')
    plt.ylabel('Type')
    plt.savefig(os.path.join(outpath, 'rate_by_type_pp.png'), bbox_inches='tight')
    print('Complete.')
    
def rate_by_charge_pp(df, census, outpath):
    print('Plotting arrest rates per charge type.')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    res = make_pivot(df, census, 'Charge Group Description')
    res.plot(kind='barh')
    plt.title('Arrest Rates by Charge in PredPol/non-PredPol Areas')
    plt.xlabel('Rate')
    plt.ylabel('Charge')
    plt.savefig(os.path.join(outpath, 'rate_by_charge_pp.png'), bbox_inches='tight')
    print('Complete.')
    