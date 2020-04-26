# Import libraries/modules
import pandas as pd
import os

# Global constants
RACE_MAP = {'B': 'Black or African American','H': 'Hispanic or Latino','O': 'Other','W': 'White','A': 'Asian','K': 'Asian','F': 'Asian','V': 'Asian','G': 'Native Hawaiian and Other Pacific Islander','C': 'Asian','X': 'Other','P': 'Native Hawaiian and Other Pacific Islander','S': 'Native Hawaiian and Other Pacific Islander','J': 'Asian','I': 'American Indian and Alaska Native','U': 'Native Hawaiian and Other Pacific Islander','L': 'Asian','Z': 'Asian','D': 'Asian'}

TYPE_MAP = {'D': 'Dependent', 'F': 'Felony', 'I': 'Infraction', 'M': 'Misdemeanor', 'O': 'Other'}

# Main driver functions
def process_arrests(inpath, outpath, cols, title='arrests', **kwargs):
    print('Processing Arrests data.')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    print('Reading raw data.')
    try:
        arrests = transform_arrests(pd.read_csv(inpath).drop(columns=['Unnamed: 0']), cols)
    except:
        arrests = transform_arrests(pd.read_csv(inpath), cols)
    name = os.path.join(outpath, '{}-processed.csv'.format(title))
    print('Exporting as csv.')
    arrests.to_csv(name, index=False)
    print('Downloaded: {}'.format(name))
    
# Helper methods
def get_pred(row):
    # check year
    yr = row.loc['Year']
    if yr < 2013:
        return 0
    elif yr >= 2015:
        return 1
    else:
        # check area
        ar = row.loc['Area Name']
        areas = ['North Hollywood', 'Sothwest', 'Foothill']
        if ar in areas:
            return 1
        else:
            return 0

def limit_cols(df, cols):
    return df[cols]

def transform_arrests(df, cols):
    print('Processing Arrests data.')
    df['Arrest Date'] = pd.to_datetime(df['Arrest Date'])
    df['Year'] = df['Arrest Date'].apply(lambda x: x.year)
    df['Descent Code'] = df['Descent Code'].map(RACE_MAP)
    df['Arrest Type Code'] = df['Arrest Type Code'].map(TYPE_MAP)
    df['predPol Deployed'] = df.apply(get_pred, axis=1)
    df['Total'] = pd.Series([1] * df.shape[0])
    return limit_cols(df, cols)
