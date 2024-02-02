import pandas as pd
import numpy as np
import logging


def scrape_sky(year):
    try:
        link = pd.read_html(
            f"https://sport.sky.it/calcio/serie-a/{year}/calendario-risultati#giornata-38"
        )
    except:
        link = pd.read_html(
            "https://sport.sky.it/calcio/serie-a/calendario-risultati#giornata-38"
        )

    logging.info("Scraping from SkySport")
    league = []
    for matchday in link:
        clean_matchday = matchday.drop(["Link partita", "Girone"], axis=1).dropna(
            axis=1
        )

        for indice, nome_squadra in enumerate(clean_matchday["Stato partita"].values):
            if len(nome_squadra) > 23:
                clean_matchday.drop(indice, inplace=True)

        for t, t1, t2 in zip(
            np.arange(10),
            clean_matchday["Risultato partita"].values,
            clean_matchday["Stato partita"].values,
        ):
            clean_matchday.iloc[t, 0] = t1.split(" ")[0]
            clean_matchday.iloc[t, 2] = t2.split(" ")[0]

        clean_matchday = clean_matchday[
            ["Risultato partita", "Stato partita", "Squadra 2"]
        ].copy()
        clean_matchday.columns = ["squadra_casa", "squadra_trasferta", "risultato"]
        clean_matchday.reset_index(inplace=True, drop=True)
        league.append(clean_matchday)

    return league
