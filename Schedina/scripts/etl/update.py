""" Update """

import pandas as pd
from set_up import league_data, league_season
from transform import creation
from set_up import config_var

path = config_var.path

def need_to_update():
    ongoing_ls = league_season.LeagueSeason('2023', ongoing=True)

    df = pd.read_csv(f'{path}/data/dataframes/{ongoing_ls.year}.csv',
                      index_col=0)

    is_need = len(df) < (league_data.latest_matchday()-5)*10

    return is_need


def update_df():

    if need_to_update():
        ongoing_ls = league_season.LeagueSeason('2023', ongoing=True)

        ongoing_ls.process_data()
        ongoing_ls.export_csv(path=path)

        df = pd.read_csv(f'{path}/data/dataframes/{ongoing_ls.year}.csv',
                          index_col=0)

        new = creation.create_matchday_df(ongoing_ls, league_data.latest_matchday())
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(f'{path}/data/dataframes/{ongoing_ls.year}.csv')