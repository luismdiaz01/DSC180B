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
CHARGE_GROUP = ['Financial/Other','Inchoate','Personal','Property','Statutory']

ARREST_TYPE = ['Dependent', 'Felony', 'Misdemeanor', 'Infraction', 'Other']

# Main driver functions
def analyze(inpath, outpath):
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    arrests = pd.read_csv(inpath)    
    test_overall(arrests, outpath)
    test_overall(arrests, outpath, arrest='Arrest Type Code')
    test_by_div(arrests, outpath)
    test_by_div(arrests, outpath, arrest='Arrest Type Code')
  
    
def format_df(df, area, arrest='Charge Group Description'):
    if not area:
        return df.loc[df.Year != 2020].groupby('predPol Deployed')[arrest].value_counts(normalize=True).unstack().T
    else:
        return df.loc[df.Year != 2020].groupby(['Area Name','predPol Deployed'])[arrest].value_counts(normalize=True).unstack()
    
def test(arrest_tp, prop_pp, prop_nonpp, pct_pp=0.562854, n=100000):
    """
    Tests a single type of arrest.
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

    df = pd.DataFrame({'predPol Deployed': M, arrest_tp: N})
    res = stats.ttest_ind(df[df['predPol Deployed']==1][arrest_tp], df[df['predPol Deployed']==0][arrest_tp])
    
    return res.statistic, res.pvalue

def test_overall(df, outpath, arrest='Charge Group Description'):
    if arrest == 'Arrest Type Code':
        curr = 'Arrest_Type'
        idx = ARREST_TYPE
    
    elif arrest == 'Charge Group Description':
        curr = 'Arrest_Charge'
        idx = CHARGE_GROUP
        
    types = format_df(df, False, arrest)
    statvals = []
    pvals = []
    for tp, row in types.iterrows():
        stat, pval = test(tp, row[1], row[0])
        statvals.append(stat.round(5))
        pvals.append(pval.round(5))
        #print('Statistic = ', stat)
        #print('P-Value = {}\n'.format(pval))
    return pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx).to_csv(os.path.join(outpath, 'ovr_{}_dist.csv'.format(curr)))
    #print('Complete.')


def test_by_div(df, outpath, arrest='Charge Group Description'):
    if arrest == 'Arrest Type Code':
        curr = 'Arrest_Type'
    elif arrest == 'Charge Group Description':
        curr = 'Arrest_Charge'
        
    if arrest == 'Arrest Type Code':
        idx = ARREST_TYPE
        print('Testing distribution of Arrest Types per division.')

    else:
        idx = CHARGE_GROUP
        print('Testing distribution of Arrest Charge Types per division.')

    types = format_df(df, True, arrest=arrest)
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
            print('Arrest Type: {}'.format(tp))
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
        detailed.append(pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx))
        divisions.append(div)
        results[div] = vals
        print('-'*20)
        print('')
    pd.concat(detailed, keys=divisions, names=['Division','{}'.format(curr)]).to_csv(os.path.join(outpath, 'div_{}_detailed.csv'.format(curr)))

    results.set_index(pd.Index(idx), inplace=True)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    sns.heatmap(results.T, annot=False, xticklabels=True, yticklabels=True, ax=ax, vmin=-1, vmax=1)
    plt.title('T-Test Results of {} Distribution by Division'.format(curr))
    plt.xlabel(curr)
    plt.ylabel('Division')
    plt.savefig(os.path.join(outpath, 'div_{}_dist.png'.format(curr)), bbox_inches='tight')
    print('Complete.')
