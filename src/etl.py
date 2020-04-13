import pandas as pd
import os

def limit_cols(df, cols):
    return df[cols]

def get_data(urls, outpath = 'data/raw', title = ['stops', 'arrests', 'crime']):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for j, i in enumerate(urls):    
        df = pd.read_csv(i)    
        name = './' + outpath + '/'+title[j] + '.csv'
        df.to_csv(name, index = False)
        print("Downloaded: ",name)
    return 'Files saved in ' + outpath     
    
def process(paths, outpath = 'data/cleaned' ,title = ['stops', 'arrests', 'crime'], **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for j,i in enumerate(paths):
        df = pd.read_csv(i)
        if 'cols' in kwargs:
            df = limit_cols(df, cols[j])
        name = './' + outpath + '/'+title[j] + '-processed.csv'
        df.to_csv(name, index = False)
        print("Downloaded: ",name)        
    return 'Files saved in ' + outpath   