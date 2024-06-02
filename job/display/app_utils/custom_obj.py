from job.display import COLORS
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, RoundedRectangle
from kivy.uix.button import Button


class CustomWidget:
    """Master class for customized widgets.
    The class variable "drawer" represents the object to be plotted with
    the .draw() method.
    """

    drawer = None

    def __init__(self):
        self.colors = COLORS

    def draw(self):
        pass


class CustomFigure(CustomWidget):
    """The CustomFigure represents static objects, i.e., Rectangles, Ellipses"""

    drawer = None

    def __init__(self, pos_hint, size_hint):
        super().__init__()
        self.pos_hint = pos_hint
        self.size_hint = size_hint

    def draw(self, screen):
        ws = Window.size
        r, g, b, a = self.colors["blob"]

        with screen.window.canvas:
            Color(r, g, b, a)
            self.drawer(
                pos=(ws[0] * self.pos_hint[0], ws[1] * self.pos_hint[1]),
                size=(ws[0] * self.size_hint[0], ws[1] * self.size_hint[1]),
            )


class CustomRectangle(CustomFigure):
    drawer = RoundedRectangle


class CustomEllipse(CustomFigure):
    drawer = Ellipse


class CustomButton(CustomWidget):
    """The CustomButton class represents dynamic objects, i.e.,
    buttons that trigger functions and callbacks
    """

    drawer = Button

    def __init__(self, text):
        super().__init__()
        self.drawer.background_normal = ""
        self.drawer.text = text

    def draw(self):
        return self.drawer()


class UtilsButton(CustomButton):
    """UtilsButton represents the buttons in the utility bar
    at the top of the app screen.
    """

    def __init__(self, text):
        super().__init__(text)
        self.drawer.background_color = self.colors["utilsbutton"]
        self.drawer.font_size = 50
        self.drawer.bold = True


class StandardButton(CustomButton):
    """StandardButton represents the generic type of button in the app screen"""

    def __init__(self, text, pos_hint, size_hint, font_size):
        super().__init__(text)
        self.drawer.background_color = self.colors["button"]
        self.drawer.pos_hint = pos_hint
        self.drawer.size_hint = size_hint
        self.drawer.font_size = font_size
