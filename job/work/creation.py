import pandas as pd


def concat_tables(df, next):
    df["status"] = "train"
    next["status"] = "test"
    dataframe = pd.concat([df, next])
    return dataframe


def add_previous_result(df):
    df = df.sort_values(by=["anno", "giornata"])
    df["esito"] = df.esito.map({"vittoria": 1, "pareggio": 0, "sconfitta": -1})

    for t in range(1, 6):
        for col in ["gol_fatti", "gol_subiti", "esito"]:
            name = f"{col}_{t}"
            df[name] = df.groupby("squadra")[col].shift(t)

    cols = ["punti", "posizione", "media_gol_fatti", "media_gol_subiti"]
    df[cols] = df.groupby("squadra")[cols].shift(1)
    df = df[df.giornata > 4]
    df_avversari = df[["anno", "giornata", "squadra", "posizione"]]
    df_avversari = df_avversari.rename(columns={"squadra": "avversario"})
    df = df.merge(
        df_avversari,
        on=["anno", "giornata", "avversario"],
        suffixes=["", "_avversario"],
    )
    return df


def round_goals(df):
    df["gol_fatti"] = df.gol_fatti.where(df.gol_fatti < 4, 4)
    df["gol_subiti"] = df.gol_subiti.where(df.gol_subiti < 4, 4)
    return df


def divide_tables(df):
    previous = df[df.status == "train"].copy()
    previous = previous.drop("status", axis=1)
    next = df[df.status == "test"].copy()
    next = next.drop("status", axis=1)
    return previous, next


def create_dataset(df, next):
    dataframe = concat_tables(df, next)
    dataframe = add_previous_result(dataframe)
    dataframe = round_goals(dataframe)
    df, next = divide_tables(dataframe)
    return df, next
