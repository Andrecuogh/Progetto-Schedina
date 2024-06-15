import pandas as pd
import numpy as np
import logging
import logging.config
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from flow import validate_datafolder, get_data
from etl_utils.creation import create_dataset
from etl_utils.prediction import Xy_split
from etl_config.league_data import seasons
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
}
targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def tune_model(X, y, model, cross_val, names):
    gscv = GridSearchCV(
        estimator=model["algorithm"],
        param_grid=model["parameters"],
        scoring="accuracy",
        cv=cross_val,
        n_jobs=2,
    )
    gscv.fit(X, y)
    logger.info(f"Estimator: {gscv.estimator}")
    logger.info(f"Parameters: {gscv.best_params_}")
    logger.info(f"Score: {np.round(gscv.best_score_, 2)}")
    log_df = X[(X.anno == 2023) & (X.giornata == 10)]
    log_pred = gscv.predict_proba(log_df)
    log_df = pd.DataFrame(log_pred, columns=gscv.classes_, index=names)
    log_df["y_hat"] = gscv.predict(X[(X.anno == 2023) & (X.giornata == 10)])
    log_df["y_true"] = y[(X.anno == 2023) & (X.giornata == 10)].values
    logger.info(f"10th match:\n{log_df}\n")


def flow(season_list):
    validate_datafolder(season_list)
    df = get_data(season_list)
    df = create_dataset(df)
    for target in targets:
        X, y = Xy_split(df, target)
        names = df[(df.anno == 2023) & (df.giornata == 10)].squadra
        tscv = TimeSeriesSplit(n_splits=4)
        logger.info(f"Target: {target}")
        for model in models.values():
            tune_model(X, y, model, tscv, names)


if __name__ == "__main__":
    flow(seasons)
