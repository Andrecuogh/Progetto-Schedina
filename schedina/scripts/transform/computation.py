""" compute """

import pandas as pd
import numpy as np

def count_goals(LS, matchday):

    match_score = LS.leagues[matchday]
    table = pd.DataFrame(np.zeros((20,3)), dtype=np.int64)

    for i in range(10):
        table.iloc[i, 0] = match_score.iloc[i,0]
        table.iloc[i+10, 0] = match_score.iloc[i, 1]

        for j in [0,1]:
            table.iloc[i, j+1] = int(match_score.iloc[i, 2].split('-')[j])
            table.iloc[i+10, j+1] = int(match_score.iloc[i, 2].split('-')[np.abs(j-1)])

    table.columns = ['Squadra', 'Gf', 'Gs']
    table.set_index('Squadra', inplace=True)

    return table