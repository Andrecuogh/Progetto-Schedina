import ssl
from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from utils.colors import colors1 as cmap
from utils.connector import Updater, Loader

ssl._create_default_https_context = ssl._create_stdlib_context


class MainApp(App):
    def __init__(self, *args, **kwargs):
        self.scale_factor = 0.3  # prod: 1.0 test 0.3
        super().__init__(*args, **kwargs)
        self.kv_directory = "layouts"
        self.match_id = 0
        LabelBase.register(
            DEFAULT_FONT,
            "utils/fonts/calibri/calibri.ttf",
            fn_bold="utils/fonts/calibri/calibrib.ttf",
        )
        self.colors = cmap
        Window.clearcolor = self.colors["background"]
        Window.size = (
            1080 * self.scale_factor,
            2400 * self.scale_factor,
        )  # only for testing in pc

    def get_data(self):
        loader = Loader()
        self.dfs = loader.load_dfs()
        self.readme = loader.download_readme()
        self.prev_enc = loader.extract_previous_encounters()

    def build(self) -> ScreenManager:
        self.get_data()
        self.sm = Builder.load_file(f"{self.kv_directory}/Schedina.kv")
        self.tutorial_boxes = self.load_tutorial()
        self.about_box = self.add_about_box()
        self.add_labels()
        self.update_if_any()
        return self.sm

    def update_if_any(self):
        self.updater = Updater()
        need_to_update = self.updater.search_update()
        if need_to_update:
            self.sm.current = "updatebox"
        else:
            self.sm.current = "homepage"

    def load_tutorial(self) -> dict[FloatLayout]:
        tutorial = Builder.load_file(f"{self.kv_directory}/Tutorial.kv")
        tut_boxes = {
            page: tutorial.children[i] for i, page in enumerate(self.sm.screen_names)
        }
        tutorial.clear_widgets()
        return tut_boxes

    def add_about_box(self) -> Button:
        about = Builder.load_file(f"{self.kv_directory}/About.kv")
        about.text = self.readme
        return about

    def add_labels(self):
        self.add_label_text(target="Gf", area_name="ScoredReceived", grid_id=2)
        self.add_label_text(target="1X2", area_name="1X2")
        self.add_label_text(target="GG-NG", area_name="Gol-NoGol")
        self.add_label_text(target="O-U", area_name="OverUnder")

    def add_label_text(self, target: str, area_name: str, grid_id: int = 1):
        area = self.get_area_from_name(area_name)
        labels = self.dfs[target].columns
        grid = area.children[grid_id]
        for widget, label in zip(grid.children, labels):
            widget.text = label

    def add_values(self):
        self.add_value_text(target="Gf", area_name="ScoredReceived", grid_id=1)
        self.add_value_text(target="Gs", area_name="ScoredReceived")
        self.add_value_text(target="1X2", area_name="1X2")
        self.add_value_text(target="GG-NG", area_name="Gol-NoGol")
        self.add_value_text(target="O-U", area_name="OverUnder")
        self.add_teams_labels()
        self.add_previous_encounters()

    def add_value_text(self, target: str, area_name: str, grid_id: int = 0):
        area = self.get_area_from_name(area_name)
        df = self.dfs[target].iloc[self.match_id]
        grid = area.children[grid_id]
        for i, widget in enumerate(grid.children):
            widget.text = "{:.0%}".format(df.iloc[i])
            widget.background_color = self.colors["colorbar"][int(df.iloc[i] * 100)]

    def add_teams_labels(self):
        home, away = self.dfs["Gf"].index[self.match_id].split("-")
        area = self.get_area_from_name("ScoredReceived")
        area.children[-2].text = home[0:3].upper()
        area.children[-3].text = away[0:3].upper()

    def get_area_from_name(self, area_name: str):
        screen = self.sm.get_screen("scorepage")
        for child in screen.children:
            if child.area == area_name:
                return child

    def add_previous_encounters(self):
        home, away = self.dfs["Gf"].index[self.match_id].split("-")
        home_match = f"{home} - {away}"
        away_match = f"{away} - {home}"
        df = self.prev_enc[self.prev_enc.partita.isin([home_match, away_match])]
        df = df.sort_values(by=["anno", "giornata"], ascending=False)
        N_RESULT = 3
        top = df.head(N_RESULT).copy()
        top["label"] = top.apply(
            lambda row: row["partita"].replace("-", row["risultato"]), axis=1
        )
        top = top.reset_index(drop=True)
        area = self.get_area_from_name("PreviousEncounters")
        result_grid = area.children[0]
        year_grid = area.children[1]
        for i in range(N_RESULT):
            res_label = result_grid.children[i]
            res_label.text = top.loc[i, "label"]
            year_label = year_grid.children[i]
            year_label.text = str(top.loc[i, "anno"])

    def change_match(self, move):
        self.match_id += move
        if self.match_id < 0:
            self.partita = 9
        elif self.match_id > 9:
            self.match_id = 0
        self.add_values()


if __name__ == "__main__":
    MainApp().run()
