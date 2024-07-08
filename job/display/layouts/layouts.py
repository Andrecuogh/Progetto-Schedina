from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ListProperty,
)
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from utils.data_provider import DataProvider
from utils.colors import colors1 as cmap

dp = DataProvider()


class SchedinaLayout(ScreenManager):

    def set_initial_screen(self, need_to_update):
        if need_to_update:
            self.current = "updatebox"
        else:
            self.current = "scorepage"


class Updater(Screen):
    name = StringProperty("updatebox")


class ScorePage(Screen):
    name = StringProperty("scorepage")
    match_id = NumericProperty(-1)
    utilbar = ObjectProperty(None)
    navigation = ObjectProperty(None)
    resultbox = ObjectProperty(None)
    input_disabled = BooleanProperty(False)

    def on_match_id(self, instance, value):
        self.navigation.change_labels(value)
        self.resultbox.change_values(value)


class UtilBar(GridLayout):
    tutorial_button = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tutorials = Tutorial()
        self.readme = Readme()

    def load_tutorial(self):
        if self.parent.input_disabled:
            return None
        self.parent.resultbox.change_screen("right")
        self.parent.input_disabled = True
        self.parent.add_widget(self.tutorials)
        self.tutorials.page_index = 0
        self.tutorials.skipbutton.text = "Skip"

    def skip_tutorial(self):
        self.parent.input_disabled = False
        self.tutorials.page_index = 0
        self.parent.remove_widget(self.tutorials)
        self.parent.resultbox.change_screen("right")

    def load_readme(self):
        if self.parent.input_disabled:
            return None
        self.parent.input_disabled = True
        self.parent.add_widget(self.readme)

    def exit_readme(self):
        self.parent.input_disabled = False
        self.parent.remove_widget(self.readme)


class Tutorial(FloatLayout):
    texts = ListProperty(dp.get_tutorials_strings())
    page_index = NumericProperty(-1)
    text_area = ObjectProperty(None)
    skipbutton = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_touch_up(self, touch):
        swipe_distance = 0.15
        x0, x1 = touch.osx, touch.psx
        dx = x1 - x0
        if dx < -swipe_distance:
            self.page_index += 1

    def on_page_index(self, instance, value):
        if value == 11:
            self.parent.utilbar.skip_tutorial()
        else:
            if value == 2:
                self.skipbutton.pos_hint = {"x": 0.04, "y": 0.92}
                self.skipbutton.size_hint = (0.92, 0.07)
            if value == 7:
                self.parent.input_disabled = False
                self.parent.resultbox.change_screen("left")
                self.parent.input_disabled = True
            elif value == 10:
                self.skipbutton.text = "Exit"
                self.skipbutton.pos_hint = {"x": 0.04, "y": 0.3}
                self.skipbutton.size_hint = (0.92, 0.1)
            self.change_layout(value)

    def change_layout(self, i):
        tdicts = self.texts[i]
        self.text_area.text = tdicts["text"]
        self.change_rect_dims(2, tdicts["top"])
        self.change_rect_dims(4, tdicts["mid"])
        self.change_rect_dims(6, tdicts["bottom"])
        self.text_area.pos_hint = tdicts["label"]["pos_hint"]
        self.text_area.size_hint = tdicts["label"]["size_hint"]
        self.text_area.texture_update()

    def change_rect_dims(self, i, dims):
        s = self.parent.size
        self.canvas.children[i].pos = [s[j] * dims["pos"][j] for j in range(2)]
        self.canvas.children[i].size = [s[j] * dims["size"][j] for j in range(2)]


class Readme(FloatLayout):
    readmelabel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readmelabel.text = dp.readme


class PageNavigator(FloatLayout):
    match = ObjectProperty(None)
    proba_button = ObjectProperty(None)
    accessory_button = ObjectProperty(None)

    def change_labels(self, match_id):
        home, away = dp.get_current_matches(match_id, short=True)
        self.match.text = f"{home} - {away}"

    def change_background_color(self, direction):
        if direction == "right":
            self.proba_button.background_color = cmap["label_pressed"]
            self.accessory_button.background_color = cmap["label"]
        elif direction == "left":
            self.proba_button.background_color = cmap["label"]
            self.accessory_button.background_color = cmap["label_pressed"]
        else:
            raise Exception("Invalid change direction")


