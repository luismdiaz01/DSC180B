# Import libraries/modules
import pandas as pd
import numpy as np
import os
from geospatial import *

# Global constants
DIV_MAP = {
    "WEST LOS ANGELES": "WEST LA",
    "77TH STREET": "SEVENTY-SEVENTH",
    "NORTHEAST": "NORTH EAST",
    "SOUTHWEST": "SOUTH WEST",
    "SOUTHEAST": "SOUTH EAST"
}

# Main driver functions
def process_stops(inpath, outpath, cols, title='stops', **kwargs):
    print('Processing Stops data.')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    print('Reading raw data.')
    stops = run_cleaning(pd.read_csv(inpath), cols)
    name = os.path.join(outpath, '{}-processed.csv'.format(title))
    print('Exporting as csv.')
    stops.to_csv(name, index=False)
    print('Downloaded: {}'.format(name))
    
# Helper methods
def run_cleaning(df, cols, **kwargs):
    print('Reading raw data.')
    df = clean_divisions(df)
    df = add_year(df)
    df = df.loc[(df['Year'] != 1900)]
    df['Reporting District'] = impute_districts(df['Reporting District'])
    df['Officer 1 Serial Number'] = df['Officer 1 Serial Number'].fillna(0).astype(int)
    df = get_stop_div(df, get_gis())
    df['Reassigned Officer'] = df['Stop Division'] == df['Division Description 1']
    return limit_cols(df.dropna(subset=['Stop Division','Stop Date', 'Reporting District', 'Post Stop Activity Indicator']), cols)

def limit_cols(df, cols):
    return df[cols]

def add_year(df, date = 'Stop Date'):
    df['Year'] = pd.to_datetime(df[date]).dt.year
    return df

def clean_divisions(df, make_dict = True, divs = ['Officer 1 Division Number', 'Officer 2 Division Number'], desc = ['Division Description 1', 'Division Description 2'], name = 'div.txt'):
    for j in desc:    
        if j == 'Division Description 1':
            df = df.dropna(subset = [j])
        df = df[~(df[j] =='**UNUSED PIU CODE**')]
    for i in divs:
        ser = df[i]
        ser = ser.astype(str)
        ser = ser.replace('0','00')
        ser = ser.str.replace('.0','', regex = False)
        ser = ser.str.lstrip('0')
        ser = ser.replace('', '0')
        ser = pd.to_numeric(df[i], errors = 'ignore')
        df[i] = ser
    if make_dict:
        df[['Officer 1 Division Number','Division Description 1']].drop_duplicates().sort_values('Officer 1 Division Number').to_csv(name, header=None, index=None, sep=' ', mode='a')
    return df

def is_int(x):
    try:
        x = int(x)
        return True
    except:
        return False
    
def rand_prob(x, start_09):
    try:
        return int(x)
    except:
        if str(x).startswith('9'):
            return 9999
        elif str(x).startswith('09'):
            return np.random.choice(start_09.index, p=start_09.values)
        return np.nan
    
def impute_districts(col):
    clean = col.loc[col.apply(is_int)]
    start_09 = clean.loc[clean.astype(str).str.startswith('09')].value_counts(normalize=True)
    return col.apply(rand_prob, start_09=start_09)

def get_gis():
    df = read_gis()
    df = df[['REPDIST','APREC']].drop_duplicates()
    return df

def get_stop_div(df, gis):
    df['Stop Division'] = df[['Reporting District']].merge(gis, left_on='Reporting District', right_on='REPDIST')['APREC'].fillna('UNK')
    df['Stop Division'] = df['Stop Division'].replace(DIV_MAP)
    return df
