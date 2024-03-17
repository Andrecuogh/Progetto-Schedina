import pandas as pd
from set_up.league_data import postponed_matches


def count_goals(LS, matchday):
    df = LS.leagues[matchday]
    goals = df.risultato.str.split(" - ", expand=True).astype(int)

    df_casa = goals.set_index(df.squadra_casa)
    df_casa.columns = ["gol_fatti", "gol_subiti"]
    df_trasferta = goals.set_index(df.squadra_trasferta)
    df_trasferta.columns = ["gol_subiti", "gol_fatti"]
    table = pd.concat([df_casa, df_trasferta])
    table.index.name = "squadra"

    return table
