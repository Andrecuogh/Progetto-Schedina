""" load """

import pandas as pd
from set_up import config_var

path = config_var.path

def load_tables(LS, g):

    try:
        partite = pd.read_csv(f'{path}/data/scores/{LS.year}/{g}.csv',
                              index_col=0)
        goals = pd.read_csv(f'{path}/data/scored_received/{LS.year}/{g}.csv',
                            index_col=0)
        prediction = False

    except:
        partite = LS.next
        goals = pd.read_csv(f'{path}/data/scored_received/{LS.year}/{g-1}.csv',
                            index_col=0)
        prediction = True

    p_prec = [pd.read_csv(f'{path}/data/scores/{LS.year}/{n}.csv',
                          index_col=0) for n in range(g-5, g)]
    table = [pd.read_csv(f'{path}/data/results/{LS.year}/{n}.csv',
                          index_col=0) for n in range(g-5, g)]
    classifica = pd.read_csv(f'{path}/data/rankings/{LS.year}/{g-1}.csv',
                              index_col=0)

    tables = {'partite': partite,
              'goals': goals,
              'p_prec': p_prec,
              'table': table,
              'classifica': classifica,
              'prediction': prediction}

    return tables