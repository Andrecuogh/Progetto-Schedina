import pandas as pd
from set_up.league_data import latest_matchday, seasons
from set_up.league_season import Stagione
from transform import creation
from set_up.config_var import PATH
import logging


class Updater:
    def __init__(self, ls):
        logging.info(f"Searching for update")
        self.ls = ls
        self.year = ls.year
        self.path = PATH
        self.df = self.check_validity()

    def check_validity(self):
        try:
            df = pd.read_csv(
                f"{self.path}/data/dataframes/{self.year}.csv",
                index_col=0,
            )
            logging.info(f"Dataframe found with {len(df)//10 + 5 + 1} matchdays")
        except:
            df = None
        return df

    def check_aggiornamento(self):
        if type(self.df) != pd.DataFrame:
            logging.info(f"No dataframe found. Creating...")
            for year, ongoing in seasons.items():
                logging.info(f"Creating {year}")
                stagione = Stagione(year, ongoing)
                stagione.process_data()
                stagione.export_csv(PATH)
                creation.create_year_df(stagione)

            self.df = self.check_validity()

        self.bisogno = len(self.df) < (latest_matchday() - 5) * 10
        logging.info(f"Need to update: {self.bisogno}")

        if self.bisogno:
            self.aggiornamento()

    def aggiornamento(self):
        logging.info("Updating data")
        self.ls.process_data()
        self.ls.export_csv(path=PATH)

        logging.info(f"Before concat | {self.df.iloc[-11:, 0]}")

        nuovo = creation.create_matchday_df(self.ls, latest_matchday())
        df = pd.concat([self.df, nuovo], ignore_index=True)

        logging.info(f"After concat | {df.tail()}")
        df.to_csv(f"{self.path}/data/dataframes/{self.year}.csv")
