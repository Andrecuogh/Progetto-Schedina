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
    startbutton = ObjectProperty(None)
    disabled_swipe = BooleanProperty(True)
    circle_grid = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_touch_up(self, touch):
        if not self.disabled_swipe:
            swipe_distance = 0.15
            x0, x1 = touch.osx, touch.psx
            dx = x1 - x0
            if dx < -swipe_distance:
                self.page_index += 1
            elif dx > swipe_distance:
                self.page_index -= 1

    def on_page_index(self, instance, value):
        if value == 0:
            if self.startbutton not in self.children:
                self.add_widget(self.startbutton)
        elif value == 1:
            self.remove_widget(self.skipbutton)
            self.remove_widget(self.startbutton)
            self.disabled_swipe = False
        elif value == 6:
            self.parent.input_disabled = False
            self.parent.resultbox.change_screen("right")
            self.parent.input_disabled = True
        elif value == 7:
            self.parent.input_disabled = False
            self.parent.resultbox.change_screen("left")
            self.parent.input_disabled = True
        elif value == 10:
            self.add_widget(self.skipbutton)
            self.disabled_swipe = True
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
        self.change_circle_ref(i)

    def change_rect_dims(self, i, dims):
        s = self.parent.size
        self.canvas.children[i].pos = [s[j] * dims["pos"][j] for j in range(2)]
        self.canvas.children[i].size = [s[j] * dims["size"][j] for j in range(2)]

    def change_circle_ref(self, i):
        if i not in [0, 10]:
            for j in range(1, 10):
                self.circle_grid.children[j].text = "○"
            self.circle_grid.children[i].text = "●"
        else:
            for j in range(1, 10):
                self.circle_grid.children[j].text = ""


class Readme(FloatLayout):
    readmelabel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readmelabel.text = dp.readme


class WarningIcon(FloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pops = WarningPopup()

    def poppingup(self):
        self.add_widget(self.pops)

    def poppingdown(self):
        self.remove_widget(self.pops)


class WarningPopup(FloatLayout):
    pass


class PageNavigator(GridLayout):
    match = ObjectProperty(None)
    proba_button = ObjectProperty(None)
    accessory_button = ObjectProperty(None)

    def preseason(self):
        if dp.matchday == 6:
            pass
            # self.match.pos_hint = {"center_x": 0.45, "y": 0.85}
            # self.add_widget(WarningIcon())

    def change_labels(self, match_id):
        home, away = dp.get_current_matches(match_id, short=True)
        self.match.text = f"{home} - {away}"

    def change_background_color(self, direction):
        if direction == "right":
            self.proba_button.background_color = cmap["navigationbarpressed"]
            self.accessory_button.background_color = cmap["navigationbar"]
        elif direction == "left":
            self.proba_button.background_color = cmap["navigationbar"]
            self.accessory_button.background_color = cmap["navigationbarpressed"]
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
        swipe_distance_x = 0.15
        swipe_distance_y = 0.1
        x0, x1, y0, y1 = touch.osx, touch.psx, touch.osy, touch.psy
        dx = x1 - x0
        dy = y1 - y0
        invalid_touch = self.check_swipe_touch_border(x0, y0)
        if invalid_touch:
            pass
        else:
            if dy > swipe_distance_y:
                self.change_match("up")
            elif dy < -swipe_distance_y:
                self.change_match("down")
            elif dx > swipe_distance_x:
                self.change_screen("right")
            elif dx < -swipe_distance_x:
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
        self.parent.match_id = dp.update_id(move[direction])

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
        self.change_team_labels(match_id)
        self.add_values(self.gfgs.scored, dp.dfs["Gf"], match_id)
        self.add_values(self.gfgs.received, dp.dfs["Gs"], match_id)
        self.add_values(self.oxt.grid, dp.dfs["1X2"], match_id)
        self.add_values(self.ggng.grid, dp.dfs["GG-NG"], match_id)
        self.add_values(self.ou.grid, dp.dfs["O-U"], match_id)

    def change_team_labels(self, match_id):
        home, away = dp.get_current_matches(match_id, short=False)
        self.gfgs.home.source = f"data/teamlogos/{home}.png"
        self.gfgs.away.source = f"data/teamlogos/{away}.png"


class AccessoriesScreen(Screen):
    prevencounter = ObjectProperty(None)
    momentum = ObjectProperty(None)
    ranking = ObjectProperty(None)

    def change_matches_data(self, match_id):
        self.change_prevenc(match_id)
        self.change_momentum(match_id)
        self.change_ranking(match_id)

    def change_prevenc(self, match_id):
        for match, year in zip(
            self.prevencounter.matches.children, self.prevencounter.years.children
        ):
            match.text = ""
            year.text = ""
        N_RESULT = 3
        df = dp.get_direct_encounters(match_id, N_RESULT)
        for i in range(len(df)):
            res_label = self.prevencounter.matches.children[i]
            res_label.text = df.loc[i, "label"]
            year_label = self.prevencounter.years.children[i]
            year_label.text = str(df.loc[i, "anno"])

    def change_momentum(self, match_id):
        self.change_team_labels(match_id)
        df = dp.get_momentum_labels(match_id)
        for block in self.momentum.grid.children:
            block.text = ""
            block.background_color = cmap["colorbar"][50]
        for child, row in zip(self.momentum.grid.children, df.itertuples()):
            child.text = row.label
            child.background_color = cmap["results"][row.color]

    def change_team_labels(self, match_id):
        home, away = dp.get_current_matches(match_id, short=False)
        self.momentum.home.source = f"data/teamlogos/{home}.png"
        self.momentum.away.source = f"data/teamlogos/{away}.png"

    def change_ranking(self, match_id):
        df = dp.get_ranking(match_id)
        for button, value in zip(self.ranking.grid.data, df.itertuples(index=False)):
            if value.highlight:
                color = cmap["highlighted"]
            else:
                color = cmap["data"]
            button["background_color"] = color
            button.update({"text": value.label})
        self.ranking.grid.refresh_from_data()
