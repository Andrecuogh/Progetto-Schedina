import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import logging

models = {
    "Gf": GradientBoostingClassifier(
        n_estimators=50,
        max_features=1.0,
        subsample=0.75,
        random_state=66,
    ),
    "Gs": GradientBoostingClassifier(
        n_estimators=50,
        max_features=1.0,
        subsample=1.0,
        random_state=66,
    ),
    "1X2": GradientBoostingClassifier(
        n_estimators=50,
        max_features=1.0,
        subsample=0.75,
        random_state=66,
    ),
    "GG-NG": GradientBoostingClassifier(
        n_estimators=50,
        max_features=1.0,
        subsample=0.75,
        random_state=66,
    ),
    "O-U": GradientBoostingClassifier(
        n_estimators=50,
        max_features=0.75,
        subsample=0.75,
        random_state=66,
    ),
}

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def Xy_split(dataframe: pd.DataFrame, target: list) -> tuple[pd.DataFrame]:
    """Split the dataframe into features (X) and target (y)"""
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


def predict_scores(df: pd.DataFrame) -> dict:
    """Predict probabilities of events"""
    logging.info("Predicting scores")
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
