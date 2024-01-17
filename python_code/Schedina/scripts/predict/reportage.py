from set_up import league_data, config_var
from predict.accuracy import corr_dict
import pandas as pd
import numpy as np
import os
import logging

foldpath = config_var.path.replace("python_code/Schedina", "")
lat_year = league_data.latest_year

def save_report(prediction_list):
    newpath = lat_year + '/' + str(league_data.latest_matchday())
    os.makedirs(f'{foldpath}/data/{newpath}', exist_ok=True)
    for forecast, category in zip(prediction_list, league_data.targets):
        if type(forecast) == list:
            forecast = pd.concat([forecast[0], pd.Series(np.full(1, np.nan)),forecast[1]])
        forecast.to_csv(
            f'{foldpath}/data/{newpath}/{category}.csv')
    logging.info(f'Folder to save | {foldpath}/data/{newpath}/{category}.csv')

    new_df = pd.DataFrame(corr_dict, index = ['Score']).T
    new_df.to_csv(f'{foldpath}/data/accuracy_dashboard/acc_dict.csv')

def display_report(prediction_list):
    for slide in prediction_list:
        print(slide)
    