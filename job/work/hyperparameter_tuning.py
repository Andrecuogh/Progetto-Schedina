import pandas as pd
import numpy as np

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import ParameterGrid
from predict.ml_functions import Xy_split

from set_up.league_data import targets

df = pd.DataFrame()
for year in [2019, 2020, 2021, 2022, 2023]:
    season = pd.read_csv(f"data/dataframes/{year}.csv", index_col=0)
    season["year"] = year
    df = pd.concat([df, season], ignore_index=True)
    df["yGf"] = df.yGf.where(df.yGf <= 4, 4)
    df["yGs"] = df.yGs.where(df.yGs <= 4, 4)

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

scores = []
for target in targets:
    print(target)
    X_train, y_train = Xy_split(df[df.year != 2023], target)
    X_test, y_test = Xy_split(df[df.year == 2023], target)
    for model in models.keys():
        algo = models[model]
        for i, param in enumerate(parameters[model]):
            algo_fit = algo(**param).fit(X_train, y_train)
            score = algo_fit.score(X_test, y_test)
            scorelist = [target, algo.__name__, str(param), np.round(score, 2)]
            scores.append(scorelist)
            print(f"{algo.__name__} : {(i+1)}/{len(parameters[model])}", end="\r")
        print("")

cols = [
    "target",
    "model",
    "parameters",
    "score",
]

scores_df = pd.DataFrame(scores, columns=cols)
scores_df = scores_df.sort_values(by="score").drop_duplicates(
    subset="target", keep="last"
)
scores_df.to_csv("data\accuracy_dashboard\ml_models_score.csv")
print(scores_df)
