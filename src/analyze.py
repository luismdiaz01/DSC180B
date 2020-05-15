# Import libraries/modules
import sys
import json
import shutil
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from random import choices
from scipy import stats
from eda import plot_graph

# Global constants
TYPES = ['Financial/Other', 'Inchoate', 'Personal', 'Property', 'Statutory']
CHARGES = ['Dependent', 'Felony', 'Infraction', 'Misdemeanor', 'Others']
RACES = ['BLACK', 'WHITE', 'ASIAN', 'OTHER', 'HISPANIC', 'AMERICAN INDIAN','MULTI-DESCENTS']
GROUP = 'PredPol Deployed'
GROUP_STOPS = 'Reassigned Officer'
GROUP2 = ['Area Name', 'PredPol Deployed']
GROUP_STOPS2 = ['Stop Division', 'Reassigned Officer']

# Main driver functions
def analyze(types, inpaths, outpaths):
    for tp, inpath, outpath in zip(types, inpaths, outpaths):
        if not os.path.exists(outpath):
            os.mkdir(outpath)
            
        df = pd.read_csv(inpath)
        for t in tp:
            test_overall(df, outpath, feat=t)
            test_by_div(df, outpath, feat=t)

# Helper methods
def format_df(df, feat, area=False, group='PredPol Deployed', group2=['Area Name', 'PredPol Deployed']):
    if feat == 'Descent Description':
        group = 'Reassigned Officer'
        group2 = ['Stop Division', 'Reassigned Officer']
    if not area:
        return df.loc[df.Year != 2020].groupby(group)[feat].value_counts(normalize=True).unstack().T
    else:
        return df.loc[df.Year != 2020].groupby(group2)[feat].value_counts(normalize=True).unstack()

def test(crime_tp, prop_pp, prop_nonpp, pct_pp=0.562854, n=100000):
    """
    Tests a single type of crime/arrest/race.
    """
    NUM_POP = n
    PCT_PREDPOL = pct_pp
    PCT_NONPREDPOL = 1-PCT_PREDPOL
    VAR_PREDPOL = 1.0
    VAR_NONPREDPOL = 1.0

    n_predpol = int(NUM_POP * PCT_PREDPOL)
    n_notpredpol = int(NUM_POP * PCT_NONPREDPOL)

    # Generate data
    M = np.array([0] * n_notpredpol + [1] * n_predpol) # generate predpol variable

    # generate error terms: using proportion of crime type
    N_PREDPOL = choices([1,0], [prop_pp,1-prop_pp], k=n_predpol)
    N_NONPREDPOL = choices([1,0], [prop_nonpp,1-prop_nonpp],k= n_notpredpol)
    N = np.append(N_NONPREDPOL, N_PREDPOL)

    df = pd.DataFrame({'PredPol Deployed': M, crime_tp: N})
    res = stats.ttest_ind(df[df['PredPol Deployed']==1][crime_tp], df[df['PredPol Deployed']==0][crime_tp])
    
    return res.statistic, res.pvalue

def test_overall(df, outpath, feat):
    print('Testing overall distribution of {}.'.format(feat))
    types = format_df(df, feat=feat)
    statvals = []
    pvals = []
    for tp, row in types.iterrows():
        print('{}: {}'.format(feat, tp))
        try:
            stat, pval = test(tp, row[1], row[0])
        except IndexError:
            stat, pval = 0.0, 0.0
        statvals.append(round(stat, 5))
        pvals.append(round(pval, 5))
        print('Statistic = ', stat)
        print('P-Value = {}\n'.format(pval))
    if feat == 'Crime Type' or feat == 'Charge Group Description':
        idx = TYPES
    elif feat == 'Crime Charge' or feat == 'Arrest Type Code':
        idx = CHARGES
    elif feat == 'Descent Description':
        idx = RACES
    try:
        pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx).to_csv(os.path.join(outpath, 'ovr_{}_dist.csv'.format(feat)))
    except ValueError:
        pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx[:-1]).to_csv(os.path.join(outpath, 'ovr_{}_dist.csv'.format(feat)))
    print('Complete.')

def test_by_div(df, outpath, feat):
    print('Testing distribution of {} per division.'.format(feat))
    if feat == 'Crime Type' or feat == 'Charge Group Description':
        idx = TYPES
    elif feat == 'Crime Charge' or feat == 'Arrest Type Code':
        idx = CHARGES
    elif feat == 'Descent Description':
        idx = RACES
    types = format_df(df, area=True, feat=feat)
    results = pd.DataFrame()
    detailed = []
    divisions = []
    for div, df in types.groupby(level=0):
        print('Analyzing division: ', div)
        new_df = df.T
        vals = []
        pvals = []
        statvals = []
        for tp, row in new_df.iterrows():
            try:
                stat, pval = test(tp, row[1], row[0])
            except IndexError: # For test data, some have null values
                stat, pval = 0, 0
            pvals.append(pval)
            statvals.append(stat)
            if pval <= 0.05:
                if stat > 0:
                    vals.append(1)
                elif stat < 0:
                    vals.append(-1)
                else:
                    vals.append(0)
            else:
                vals.append(0)
            print('Statistic = ', stat)
            print('P-Value = {}\n'.format(pval))
        try:
            detailed.append(pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx))
        except ValueError:
            detailed.append(pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx[:-1]))
        divisions.append(div)
        results[div] = vals
        print('-'*20)
        print('')
    pd.concat(detailed, keys=divisions, names=['Division','{}'.format(feat)]).to_csv(os.path.join(outpath, 'div_{}_detailed.csv'.format(feat)))
    try:
        results.set_index(pd.Index(idx), inplace=True)
    except ValueError:
        results.set_index(pd.Index(idx[:-1]), inplace=True)
    results.T.to_csv(os.path.join(outpath, 'div_{}_dist.csv'.format(feat)))
    plot_graph(results.T, outpath, 'heat', 'T-Test Results of {} Distribution by Division'.format(feat), feat, 'Division')
