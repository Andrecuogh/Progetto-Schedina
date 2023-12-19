""" extraction """

import pandas as pd
import numpy as np
from transform import computation


def get_ranking(LS):
    rank_df = pd.DataFrame(np.zeros((20, 8)))
    rank_df.columns = ['Squadra', 'Gf', 'Gs', 'Punti', 'V', 'N', 'P', 'Diff']
    rank_df['Squadra'] = LS.teams
    rank_df.set_index('Squadra', inplace=True)

    ranking = []
    for matchday in range(LS.days):

        rank_day = computation.count_goals(LS, matchday)
        rank_day[['V', 'N', 'P', 'Punti']] = 0

        for indx, team in enumerate(rank_day.index):
            if rank_day.loc[team, 'Gf'] > rank_day.loc[team, 'Gs']:
                rank_day.iloc[indx, 2] = 3
                rank_day.iloc[indx, 3] = 1
            elif rank_day.loc[team, 'Gf'] == rank_day.loc[team, 'Gs']:
                rank_day.iloc[indx, 2] = 1
                rank_day.iloc[indx, 4] = 1
            else:
                rank_day.iloc[indx, 5] = 1

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
        resdf = LS.leagues[matchday]
        result = pd.DataFrame(np.zeros((20, 2)))

        for score in resdf.index:
            result.iloc[score, 0] = resdf.iloc[score, 0]
            result.iloc[score + 10, 0] = resdf.iloc[score, 1]

            if resdf.iloc[score, 2].split(' - ')[0] > resdf.iloc[score, 2].split(' - ')[1]:
                result.iloc[score, 1] = 'V'
                result.iloc[score + 10, 1] = 'P'

            elif resdf.iloc[score, 2].split(' - ')[0] == resdf.iloc[score, 2].split(' - ')[1]:
                result.iloc[score, 1] = 'N'
                result.iloc[score + 10, 1] = 'N'

            else:
                result.iloc[score, 1] = 'P'
                result.iloc[score + 10, 1] = 'V'

        result.columns = ['Squadra', 'Risultato']
        result_year.append(result)

    return result_year


def get_goals(LS):
    dgs = pd.DataFrame(np.zeros((20,1)))
    dgs.index = LS.rankings[0].index
    dgr = dgs.copy()

    gsgr_campion = []
    for gsgr_giorn in range(LS.days):
        gg = computation.count_goals(LS, gsgr_giorn)
        dgs = pd.concat([dgs, gg['Gf']], axis=1)
        dgr = pd.concat([dgr, gg['Gs']], axis=1)

    dgs.drop(0, axis=1, inplace=True)
    dgr.drop(0, axis=1, inplace=True)
    dgs.columns = [i for i in range(1, LS.days + 1)]
    dgr.columns = [i for i in range(1, LS.days + 1)]

    for n in range(LS.days):
        cc = pd.DataFrame(np.zeros((20, 4)))
        cc.index = dgs.index
        cc[0] = dgs.loc[:, 1:n+1].mean(axis=1)
        cc[1] = dgs.loc[:, 1:n+1].std(axis=1)
        cc[2] = dgr.loc[:, 1:n+1].mean(axis=1)
        cc[3] = dgr.loc[:, 1:n+1].std(axis=1)
        cc.fillna(0, inplace=True)
        cc.columns = ['Mgf', 'Sgf', 'Mgs', 'Sgs']
        gsgr_campion.append(cc)

    return gsgr_campion