from job.display.app_utils.update import AppConfigurer
from app_utils.custom_obj import CustomRectangle, CustomButton


from set_up_kivy.config_var import REPOPATH
import requests


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
