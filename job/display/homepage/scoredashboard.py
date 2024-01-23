import pandas as pd
from app_utils.custom_obj import CustomButton, CustomRectangle

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