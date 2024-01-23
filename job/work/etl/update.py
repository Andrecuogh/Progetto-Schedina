""" Update """

import pandas as pd
from set_up import league_data, league_season
from transform import creation
from set_up import config_var
import logging

path = config_var.path

def need_to_update():
    ongoing_ls = league_season.LeagueSeason('2023', ongoing=True)

    df = pd.read_csv(f'{path}/data/dataframes/{ongoing_ls.year}.csv',
                      index_col=0)

    is_need = len(df) < (league_data.latest_matchday()-5)*10

    logging.info(f'Need to update? | {is_need}')
    return is_need


def update_df():

    if need_to_update():
        ongoing_ls = league_season.LeagueSeason('2023', ongoing=True)

        ongoing_ls.process_data()
        ongoing_ls.export_csv(path=path)

        df = pd.read_csv(f'{path}/data/dataframes/{ongoing_ls.year}.csv',
                          index_col=0)

        logging.info(f'Before concat | {df.tail()}')

        new = creation.create_matchday_df(ongoing_ls, league_data.latest_matchday())
        df = pd.concat([df, new], ignore_index=True)

        logging.info(f"After concat | {df.tail()}")
        df.to_csv(f'{path}/data/dataframes/{ongoing_ls.year}.csv')