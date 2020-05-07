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

# Global constants
TYPES = ['Financial/Other','Inchoate','Personal','Property','Statutory']
CHARGES = ['Felony','Infraction','Misdemeanor','Others','Wobbler','Wobblette']

# Main driver functions
def analyze(inpath, outpath):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    crimes = pd.read_csv(inpath)
    test_overall(crimes, outpath)
    test_by_div(crimes, outpath)
    test_overall(crimes, outpath, crime='Charge')
    test_by_div(crimes, outpath, crime='Charge')

# Helper methods
def format_df(df, area=False, crime='Type'):
    if not area:
        return df.loc[df.Year != 2020].groupby('PredPol Deployed')['Crime {}'.format(crime)].value_counts(normalize=True).unstack().T
    else:
        return df.loc[df.Year != 2020].groupby(['AREA NAME','PredPol Deployed'])['Crime {}'.format(crime)].value_counts(normalize=True).unstack()

def test(crime_tp, prop_pp, prop_nonpp, pct_pp=0.562854, n=100000):
    """
    Tests a single type of crime.
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

def test_overall(df, outpath, crime='Type'):
    print('Testing overall distribution of crime {}s.'.format(crime))
    types = format_df(df, crime=crime)
    statvals = []
    pvals = []
    for tp, row in types.iterrows():
        print('Crime {}: {}'.format(crime, tp))
        stat, pval = test(tp, row[1], row[0])
        statvals.append(stat.round(5))
        pvals.append(pval.round(5))
        print('Statistic = ', stat)
        print('P-Value = {}\n'.format(pval))
    if crime == 'Type':
        idx = TYPES
    else:
        idx = CHARGES
    pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx).to_csv(os.path.join(outpath, 'ovr_{}_dist.csv'.format(crime)), index=False)
    print('Complete.')
    
def test_by_div(df, outpath, crime='Type'):
    print('Testing distribution of crime {}s per division.'.format(crime))
    if crime == 'Type':
        idx = TYPES
    else:
        idx = CHARGES
    types = format_df(df, area=True, crime=crime)
    results = pd.DataFrame()
    for div, df in types.groupby(level=0):
        print('Analyzing division: ', div)
        new_df = df.T
        vals = []
        pvals = []
        statvals = []
        for tp, row in new_df.iterrows():
            print('Crime {}: {}'.format(crime, tp))
            stat, pval = test(tp, row[1], row[0])
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
        pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx).to_csv(os.path.join(outpath, '{}_{}_dist.csv'.format(div, crime)), index=False)
        results[div] = vals
        print('-'*20)
        print('')
    results.set_index(pd.Index(idx), inplace=True)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    sns.heatmap(results.T, annot=False, xticklabels=True, yticklabels=True, ax=ax)
    plt.title('T-Test Results of Crime {} Distribution by Division'.format(crime))
    plt.xlabel('Crime {}'.format(crime))
    plt.ylabel('Division')
    plt.savefig(os.path.join(outpath, 'div_{}_dist.png'.format(crime)), bbox_inches='tight')
    print('Complete.')
    
