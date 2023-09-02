# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 12:44:05 2023

@author: medchaya
"""

import pandas as pd
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt


np.random.seed(42)

# number of individuals
n_treated = 1000
n_untreated = 1000
mean_species = 200
sd_species = 10

# initial dataframe

## Distributions for the two groups

# treated forests slightly fewer species
num_species_t = pd.Series(np.round(np.random.normal(mean_species-1,sd_species,n_treated)))
num_species_nt = pd.Series(np.round(np.random.normal(mean_species,sd_species,n_untreated)))


type_t = pd.Series(np.random.choice(('temperate','tropical'),n_treated))
type_nt = pd.Series(np.random.choice(('temperate','tropical'),n_untreated))


## Full df
treated_status = np.append(np.zeros(n_treated), np.ones(n_untreated)).astype(bool)

df = pd.DataFrame({'treated_status':treated_status,
                   'n_species':pd.concat([num_species_nt,num_species_t]),
                   'type':pd.concat([type_t,type_nt])})


g_untreated = df.loc[df['treated_status']==False, 'n_species']    
g_treated = df.loc[df['treated_status']==True, 'n_species']


print('Mean sd: {} {}, {} {}'.format(np.mean(g_untreated),np.std(g_untreated),
                                     np.mean(g_treated),np.std(g_treated),))

## plot num species per group    
plt.boxplot((g_untreated,g_treated))
for x,v in enumerate(zip((n_untreated, n_treated), [False,True])):
    n = v[0]
    status = v[1]
    plt.scatter(pd.Series([x+1]*n) + np.random.normal(0,.02,n),
                df.loc[df['treated_status']==status, 'n_species'], alpha=0.5)
plt.xticks((1,2),['untreated','treated'])
plt.ylabel('Number of species')

# Compare differences in number of species:


t_res = stats.ttest_ind(g_untreated,
                        g_treated)

t_res_pval = t_res[1]
print('P val: {}'.format(t_res_pval))
## effect size:
    
cohens_d = (np.mean(g_untreated) - np.mean(g_treated)) / (np.sqrt((np.std(g_untreated) ** 2 + np.std(g_treated) ** 2) / 2))
print('Cohens D: {}'.format(cohens_d))


