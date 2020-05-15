
import pandas as pd
import sys
import os
import numpy as np
from random import choices
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

TYPES = ['BLACK', 'WHITE', 'ASIAN', 'OTHER', 'HISPANIC', 'AMERICAN INDIAN','MULTI-DESCENTS']

def analyze(inpath, outpath):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    stops = pd.read_csv(inpath)
    test_overall(stops, outpath)
    test_by_div(stops, outpath)
    
def format_df(df, area=False):
    if not area:
        return df.loc[df.Year != 2020].groupby('Reassigned Officer')['Descent Description'].value_counts(normalize=True).unstack().T
    else:
        return df.loc[df.Year != 2020].groupby(['Stop Division','Reassigned Officer'])['Descent Description'].value_counts(normalize=True).unstack()
    
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

    df = pd.DataFrame({'Reassigned Officer': M, crime_tp: N})
    res = stats.ttest_ind(df[df['Reassigned Officer']==1][crime_tp], df[df['Reassigned Officer']==0][crime_tp])
    
    return res.statistic, res.pvalue

def test_overall(df, outpath):
    print('Testing overall distribution of Race.')
    types = format_df(df)
    statvals = []
    pvals = []
    for race, row in types.iterrows():
        print('Stops: {}'.format(race))
        stat, pval = test(race, row[1], row[0])
        statvals.append(stat.round(5))
        pvals.append(pval.round(5))
        print('Statistic = ', stat)
        print('P-Value = {}\n'.format(pval))
    idx = TYPES
    pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx).to_csv(os.path.join(outpath, 'ovr_Race_dist.csv'))
    print('Complete.')

def test_by_div(df, outpath):
    print('Testing distribution of race per division.')
    idx = TYPES
    types = format_df(df, area=True)
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
            print('Race: {}'.format(tp))
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
        detailed.append(pd.DataFrame({'Statistic':statvals, 'P-Value':pvals}, index=idx))
        divisions.append(div)
        results[div] = vals
        print('-'*20)
        print('')
    pd.concat(detailed, keys=divisions, names=['Division','Descent Description']).to_csv(os.path.join(outpath, 'div_Race_detailed.csv'))
    results.set_index(pd.Index(idx), inplace=True)
    results.T.to_csv(os.path.join(outpath, 'div_Race_dist.csv'))
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1,1,1)
    sns.heatmap(results.T, annot=False, xticklabels=True, yticklabels=True, ax=ax)
    plt.title('T-Test Results of Race Distribution by Division')
    plt.xlabel('Race')
    plt.ylabel('Division')
    plt.savefig(os.path.join(outpath, 'div_Race_dist.png'), bbox_inches='tight')
    print('Complete.')
