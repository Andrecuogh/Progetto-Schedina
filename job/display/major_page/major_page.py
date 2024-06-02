import numpy as np

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from job.display.app_utils.update import AppConfigurer
from app_utils.custom_obj import CustomButton, CustomEllipse, CustomRectangle
from app_utils.page import Page


class MajorPage(Page):
    def __init__(self):
        self.page = "Major"

    def pagelayout(self, screen):
        screen.gfgshead = GridLayout(
            size_hint=(0.8, 0.05),
            pos_hint={"center_x": 0.55, "center_y": 0.85},
            cols=5,
            spacing=[2, 2],
        )

        screen.gfgsdesc = CustomButton(
            category="label",
            text="GOL",
            font_size=40,
            size_hint=(0.1, 0.05),
            pos_hint={"center_x": 0.08, "center_y": 0.85},
        )

        screen.gflab = GridLayout(
            size_hint=(0.8, 0.095),
            pos_hint={"center_x": 0.55, "center_y": 0.77},
            cols=5,
            spacing=[2, 2],
        )

        screen.gslab = GridLayout(
            size_hint=(0.8, 0.095),
            pos_hint={"center_x": 0.55, "center_y": 0.67},
            cols=5,
            spacing=[2, 2],
        )

        screen.gglab = GridLayout(
            size_hint=(0.4, 0.1),
            pos_hint={"center_x": 0.27, "center_y": 0.46},
            cols=2,
            spacing=[2, 2],
        )

        screen.gghead = GridLayout(
            size_hint=(0.4, 0.05),
            pos_hint={"center_x": 0.27, "center_y": 0.54},
            cols=2,
            spacing=[2, 2],
        )

        screen.uolab = GridLayout(
            size_hint=(0.4, 0.1),
            pos_hint={"center_x": 0.73, "center_y": 0.46},
            cols=2,
            spacing=[2, 2],
        )

        screen.uohead = GridLayout(
            size_hint=(0.4, 0.05),
            pos_hint={"center_x": 0.73, "center_y": 0.54},
            cols=2,
            spacing=[2, 2],
        )

        screen.ox2head = GridLayout(
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.33},
            cols=3,
            spacing=[2, 2],
        )

        screen.ox2lab = GridLayout(
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.25},
            cols=3,
            spacing=[2, 2],
        )

        screen.teamh = CustomButton(
            category="label",
            size_hint=(0.1, 0.09),
            pos_hint={"center_x": 0.08, "center_y": 0.77},
            font_size=40,
        )

        screen.teama = CustomButton(
            category="label",
            size_hint=(0.1, 0.09),
            pos_hint={"center_x": 0.08, "center_y": 0.67},
            font_size=40,
        )

    def navigation(self, screen):
        screen.prec = Label(
            size_hint=(0.26, 0.1),
            pos_hint={"x": 0.09, "y": 0.05},
            text="Precedente",
            font_size=45,
        )

        screen.suc = Label(
            size_hint=(0.26, 0.1),
            pos_hint={"x": 0.65, "y": 0.05},
            text="Successivo",
            font_size=45,
        )

        screen.home = Label(
            size_hint=(0.1, 0.08),
            pos_hint={"x": 0.45, "y": 0.06},
            text="Home",
            font_size=35,
        )

        CustomEllipse(pos_hint=(0.09, 0.05), size_hint=(0.26, 0.1)).draw(
            screen, color="button"
        )

        CustomEllipse(pos_hint=(0.65, 0.05), size_hint=(0.26, 0.1)).draw(
            screen, color="button"
        )

        CustomRectangle(pos_hint=(0.45, 0.06), size_hint=(0.1, 0.08)).draw(
            screen, color="button"
        )

    def initializecanvas(self, screen):
        screen.partita = 0

        self.cleaning(screen)
        self.pagelayout(screen)
        self.navigation(screen)

        objects = [
            screen.gfgshead,
            screen.gfgsdesc,
            screen.gflab,
            screen.gslab,
            screen.gglab,
            screen.gghead,
            screen.uolab,
            screen.uohead,
            screen.ox2lab,
            screen.ox2head,
            screen.teamh,
            screen.teama,
            screen.prec,
            screen.suc,
            screen.home,
        ]

        for obj in objects:
            screen.window.add_widget(obj)

        for i in range(5):
            screen.gfgshead.add_widget(
                CustomButton(
                    category="label", text=str(screen.df1.columns[i]), font_size=45
                )
            )
            screen.gflab.add_widget(CustomButton(category="button", font_size=40))
            screen.gslab.add_widget(CustomButton(category="button", font_size=40))

        for i in range(3):
            screen.ox2head.add_widget(
                CustomButton(category="label", text=["1", "X", "2"][i], font_size=45)
            )
            screen.ox2lab.add_widget(CustomButton(category="button", font_size=40))

        for i in range(2):
            screen.gghead.add_widget(
                CustomButton(category="label", text=screen.df4.columns[i], font_size=45)
            )
            screen.gglab.add_widget(CustomButton(category="button", font_size=40))
            screen.uohead.add_widget(
                CustomButton(
                    category="label", text=screen.df5.columns[i] + " 2.5", font_size=45
                )
            )
            screen.uolab.add_widget(CustomButton(category="button", font_size=40))

    def paintcanvas(self, screen):
        team_home, team_away = screen.df1.index[screen.partita].split("-")
        screen.teamh.text = team_home[0:3].upper()
        screen.teama.text = team_away[0:3].upper()

        colorbar = AppConfigurer().paint()["colorbar"]

        for i, but in enumerate(screen.gflab.children):
            but.text = self.proba_string(screen.df1, screen.partita, 4 - i)
            but.background_color = colorbar[
                int(screen.df1.iloc[screen.partita, 4 - i] * 100)
            ]

        for i, but in enumerate(screen.gslab.children):
            but.text = self.proba_string(screen.df2, screen.partita, 4 - i)
            but.background_color = colorbar[
                int(screen.df2.iloc[screen.partita, 4 - i] * 100)
            ]

        for i, but in enumerate(screen.ox2lab.children):
            but.text = self.proba_string(screen.df3, screen.partita, 2 - i)
            but.background_color = colorbar[
                int(screen.df3.iloc[screen.partita, 2 - i] * 100)
            ]

        for i, but in enumerate(screen.gglab.children):
            but.text = self.proba_string(screen.df4, screen.partita, 1 - i)
            but.background_color = colorbar[
                int(screen.df4.iloc[screen.partita, 1 - i] * 100)
            ]

        for i, but in enumerate(screen.uolab.children):
            but.text = self.proba_string(screen.df5, screen.partita, 1 - i)
            but.background_color = colorbar[
                int(screen.df5.iloc[screen.partita, 1 - i] * 100)
            ]

    def proba_string(self, df, match, index):
        proba_label = f"{np.round(df.iloc[match, index]*100, 1)} %"
        return proba_label
