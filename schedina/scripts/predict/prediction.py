""" prediction """

import pandas as pd
from predict import ml_functions
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.multioutput import MultiOutputClassifier

def predict_scores(df, target, preds):

    X, y = ml_functions.Xy_split(df, target=target)
    names = preds['Partita']
    Xnot = preds.drop(['Partita', 'yGf', 'yGs'], axis=1)

    if target == 'Goals':
        bay = ComplementNB()
        model = MultiOutputClassifier(bay)
        model.fit(X,y)
        y_pred = model.predict_proba(Xnot)
        df = [pd.DataFrame(y_pred[i]).set_index(names) for i in [0,1]]

    else:
        if target == '1X2':
            model = LogisticRegression(max_iter = 1000, multi_class = 'multinomial')

        elif target == 'GG-NG':
            model = LogisticRegression(max_iter = 1000)

        elif target == 'O-U':
            model = ComplementNB()


        model.fit(X,y)
        y_pred = model.predict_proba(Xnot)
        df = pd.DataFrame(y_pred, columns = model.classes_).set_index(names)

        try:
            df = df[['V', 'N', 'P']]
        except:
            pass

    return df