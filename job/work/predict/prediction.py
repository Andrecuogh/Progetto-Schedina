""" prediction """

import pandas as pd
from predict import ml_functions
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

def predict_scores(df, target, preds):

    X, y = ml_functions.Xy_split(df, target=target)
    names = preds['Partita']
    Xnot = preds.drop(['Partita', 'yGf', 'yGs'], axis=1)

    if target == 'Gf':
        model = GradientBoostingClassifier(n_estimators = 50,
            random_state = 66,
            max_depth = 5,
            subsample = 0.8,
            min_samples_leaf = 0.01,
            min_samples_split = 50)

    elif target == 'Gs':
        model = GradientBoostingClassifier(n_estimators = 50,
            random_state = 66,
            max_depth = 3,
            subsample = 0.8,
            min_samples_leaf = 1,
            min_samples_split = 50)

    else:
        if target == '1X2':
            model = LinearDiscriminantAnalysis()

        elif target == 'GG-NG':
            model = KNeighborsClassifier(n_neighbors=211)

        elif target == 'O-U':
            model = LinearDiscriminantAnalysis()


    model.fit(X,y)
    y_pred = model.predict_proba(Xnot)
    df = pd.DataFrame(y_pred, columns = model.classes_).set_index(names)

    try:
        df = df[['V', 'N', 'P']]
    except:
        pass

    return df
