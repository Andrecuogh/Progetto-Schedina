import pandas as pd

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from display.window_config import CustomButton, CustomRectangle, Page
from gitconnect.retrieval import retrieve


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


class ScoreDashboard():

    def __init__(self):
        pass

    def show(self, screen):
        repo = "https://raw.githubusercontent.com/Andrecuogh/Progetto-Schedina/"
        path = "main/data/accuracy_dashboard/acc_dict.csv"
        acc_dict = pd.read_csv(repo+path, index_col=0)

        CustomRectangle(
            pos_hint=(0.02, 0.6),
            size_hint=(0.96, 0.245)
            ).draw(screen)

        for i, trgt in enumerate(acc_dict['Score']):
            cy = 0.79 - i*0.04
            
            score_container = CustomButton(
                category = 'sc_dash_cont',
                text='',
                size_hint=(0.75, 0.038),
                pos_hint={'x': .2, 'center_y': cy}
                )
            screen.window.add_widget(score_container)

            
            score_bar = CustomButton(
                category = 'sc_dash_bar',
                text=str(trgt*100)[0:5]+' %',
                font_size = 40,
                size_hint=(0.75*trgt, 0.025),
                pos_hint={'x': .2, 'center_y': cy},
                halign = 'center'
                )
            screen.window.add_widget(score_bar)

            score_label = CustomButton(
                category = 'label',
                text=acc_dict.index[i],
                font_size = 45,
                size_hint=(0.15, 0.038),
                pos_hint={'x': .05, 'center_y': cy},
                halign = 'center'
                )       
            screen.window.add_widget(score_label)

        score_title = CustomButton(
            category = 'label',
            text = 'Precisione del modello',
            font_size = 40,
            halign = 'center',
            size_hint=(0.75, 0.05),
            pos_hint={'center_x': .5, 'center_y': 0.845}
            )
        screen.window.add_widget(score_title)


class WarningBox():

    def __init__(self):
        pass

    def popup(self, screen):
        screen.warn_box = FloatLayout(
            size_hint=(0.82, 0.42),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
        
        warnbord1 = Button(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal = '',
            background_color = 'red'
            )
        screen.warn_box.add_widget(warnbord1)
        
        warnbord2 = CustomButton(
            category = 'label',
            size_hint=(0.99, 0.99),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
        screen.warn_box.add_widget(warnbord2)
        
        screen.warnlabel = Label(
            text='',
            size_hint=(0.99, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
            )
        screen.warn_box.add_widget(screen.warnlabel)
    
        screen.warnback = CustomButton(
            category = 'bbcolor',
            text='Ok', 
            size_hint=(0.4, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            font_size = 40
            )
        screen.warn_box.add_widget(screen.warnback)

        screen.bupdate = CustomButton(
            category = 'bbcolor',
            text='Aggiorna', 
            size_hint=(0.2, 0.2),
            pos_hint={'center_x': 0.25, 'center_y': 0.2},
            font_size = 40
            )

        screen.bskip = CustomButton(
            category = 'bbcolor',
            text='Non ora', 
            size_hint=(0.2, 0.2),
            pos_hint={'center_x': 0.75, 'center_y': 0.2},
            font_size = 40
            )