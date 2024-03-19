import pandas as pd
from predict import ml_functions
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def predict_scores(df, target, preds):
    X, y = ml_functions.Xy_split(df, target=target)
    names = preds["Partita"]
    Xnot = preds.drop(["Partita", "yGf", "yGs"], axis=1)

    if target == "Gf":
        model = GradientBoostingClassifier(
            n_estimators=50,
            random_state=66,
            max_depth=5,
            subsample=0.8,
            min_samples_leaf=0.01,
            min_samples_split=50,
        )

    elif target == "Gs":
        model = GradientBoostingClassifier(
            n_estimators=50,
            random_state=66,
            max_depth=3,
            subsample=0.8,
            min_samples_leaf=1,
            min_samples_split=50,
        )

    else:
        if target == "1X2":
            model = LinearDiscriminantAnalysis()

        elif target == "GG-NG":
            model = KNeighborsClassifier(n_neighbors=211)

        elif target == "O-U":
            model = LinearDiscriminantAnalysis()

    model.fit(X, y)
    y_pred = model.predict_proba(Xnot)
    df = pd.DataFrame(y_pred, columns=model.classes_).set_index(names)

    if target == "1X2":
        df = df[["V", "N", "P"]]

    return df


""" ml_functions """


def Xy_split(dataframe, target):
    df = dataframe.copy()

    if target == "Gf":
        X = df.drop(["yGf", "yGs", "Partita"], axis=1).copy()
        y = df["yGf"].copy()

    elif target == "Gs":
        X = df.drop(["yGf", "yGs", "Partita"], axis=1).copy()
        y = df["yGs"].copy()

    else:
        df["Classe"] = ""
        if target == "1X2":
            df.loc[df.yGf > df.yGs, "Classe"] = "V"
            df.loc[df.yGf == df.yGs, "Classe"] = "N"
            df.loc[df.yGf < df.yGs, "Classe"] = "P"

        elif target == "GG-NG":
            goal_mask = (df.yGf > 0) & (df.yGs > 0)
            df.loc[goal_mask, "Classe"] = "GG"
            df.loc[~goal_mask, "Classe"] = "NG"

        elif target == "O-U":
            o_u_mask = (df.yGf + df.yGs) > 2
            df.loc[o_u_mask, "Classe"] = "O"
            df.loc[~o_u_mask, "Classe"] = "U"

        else:
            return "Invalid target variable"

        X = df.drop(["Classe", "Partita", "yGf", "yGs"], axis=1).copy()
        y = df["Classe"].copy()

    return X, y
