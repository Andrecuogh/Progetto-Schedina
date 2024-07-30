import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from utils.connector import AppUpdater
from utils.colors import colors1 as cmap
from layouts.layouts import SchedinaLayout


class SchedinaApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = cmap
        # self.kv_directory = "layouts"
        self._init_screen()
        self.register_fonts()

    def _init_screen(self):
        self.sf = 1.0  # prod: 1.0; test 0.314
        self.screen_to_body = 0.852
        # Window.size = (
        #     1080 * self.screen_to_body * self.sf,
        #     2400 * self.screen_to_body * self.sf,
        # )  # only for testing in pc

    def build(self):
        Builder.load_file("layouts/Schedina.kv")
        self.root = SchedinaLayout()
        self.update_if_any()
        self.root.current_screen.match_id = 0
        return self.root

    def register_fonts(self):
        font_path = "utils/fonts"
        LabelBase.register(
            DEFAULT_FONT,
            f"{font_path}/calibri/calibri.ttf",
            fn_bold=f"{font_path}/calibri/calibrib.ttf",
        )
        LabelBase.register("arial", f"{font_path}/arial/arial.ttf")

    def update_if_any(self):
        self.updater = AppUpdater()
        need_to_update = self.updater.search_update()
        self.root.set_initial_screen(need_to_update)


if __name__ == "__main__":
    SchedinaApp().run()
