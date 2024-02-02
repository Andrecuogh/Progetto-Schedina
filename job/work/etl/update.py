import pandas as pd
from set_up.league_data import latest_matchday, seasons
from set_up.league_season import Stagione
from transform import creation
from set_up.config_var import PATH
import logging

class Updater():
    def __init__(self):
        self.stagione_attuale = Stagione('2023', ongoing=True)
        self.path = PATH

    def check_aggiornamento(self):
        try:
            df = pd.read_csv(
                f'{self.path}/data/dataframes/{self.stagione_attuale.year}.csv',
                index_col=0
                )
            logging.info(f'Dataframe found with {len(df)//10} matchdays')
        except:
            logging.info(f'No dataframe found. Creating...')
            for year in seasons.keys():
                logging.info(f'Creating {year}')
                stagione = Stagione(year, True)
                stagione.process_data()
                stagione.export_csv(PATH)
                creation.create_year_df(stagione)

            df = pd.read_csv(
                f'{self.path}/data/dataframes/{self.stagione_attuale.year}.csv',
                index_col=0
                )

        self.bisogno = len(df) < (latest_matchday()-5)*10

    def aggiornamento(self):
        logging.info(f'Searching for update')
        self.check_aggiornamento()
        if self.bisogno:

            self.stagione_attuale.process_data()
            self.stagione_attuale.export_csv(path=PATH)

            df = pd.read_csv(
                f'{self.path}/data/dataframes/{self.stagione_attuale.year}.csv',
                index_col=0
                )

            logging.info(f'Before concat | {df.tail()}')

            nuovo = creation.create_matchday_df(
                self.stagione_attuale, 
                latest_matchday()
                )
            df = pd.concat(
                [df, nuovo], 
                ignore_index=True
                )

            logging.info(f"After concat | {df.tail()}")
            df.to_csv(
                f'{self.path}/data/dataframes/{self.stagione_attuale.year}.csv'
                )