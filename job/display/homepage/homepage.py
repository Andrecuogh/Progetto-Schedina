from job.display.app_utils.custom_obj import CustomButton
from app_utils.page import Page
from set_up.gitconnect.retrieval import retrieve
from transversal.warning import WarningBox
from homepage.scoredashboard import ScoreDashboard


class Homepage(Page):

    def __init__(self):
        self.page = 'Home'
        self.first = False
        self.ask_upd = False
    
    def initializing(self, screen):
        screen.button = CustomButton(
            category = 'button',
            text='Predici',
            font_size = 60, 
            size_hint=(0.5, 0.175),
            pos_hint={'center_x': .5, 'center_y': .275}
            )
        screen.window.add_widget(screen.button)

        screen.archivio = CustomButton(
            category = 'button',
            text='Archivio',
            font_size = 50,
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': .5, 'center_y': .45}
            )
        screen.window.add_widget(screen.archivio)

        WarningBox().popup(screen)
        ScoreDashboard().show(screen)

    def loading(self, screen, d):
        screen.datasets = retrieve(d)
        screen.df1 = screen.datasets[0]
        screen.df2 = screen.datasets[1]
        screen.df3 = screen.datasets[2]
        screen.df4 = screen.datasets[3]
        screen.df5 = screen.datasets[4]

        self.cleaning(screen)
        screen.button.text = 'Raccogliendo\ni dati'
        screen.button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        screen.window.add_widget(screen.button)