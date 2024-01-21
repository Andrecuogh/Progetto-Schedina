import pandas as pd

from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase, DEFAULT_FONT
from display.colors import colors1 as cmap


class AppConfigurer():

    def __init__(self):
        pass

    def custom_init(self):
        LabelBase.register(
            DEFAULT_FONT, 
            "display/fonts/calibri/calibri.ttf", 
            fn_bold="display/fonts/calibri/calibrib.ttf"
            )
        Window.clearcolor = self.paint()['background']

    def paint(self):
        return cmap

    def check_update(self, version):
        self.curr_version = version
        self.version_path = "https://raw.githubusercontent.com/Andrecuogh/Progetto-Schedina/main/version/versions.csv"
        self.upd_link = "https://raw.githubusercontent.com/Andrecuogh/Progetto-Schedina/main/version/latest.apk"
        self.line = 'Nuovo aggiornamento disponibile.'

        df = pd.read_csv(self.version_path)
        self.latest_version = df[df['Latest']]['Version'].values[0]
        self.no_updated = self.latest_version > self.curr_version

        return self.no_updated


class CustomFigure():

    def __init__(self, pos_hint, size_hint):
        self.pos_hint = pos_hint
        self.size_hint = size_hint
        self.drawer = None

    def draw(self, screen, color='blob'):
        ws = Window.size
        r,g,b,a = AppConfigurer().paint()[color]

        with screen.window.canvas:
            Color(r, g, b, a)
            self.drawer(
                pos=(ws[0]*self.pos_hint[0], ws[1]*self.pos_hint[1]),
                size=(ws[0]*self.size_hint[0], ws[1]*self.size_hint[1])
                )


class CustomRectangle(CustomFigure):

    def __init__(self, pos_hint, size_hint):
        super().__init__(pos_hint, size_hint)
        self.drawer = RoundedRectangle


class CustomEllipse(CustomFigure):

    def __init__(self, pos_hint, size_hint):
        super().__init__(pos_hint, size_hint)
        self.drawer = Ellipse



class CustomButton(Button):

    def __init__(self,  category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        colors = AppConfigurer().paint()
        self.background_normal = ''
        self.background_color = colors[category]
        

class Page():

    def __init__(self):
        self.page = None

    def cleaning(self, screen, canvas=True):
        if canvas:
            screen.window.canvas.clear()
        screen.window.clear_widgets()

        UtilBar().draw(screen)


class UtilBar():

    def __init__(self):
        pass

    def draw(self, screen):
        colors = AppConfigurer().paint()

        CustomRectangle(
            pos_hint=(0.01, 0.905),
            size_hint=(0.98, 0.09)
            ).draw(screen)

        screen.utilbar = GridLayout(
            pos_hint={'x': 0.02, 'y': 0.92},
            size_hint=(0.96, 0.06),
            cols = 3, spacing = [20, 0]
            )
        screen.window.add_widget(screen.utilbar)

        screen.tutorial = ToggleButton(
            text = 'Tutorial', 
            font_size=50, 
            bold = True,
            background_normal = '', 
            background_color = colors['utilsbutton']
            )
        screen.utilbar.add_widget(screen.tutorial)
        
        screen.info = CustomButton(
            category = 'utilsbutton',
            text = 'About', 
            font_size=50, 
            bold = True
            )
        screen.utilbar.add_widget(screen.info)

        screen.quitting = CustomButton(
            category = 'utilsbutton',
            text = 'Quit', 
            font_size=50, 
            bold = True
            )
        screen.utilbar.add_widget(screen.quitting)