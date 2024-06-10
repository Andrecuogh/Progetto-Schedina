from job.work.flow import validate_datafolder, get_data
from creation import create_dataset
from prediction import Xy_split
from job.work.league_data import seasons
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
    AdaBoostClassifier,
)
from sklearn.model_selection import GridSearchCV

models = {
    "lda": LinearDiscriminantAnalysis(),
    "knn": KNeighborsClassifier(),
    "gb": GradientBoostingClassifier(),
    "rf": RandomForestClassifier(),
    "ada": AdaBoostClassifier(),
}

parameters = {
    "lda": {"solver": ["svd"]},
    "knn": {"n_neighbors": np.arange(1, 298, 11)},
    "gb": {
        "n_estimators": [50, 100, 150],
        "learning_rate": [0.1, 0.3],
        "max_depth": [3, 5],
        "subsample": [0.75, 1.0],
        "max_features": [1.0, 0.75],
        "random_state": [66],
    },
    "rf": {
        "n_estimators": [100],
        "max_depth": [None, 3, 5],
        "max_features": ["sqrt", 1.0],
        "random_state": [66],
    },
    "ada": {
        "n_estimators": [50, 100, 150],
        "algorithm": ["SAMME"],
        "random_state": [66],
    },
}

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def tune_model(X, y, target):
    scores = []
    print(target)
    for algorithm in models.keys():
        model = models[algorithm]
        params = parameters[algorithm]
        gscv = GridSearchCV(
            estimator=model,
            param_grid=params,
            scoring="accuracy",
            cv=4,
            verbose=1,
            n_jobs=2,
        )
        gscv.fit(X, y)
        scorelist = [
            target,
            str(gscv.best_estimator_),
            str(gscv.best_params_),
            gscv.best_score_,
        ]
        scores.append(scorelist)

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
    df = get_data(season_list)
    df = create_dataset(df)
    scores_df = pd.DataFrame()
    for target in targets:
        X, y = Xy_split(df, target)
        scores = tune_model(X, y, target)
        scores_df = update_df(scores_df, scores)
    scores_df = get_max_score(scores_df)
    results = scores_df.sort_values(by="score", ascending=False)
    results = results.drop_duplicates(subset="target")
    for t in results.target:
        param = results[results.target == t].parameters.item()
        score = results[results.target == t].score.item()
        print(f"\n{t}\n{param}\n{score}")


if __name__ == "__main__":
    flow(seasons)
