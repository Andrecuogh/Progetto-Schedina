import pandas as pd
from etl_config.log import logger


def remove_junk_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove junk rows"""
    junk_rows = df.squadra_casa.str.len() > 23
    df = df[~junk_rows]
    return df


def strip_teams_names(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate teams string
    "Atalanta Atalanta" -> Atalanta
    """
    for col in ["squadra_casa", "squadra_trasferta"]:
        df[col] = df[col].str.split(" ", expand=True)[0]
    return df


def clean_link(link: list, day: int) -> pd.DataFrame:
    """Clean skysport.com tables"""
    df = link[day].dropna(axis=1)
    df.columns = ["squadra_casa", "risultato", "squadra_trasferta"]
    df = remove_junk_rows(df)
    df = strip_teams_names(df)
    df["giornata"] = day + 1
    return df


def get_pd_html(year: int, ongoing: bool) -> pd.DataFrame:
    """Read skysport.com data"""
    if ongoing:
        link_year = ""
    else:
        link_year = year
    link = pd.read_html(
        f"https://sport.sky.it/calcio/serie-a/{link_year}/calendario-risultati#giornata-38"
    )
    return link


def handle_new_or_postponed(df: pd.DataFrame) -> pd.DataFrame:
    """Handle postponed matches"""
    invalid = df.risultato.str.contains(r"^(?!\d+ - \d+$)")
    df.loc[invalid, "risultato"] = "0 - 0"
    return df


def separate_goals(df: pd.DataFrame) -> pd.DataFrame:
    """Separate results into goals scored and received
    "1 - 0" ->
        scored = 1
        received = 0
    """
    df[["goal_casa", "goal_trasferta"]] = df.risultato.str.split(
        " - ", expand=True
    ).astype(int)
    df = df.drop("risultato", axis=1)
    return df


def get_next_matches(link: list, days: int) -> pd.DataFrame:
    """If ongoing season, extract prediction matches"""
    goal_cols = ["goal_casa", "goal_trasferta"]
    next = clean_link(link, days)
    next = next.drop("risultato", axis=1)
    next[goal_cols] = 0
    return next


def scrape_sky(year: int, ongoing: bool, days: int) -> None:
    """Flow of data scraping"""
    link = get_pd_html(year, ongoing)
    df = pd.DataFrame()
    for day in range(days):
        matchday = clean_link(link, day)
        df = pd.concat([df, matchday], ignore_index=True)
    df = handle_new_or_postponed(df)
    df = separate_goals(df)
    df["anno"] = year
    df.to_csv(f"data/leagues/{year}.csv")
