import pandas as pd
import numpy as np
import logging
import logging.config
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
    AdaBoostClassifier,
)
from sklearn.model_selection import GridSearchCV, GroupKFold
from league_data import seasons
from flow import validate_datafolder, get_data
from etl_utils.creation import create_dataset
from etl_utils.prediction import Xy_split
from etl_config.log import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("etl_flow")


models = {
    "lda": {
        "algorithm": LinearDiscriminantAnalysis(),
        "parameters": {"solver": ["svd"]},
    },
    "knn": {
        "algorithm": KNeighborsClassifier(),
        "parameters": {"n_neighbors": np.arange(1, 298, 11)},
    },
    "gb": {
        "algorithm": GradientBoostingClassifier(),
        "parameters": {
            "n_estimators": [50],
            "learning_rate": [0.1, 0.3],
            "max_depth": [3],
            "subsample": [0.75, 1.0],
            "max_features": [1.0, 0.75],
            "random_state": [66],
        },
    },
    "rf": {
        "algorithm": RandomForestClassifier(),
        "parameters": {
            "n_estimators": [50],
            "max_depth": [3, 5],
            "max_features": ["sqrt", 1.0],
            "random_state": [66],
        },
    },
    "ada": {
        "algorithm": AdaBoostClassifier(),
        "parameters": {
            "n_estimators": [50],
            "algorithm": ["SAMME"],
            "random_state": [66],
        },
    },
}
targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def tune_model(X, y, model, cross_val):
    gscv = GridSearchCV(
        estimator=model["algorithm"],
        param_grid=model["parameters"],
        scoring="accuracy",
        cv=cross_val,
        n_jobs=2,
    )
    gscv.fit(X, y, groups=X["anno"])

    logger.info(f"Estimator: {gscv.estimator}")
    logger.info(f"Parameters: {gscv.best_params_}")
    logger.info(f"Score: {np.round(gscv.best_score_, 2)}\n")


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
        group_kfold = GroupKFold(n_splits=len(df["anno"].unique()))
        logger.info(f"Target: {target}")
        for model in models.values():
            tune_model(X, y, model, group_kfold)


if __name__ == "__main__":
    flow(seasons)
