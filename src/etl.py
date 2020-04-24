# Import libraries/modules
import pandas as pd
import numpy as np
import os
from process_crimes import process_crimes

# Global constants

# Main driver functions
def get_data(urls, outpath = 'data/raw', title = ['stops', 'arrests', 'crime']):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for j, i in enumerate(urls):    
        df = pd.read_csv(i)    
        name = './' + outpath + '/'+title[j] + '.csv'
        df.to_csv(name, index = False)
        print("Downloaded: ",name)
    return 'Files saved in ' + outpath

def process(paths, cols, outpath = 'data/cleaned' ,title = ['stops', 'arrests', 'crime'], **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for j,i in enumerate(paths):
        if title[j] == 'crime':
            process_crimes(i, outpath, cols[j])
        else:
            df = pd.read_csv(i)
            if title[j] == 'stops':
                df = run_cleaning(df)
            df = limit_cols(df, cols[j])
            name = './' + outpath + '/'+title[j] + '-processed.csv'
            df.to_csv(name, index = False)
            print("Downloaded: ",name)        
    return 'Files saved in ' + outpath

# Helper methods
def limit_cols(df, cols):
    return df[cols]

def run_cleaning(df, **kwargs):
    df = clean_divisions(df)
    df = add_year(df)
    df = df.loc[df['Year'] != 1900]
    df['Reporting District'] = impute_districts(df['Reporting District'])
    df['Officer 1 Serial Number'] = df['Officer 1 Serial Number'].fillna(0).astype(int)
    
    return df.dropna(subset=['Stop Date', 'Reporting District', 'Post Stop Activity Indicator'])

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
    