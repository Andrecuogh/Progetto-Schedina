"""
extract feature tables from raw scores
e.g. : raw score --> Milan - Salernitana 2-1
       features --> Goal scored home: 2; goal scored away: 1
                    Result: V (win for home)
                    Ranking: Milan advances 3 point in ranking
"""

import pandas as pd
import numpy as np
from transform import computation


def get_ranking(LS):

    # set up the empty dataframe
    rank_df = pd.DataFrame(np.zeros((20, 8)))
    rank_df.columns = ['Squadra', 'Gf', 'Gs', 'Punti', 'V', 'N', 'P', 'Diff']
    rank_df['Squadra'] = LS.teams
    rank_df.set_index('Squadra', inplace=True)

    # fill the dataframe
    ranking = []
    for matchday in range(LS.days):

        rank_day = computation.count_goals(LS, matchday)
        rank_day[['V', 'N', 'P', 'Punti']] = 0

        for team in rank_day.index:
            if rank_day.loc[team, 'Gf'] > rank_day.loc[team, 'Gs']:
                rank_day.loc[team, 'Punti'] = 3
                rank_day.loc[team, 'V'] = 1
            elif rank_day.loc[team, 'Gf'] == rank_day.loc[team, 'Gs']:
                rank_day.loc[team, 'Punti'] = 1
                rank_day.loc[team, 'N'] = 1
            else:
                rank_day.loc[team, 'P'] = 1

        rank_day['Diff'] = rank_day['Gf'] - rank_day['Gs']
        rank_df = rank_day + rank_df
        rank_df.sort_values(by=['Punti', 'Diff', 'Gf', 'Squadra'],
                            ascending = [False, False, False, True],
                            inplace=True)
        rank_df['Posizione'] = np.arange(1, 21)
        ranking.append(rank_df)

    return ranking


def get_results(LS):
    result_year = []
    for matchday in range(LS.days):
        
        # load matchday scores
        # resdf.columns = ['Home', 'Away', 'Scoresheet'] scoresheet = 'Goal-Goal'
        resdf = LS.leagues[matchday]
        result = pd.DataFrame(np.zeros((20, 2)))
        result.columns = ['Squadra', 'Risultato']

        for score in resdf.index:
            result.loc[score, 'Squadra'] = resdf.loc[score, 'Home']
            result.loc[score + 10, 'Squadra'] = resdf.loc[score, 'Away']
            
            scoresh = resdf.loc[score, 'Scoresheet'].split(' - ')
            if scoresh[0] > scoresh[1]:
                result.loc[score, 'Risultato'] = 'V'
                result.loc[score + 10, 'Risultato'] = 'P'

            elif scoresh[0] == scoresh[1]:
                result.loc[score, 'Risultato'] = 'N'
                result.loc[score + 10, 'Risultato'] = 'N'

            else:
                result.loc[score, 'Risultato'] = 'P'
                result.loc[score + 10, 'Risultato'] = 'V'

        result_year.append(result)

    return result_year


def get_goals(LS):
    dgs = pd.DataFrame(np.zeros((20,1)))
    dgs.index = LS.teams
    dgr = dgs.copy()

    for day in range(LS.days):
        gg = computation.count_goals(LS, day)
        dgs = pd.concat([dgs, gg['Gf']], axis=1)
        dgr = pd.concat([dgr, gg['Gs']], axis=1)

    dgs.drop(0, axis=1, inplace=True)
    dgr.drop(0, axis=1, inplace=True)
    dgs.columns = [i for i in range(1, LS.days + 1)]
    dgr.columns = [i for i in range(1, LS.days + 1)]

    gsgr_campion = []
    for n in range(LS.days):
        cc = pd.DataFrame(np.zeros((20, 4)))
        cc.index = dgs.index
        cc['Mgf'] = dgs.loc[:, 1:n+1].mean(axis=1)
        cc['Sgf'] = dgs.loc[:, 1:n+1].std(axis=1)
        cc['Mgs'] = dgr.loc[:, 1:n+1].mean(axis=1)
        cc['Sgs'] = dgr.loc[:, 1:n+1].std(axis=1)
        cc.fillna(0, inplace=True)
        gsgr_campion.append(cc)

    return gsgr_campion
