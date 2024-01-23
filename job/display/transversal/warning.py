from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from app_utils.custom_obj import CustomButton


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