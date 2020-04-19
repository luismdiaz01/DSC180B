import pandas as pd
import os

PETTY = ['petty','violation','yield','dumping','pickpocket','replica firearms',]

MISDEMEANOR = ['simple assault','misdeameanor','misdemeanor','shoplift','reckless driving','abortion','inciting','disperse',
       'beastiality','disrupt school', 'drugs, to a minor','threat','trespassing','lewd','brandish','battery with sex',
      'battery police','contempt of court','indecent','resisting arrest','bomb scare','peeping','prowler','$950 & under',
      'document worthless','motorized',]

FELONY = ['felony','aggravated assault','grand','train wreck','manslaughter','incest','lynching','bribery','robbery','rape','child',
      'sex,unlawful','arson','foreign object','extortion','dwelling','kidnap','assault with dead','$950.01 & over','traffick',
      'pimping','pandering','homicide','chld']

WOBBLER = ['dwoc','bigamy','theft','telephone property','conspiracy','burglary','discharge','stalk','oral copulation','throwing',
      'sodomy','computer','cruelty','false imprisonment','counterfeit','false police report','battery on a firefighter',
      'shots fired at moving','weapons possession','stolen','snatch']

WOBBLETTE = ['disturbing',]

def classify_crm_cd_desc(x):
    lowered = x.lower()
    if any(substring in lowered for substring in PETTY):
        return 'Infraction'
    elif any(substring in lowered for substring in MISDEMEANOR):
        return 'Misdemeanor'
    elif any(substring in lowered for substring in FELONY):
        return 'Felony'
    elif any(substring in lowered for substring in WOBBLER):
        return 'Wobbler'
    elif any(substring in lowered for substring in WOBBLETTE):
        return 'Wobblette'
    else:
        return 'Others'

def limit_cols(df, cols):
    return df[cols]

def arrest(x):
    if 'arrest' in x.lower():
        return 1
    return 0

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

def process_crimes(inpath, outpath, cols, title='crime', **kwargs):
    print('Processing Crimes data.')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    print('Reading raw data.')
    crimes = pd.read_csv(inpath, parse_dates=[2])
    crimes['Year'] = crimes['Date Rptd'].dt.year  
    print('Adding column: Arrested.')
    crimes['Arrested'] = crimes['Status Desc'].apply(arrest)
    print('Adding column: Crime Type.')
    crimes['Crime Type'] = crimes['Crm Cd Desc'].apply(classify_crm_cd_desc)
    crimes = limit_cols(crimes, cols)
    name = os.path.join(outpath, '{}-processed.csv'.format(title))
    print('Exporting as csv.')
    crimes.to_csv(name, index=False)
    print('Processed Crimes data.')