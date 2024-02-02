import pandas as pd
from set_up.config_var import PATH

def computegf(df):
    return [i.split(' - ')[0] for i in df['risultato']]

def computegs(df):
    return [i.split(' - ')[1] for i in df['risultato']]

def compute1x2(df):
    newlist = []
    for score in df['risultato']:
        s1 = int(score.split(' - ')[0])
        s2 = int(score.split(' - ')[1])
        if s1 > s2:
            newlist.append('V')
        elif s1 < s2:
            newlist.append('P')
        else:
            newlist.append('N')
    return newlist

def computegoals(df):
    newlist = []
    for score in df['risultato']:
        s1 = int(score.split(' - ')[0])
        s2 = int(score.split(' - ')[1])
        if s1 > 0 and s2 > 0:
            newlist.append('GG')
        else:
            newlist.append('NG')
    return newlist

def computeOU(df):
    newlist = []
    for score in df['risultato']:
        s1 = int(score.split(' - ')[0])
        s2 = int(score.split(' - ')[1])
        if s1 + s2 > 2:
            newlist.append('O')
        else:
            newlist.append('U')
    return newlist

trgts = ['Gf', 'Gs', '1X2', 'GG-NG', 'O-U']
fun = [computegf, computegs, compute1x2, computegoals, computeOU]
lim = 19
tot = 10*(lim-6-2)

corr_dict = {}
for f, trgt in zip(fun, trgts):
    correct = 0
    for i in range(6, lim):
        if i == 15 or i == 16:
            continue
        df_score = pd.read_csv(f'{PATH}/data/scores/2023/{i}.csv', index_col = 0)
        scores = f(df_score)
        df_pred = pd.read_csv(f'{PATH}/data/2023/{i}/{trgt}.csv', index_col = 0)
        pred = df_pred.T.idxmax().values
        for j in range(10):
            if scores[j] == pred[j]:
                correct += 1
    corr_dict[trgt] = correct/tot
