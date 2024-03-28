import os
import pandas as pd


def save_report(pred):
    anno = pred["anno"]
    giornata = pred["giornata"]
    os.makedirs(f"data/{anno}/{giornata}", exist_ok=True)
    for name, df in pred.items():
        if name in ["anno", "giornata"]:
            continue
        df.to_csv(f"data/{anno}/{giornata}/{name}.csv")


def display_report(pred):
    for name, df in pred.items():
        print(name)
        print(df, end="\n\n")


def formatt(pred):
    pred["Gf"].columns = pred["Gf"].columns.astype(int)
    pred["Gs"].columns = pred["Gs"].columns.astype(int)
    pred["1X2"] = pred["1X2"][["1", "X", "2"]]

    for name, df in pred.items():
        pred[name] = pred[name].round(2)

    return pred


def report(pred):
    pred = formatt(pred)
    save_report(pred)
    display_report(pred)
