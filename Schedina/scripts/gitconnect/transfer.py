import pandas as pd
from github import Github as gh
from gitconnect.gitset import token, repopath
from set_up import league_data, config_var

foldpath = config_var.path

g = gh(token)
repo = g.get_repo(repopath)
year = league_data.latest_year
day = league_data.latest_matchday()
forecasts = league_data.targets

def to_git():
    for target in forecasts:
        name = f'{year}/{day}/{target}.csv'
        path = f'{foldpath}/data/forecasts/{name}'
        with open(path, 'r') as file:
            data = file.read()
        repo.create_file(f'data/{name}', 'create', data)