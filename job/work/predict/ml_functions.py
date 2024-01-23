""" ml_functions """


def Xy_split(dataframe, target):

    df = dataframe.copy()

    if target == 'Gf':
        X = df.drop(['yGf', 'yGs', 'Partita'], axis=1).copy()
        y = df['yGf'].copy()
    
    elif target == 'Gs':
        X = df.drop(['yGf', 'yGs', 'Partita'], axis=1).copy()
        y = df['yGs'].copy()

    else:
        df['Classe'] = 0
        for i in df.index:
            if target == '1X2':
                if df.loc[i, 'yGf'] > df.loc[i, 'yGs']:
                    df.loc[i, 'Classe'] = 'V'
                elif df.loc[i, 'yGf'] == df.loc[i, 'yGs']:
                    df.loc[i, 'Classe'] = 'N'
                else:
                    df.loc[i, 'Classe'] = 'P'

            elif target == "GG-NG":
                if df.loc[i, 'yGf'] != 0 and df.loc[i, 'yGs'] != 0:
                    df.loc[i, 'Classe'] = 'GG'
                else:
                    df.loc[i, 'Classe'] = 'NG'

            elif target == 'O-U':
                if df.loc[i, 'yGf'] + df.loc[i, 'yGs'] > 2:
                    df.loc[i, 'Classe'] = 'O'
                else:
                    df.loc[i, 'Classe'] = 'U'

            else:
                return "Invalid target variable"

        X = df.drop(['Classe', 'Partita', 'yGf', 'yGs'], axis=1).copy()
        y = df['Classe'].copy()

    return X, y