# Import libraries/modules
import pandas as pd
import os

# Global constants
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

PERSONAL = ['assault','battery','arson','abuse','kidnap','rape','homicide','manslaughter','brandish','child','chld','sex',
           'oral','stalk','traffick','discharge','peep','pimp','abortion','lynch']

PROPERTY = ['theft','burglary','larceny','robbery','shoplift','vandalism','stolen','trespass','snatch','steal','throwing',
           'pickpocket','dumping','vehicle','dwelling','prowler','wreck','till','property',]

INCHOATE = ['attempt','conspiracy','contribut','threat','scare','bribe','pandering','possession']

STATUTORY = ['driv','drunk','drug','yield','disrupt','violation','lewd','indecent','contempt','disturb','incit','resist']

# Main driver functions
def process_crimes(inpath, outpath, cols, title='crime', **kwargs):
    print('Processing Crimes data.')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    print('Reading raw data.')
    crimes = transform_crimes(pd.read_csv(inpath, parse_dates=[1]), cols)
    name = os.path.join(outpath, '{}-processed.csv'.format(title))
    print('Exporting as csv.')
    crimes.to_csv(name, index=False)
    print('Downloaded: {}'.format(name))

# Helper methods
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
    
def crm_category(x):
    lowered = x.lower()
    if any(substring in lowered for substring in INCHOATE):
        return 'Inchoate'
    elif any(substring in lowered for substring in PROPERTY):
        return 'Property'
    elif any(substring in lowered for substring in PERSONAL):
        return 'Personal'
    elif any(substring in lowered for substring in STATUTORY):
        return 'Statutory'
    return 'Financial/Other'

def limit_cols(df, cols):
    return df[cols]

def arrest(x):
    if 'arrest' in x.lower():
        return 1
    return 0

def transform_crimes(df, cols):
    df['Year'] = df['Date Rptd'].dt.year  
    print('Adding column: Arrested.')
    df['Arrested'] = df['Status Desc'].apply(arrest)
    print('Adding column: Crime Type.')
    df['Crime Type'] = df['Crm Cd Desc'].apply(crm_category)
    print('Adding column: Crime Severity.')
    df['Crime Severity'] = df['Crm Cd Desc'].apply(classify_crm_cd_desc)
    return limit_cols(df, cols)    
