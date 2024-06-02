# from transversal.utilbar import UtilBar
import pandas as pd
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from job.display.app_utils.colors import colors1 as cmap
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from job.display.app_utils.custom_obj import UtilsButton, CustomRectangle


class Page:
    def __init__(self):
        self.page = None

    def config(self, app: App):
        """Config the pages"""
        app.window = FloatLayout()
        LabelBase.register(
            DEFAULT_FONT,
            "job/display/app_utils/fonts/calibri/calibri.ttf",
            fn_bold="job/display/app_utils/fonts/calibri/calibrib.ttf",
        )
        Window.clearcolor = self.get_colors()["background"]

    def cleaning(self, screen, canvas=True):
        if canvas:
            screen.window.canvas.clear()
        screen.window.clear_widgets()

    def draw(self, screen):
        self.add_help_bar(screen)

    def get_colors(self):
        return cmap

    def add_help_bar(self, screen):
        CustomRectangle(pos_hint=(0.01, 0.905), size_hint=(0.98, 0.09)).draw(screen)
        screen.utilbar = self.add_bar_container()
        screen.tutorial = self.add_utils_button("Tutorial")
        screen.info = self.add_utils_button("About")
        screen.quit = self.add_utils_button("Quit")
        screen.utilbar.add_widget(screen.tutorial)
        screen.utilbar.add_widget(screen.info)
        screen.utilbar.add_widget(screen.quit)
        screen.window.add_widget(screen.utilbar)
        # WarningBox().popup(screen)

    def add_bar_container(self):
        layout = GridLayout(
            pos_hint={"x": 0.02, "y": 0.92},
            size_hint=(0.96, 0.06),
            cols=3,
            spacing=[20, 0],
        )
        return layout

    def add_utils_button(self, text):
        button = UtilsButton(text).draw()
        return button
