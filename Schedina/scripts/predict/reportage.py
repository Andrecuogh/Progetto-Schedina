from set_up import league_data, config_var
import pandas as pd
import numpy as np
import os

foldpath = config_var.path
lat_year = league_data.latest_year

def save_report(prediction_list):
    newpath = lat_year + '/' + str(league_data.latest_matchday())
    os.makedirs(f'{foldpath}/data/forecasts/{newpath}', exist_ok=True)
    for forecast, category in zip(prediction_list, league_data.targets):
        if type(forecast) == list:
            forecast = pd.concat([forecast[0], pd.Series(np.full(1, np.nan)),forecast[1]])
        forecast.to_csv(
            f'{foldpath}/data/forecasts/{newpath}/{category}.csv')

def display_report(prediction_list):
    for slide in prediction_list:
        print(slide)
    