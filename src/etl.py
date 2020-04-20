# Import libraries/modules
import pandas as pd
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
            df = limit_cols(df, cols[j])
            name = './' + outpath + '/'+title[j] + '-processed.csv'
            df.to_csv(name, index = False)
            print("Downloaded: ",name)        
    return 'Files saved in ' + outpath

# Helper methods
def limit_cols(df, cols):
    return df[cols]     
    