""" create """

import pandas as pd
import numpy as np
from etl.load import Loader
from set_up import config_var
import logging

foldpath = config_var.PATH


def create_empty():
    df = pd.DataFrame(np.zeros((10, 43)))
    col_dict = {
        "Partita": str,
        "Rt-5h": int,
        "Rt-4h": int,
        "Rt-3h": int,
        "Rt-2h": int,
        "Rt-1h": int,
        "Classifica h": int,
        "Rt-5a": int,
        "Rt-4a": int,
        "Rt-3a": int,
        "Rt-2a": int,
        "Rt-1a": int,
        "Classifica a": int,
        "media gol_fatti h": float,
        "media gol_subiti h": float,
        "media gol_fatti a": float,
        "media gol_subiti a": float,
        "varianza gol_fatti h": float,
        "varianza gol_subiti h": float,
        "varianza gol_fatti a": float,
        "varianza gol_subiti a": float,
        "Gf-5h": int,
        "Gf-4h": int,
        "Gf-3h": int,
        "Gf-2h": int,
        "Gf-1h": int,
        "Gs-5h": int,
        "Gs-4h": int,
        "Gs-3h": int,
        "Gs-2h": int,
        "Gs-1h": int,
        "Gf-5a": int,
        "Gf-4a": int,
        "Gf-3a": int,
        "Gf-2a": int,
        "Gf-1a": int,
        "Gs-5a": int,
        "Gs-4a": int,
        "Gs-3a": int,
        "Gs-2a": int,
        "Gs-1a": int,
        "yGf": int,
        "yGs": int,
    }

    df.columns = col_dict.keys()
    df = df.astype(col_dict)

    return df


def create_matchday_df(LS, g):
    df = create_empty()
    tables = Loader(LS).process(g)

    for m in tables["partite"].index:
        sfida = (
            tables["partite"].loc[m, "squadra_casa"]
            + "-"
            + tables["partite"].loc[m, "squadra_trasferta"]
        )
        df.loc[m, "Partita"] = sfida

        if not tables["prediction"]:
            scoresh = tables["partite"].loc[m, "risultato"].split(" - ")
            df.loc[m, "yGf"] = int(scoresh[0])
            df.loc[m, "yGs"] = int(scoresh[1])

    for j, partita_prec in enumerate(tables["p_prec"]):
        for i, incontro in enumerate(df["Partita"].values):
            st1 = "Gf-" + str(5 - j) + "h"
            st2 = "Gs-" + str(5 - j) + "h"
            st3 = "Gf-" + str(5 - j) + "a"
            st4 = "Gs-" + str(5 - j) + "a"
            teamh = incontro.split("-")[0]
            teama = incontro.split("-")[1]

            if teamh in partita_prec.loc[:, "squadra_casa"].values:
                e = int(
                    partita_prec["risultato"][partita_prec["squadra_casa"] == teamh]
                    .values[0]
                    .split("-")[0]
                )
            else:
                e = int(
                    partita_prec["risultato"][
                        partita_prec["squadra_trasferta"] == teamh
                    ]
                    .values[0]
                    .split("-")[1]
                )
            df.loc[i, st1] = e

            if teama in partita_prec.loc[:, "squadra_casa"].values:
                e = int(
                    partita_prec["risultato"][partita_prec["squadra_casa"] == teama]
                    .values[0]
                    .split("-")[0]
                )
            else:
                e = int(
                    partita_prec["risultato"][
                        partita_prec["squadra_trasferta"] == teama
                    ]
                    .values[0]
                    .split("-")[1]
                )
            df.loc[i, st3] = e

            if teamh in partita_prec.loc[:, "squadra_casa"].values:
                f = int(
                    partita_prec["risultato"][partita_prec["squadra_casa"] == teamh]
                    .values[0]
                    .split("-")[1]
                )
            else:
                f = int(
                    partita_prec["risultato"][
                        partita_prec["squadra_trasferta"] == teamh
                    ]
                    .values[0]
                    .split("-")[0]
                )
            df.loc[i, st2] = f

            if teama in partita_prec.loc[:, "squadra_casa"].values:
                f = int(
                    partita_prec["risultato"][partita_prec["squadra_casa"] == teama]
                    .values[0]
                    .split("-")[1]
                )
            else:
                f = int(
                    partita_prec["risultato"][
                        partita_prec["squadra_trasferta"] == teama
                    ]
                    .values[0]
                    .split("-")[0]
                )
            df.loc[i, st4] = f

    for i, risultato_prec in enumerate(tables["table"]):
        for pair in range(10):
            teamh = df.loc[pair, "Partita"].split("-")[0]
            teama = df.loc[pair, "Partita"].split("-")[1]

            rt5h = risultato_prec[risultato_prec["squadra"] == teamh]["esito"].values[0]
            stringa_th = "Rt-" + str(5 - i) + "h"
            if rt5h == "vittoria":
                df.loc[pair, stringa_th] = 2
            elif rt5h == "pareggio":
                df.loc[pair, stringa_th] = 1
            else:
                df.loc[pair, stringa_th] = 0

            rt5a = risultato_prec[risultato_prec["squadra"] == teama]["esito"].values[0]
            stringa_ta = "Rt-" + str(5 - i) + "a"
            if rt5a == "vittoria":
                df.loc[pair, stringa_ta] = 2
            elif rt5a == "pareggio":
                df.loc[pair, stringa_ta] = 1
            else:
                df.loc[pair, stringa_ta] = 0

    for matchn in range(10):
        teamh = df.loc[matchn, "Partita"].split("-")[0]
        teama = df.loc[matchn, "Partita"].split("-")[1]

        for pitch, team in zip(["h", "a"], [teamh, teama]):
            df.loc[matchn, "Classifica " + pitch] = tables["classifica"].loc[
                team, "posizione"
            ]

            for descr_stat in ["media", "varianza"]:
                for gs_or_gr in ["gol_fatti", "gol_subiti"]:
                    gol_stat = descr_stat + " " + gs_or_gr + " " + pitch
                    df.loc[matchn, gol_stat] = tables["goals"].loc[
                        team, descr_stat + "_" + gs_or_gr.lower()
                    ]

    return df


def create_year_df(LS):
    logging.info("Creating dataframe")
    d = []
    for g in range(5, LS.days):
        matchday_df = create_matchday_df(LS, g)
        d.append(matchday_df)

    year_df = pd.concat(d, ignore_index=True)
    year_df.to_csv(f"{foldpath}/data/dataframes/{LS.year}.csv")
