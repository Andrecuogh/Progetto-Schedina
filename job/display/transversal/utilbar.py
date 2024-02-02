from app_utils.window_config import AppConfigurer
from app_utils.custom_obj import CustomRectangle, CustomButton
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from set_up.config_var import REPOPATH
import requests


class UtilBar:
    def __init__(self):
        pass

    def draw(self, screen):
        colors = AppConfigurer().paint()

        CustomRectangle(pos_hint=(0.01, 0.905), size_hint=(0.98, 0.09)).draw(screen)

        screen.utilbar = GridLayout(
            pos_hint={"x": 0.02, "y": 0.92},
            size_hint=(0.96, 0.06),
            cols=3,
            spacing=[20, 0],
        )
        screen.window.add_widget(screen.utilbar)

        screen.tutorial = ToggleButton(
            text="Tutorial",
            font_size=50,
            bold=True,
            background_normal="",
            background_color=colors["utilsbutton"],
        )
        screen.utilbar.add_widget(screen.tutorial)

        screen.info = CustomButton(
            category="utilsbutton", text="About", font_size=50, bold=True
        )
        screen.utilbar.add_widget(screen.info)

        screen.quitting = CustomButton(
            category="utilsbutton", text="Quit", font_size=50, bold=True
        )
        screen.utilbar.add_widget(screen.quitting)


class Infos:
    def __init__(self):
        path = f"https://raw.githubusercontent.com/{REPOPATH}/main/README.md"
        response = requests.get(path)
        self.text = response.text

    def informating(self, screen):
        screen.infolayout = CustomButton(
            category="button",
            text=self.text,
            font_size=18,
            pos_hint={"x": 0.05, "y": 0.05},
            size_hint=(0.9, 0.9),
            text_size=(screen.window.size[0] * 0.85, screen.window.size[0] * 0.85),
            padding=[0, 100],
            valign="top",
            markup=True,
        )

        screen.infobackbutton = CustomButton(
            category="bbcolor",
            text="Ok",
            pos_hint={"x": 0.475, "y": 0.1},
            size_hint=(0.05, 0.05),
        )

        screen.window.add_widget(screen.infolayout)
        screen.window.add_widget(screen.infobackbutton)
