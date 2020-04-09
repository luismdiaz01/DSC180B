import pandas as pd

def get_data(url, outpath = 'raw', title = 'stops'):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    df = pd.read_csv(url)    
    name = './' + outpath + '/'+title + '.csv'
    df.to_csv(name)
    return 'Files saved in ' + outpath  