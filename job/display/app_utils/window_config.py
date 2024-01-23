import pandas as pd

from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT

from app_utils.colors import colors1 as cmap


class AppConfigurer():

    def __init__(self):
        pass

    def custom_init(self):
        LabelBase.register(
            DEFAULT_FONT, 
            "fonts/calibri/calibri.ttf", 
            fn_bold="fonts/calibri/calibrib.ttf"
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