#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[15]:

def Forecasts(g, names):
    df = pd.DataFrame(np.zeros((10, 41)))
    df.columns = ['Partita',
                  'Rt-5h', 'Rt-4h', 'Rt-3h', 'Rt-2h', 'Rt-1h', 'Classifica h', 
                  'Rt-5a', 'Rt-4a', 'Rt-3a', 'Rt-2a', 'Rt-1a', 'Classifica a',
                  'MGf h', 'MGs h', 'MGf a', 'MGs a', 'SGf h', 'SGs h', 'SGf a', 'SGs a',
                  'Gf-5h', 'Gf-4h', 'Gf-3h', 'Gf-2h', 'Gf-1h',
                  'Gs-5h', 'Gs-4h', 'Gs-3h', 'Gs-2h', 'Gs-1h',
                  'Gf-5a', 'Gf-4a', 'Gf-3a', 'Gf-2a', 'Gf-1a',
                  'Gs-5a', 'Gs-4a', 'Gs-3a', 'Gs-2a', 'Gs-1a']

    p_prec = [pd.read_excel('Results22.xlsx', sheet_name = n, index_col = 0) for n in range(g-5, g)]
    table = [pd.read_excel('Hystory22.xlsx', sheet_name = n, index_col = 0, usecols=[1,2]) for n in range(g-5, g)]
    classifica = pd.read_excel('Stand22.xlsx', sheet_name = g-1 , index_col = 0, usecols=[c for c in range(9)])
    goals = pd.read_excel('Gols22.xlsx', sheet_name = g-1 , index_col = 0)

    df['Partita'] = names[0].values

    for j, data in enumerate(p_prec):
        for i, incontro in enumerate(df['Partita'].values):
            st1 = 'Gf-' + str(5-j) + 'h'
            st2 = 'Gs-' + str(5-j) + 'h'
            st3 = 'Gf-' + str(5-j) + 'a'
            st4 = 'Gs-' + str(5-j) + 'a'
            teamh = incontro.split('-')[0]
            teama = incontro.split('-')[1]
            if teamh in data.iloc[:, 0].values:
                e = int(data[2][data[0] == teamh].values[0].split('-')[0])
            else:
                e = int(data[2][data[1] == teamh].values[0].split('-')[1])
            df.loc[i, st1] = e
            if teama in data.iloc[:, 0].values:
                e = int(data[2][data[0] == teama].values[0].split('-')[0])
            else:
                e = int(data[2][data[1] == teama].values[0].split('-')[1])
            df.loc[i, st3] = e
            if teamh in data.iloc[:, 0].values:
                f = int(data[2][data[0] == teamh].values[0].split('-')[1])
            else:
                f = int(data[2][data[1] == teamh].values[0].split('-')[0])
            df.loc[i, st2] = f
            if teama in data.iloc[:, 0].values:
                f = int(data[2][data[0] == teama].values[0].split('-')[1])
            else:
                f = int(data[2][data[1] == teama].values[0].split('-')[0])
            df.loc[i, st4] = f

    for i, data in enumerate(table):
        for pair in range(10):
            teamh = df.loc[pair, 'Partita'].split('-')[0]
            rt5h = data.loc[teamh, 'Risultato']
            stringa_th = 'Rt-' + str(5-i) + 'h'
            if rt5h == 'V':
                df.loc[pair, stringa_th] = 2
            elif rt5h == 'N':
                df.loc[pair, stringa_th] = 1
            else:
                df.loc[pair, stringa_th] = 0
            teama = df.loc[pair, 'Partita'].split('-')[1]
            rt5a = data.loc[teama, 'Risultato']
            stringa_ta = 'Rt-' + str(5-i) + 'a'
            if rt5a == 'V':
                df.loc[pair, stringa_ta] = 2
            elif rt5a == 'N':
                df.loc[pair, stringa_ta] = 1
            else:
                df.loc[pair, stringa_ta] = 0

    for pair in range(10):
        teamh = df.loc[pair, 'Partita'].split('-')[0]
        df.loc[pair, 'Classifica h'] = classifica.loc[teamh, 'Posizione']
        teama = df.loc[pair, 'Partita'].split('-')[1]
        df.loc[pair, 'Classifica a'] = classifica.loc[teama, 'Posizione']

    for gol in range(10):
        teamh = df.loc[gol, 'Partita'].split('-')[0]
        df.loc[gol, 'MGf h'] = goals.loc[teamh, 'Mgf']
        df.loc[gol, 'SGf h'] = goals.loc[teamh, 'Sgf']
        df.loc[gol, 'MGs h'] = goals.loc[teamh, 'Mgs']
        df.loc[gol, 'SGs h'] = goals.loc[teamh, 'Sgs']
        teama = df.loc[gol, 'Partita'].split('-')[1]
        df.loc[gol, 'MGf a'] = goals.loc[teama, 'Mgf']
        df.loc[gol, 'SGf a'] = goals.loc[teama, 'Sgf']
        df.loc[gol, 'MGs a'] = goals.loc[teama, 'Mgs']
        df.loc[gol, 'SGs a'] = goals.loc[teama, 'Sgs']
    return df


# In[ ]:




