from app_utils.window_config import AppConfigurer
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, RoundedRectangle
from kivy.uix.button import Button

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