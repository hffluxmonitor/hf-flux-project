# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:44:55 2018

@author: FluxMonitor
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

username = os.getlogin()
df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df.set_index('datetime',inplace=True)
df.index = pd.to_datetime(df.index)
df['month'] = df.index.month
df = df.reset_index()

from sklearn.preprocessing import StandardScaler

features = ['gradient', 'Wspd.m/s', 'Wdir.deg', 'T_K', 'H',
            'GEM_avg_conc','flux']

# Separating out the features
x = df.loc[:, features].ffill().values
# Separating out the target
y = df.loc[:,['month']].ffill().values
# Standardizing the features
x = StandardScaler().fit_transform(x)

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1','principal component 2'])

finalDf = pd.concat([principalDf, df[['month']]], axis = 1)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [4,5,6,7,8]
colors = ['r', 'g', 'b','orange','y']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['month'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()

from sklearn.decomposition import PCA
# Make an instance of the Model
pca = PCA(.95)

pca.fit(x)

x = pca.transform(x)

from sklearn.linear_model import LogisticRegression

# all parameters not specified are set to their defaults
# default solver is incredibly slow which is why it was changed to 'lbfgs'
logisticRegr = LogisticRegression(solver = 'lbfgs')

from matplotlib.mlab import PCA

df = df.ffill()
results = PCA(x)

tim = results.frac
tim2 = results.Y








































