""" create """

import pandas as pd
import numpy as np
from etl import load
from set_up import config_var

foldpath = config_var.path

def create_empty():
    df = pd.DataFrame(np.zeros((10, 43)))
    df.columns = ['Partita',
                  'Rt-5h', 'Rt-4h', 'Rt-3h', 'Rt-2h', 'Rt-1h', 'Classifica h',
                  'Rt-5a', 'Rt-4a', 'Rt-3a', 'Rt-2a', 'Rt-1a', 'Classifica a',
                  'MGf h', 'MGs h', 'MGf a', 'MGs a', 'SGf h', 'SGs h', 'SGf a', 'SGs a',
                  'Gf-5h', 'Gf-4h', 'Gf-3h', 'Gf-2h', 'Gf-1h',
                  'Gs-5h', 'Gs-4h', 'Gs-3h', 'Gs-2h', 'Gs-1h',
                  'Gf-5a', 'Gf-4a', 'Gf-3a', 'Gf-2a', 'Gf-1a',
                  'Gs-5a', 'Gs-4a', 'Gs-3a', 'Gs-2a', 'Gs-1a',
                  'yGf', 'yGs']

    return df
    

def create_matchday_df(LS, g):

    df = create_empty()
    tables = load.load_tables(LS, g)

    for m in tables['partite'].index:
        sfida = tables['partite'].loc[m,'Home'] + '-' + tables['partite'].loc[m,'Away']
        df.loc[m, 'Partita'] = sfida

        if not tables['prediction']:
            scoresh = tables['partite'].loc[m, 'Scoresheet'].split('-')
            df.loc[m, 'yGf'] = scoresh[0]
            df.loc[m, 'yGs'] = scoresh[1]

    for j, data in enumerate(tables['p_prec']):
        for i, incontro in enumerate(df['Partita'].values):
            st1 = 'Gf-' + str(5-j) + 'h'
            st2 = 'Gs-' + str(5-j) + 'h'
            st3 = 'Gf-' + str(5-j) + 'a'
            st4 = 'Gs-' + str(5-j) + 'a'
            teamh = incontro.split('-')[0]
            teama = incontro.split('-')[1]

            if teamh in data.loc[:, 'Home'].values:
                e = int(data['Scoresheet'][data['Home'] == teamh].values[0].split('-')[0])
            else:
                e = int(data['Scoresheet'][data['Away'] == teamh].values[0].split('-')[1])
            df.loc[i, st1] = e

            if teama in data.loc[:, 'Home'].values:
                e = int(data['Scoresheet'][data['Home'] == teama].values[0].split('-')[0])
            else:
                e = int(data['Scoresheet'][data['Away'] == teama].values[0].split('-')[1])
            df.loc[i, st3] = e

            if teamh in data.loc[:, 'Home'].values:
                f = int(data['Scoresheet'][data['Home'] == teamh].values[0].split('-')[1])
            else:
                f = int(data['Scoresheet'][data['Away'] == teamh].values[0].split('-')[0])
            df.loc[i, st2] = f

            if teama in data.loc[:, 'Home'].values:
                f = int(data['Scoresheet'][data['Home'] == teama].values[0].split('-')[1])
            else:
                f = int(data['Scoresheet'][data['Away'] == teama].values[0].split('-')[0])
            df.loc[i, st4] = f

    for i, data2 in enumerate(tables['table']):
        for pair in range(10):

            teamh = df.loc[pair, 'Partita'].split('-')[0]
            teama = df.loc[pair, 'Partita'].split('-')[1]

            rt5h = data2[data2['Squadra']==teamh]['Risultato'].values[0]
            stringa_th = 'Rt-' + str(5-i) + 'h'
            if rt5h == 'V':
                df.loc[pair, stringa_th] = 2
            elif rt5h == 'N':
                df.loc[pair, stringa_th] = 1
            else:
                df.loc[pair, stringa_th] = 0

            rt5a = data2[data2['Squadra']==teama]['Risultato'].values[0]
            stringa_ta = 'Rt-' + str(5-i) + 'a'
            if rt5a == 'V':
                df.loc[pair, stringa_ta] = 2
            elif rt5a == 'N':
                df.loc[pair, stringa_ta] = 1
            else:
                df.loc[pair, stringa_ta] = 0


    for matchn in range(10):
        teamh = df.loc[matchn, 'Partita'].split('-')[0]
        teama = df.loc[matchn, 'Partita'].split('-')[1]

        for pitch, team in zip(['h', 'a'], [teamh, teama]):
            df.loc[matchn, 'Classifica '+pitch] = tables['classifica'].loc[team, 'Posizione']

            for descr_stat in ['M', 'S']:
                for gs_or_gr in ['Gf', 'Gs']:
                    gol_stat = descr_stat + gs_or_gr + ' ' + pitch
                    df.loc[matchn, gol_stat] = tables['goals'].loc[team, descr_stat + gs_or_gr.lower()]

    return df


def create_year_df(LS):
    d = []
    for g in range(5, LS.days):
        matchday_df = create_matchday_df(LS, g)
        d.append(matchday_df)

    year_df = pd.concat(d, ignore_index=True)
    year_df.to_csv(f'{foldpath}/data/dataframes/{LS.year}.csv')

    return year_df
