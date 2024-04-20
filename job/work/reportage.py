import os

targets = ["Gf", "Gs", "1X2", "GG-NG", "O-U"]


def save_report(pred):
    anno = pred["anno"]
    giornata = pred["giornata"]
    os.makedirs(f"data/{anno}/{giornata}", exist_ok=True)
    for target in targets:
        pred[target].to_csv(f"data/{anno}/{giornata}/{target}.csv")


def display_report(pred):
    for name, df in pred.items():
        print(name)
        print(df, end="\n\n")


def formatt(pred):
    pred["Gf"].columns = pred["Gf"].columns.astype(int)
    pred["Gs"].columns = pred["Gs"].columns.astype(int)
    pred["1X2"] = pred["1X2"][["1", "X", "2"]]
    for target in targets:
        pred[target] = pred[target].round(2)
    return pred


def compatible(pred):
    for target in targets:
        pred[target].index.name = "Partita"
    pred["1X2"] = pred["1X2"].rename({"1": "V", "X": "N", "2": "P"}, axis=1)
    return pred


def report(pred):
    pred = formatt(pred)
    pred = compatible(pred)
    save_report(pred)
    display_report(pred)
