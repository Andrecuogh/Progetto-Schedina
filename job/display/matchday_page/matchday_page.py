from app_utils.custom_obj import CustomRectangle, CustomButton
from app_utils.page import Page
from kivy.uix.gridlayout import GridLayout


class MatchdayPage(Page):
    def __init__(self, lday):
        self.page = "Matchday"
        self.lday = lday
        self.warning_text = " NON DISPONIBILE\n\
            Le previsioni dei risultati vengono fatte sulla base \
            delle 5 partite precedenti. \
            Quindi, per insufficienza di dati, per le prime 5 giornate \
            non ci sono le previsioni delle partite. "

    def list_matchdays(self, screen):
        self.cleaning(screen)

        CustomRectangle(pos_hint=(0.02, 0.02), size_hint=(0.96, 0.78)).draw(screen)

        daylabel = CustomButton(
            category="label",
            text="Selezionare una giornata",
            font_size=40,
            size_hint=(0.7, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )
        screen.window.add_widget(daylabel)

        screen.daygrid = GridLayout(
            size_hint=(0.9, 0.65),
            spacing=[10, 10],
            pos_hint={"center_x": 0.5, "center_y": 0.375},
            cols=5,
        )

        for i in range(self.lday + 1):
            daybutton = CustomButton(category="button", text=str(i + 1), font_size=40)
            screen.daygrid.add_widget(daybutton)
        screen.window.add_widget(screen.daygrid)
