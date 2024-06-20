import ssl
from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.clock import Clock
from utils.colors import colors1 as cmap
from utils.connector import Updater
from utils.data_provider import DataProvider

ssl._create_default_https_context = ssl._create_stdlib_context


class MainApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_screen()
        self.kv_directory = "layouts"
        self.register_fonts()
        self.colors = cmap
        Window.clearcolor = self.colors["background"]

    def build(self) -> ScreenManager:
        self.dp = DataProvider()
        self.sm = Builder.load_file(f"{self.kv_directory}/Schedina.kv")
        self.score_sm = self.sm.get_screen("scorepage").children[0].children[0]
        self.tutorial_boxes = self.load_tutorial()
        self.about_box = self.add_about_box()
        self.add_values()
        self.update_if_any()
        return self.sm

    def init_screen(self):
        self.sf = 1.0  # prod: 1.0; test 0.314
        self.screen_to_body = 0.852
        # Window.size = (
        #     1080 * self.screen_to_body * self.sf,
        #     2400 * self.screen_to_body * self.sf,
        # )  # only for testing in pc

    def register_fonts(self):
        font_path = "utils/fonts"
        LabelBase.register(
            DEFAULT_FONT,
            f"{font_path}/calibri/calibri.ttf",
            fn_bold=f"{font_path}/calibri/calibrib.ttf",
        )
        LabelBase.register("arial", f"{font_path}/arial/arial.ttf")

    def update_if_any(self):
        self.updater = Updater()
        need_to_update = self.updater.search_update()
        if need_to_update:
            self.sm.current = "updatebox"
        else:
            self.sm.current = "scorepage"

    def load_tutorial(self) -> dict[FloatLayout]:
        tutorial = Builder.load_file(
            f"{self.kv_directory}/scorepage/utilbar/Tutorial.kv"
        )
        tut_boxes = {
            page: tutorial.children[i] for i, page in enumerate(self.sm.screen_names)
        }
        tutorial.clear_widgets()
        return tut_boxes

    def add_about_box(self) -> Button:
        about = Builder.load_file(f"{self.kv_directory}/scorepage/utilbar/About.kv")
        about.text = self.dp.readme
        return about

    def add_label_text(self, target: str, area_name: str, grid_id: int = 1):
        area = self.get_area_from_name(area_name)
        labels = self.dp.get_columns(target)
        grid = area.children[grid_id]
        for widget, label in zip(grid.children, labels):
            widget.text = label

    def add_values(self):
        self.add_probabilities_values()
        self.add_accessories_values()

    def add_probabilities_values(self):
        self.add_value_text(target="Gf", area_name="ScoredReceived", grid_id=1)
        self.add_value_text(target="Gs", area_name="ScoredReceived")
        self.add_value_text(target="1X2", area_name="1X2")
        self.add_value_text(target="GG-NG", area_name="Gol-NoGol")
        self.add_value_text(target="O-U", area_name="OverUnder")
        self.add_teams_labels()

    def add_accessories_values(self):
        self.add_previous_encounters()
        self.add_momentum()
        self.add_ranking()

    def add_value_text(self, target: str, area_name: str, grid_id: int = 0):
        area = self.get_area_from_name(area_name)
        df = self.dp.get_current_match_row(target)
        grid = area.children[grid_id]
        for i, widget in enumerate(grid.children):
            text, color_i = self.dp.format_perc(df, i)
            widget.text = text
            widget.background_color = self.colors["colorbar"][color_i]

    def add_teams_labels(self):
        home, away = self.dp.get_current_matches(short=True)
        proba_area = self.get_area_from_name("ScoredReceived")
        proba_area.children[-2].text = home
        proba_area.children[-3].text = away
        form_area = self.get_area_from_name("momentum", screen="accessory_current")
        form_grid = form_area.children[2]
        form_grid.children[1].text = home
        form_grid.children[0].text = away
        navigation_area = self.sm.get_screen("scorepage").children[1]
        label = navigation_area.children[0]
        label.text = f"{home} - {away}"

    def get_area_from_name(self, area_name: str, screen: str = "probability_current"):
        screen = (
            self.sm.get_screen("scorepage").children[0].children[0].get_screen(screen)
        )
        for child in screen.children:
            if child.area == area_name:
                return child

    def add_previous_encounters(self):
        N_RESULT = 3
        df = self.dp.get_direct_encounters(n_encounters=N_RESULT)
        area = self.get_area_from_name("PreviousEncounters", screen="accessory_current")
        result_grid = area.children[0]
        year_grid = area.children[1]
        for i in range(len(df)):
            res_label = result_grid.children[i]
            res_label.text = df.loc[i, "label"]
            year_label = year_grid.children[i]
            year_label.text = str(df.loc[i, "anno"])

    def add_momentum(self):
        df = self.dp.get_momentum_labels()
        area = self.get_area_from_name("momentum", screen="accessory_current")
        grid = area.children[0]
        for child, row in zip(grid.children, df.itertuples()):
            child.text = row.label
            child.background_color = self.colors["results"][row.color]

    def add_ranking(self):
        area = self.get_area_from_name("Ranking", screen="accessory_current")
        grid = area.children[0]
        df = self.dp.get_ranking()
        for button, highlight in zip(grid.data, df.highlight):
            if highlight:
                color = self.colors["highlighted"]
            else:
                color = self.colors["colorbar"][90]
            button["background_color"] = color
        grid.refresh_from_data()

    def change_view(self, touch):
        x0, y0 = touch.pos_initial
        x1, y1 = touch.pos_final
        dx = x1 - x0
        dy = y1 - y0
        navigation_area = self.sm.get_screen("scorepage").children[1]
        if y0 < touch.size[1] * 0.4 and self.score_sm.current == "accessory_current":
            pass
        elif dy > touch.swipe_distance:
            navigation_button = navigation_area.children[1]
            navigation_button.trigger_action(0)
        elif dy < -touch.swipe_distance:
            navigation_button = navigation_area.children[3]
            navigation_button.trigger_action(0)
        elif dx > touch.swipe_distance:
            navigation_button = navigation_area.children[-1].children[1]
            navigation_button.trigger_action(0)
            navigation_button.trigger_action(1)
        elif dx < -touch.swipe_distance:
            navigation_button = navigation_area.children[-1].children[0]
            navigation_button.trigger_action(0)
            navigation_button.trigger_action(1)

    def change_match(self, move):
        self.dp.update_id(move)
        self.add_values()

    def go_to_screen(self, direction):
        screen_list = {
            2: "probability_current",
            3: "accessory_current",
            0: "probability_next",
            1: "accessory_next",
        }
        self.score_sm.transition.direction = direction
        self.score_sm.current = self.score_sm.current.replace("current", "next")
        for i, name in screen_list.items():
            self.score_sm.screen_list[i].name = f"{name}_temp"
        for screen in self.score_sm.screens:
            screen.name = screen.name.replace("_temp", "")
        self.score_sm.screen_list = [
            self.score_sm.get_screen(name) for name in screen_list.values()
        ]


if __name__ == "__main__":
    MainApp().run()
