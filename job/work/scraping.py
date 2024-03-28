import pandas as pd
import logging


def clean_link(link, day):
    matchday = link[day].dropna(axis=1)
    matchday.columns = ["squadra_casa", "risultato", "squadra_trasferta"]

    junk_rows = matchday.squadra_casa.str.len() > 23
    matchday = matchday[~junk_rows]

    for col in ["squadra_casa", "squadra_trasferta"]:
        matchday[col] = matchday[col].str.split(" ", expand=True)[0]
    matchday["giornata"] = day
    return matchday


def scrape_sky(year, ongoing, days):
    link_year = "" if ongoing else year
    link = pd.read_html(
        f"https://sport.sky.it/calcio/serie-a/{link_year}/calendario-risultati#giornata-38"
    )
    logging.info(f"Scraping from SkySport: season {year}")
    df = pd.DataFrame()
    for day in range(days):
        matchday = clean_link(link, day)
        df = pd.concat([df, matchday], ignore_index=True)

    postponed = df.risultato == "-"
    df.loc[postponed, "risultato"] = "0 - 0"

    goal_cols = ["goal_casa", "goal_trasferta"]
    df[goal_cols] = df.risultato.str.split(" - ", expand=True).astype(int)
    df = df.drop("risultato", axis=1)
    df["anno"] = year
    df.to_csv(f"data/leagues/{year}.csv")

    if ongoing:
        next = clean_link(link, days)
        next = next.drop("risultato", axis=1)
        next_casa = next.rename(
            columns={
                "squadra_casa": "squadra",
                "squadra_trasferta": "avversario",
            }
        )
        next_trasferta = next.rename(
            columns={
                "squadra_casa": "avversario",
                "squadra_trasferta": "squadra",
            }
        )
        next = pd.concat([next_casa, next_trasferta], ignore_index=True)
        next["anno"] = year
        next.to_csv("data/leagues/next.csv")
    else:
        None
