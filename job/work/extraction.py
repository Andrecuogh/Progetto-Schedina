import pandas as pd
import logging


def count_goals(df):
    casa_mapper = {
        "squadra_casa": "squadra",
        "squadra_trasferta": "avversario",
        "goal_casa": "gol_fatti",
        "goal_trasferta": "gol_subiti",
    }
    df_casa = df.rename(columns=casa_mapper)

    trasferta_mapper = {
        "squadra_trasferta": "squadra",
        "squadra_casa": "avversario",
        "goal_casa": "gol_subiti",
        "goal_trasferta": "gol_fatti",
    }
    df_trasferta = df.rename(columns=trasferta_mapper)

    table = pd.concat([df_casa, df_trasferta], ignore_index=True)
    table = table.sort_values("giornata")
    return table


def assign_points(df):
    df.loc[df.gol_fatti > df.gol_subiti, "esito"] = "vittoria"
    df.loc[df.gol_fatti < df.gol_subiti, "esito"] = "sconfitta"
    df.loc[df.gol_fatti == df.gol_subiti, "esito"] = "pareggio"
    punti_map = {"vittoria": 3, "pareggio": 1, "sconfitta": 0}
    df["punti"] = df.esito.map(punti_map)
    return df


def cumulative_goals_points(df):
    df["gol_fatti_cum"] = df.groupby("squadra").gol_fatti.cumsum()
    df["gol_subiti_cum"] = df.groupby("squadra").gol_subiti.cumsum()
    df["punti"] = df.groupby("squadra").punti.cumsum()
    df["differenza_reti"] = df.gol_fatti_cum - df.gol_subiti_cum
    return df


def rank_position(df):
    ord_cols = ["giornata", "punti", "differenza_reti", "gol_fatti_cum"]
    df = df.sort_values(by=ord_cols, ascending=False)
    days = len(df) // 20
    df["posizione"] = list(range(1, 21)) * days
    return df


def previous_gol(df):
    df = df.sort_values(by=["anno", "giornata"])
    df["esito"] = df.esito.map({"vittoria": 1, "pareggio": 0, "sconfitta": -1})
    df["gol_fatti"] = df.gol_fatti.where(df.gol_fatti < 4, 4)
    df["gol_subiti"] = df.gol_subiti.where(df.gol_subiti < 4, 4)
    for t in range(1, 6):
        for col in ["gol_fatti", "gol_subiti", "esito"]:
            name = f"{col}_{t}"
            df[name] = df.groupby("squadra")[col].shift(t)
    df["posizione"] = df.groupby("squadra").posizione.shift(1)
    return df


def cleaning_df(df):
    df = df.drop(
        [
            "gol_fatti_cum",
            "gol_subiti_cum",
            "differenza_reti",
            "avversario",
            "punti",
            "esito",
        ],
        axis=1,
    )
    df = df.dropna()
    return df


def extract_features(leagues):
    matches = leagues.drop(["goal_casa", "goal_trasferta"], axis=1)
    dataframe = count_goals(leagues)
    dataframe = assign_points(dataframe)
    dataframe = cumulative_goals_points(dataframe)
    dataframe = rank_position(dataframe)
    dataframe = previous_gol(dataframe)
    dataframe = cleaning_df(dataframe)
    return dataframe, matches
