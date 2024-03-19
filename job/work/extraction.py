import pandas as pd
import logging


def count_goals(df):
    df_casa = df[["squadra_casa", "goal_casa", "goal_trasferta"]]
    df_casa.columns = ["squadra", "gol_fatti", "gol_subiti"]
    df_trasferta = df[["squadra_trasferta", "goal_casa", "goal_trasferta"]]
    df_trasferta.columns = ["squadra", "gol_subiti", "gol_fatti"]
    table = pd.concat([df_casa, df_trasferta], ignore_index=True)
    return table


def assign_points(df):
    df.loc[df.gol_fatti > df.gol_subiti, "esito"] = "vittoria"
    df.loc[df.gol_fatti < df.gol_subiti, "esito"] = "sconfitta"
    df.loc[df.gol_fatti == df.gol_subiti, "esito"] = "pareggio"
    punti_map = {"vittoria": 3, "pareggio": 1, "sconfitta": 0}
    df["punti"] = df.esito.map(punti_map)
    return df


def cumulative_goals_points(df):
    cum_cols = ["gol_fatti", "gol_subiti", "punti"]
    df[cum_cols] = df.groupby("squadra")[cum_cols].cumsum()
    df["differenza_reti"] = df.gol_fatti - df.gol_subiti
    return df


def rank_position(df):
    ord_cols = ["giornata", "punti", "differenza_reti", "gol_fatti"]
    df = df.sort_values(by=ord_cols, ascending=False)
    df["posizione"] = list(range(1, 21)) * 38
    return df


def average_goals(df):
    for avg_col in ["gol_fatti", "gol_subiti"]:
        name = f"media_{avg_col}"
        df[name] = df[avg_col] / (df.giornata + 1)
        df.loc[df[avg_col] > 4, avg_col] = 4


def extract_features(leagues):
    dataframe = count_goals(leagues)
    dataframe = assign_points(dataframe)
    dataframe = cumulative_goals_points(dataframe)
    dataframe = rank_position(dataframe)
    dataframe = average_goals(dataframe)

    return dataframe
