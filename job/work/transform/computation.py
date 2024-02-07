""" compute """

import pandas as pd
import numpy as np
from set_up.league_data import postponed_matches


def count_goals(LS, matchday):
    match_score = LS.leagues[matchday]

    for i in postponed_matches.values():
        target_match = (
            match_score.loc[i, "squadra_casa"]
            + "-"
            + match_score.loc[i, "squadra_trasferta"]
        )
        if target_match in postponed_matches.keys():
            match_score.loc[i, "risultato"] = "0 - 0"

    table = pd.DataFrame(np.zeros((20, 3)), dtype=np.int64)
    table.columns = ["Squadra", "gol_fatti", "gol_subiti"]

    for i in range(10):
        table.loc[i, "Squadra"] = match_score.loc[i, "squadra_casa"]
        table.loc[i + 10, "Squadra"] = match_score.loc[i, "squadra_trasferta"]

        scoresh = match_score.loc[i, "risultato"].split("-")
        for j in [0, 1]:
            table.iloc[i, j + 1] = int(scoresh[j])
            table.iloc[i + 10, j + 1] = int(scoresh[np.abs(j - 1)])

    table.set_index("Squadra", inplace=True)

    return table
