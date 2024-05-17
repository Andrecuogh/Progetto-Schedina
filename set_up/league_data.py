import pandas as pd

teamlist = {
    "2019": [
        "Milan",
        "Sampdoria",
        "Genoa",
        "Parma",
        "Fiorentina",
        "Lazio",
        "Spal",
        "Lecce",
        "Verona",
        "Juventus",
        "Udinese",
        "Atalanta",
        "Inter",
        "Torino",
        "Cagliari",
        "Bologna",
        "Roma",
        "Brescia",
        "Napoli",
        "Sassuolo",
    ],
    "2020": [
        "Milan",
        "Sampdoria",
        "Genoa",
        "Parma",
        "Fiorentina",
        "Lazio",
        "Crotone",
        "Spezia",
        "Verona",
        "Juventus",
        "Udinese",
        "Atalanta",
        "Inter",
        "Torino",
        "Cagliari",
        "Bologna",
        "Roma",
        "Benevento",
        "Napoli",
        "Sassuolo",
    ],
    "2021": [
        "Milan",
        "Sampdoria",
        "Genoa",
        "Venezia",
        "Fiorentina",
        "Lazio",
        "Salernitana",
        "Spezia",
        "Verona",
        "Juventus",
        "Udinese",
        "Atalanta",
        "Inter",
        "Torino",
        "Cagliari",
        "Bologna",
        "Roma",
        "Empoli",
        "Napoli",
        "Sassuolo",
    ],
    "2022": [
        "Milan",
        "Sampdoria",
        "Lecce",
        "Monza",
        "Fiorentina",
        "Lazio",
        "Salernitana",
        "Spezia",
        "Verona",
        "Juventus",
        "Udinese",
        "Atalanta",
        "Inter",
        "Torino",
        "Cremonese",
        "Bologna",
        "Roma",
        "Empoli",
        "Napoli",
        "Sassuolo",
    ],
    "2023": [
        "Milan",
        "Frosinone",
        "Lecce",
        "Monza",
        "Fiorentina",
        "Lazio",
        "Salernitana",
        "Genoa",
        "Verona",
        "Juventus",
        "Udinese",
        "Atalanta",
        "Inter",
        "Torino",
        "Cagliari",
        "Bologna",
        "Roma",
        "Empoli",
        "Napoli",
        "Sassuolo",
    ],
}

seasons = {"2019": False, "2020": False, "2021": False, "2022": False, "2023": True}

latest_year = [year for year in seasons.keys() if seasons[year]][0]

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]

postponed_days = [28]
postponed_matches = {}


def latest_matchday():
    scrap = pd.read_html(
        "https://sport.sky.it/calcio/serie-a/calendario-risultati#giornata-38"
    )
    for i, evento in enumerate(scrap):
        if i in postponed_days:
            continue
        if len(evento["Squadra 2"].iloc[-1].split(" ")) < 2:
            current = i
            break
    return current
