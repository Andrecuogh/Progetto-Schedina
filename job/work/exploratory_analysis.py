import pandas as pd
import numpy as np
import logging
import logging.config
from flow import validate_datafolder, get_data
from etl_utils.creation import create_dataset
from etl_utils.prediction import Xy_split
from etl_config.league_data import seasons
from etl_config.log import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("etl_flow")

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def flow(season_list):
    validate_datafolder(season_list)
    df = get_data(season_list)
    df = create_dataset(df)
    logger.info(f"Dataframe rows x columns: {df.shape[0]} x {df.shape[1]}")
    logger.info(f"Seasons: {df.anno.unique()}")
    year_df = df.groupby("anno", as_index=False).giornata.count()
    logger.info(f"\nNumber of matchdays per season:\n{year_df}")
    goals_df = df.groupby("anno")[["gol_fatti_casa", "gol_fatti_trasferta"]].mean()
    logger.info(f"\nAverage goals per mathces per season:\n{goals_df.round(2)}")
    for target in targets:
        X, y = Xy_split(df, target)
        total = pd.concat([X, y], axis=1)
        pivoted = total.groupby(["anno", "classe"]).size().unstack(fill_value=0)
        logger.info(f"\nNumber of classes for target {target}\n{pivoted}")
    logger.info()


if __name__ == "__main__":
    flow(seasons)
