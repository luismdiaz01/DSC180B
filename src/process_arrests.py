# Import libraries/modules
import pandas as pd
import os

# Global constants

# Main driver functions
def process_arrests(inpath, outpath, cols, title='arrests', **kwargs):
    print('Processing Arrests data.')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    print('Reading raw data.')
    arrests = transform_arrests(pd.read_csv(inpath).drop(columns=['Unnamed: 0']), cols)
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
    df['predPol Deployed'] = df.apply(get_pred, axis=1)
    df['Total'] = pd.Series([1] * df.shape[0])
    return limit_cols(df, cols)