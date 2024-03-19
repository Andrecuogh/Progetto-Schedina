import pandas as pd
import logging


def create_matchday_df(LS, g):
    df = pd.DataFrame()
    tables = Loader(LS).process(g)
    gol_cols = ["goal_casa", "goal_trasferta"]
    team_cols = ["squadra_casa", "squadra_trasferta"]
    partita_curr = tables["partite"].copy()
    partita_curr[gol_cols] = partita_curr.risultato.str.split(
        " - ", expand=True
    ).astype(int)

    df[team_cols] = partita_curr[team_cols]

    if not tables["prediction"]:
        df[["yGf", "yGs"]] = partita_curr[gol_cols]

    for j, partita_prec in enumerate(tables["p_prec"]):
        partita_prec[gol_cols] = partita_prec.risultato.str.split(
            " - ", expand=True
        ).astype(int)

        pitchs = ["casa", "trasferta"]
        for campo in pitchs:
            merged = pd.DataFrame()
            for i in [0, 1]:
                str_gf = f"Gf-{str(5 - j)}-{campo}"
                str_gs = f"Gs-{str(5 - j)}-{campo}"
                pitch = pitchs[i]
                other = pitchs[i - 1]
                correspondence = partita_curr.merge(
                    right=partita_prec,
                    left_on=f"squadra_{campo}",
                    right_on=f"squadra_{pitch}",
                    suffixes=("", "_y"),
                )
                correspondence = correspondence[
                    [f"squadra_{campo}", "goal_casa_y", "goal_trasferta_y"]
                ]
                correspondence = correspondence.rename(
                    {f"goal_{pitch}_y": str_gf, f"goal_{other}_y": str_gs},
                    axis=1,
                )
                merged = pd.concat([merged, correspondence])

            df = df.merge(merged, on=f"squadra_{campo}")
        df = df.rename(
            {
                f"Gf-{str(5 - j)}-casa": f"Gf-{str(5 - j)}-h",
                f"Gs-{str(5 - j)}-casa": f"Gs-{str(5 - j)}-h",
                f"Gf-{str(5 - j)}-trasferta": f"Gf-{str(5 - j)}-a",
                f"Gs-{str(5 - j)}-trasferta": f"Gs-{str(5 - j)}-a",
            },
            axis=1,
        )

    for i, risultato_prec in enumerate(tables["table"]):
        result_mapper = {
            "vittoria": 2,
            "pareggio": 1,
            "sconfitta": 0,
        }
        risultato_prec["esito"] = risultato_prec.esito.map(result_mapper)
        for pitch in ["casa", "trasferta"]:
            str_rt = f"Rt-{str(5 - i)}"
            df[str_rt] = df.merge(
                right=risultato_prec,
                left_on=f"squadra_{pitch}",
                right_on="squadra",
                suffixes=("-h", "-a"),
            ).esito

    for pitch in ["casa", "trasferta"]:
        df = df.merge(
            right=tables["classifica"].posizione,
            left_on=f"squadra_{pitch}",
            right_on="squadra",
            right_index=True,
            suffixes=("-h", "-a"),
        )

    for pitch in ["casa", "trasferta"]:
        df = df.merge(
            right=tables["goals"],
            left_on=f"squadra_{pitch}",
            right_index=True,
            suffixes=("_h", "_a"),
        )

    df["Partita"] = df["squadra_casa"] + "-" + df["squadra_trasferta"]
    df = df.drop(["squadra_casa", "squadra_trasferta"], axis=1)
    return df


def create_year_df(LS):
    logging.info("Creating dataframe")
    d = []
    for g in range(5, LS.days):
        matchday_df = create_matchday_df(LS, g)
        d.append(matchday_df)

    year_df = pd.concat(d, ignore_index=True)
    year_df.to_csv(f"data/dataframes/{LS.year}.csv")
