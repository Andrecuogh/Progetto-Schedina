from job.display.app_utils.custom_obj import StandardButton, CustomRectangle
from job.display.app_utils.page import Page


# from set_up_kivy.retrieval import retrieve
# from transversal.warning import WarningBox
# from homepage.scoredashboard import ScoreDashboard


class HomePage(Page):
    def __init__(self):
        self.page = "Home"
        self.first = False
        self.ask_upd = False

    def draw(self, screen):
        super().draw(screen)
        self.add_predict_button(screen)

    def add_predict_button(self, screen):
        screen.button = StandardButton(
            text="Predici",
            font_size=60,
            size_hint=(0.5, 0.175),
            pos_hint={"center_x": 0.5, "center_y": 0.275},
        ).draw()
        screen.window.add_widget(screen.button)

    def loading(self, screen, d):

        self.cleaning(screen)
        screen.button.text = "Raccogliendo\ni dati"
        screen.button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        screen.window.add_widget(screen.button)
