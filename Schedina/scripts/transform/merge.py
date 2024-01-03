""" merge """

import pandas as pd
from set_up import config_var

foldpath = config_var.path

def merge_df(list_LS):

    sheet = []
    for ls in list_LS:
        year_df = pd.read_csv(f'{foldpath}/data/dataframes/{ls.year}.csv',
                              index_col=0)
        sheet.append(year_df)

    datafinal = pd.concat(sheet, ignore_index=True)
    datafinal['yGf'] = datafinal['yGf'].astype(int)
    datafinal['yGs'] = datafinal['yGs'].astype(int)

    for indice in datafinal.index:
        if datafinal.loc[indice, 'yGf'] > 4:
            datafinal.loc[indice, 'yGf'] = 4
        if datafinal.loc[indice, 'yGs'] > 4:
            datafinal.loc[indice, 'yGs'] = 4

    return datafinal