class ResultBox(ScreenManager):
    probability = ObjectProperty(None)
    accessory = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_list = self.screens

    def update_screen_ref(self):
        self.probability = self.get_screen("probability_current")
        self.accessory = self.get_screen("accessory_current")

    def change_values(self, match_id):
        self.update_screen_ref()
        self.probability.change_proba(match_id)
        self.accessory.change_matches_data(match_id)

    def on_touch_up(self, touch):
        swipe_distance = 0.15
        x0, x1, y0, y1 = touch.osx, touch.psx, touch.osy, touch.psy
        dx = x1 - x0
        dy = y1 - y0
        invalid_touch = self.check_swipe_touch_border(x0, y0)
        if invalid_touch:
            pass
        else:
            if dy > swipe_distance:
                self.change_match("up")
            elif dy < -swipe_distance:
                self.change_match("down")
            elif dx > swipe_distance:
                self.change_screen("right")
            elif dx < -swipe_distance:
                self.change_screen("left")

    def check_swipe_touch_border(self, x, y):
        collide_ranking = y < 0.35 and self.current == "accessory_current"
        collide_utilbar = y > 0.9
        return any([collide_ranking, collide_utilbar])

    def change_match(self, direction):
        if self.parent.input_disabled:
            return None
        self.transition.direction = direction
        self.current = self.current.replace("current", "next")
        self.update_screen_list()
        move = {"up": 1, "down": -1}
        self.parent.match_id += move[direction]

    def update_screen_list(self):
        screen_list = {
            2: "probability_current",
            3: "accessory_current",
            0: "probability_next",
            1: "accessory_next",
        }
        for i, name in screen_list.items():
            self.screen_list[i].name = f"{name}_temp"
        for screen in self.screens:
            screen.name = screen.name.replace("_temp", "")
        self.screen_list = [self.get_screen(name) for name in screen_list.values()]

    def change_screen(self, direction):
        if self.parent.input_disabled:
            return None
        destination = {
            "left": "accessory_current",
            "right": "probability_current",
        }
        self.transition.direction = direction
        self.current = destination[direction]
        self.parent.navigation.change_background_color(direction)


class ProbabilityScreen(Screen):
    gfgs = ObjectProperty(None)
    oxt = ObjectProperty(None)
    ggng = ObjectProperty(None)
    ou = ObjectProperty(None)

    def format_perc(self, df, i):
        value = df.iloc[i]
        text = "{:.0%}".format(value)
        color_i = int(value * 100)
        return text, color_i

    def add_values(self, grid, df, match_id):
        matchday_df = df.iloc[match_id]
        for i, widget in enumerate(grid.children):
            text, color_i = self.format_perc(matchday_df, i)
            widget.text = text
            widget.background_color = cmap["colorbar"][color_i]

    def change_proba(self, match_id):
        self.gfgs.change_team_labels(match_id)
        self.add_values(self.gfgs.scored, dp.dfs["Gf"], match_id)
        self.add_values(self.gfgs.received, dp.dfs["Gs"], match_id)
        self.add_values(self.oxt.grid, dp.dfs["1X2"], match_id)
        self.add_values(self.ggng.grid, dp.dfs["GG-NG"], match_id)
        self.add_values(self.ou.grid, dp.dfs["O-U"], match_id)


class AccessoriesScreen(Screen):
    prevencounter = ObjectProperty(None)
    momentum = ObjectProperty(None)
    ranking = ObjectProperty(None)

    def change_matches_data(self, match_id):
        self.prevencounter.change_values(match_id)
        self.momentum.change_values(match_id)
        self.ranking.change_values(match_id)


class ScoredReceived(FloatLayout):
    scored = ObjectProperty(None)
    received = ObjectProperty(None)
    home = ObjectProperty(None)
    away = ObjectProperty(None)

    def change_team_labels(self, match_id):
        home, away = dp.get_current_matches(match_id, short=True)
        self.home.text = home
        self.away.text = away


class OneXTwo(FloatLayout):
    grid = ObjectProperty(None)


class GolNoGol(FloatLayout):
    grid = ObjectProperty(None)


class OverUnder(FloatLayout):
    grid = ObjectProperty(None)


class PrevEncounter(FloatLayout):
    matches = ObjectProperty(None)
    years = ObjectProperty(None)

    def change_values(self, match_id):
        N_RESULT = 3
        df = dp.get_direct_encounters(match_id, N_RESULT)
        for i in range(len(df)):
            res_label = self.matches.children[i]
            res_label.text = df.loc[i, "label"]
            year_label = self.years.children[i]
            year_label.text = str(df.loc[i, "anno"])


class Momentum(FloatLayout):
    home = ObjectProperty(None)
    away = ObjectProperty(None)
    grid = ObjectProperty(None)

    def change_values(self, match_id):
        self.change_team_labels(match_id)
        df = dp.get_momentum_labels(match_id)
        for child, row in zip(self.grid.children, df.itertuples()):
            child.text = row.label
            child.background_color = cmap["results"][row.color]

    def change_team_labels(self, match_id):
        home, away = dp.get_current_matches(match_id, short=True)
        self.home.text = home
        self.away.text = away


class Ranking(FloatLayout):
    grid = ObjectProperty(None)

    def change_values(self, match_id):
        df = dp.get_ranking(match_id)
        for button, value in zip(self.grid.data, df.itertuples(index=False)):
            if value.highlight:
                color = cmap["highlighted"]
            else:
                color = cmap["colorbar"][90]
            button["background_color"] = color
            button.update({"text": value.label})
        self.grid.refresh_from_data()
