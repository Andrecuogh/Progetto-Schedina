""" compute """

import pandas as pd
import numpy as np

def count_goals(LS, matchday):

    match_score = LS.leagues[matchday]
    table = pd.DataFrame(np.zeros((20,3)), dtype=np.int64)
    table.columns = ['Squadra', 'Gf', 'Gs']

    for i in range(10):
        table.loc[i, 'Squadra'] = match_score.loc[i,'Home']
        table.loc[i+10, 'Squadra'] = match_score.loc[i, 'Away']

        scoresh = match_score.loc[i, 'Scoresheet'].split('-')
        for j in [0,1]:
            table.iloc[i, j+1] = int(scoresh[j])
            table.iloc[i+10, j+1] = int(scoresh[np.abs(j-1)])

    table.set_index('Squadra', inplace=True)

    return table
