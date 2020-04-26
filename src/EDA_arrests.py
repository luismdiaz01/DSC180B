# Import libraries/modules
import sys
import json
import shutil
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Global constants
RACE_MAP = {'B': 'Black','H': 'Hispanic/Latin/Mexican','O': 'Other','W': 'White','A': 'Other Asian','K': 'Korean','F': 'Filipino','V': 'Vietnamese','G': 'Guamanian','C': 'Chinese','X': 'Unknown','P': 'Pacific Islander','S': 'Samoan','J': 'Japanese','I': 'American Indian/Alaskan Native','U': 'Hawaiian','L': 'Laotian','Z': 'Asian Indian','D': 'Cambodian'}

TYPE_MAP = {'D': 'Dependent', 'F': 'Felony', 'I': 'Infraction', 'M': 'Misdemeanor', 'O': 'Other'}

# Main driver functions
def generate_viz(inpath='data/cleaned/arrests-processed.csv', outpath='viz/EDA/Arrests', **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    df = pd.read_csv(inpath)
    describe_null(outpath)
    rate_by_race(df, outpath)
    rate_by_type(df, outpath)
    rate_by_charge(df, outpath)
    rate_by_race_pp(df, outpath)
    rate_by_type_pp(df, outpath)
    rate_by_charge_pp(df, outpath)

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
    
def rate_by_race(df, outpath):
    print('Plotting arrest rates per race.')
#     fig = plt.figure(figsize=(10, 6))
#     ax = fig.add_subplot(1,1,1)
    AR_race = pd.DataFrame(df.loc[df.Year != 2020].groupby('Descent Code').apply(lambda x: len(x) / df.shape[0]), columns=['Arrest Rate'])
    AR_race.index = AR_race.index.map(lambda x: RACE_MAP[x])
    AR_race.to_csv(os.path.join(outpath, 'rate_by_race.csv'))
#     AR_race.plot(kind='barh', ax=ax)
#     plt.title('Arrest Rates by Race')
#     plt.xlabel('Rate')
#     plt.ylabel('Race')
#     plt.savefig(os.path.join(outpath, 'rates_by_race.png'), bbox_inches='tight')
    print('Complete.')
    
def rate_by_type(df, outpath):
    print('Plotting arrest rates per crime type.')
    AR_type = pd.DataFrame(df.groupby('Arrest Type Code').apply(lambda x: len(x)), columns=['Total Arrests by Type'])
    AR_type['Arrest Rates by Crime Type'] = AR_type['Total Arrests by Type'].apply(lambda x: x / df.shape[0])
    AR_type['Crime Description'] = AR_type.index.map(lambda x: TYPE_MAP[x])
    AR_type.sort_values(by=['Arrest Rates by Crime Type'], ascending=False).to_csv(os.path.join(outpath, 'rate_by_type.csv'))
    print('Complete.')
    
def rate_by_charge(df, outpath):
    print('Plotting arrest rates per charge type.')
    AR_type_2 = pd.DataFrame(df.groupby('Charge Group Description').apply(lambda x: len(x)), columns=['Total Arrests by Charge Group Description'])
    AR_type_2['Arrest Rates by Charge Group Description'] = AR_type_2['Total Arrests by Charge Group Description'].apply(lambda x: x / df.shape[0])
    AR_type_2.sort_values(by=['Arrest Rates by Charge Group Description'], ascending=False).to_csv(os.path.join(outpath, 'rate_by_charge.csv'))
    print('Complete.')
    
def get_gb(df, col):
    return df.groupby(['predPol Deployed', col])

def make_pivot(df, col):
    def arrest_rates():
        return lambda x: sum(x) / df.shape[0]

    return pd.pivot_table(df, values='Total', index=[col],
                    columns=['predPol Deployed'], aggfunc=arrest_rates())

def rate_by_race_pp(df, outpath):
    print('Plotting arrest rates per race.')
    res = make_pivot(df, 'Descent Code')
    res.index = res.index.map(lambda x: RACE_MAP[x])
    res.to_csv(os.path.join(outpath, 'rate_by_race_pp.csv'))
    print('Complete.')
    
def rate_by_type_pp(df, outpath):
    print('Plotting arrest rates per crime type.')
    res = make_pivot(df, 'Arrest Type Code')
    res.index = res.index.map(lambda x: TYPE_MAP[x])
    res.to_csv(os.path.join(outpath, 'rate_by_type_pp.csv'))
    print('Complete.')
    
def rate_by_charge_pp(df, outpath):
    print('Plotting arrest rates per charge type.')
    res = make_pivot(df, 'Charge Group Description')
    res.to_csv(os.path.join(outpath, 'rate_by_charge_pp.csv'))
    print('Complete.')
        