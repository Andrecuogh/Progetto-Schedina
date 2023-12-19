import pandas as pd
from gitconnect.gitset import repopath
from set_up import league_data

year = league_data.latest_year
day = league_data.latest_year
forecasts = league_data.targets

def retrieve():
    for target in forecasts:
        name = f'{year}/{day}/{target}.csv'
        path = f'https://raw.githubusercontent.com/{repopath}/main/data/{name}'
        df = pd.read_csv(path, index_col=0)