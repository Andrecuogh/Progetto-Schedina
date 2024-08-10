import pandas as pd
from etl_config.log import logger


def merge_df(df: pd.DataFrame) -> pd.DataFrame:
    """Merge home and away dataframes"""
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


def create_match_label(df: pd.DataFrame) -> pd.DataFrame:
    """Create the match label by adding the home and away teams names"""
    df["squadra"] = df.squadra_casa + "-" + df.squadra_trasferta
    df = df.drop(["squadra_casa", "squadra_trasferta"], axis=1)
    return df


def standardize_goals(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns"""
    df = df.drop(
        [
            "gol_subiti_casa",
            "gol_subiti_trasferta",
            "gol_fatti_cum_casa",
            "gol_subiti_cum_trasferta",
            "gol_fatti_cum_trasferta",
            "gol_subiti_cum_casa",
            "punti_casa",
            "punti_trasferta",
        ],
        axis=1,
    )
    return df


def create_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline of processes"""
    logger.info("Start transformation of data")
    df = merge_df(df)
    df = create_match_label(df)
    df = standardize_goals(df)
    logger.info(f"Years: {df.groupby("anno", as_index=False)["giornata"].agg({"count", "max"}).T}")
    logger.info("End transformation of data\n")
    return df


def reduce_teams_names(squadra: str, single=True) -> str:
    if single:
        return squadra[0:3].upper()
    else:
        squadre = squadra.split(" - ")
        abbreviazioni = [squadra[:3].upper() for squadra in squadre]
        return " - ".join(abbreviazioni)


def transform_previous_encounters(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(by=["anno", "giornata"])
    df = df.iloc[:-10].copy()
    df["partita"] = df["squadra_casa"] + " - " + df["squadra_trasferta"]
    df["risultato"] = (
        df["goal_casa"].astype(str) + " - " + df["goal_trasferta"].astype(str)
    )
    df = df.drop(
        ["squadra_casa", "squadra_trasferta", "goal_casa", "goal_trasferta"], axis=1
    )
    df["partita_short"] = df["partita"].apply(reduce_teams_names, single=False)
    return df


def view_ranking(leagues: dict) -> pd.DataFrame:
    data = leagues["goals"].copy()
    df = filter_latest_day(data, step=1)
    if df.empty:
        df = filter_latest_day(data, step=0)
        df["posizione"] = df.squadra.rank()
        df[["punti", "gol_fatti_cum", "gol_subiti_cum"]] = 0
    df = df.sort_values(by=["posizione"])
    df["posizione"] = df.posizione.astype(int)
    df["squadra"] = df["squadra"].apply(reduce_teams_names)
    df = df[
        [
            "posizione",
            "squadra",
            "punti",
            "gol_fatti_cum",
            "gol_subiti_cum",
        ]
    ]
    df.columns = ["posizione", "squadra", "punti", "Gf", "Gs"]
    return df


def filter_latest_day(df: pd.DataFrame, step: int = 0) -> pd.DataFrame:
    df = df[df.anno == df.anno.max()]
    df = df[df.giornata == df.giornata.max() - step]
    return df
