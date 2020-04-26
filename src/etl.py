# Import libraries/modules
import pandas as pd
import numpy as np
import os
from process_crimes import process_crimes
from process_arrests import process_arrests
from process_stops import process_stops

# Global constants

# Main driver functions
def get_data(urls, outpath = 'data/raw', title = ['stops', 'arrests', 'crime'], **kwargs):
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
        elif title[j] == 'arrests':
            process_arrests(i, outpath, cols[j])
        else:
            process_stops(i, outpath, cols[j])       
    return 'Files saved in ' + outpath

# Helper methods
    