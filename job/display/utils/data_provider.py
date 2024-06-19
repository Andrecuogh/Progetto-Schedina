import pandas as pd
from utils.connector import Loader


class DataProvider:
    def __init__(self):
        self.get_data()
        self.store_match_info()

    def get_data(self):
        loader = Loader()
        self.dfs = loader.load_dfs()
        self.readme = loader.download_readme()
        self.prev_enc = loader.extract_previous_encounters()
        self.ranking = loader.load_ranking()
        self.momentum = loader.load_momentum()

    def store_match_info(self, match_index=0):
        self.id = match_index
        self.home, self.away = self.dfs["Gf"].index[self.id].split("-")
        self.h_short = self.home[0:3].upper()
        self.a_short = self.away[0:3].upper()

    def update_id(self, move):
        new_id = self.id + move
        if new_id < 0:
            new_id = 9
        elif new_id > 9:
            new_id = 0
        self.store_match_info(new_id)

    def get_columns(self, target):
        df = self.dfs[target].copy()
        return df.columns

    def get_current_match_row(self, target):
        df = self.dfs[target].copy()
        return df.iloc[self.id]

    def format_perc(self, df, i):
        value = df.iloc[i]
        text = "{:.0%}".format(value)
        color_i = int(value * 100)
        return text, color_i

    def get_current_matches(self, short=False):
        if short:
            return self.h_short, self.a_short
        else:
            return self.home, self.away

    def get_direct_encounters(self, n_encounters):
        home, away = self.get_current_matches()
        home_match = f"{home} - {away}"
        away_match = f"{away} - {home}"
        encounters = [home_match, away_match]
        df = self.prev_enc[self.prev_enc.partita.isin(encounters)]
        df = df.sort_values(by=["anno", "giornata"], ascending=False)
        top = df.head(n_encounters).copy()
        top["label"] = top.apply(
            lambda row: row["partita_short"].replace("-", row["risultato"]), axis=1
        )
        top = top.reset_index(drop=True)
        return top

    def get_momentum_labels(self):
        home_matches = self.momentum[
            self.momentum.partita_short.str.contains(self.h_short)
        ].head(5)
        away_matches = self.momentum[
            self.momentum.partita_short.str.contains(self.a_short)
        ].head(5)
        home_matches["score"] = home_matches.apply(
            self.get_markup_score, team=self.home, axis=1
        )
        away_matches["score"] = away_matches.apply(
            self.get_markup_score, team=self.away, axis=1
        )
        home_matches["color"] = home_matches.apply(
            self.get_color_from_result, team=self.home, axis=1
        )
        away_matches["color"] = away_matches.apply(
            self.get_color_from_result, team=self.away, axis=1
        )
        home_matches["label"] = (
            " vs "
            + home_matches.partita_short.str.replace(self.h_short, "").str.replace(
                " - ", ""
            )
            + "\n"
            + home_matches.score
        )
        away_matches["label"] = (
            " vs "
            + away_matches.partita_short.str.replace(self.a_short, "").str.replace(
                " - ", ""
            )
            + "\n"
            + away_matches.score
        )
        labels = pd.concat([home_matches, away_matches])
        return labels

    def get_markup_score(self, row, team):
        i = row["partita"].split(" - ").index(team)
        goals = row["risultato"].split(" - ")
        goals[i] = f"[u][b]{goals[i]}[/b][/u]"
        return " - ".join(goals)

    def get_color_from_result(self, row, team):
        i = row["partita"].split(" - ").index(team)
        j = abs(i - 1)
        gol_team = row["risultato"].split(" - ")[i]
        gol_opponent = row["risultato"].split(" - ")[j]
        if gol_team > gol_opponent:
            return "win"
        elif gol_team < gol_opponent:
            return "loss"
        elif gol_team == gol_opponent:
            return "draw"
        else:
            raise Exception()

    def get_ranking(self):
        df = pd.DataFrame(self.ranking.values.reshape(-1, 1), columns=["label"])
        df["label"] = df.astype(str)
        home_i = df[df.label == self.h_short].index[0]
        away_i = df[df.label == self.a_short].index[0]
        df["highlight"] = False
        for i in [home_i, away_i]:
            df.loc[i - 1 : i + 3, "highlight"] = True
        return df
