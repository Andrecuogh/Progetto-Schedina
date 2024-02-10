import pandas as pd
from set_up_kivy.config_var import REPOPATH
from set_up_kivy.league_data import latest_year, targets


def retrieve(day):
    list_df = []
    for target in targets:
        act_day = int(day) - 1
        name = f"{latest_year}/{act_day}/{target}.csv"
        path = f"https://raw.githubusercontent.com/{REPOPATH}/main/data/{name}"
        print(path)
        df = pd.read_csv(path, index_col=0)
        list_df.append(df)
    return list_df
