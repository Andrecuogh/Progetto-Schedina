from set_up import league_data
from display.window_config import colors, cleaning
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

lday = league_data.latest_matchday()

warning_text = " NON DISPONIBILE\n\
Le previsioni dei risultati vengono fatte sulla base \
delle 5 partite precedenti. \
Quindi, per insufficienza di dati, per le prime 5 giornate \
non ci sono le previsioni delle partite. "

def list_matchdays(self):

    self.page = 'Matchday'
    cleaning(self)

    daylabel = Button(text='Selezionare una giornata',
                      font_size = 40, 
                      size_hint=(0.7, 0.08),
                      pos_hint={'center_x': 0.5, 'center_y': 0.8},
                      background_normal = '',
                      background_color = colors['label'])
    
    self.window.add_widget(daylabel)


    self.daygrid = GridLayout(size_hint=(0.9, 0.65), spacing = [10, 10],
                         pos_hint={'center_x': 0.5, 'center_y': 0.375}, cols = 5)
    
    for i in range(lday+1):
        daybutton = Button(text=str(i+1),
                           font_size = 40, color = colors['text'],
                           background_normal = '',
                           background_color = colors['label'])
        self.daygrid.add_widget(daybutton)      
    self.window.add_widget(self.daygrid)

            
    
