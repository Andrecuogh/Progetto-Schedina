import pandas as pd
from etl_config.log import logger


def get_pd_html(year: int, ongoing: bool) -> list:
    """Read skysport.com data

    Args:
        year (int): year of the season
        ongoing (bool): if True, the season is the current season

    Returns:
        list: list of matchday tables
    """
    link_year = "" if ongoing else year
    link = pd.read_html(
        f"https://sport.sky.it/calcio/serie-a/{link_year}/calendario-risultati#giornata-38"
    )
    return link


def remove_junk_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove junk rows

    Args:
        df (pd.DataFrame): pandas dataframe

    Returns:
        pd.DataFrame: filtered dataframe
    """
    junk_rows = df.squadra_casa.str.len() > 23
    df = df[~junk_rows]
    return df


def strip_teams_names(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate teams string
        "Atalanta Atalanta" -> Atalanta

    Args:
        df (pd.DataFrame): pandas dataframe

    Returns:
        pd.DataFrame: filtered dataframe
    """
    for col in ["squadra_casa", "squadra_trasferta"]:
        df[col] = df[col].str.split(" ", expand=True)[0]
    return df


def clean_link(link: list, day: int) -> pd.DataFrame:
    """Clean skysport.com tables

    Args:
        link (list): list of scraped matchdays
        day (int): matchday index

    Returns:
        pd.DataFrame: cleaned dataframe from scraping
    """
    df = link[day].dropna(axis=1)
    df.columns = ["squadra_casa", "risultato", "squadra_trasferta"]
    df = remove_junk_rows(df)
    df = strip_teams_names(df)
    df["giornata"] = day + 1
    return df


def handle_new_or_postponed(df: pd.DataFrame) -> pd.DataFrame:
    """Handle postponed matches

    Args:
        df (pd.DataFrame): dataframe

    Returns:
        pd.DataFrame: dataframe with fixed values for postponed
    """
    invalid = df.risultato.str.contains(r"^(?!\d+ - \d+$)")
    df.loc[invalid, "risultato"] = "0 - 0"
    return df


def separate_goals(df: pd.DataFrame) -> pd.DataFrame:
    """Separate results into goals scored and received

    Args:
        df (pd.DataFrame): dataframe

    Returns:
        pd.DataFrame: dataframe with separated scored and received goals
    """
    df[["goal_casa", "goal_trasferta"]] = df.risultato.str.split(
        " - ", expand=True
    ).astype(int)
    df = df.drop("risultato", axis=1)
    return df


def scrape_sky(year: int, ongoing: bool, days: int):
    """Flow of data scraping

    The matches data are taken from skysport.com,
        processed and then saved in the data folder

    Args:
        year (int): year of the season
        ongoing (bool): if True, the season is the current season
        days (int): number of played matchdays in the season
    """
    link = get_pd_html(year, ongoing)
    df = pd.DataFrame()
    for day in range(days):
        matchday = clean_link(link, day)
        df = pd.concat([df, matchday], ignore_index=True)
    df = handle_new_or_postponed(df)
    df = separate_goals(df)
    df["anno"] = year
    df.to_csv(f"data/leagues/{year}.csv")
