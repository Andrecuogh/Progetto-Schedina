from display.window_config import Page, CustomButton
from gitconnect.gitset import repopath
import requests

class InfoPage(Page):

    def __init__(self):
        path = f'https://raw.githubusercontent.com/{repopath}/main/README.md'
        response = requests.get(path)
        self.text= response.text
        
    def informating(self, screen):
        self.cleaning(screen)

        screen.infolayout = CustomButton(
            category='button',
            text = self.text,
            pos_hint={'x': 0.2, 'y': 0.2},
            size_hint=(0.6, 0.6)
        )

        screen.infobackbutton = CustomButton(
            category='bbcolor',
            text = 'Ok',
            pos_hint = {'x': 0.475, 'y': 0.675},
            size_hint = (0.05, 0.05)
        )

        screen.window.add_widget(screen.infolayout)
        screen.window.add_widget(screen.infobackbutton)