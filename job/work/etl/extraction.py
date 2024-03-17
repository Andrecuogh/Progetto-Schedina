import pandas as pd
import numpy as np
from transform import computation
import logging


class Extractor:
    def __init__(self, ls):
        self.year = ls.year
        self.teams = ls.teams
        self.leagues = ls.leagues
        self.days = ls.days


class ExtractorRanking(Extractor):
    def process(self):
        logging.info(f"Computing ranking")
        ranking = pd.DataFrame()

        classifica = []
        for giorno in range(self.days):
            df = computation.count_goals(self, giorno)

            df.loc[df.gol_fatti > df.gol_subiti, "esito"] = "vittoria"
            df.loc[df.gol_fatti < df.gol_subiti, "esito"] = "sconfitta"
            df.loc[df.gol_fatti == df.gol_subiti, "esito"] = "pareggio"

            punti_map = {"vittoria": 3, "pareggio": 1, "sconfitta": 0}
            df["punti"] = df.esito.map(punti_map)

            df = pd.get_dummies(df, columns=["esito"], prefix="", prefix_sep="")

            df["differenza_reti"] = df.gol_fatti - df.gol_subiti
            ranking = df.add(ranking, fill_value=0)
            ranking.sort_values(
                by=[
                    "punti",
                    "differenza_reti",
                    "gol_fatti",
                ],
                ascending=False,
                inplace=True,
            )
            ranking["posizione"] = np.arange(1, 21)
            classifica.append(ranking)

        return classifica


class ExtractorResults(Extractor):
    def process(self):
        logging.info(f"Computing results")
        risultati = []
        for giorno in range(self.days):
            df = computation.count_goals(self, giorno)

            df.loc[df.gol_fatti > df.gol_subiti, "esito"] = "vittoria"
            df.loc[df.gol_fatti < df.gol_subiti, "esito"] = "sconfitta"
            df.loc[df.gol_fatti == df.gol_subiti, "esito"] = "pareggio"

            df = df["esito"].reset_index()

            risultati.append(df)

        return risultati


class ExtractorGoals(Extractor):
    def process(self):
        logging.info(f"Computing goals")
        goal_segnati = pd.DataFrame()
        goal_segnati.index = self.teams
        goal_subiti = goal_segnati.copy()

        for giorno in range(self.days):
            goal = computation.count_goals(self, giorno)
            goal_segnati = pd.concat([goal_segnati, goal["gol_fatti"]], axis=1)
            goal_subiti = pd.concat([goal_subiti, goal["gol_subiti"]], axis=1)

        goal_segnati.columns = [i for i in range(1, self.days + 1)]
        goal_subiti.columns = [i for i in range(1, self.days + 1)]

        goal_totali = []
        for giornata in range(self.days):
            goal = pd.DataFrame(np.zeros((20, 4)))
            goal.columns = [
                "media_gol_fatti",
                "varianza_gol_fatti",
                "media_gol_subiti",
                "varianza_gol_subiti",
            ]
            goal.index = self.teams

            goal["media_gol_fatti"] = goal_segnati.loc[:, 1 : giornata + 1].mean(axis=1)
            goal["varianza_gol_fatti"] = goal_segnati.loc[:, 1 : giornata + 1].std(
                axis=1
            )
            goal["media_gol_subiti"] = goal_subiti.loc[:, 1 : giornata + 1].mean(axis=1)
            goal["varianza_gol_subiti"] = goal_subiti.loc[:, 1 : giornata + 1].std(
                axis=1
            )

            goal.fillna(0, inplace=True)
            goal_totali.append(goal)

        return goal_totali
