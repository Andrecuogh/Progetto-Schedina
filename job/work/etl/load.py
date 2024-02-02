import pandas as pd
from set_up.config_var import PATH
from set_up.league_season import Stagione


class Loader(Stagione):
    def __init__(self, ls):
        self.year = ls.year
        self.teams = ls.teams
        self.leagues = ls.leagues
        self.days = ls.days
        self.next = ls.next

    def process(self, giorno):
        try:
            partite = pd.read_csv(
                f"{PATH}/data/scores/{self.year}/{giorno}.csv", index_col=0
            )
            goals = pd.read_csv(
                f"{PATH}/data/scored_received/{self.year}/{giorno}.csv", index_col=0
            )
            prediction = False

        except:
            partite = self.next
            goals = pd.read_csv(
                f"{PATH}/data/scored_received/{self.year}/{giorno-1}.csv", index_col=0
            )
            prediction = True

        p_prec = [
            pd.read_csv(f"{PATH}/data/scores/{self.year}/{n}.csv", index_col=0)
            for n in range(giorno - 5, giorno)
        ]
        table = [
            pd.read_csv(f"{PATH}/data/results/{self.year}/{n}.csv", index_col=0)
            for n in range(giorno - 5, giorno)
        ]
        classifica = pd.read_csv(
            f"{PATH}/data/rankings/{self.year}/{giorno-1}.csv", index_col=0
        )

        tables = {
            "partite": partite,
            "goals": goals,
            "p_prec": p_prec,
            "table": table,
            "classifica": classifica,
            "prediction": prediction,
        }

        return tables
