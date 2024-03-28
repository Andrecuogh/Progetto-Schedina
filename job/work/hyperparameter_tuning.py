from magic_job import validate_datafolder, get_data
from creation import create_dataset
from prediction import Xy_split
from set_up.league_data import seasons
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import ParameterGrid

models = {
    "lda": LinearDiscriminantAnalysis,
    "knn": KNeighborsClassifier,
    "gb": GradientBoostingClassifier,
}

parameters = {
    "lda": ParameterGrid({"solver": ["svd"]}),
    "knn": ParameterGrid({"n_neighbors": np.arange(1, 298, 11)}),
    "gb": ParameterGrid(
        {
            "n_estimators": [50, 100, 150],
            "max_depth": [3, 5],
            "min_samples_split": [2, 10, 20],
            "subsample": [0.75, 1.0],
            "max_features": [1.0, 0.75],
            "random_state": [66],
            "n_iter_no_change": [5, 10, 20],
        }
    ),
}

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def train_test_split(df, target):
    prev_year_df = df[df.anno != df.anno.max()]
    last_year_df = df[df.anno == df.anno.max()]
    X_train, y_train = Xy_split(prev_year_df, target)
    X_test, y_test = Xy_split(last_year_df, target)
    return X_train, y_train, X_test, y_test


def tune_model(X_train, y_train, X_test, y_test, target):
    scores = []
    print(target)
    for algorithm in models.keys():
        model = models[algorithm]
        for i, param in enumerate(parameters[algorithm]):
            model_fit = model(**param).fit(X_train, y_train)
            score = model_fit.score(X_test, y_test)
            scorelist = [target, model.__name__, str(param), np.round(score, 2)]
            scores.append(scorelist)
            print(f"{model.__name__} : {(i+1)}/{len(parameters[algorithm])}", end="\r")
        print("")

    return scores


def update_df(df, scores):
    cols = [
        "target",
        "model",
        "parameters",
        "score",
    ]
    scores_df = pd.DataFrame(scores, columns=cols)
    df = pd.concat([df, scores_df], ignore_index=True)
    return df


def get_max_score(df):
    df = df.sort_values(by=["target", "model", "score"])
    df = df.drop_duplicates(subset=["target", "model"], keep="last")
    return df


def flow(season_list):
    validate_datafolder(season_list)
    df, Xnot = get_data(season_list)
    df, Xnot = create_dataset(df, Xnot)
    scores_df = pd.DataFrame()
    for target in targets:
        X_train, y_train, X_test, y_test = train_test_split(df, target)
        scores = tune_model(X_train, y_train, X_test, y_test, target)
        scores_df = update_df(scores_df, scores)
    scores_df = get_max_score(scores_df)
    print(scores_df)


if __name__ == "__main__":
    flow(seasons)
