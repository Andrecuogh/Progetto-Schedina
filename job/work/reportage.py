import os
import logging
import pandas as pd

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def save_report(pred: dict) -> None:
    """Save predictions"""
    anno = pred["anno"]
    giornata = pred["giornata"]
    os.makedirs(f"data/{anno}/{giornata}", exist_ok=True)
    for target in targets:
        pred[target].to_csv(f"data/{anno}/{giornata}/{target}.csv")
    metadata = pd.read_csv("data/metadata.csv")
    metadata_to_add = pd.DataFrame({"giornata": [giornata]})
    metadata = pd.concat([metadata, metadata_to_add], ignore_index=True)
    metadata.to_csv("data/metadata.csv", index=False)


def display_report(pred: dict) -> None:
    """Print predictions"""
    for name, df in pred.items():
        print(name)
        print(df, end="\n\n")


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
    pred["1X2"] = pred["1X2"].rename({"1": "V", "X": "N", "2": "P"}, axis=1)
    return pred


def report(pred: dict) -> None:
    """Report the results of predictions"""
    logging.info("Reporting results")
    pred = formatt(pred)
    pred = compatible(pred)
    save_report(pred)
    display_report(pred)
