import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier

models = {
    "Gf": KNeighborsClassifier(n_neighbors=67),
    "Gs": KNeighborsClassifier(n_neighbors=210),
    "1X2": GradientBoostingClassifier(
        max_depth=5,
        max_features=0.75,
        min_samples_split=10,
        n_estimators=150,
        n_iter_no_change=5,
        random_state=66,
        subsample=0.75,
    ),
    "GG-NG": KNeighborsClassifier(n_neighbors=23),
    "O-U": KNeighborsClassifier(n_neighbors=23),
}

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def Xy_split(dataframe, target):

    df = dataframe.copy()
    df["classe"] = ""

    if target == "Gf":
        df["classe"] = df["gol_fatti_casa"]

    elif target == "Gs":
        df["classe"] = df["gol_fatti_trasferta"]

    elif target == "1X2":
        df.loc[df.gol_fatti_casa > df.gol_fatti_trasferta, "classe"] = "1"
        df.loc[df.gol_fatti_casa == df.gol_fatti_trasferta, "classe"] = "X"
        df.loc[df.gol_fatti_casa < df.gol_fatti_trasferta, "classe"] = "2"

    elif target == "GG-NG":
        goal_mask = (df.gol_fatti_casa > 0) & (df.gol_fatti_trasferta > 0)
        df.loc[goal_mask, "classe"] = "GG"
        df.loc[~goal_mask, "classe"] = "NG"

    elif target == "O-U":
        o_u_mask = (df.gol_fatti_casa + df.gol_fatti_trasferta) > 2
        df.loc[o_u_mask, "classe"] = "O"
        df.loc[~o_u_mask, "classe"] = "U"

    else:
        return "Invalid target"

    X = df.drop(["classe", "squadra", "gol_fatti_casa", "gol_fatti_trasferta"], axis=1)
    y = df["classe"]

    return X, y


def predict_scores(df):
    Xnot = df.sort_values(by=["anno", "giornata"]).iloc[-10:]
    probabilities = {
        "giornata": Xnot.giornata.max(),
        "anno": Xnot.anno.max(),
        "partite": Xnot.squadra,
    }
    Xnot = Xnot.drop(["squadra", "gol_fatti_casa", "gol_fatti_trasferta"], axis=1)
    for target in targets:
        X, y = Xy_split(df, target)
        model = models[target]
        model.fit(X, y)
        y_pred = model.predict_proba(Xnot)
        df_proba = pd.DataFrame(
            y_pred, columns=model.classes_, index=probabilities["partite"]
        )
        probabilities.update({target: df_proba})

    return probabilities
