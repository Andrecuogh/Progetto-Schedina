import pandas as pd


def merge_df(df):
    goals_casa = df["goals"].rename({"squadra": "squadra_casa"}, axis=1)
    goals_trasferta = df["goals"].rename({"squadra": "squadra_trasferta"}, axis=1)
    matches = df["matches"]
    df_casa = matches.merge(
        goals_casa,
        on=["squadra_casa", "giornata", "anno"],
        how="inner",
    )
    df_trasferta = matches.merge(
        goals_trasferta,
        on=["squadra_trasferta", "giornata", "anno"],
        how="inner",
    )
    dataframe = df_casa.merge(
        df_trasferta,
        on=["squadra_casa", "squadra_trasferta", "giornata", "anno"],
        suffixes=("_casa", "_trasferta"),
    )
    return dataframe


def create_match_label(df):
    df["squadra"] = df.squadra_casa + "-" + df.squadra_trasferta
    df = df.drop(["squadra_casa", "squadra_trasferta"], axis=1)
    return df


def standardize_goals(df):
    df = df.drop(["gol_subiti_casa", "gol_subiti_trasferta"], axis=1)
    return df


def create_dataset(df):
    df = merge_df(df)
    df = create_match_label(df)
    df = standardize_goals(df)
    return df
