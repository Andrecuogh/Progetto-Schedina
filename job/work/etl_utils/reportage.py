import os
import pandas as pd
from etl_config.log import logger

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def formatt(pred: dict) -> dict:
    """Format predictions dataframes"""
    pred["Gf"].columns = pred["Gf"].columns.astype(int)
    pred["Gs"].columns = pred["Gs"].columns.astype(int)
    pred["1X2"] = pred["1X2"][["1", "X", "2"]]
    for target in targets:
        pred[target] = pred[target].round(2)
    return pred


def compatible(pred: dict) -> dict:
    """Make predictions compatible with display API"""
    for target in targets:
        pred[target].index.name = "Partita"
    return pred


def save_report(pred: dict) -> None:
    """Save predictions"""
    anno = pred["anno"]
    giornata = pred["giornata"]
    os.makedirs(f"data/predictions/{anno}/{giornata}", exist_ok=True)
    for target in targets:
        pred[target].to_csv(f"data/predictions/{anno}/{giornata}/{target}.csv")
    metadata = pd.read_csv("data/metadata.csv")
    metadata_to_add = pd.DataFrame({"anno": [anno], "giornata": [giornata]})
    metadata = pd.concat([metadata, metadata_to_add], ignore_index=True)
    metadata.to_csv("data/metadata.csv", index=False)


def save_accessories_tables(accessories: dict) -> None:
    path = "data/accessories"
    os.makedirs(path, exist_ok=True)
    accessories["previous_encounters"].to_csv(
        f"{path}/previous_encounters.csv", index=False
    )
    accessories["ranking"].to_csv(f"{path}/ranking.csv", index=False)


def display_report(pred: dict) -> None:
    """Print predictions"""
    for name, df in pred.items():
        if type(df) in [pd.Series, pd.DataFrame]:
            logger.info(f"{name}:\n{df}")
        else:
            logger.info(f"{name}: {df}")


def report(accessories: dict, pred: dict) -> None:
    """Report the results of predictions"""
    logger.info("Start reportage of results")
    pred = formatt(pred)
    pred = compatible(pred)
    save_report(pred)
    save_accessories_tables(accessories)
    display_report(pred)
    logger.info("End reportage of results\n")
