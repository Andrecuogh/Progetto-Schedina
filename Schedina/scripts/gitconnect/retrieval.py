import pandas as pd
from gitconnect.gitset import repopath
from set_up import league_data

year = league_data.latest_year
day = league_data.latest_matchday()
forecasts = league_data.targets

def retrieve():
    list_df = []
    for target in forecasts:
        name = f'{year}/{day}/{target}.csv'
        path = f'https://raw.githubusercontent.com/{repopath}/main/data/{name}'
        df = pd.read_csv(path, index_col=0)
        list_df.append(df)
    return list_df

