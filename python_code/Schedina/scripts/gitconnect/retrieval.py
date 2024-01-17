import pandas as pd
from gitconnect.gitset import repopath
from set_up import league_data

year = league_data.latest_year
forecasts = league_data.targets

def retrieve(day):
    list_df = []
    for target in forecasts:
        act_day = int(day) - 1
        name = f'{year}/{act_day}/{target}.csv'
        path = f'https://raw.githubusercontent.com/{repopath}/main/data/{name}'
        df = pd.read_csv(path, index_col=0)
        list_df.append(df)
    return list_df

