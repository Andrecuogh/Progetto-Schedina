import pandas as pd

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from display.window_config import colors, cleaning
from gitconnect import retrieval

curr_version = 0.3
version_path = "https://raw.githubusercontent.com/Andrecuogh/Progetto-Schedina/main/version/versions.csv"
upd_link = "https://raw.githubusercontent.com/Andrecuogh/Progetto-Schedina/main/version/latest.apk"
df = pd.read_csv(version_path)
latest_version = df[df['Latest']]['Version'].values[0]
no_updated = latest_version > curr_version

line = 'Nuovo aggiornamento disponibile.'


def scoredashboard(self):
    acc_dict = pd.read_csv("https://raw.githubusercontent.com/Andrecuogh/Progetto-Schedina/main/data/accuracy_dashboard/acc_dict.csv",
                                index_col=0)

    wind_size = self.window.size
    r,g,b,a = colors['text']
    
    with self.window.canvas:
        Color(r, g, b, a)
        RoundedRectangle(pos=[wind_size[0]*0.02, wind_size[1]*0.6],
                         size=[wind_size[0]*0.96, wind_size[1]*0.245])


    for i, trgt in enumerate(acc_dict['Score']):
        cy = 0.79 - i*0.04
        
        score_container = Button(text='',
                                 size_hint=(0.75, 0.038),
                                 pos_hint={'x': .2, 'center_y': cy},
                                 background_normal = '',
                                 background_color = colors['button'])
        
        self.window.add_widget(score_container)

        
        score_bar = Button(text=str(trgt*100)[0:5]+' %',
                           font_size = 40,
                           size_hint=(0.75*trgt, 0.025),
                           pos_hint={'x': .2, 'center_y': cy},
                           halign = 'center',
                           background_normal = '',
                           background_color = colors['background'])
        
        self.window.add_widget(score_bar)


        score_label = Button(text=acc_dict.index[i],
                             font_size = 45,
                             size_hint=(0.15, 0.038),
                             pos_hint={'x': .05, 'center_y': cy},
                             halign = 'center',
                             background_normal = '',
                             background_color = colors['label'])
        
        self.window.add_widget(score_label)


    score_title = Button(text = 'Precisione del modello',
                         font_size = 40,
                         halign = 'center',
                         size_hint=(0.75, 0.05),
                         pos_hint={'center_x': .5, 'center_y': 0.845},
                         background_normal = '',
                         background_color = colors['label'])
    
    self.window.add_widget(score_title)


def initializing(self):

    self.page = 'Home'
    self.first = False
    self.ask_upd = False
    
    Window.clearcolor = colors['background']
        
    self.button = Button(text='Predici',
                         font_size = 60, color = colors['text'],
                         size_hint=(0.5, 0.175),
                         pos_hint={'center_x': .5, 'center_y': .275},
                         background_normal = '',
                         background_color = colors['label'])
    self.window.add_widget(self.button)

    self.archivio = Button(text='Archivio',
                           font_size = 50, color = colors['text'],
                           size_hint=(0.4, 0.1),
                           pos_hint={'center_x': .5, 'center_y': .45},
                           background_normal = '',
                           background_color = colors['label'])
    self.window.add_widget(self.archivio)

    warningbox(self)
    scoredashboard(self)


def loading(self, d):
    self.datasets = retrieval.retrieve(d)
    self.df1 = self.datasets[0]
    self.df2 = self.datasets[1]
    self.df3 = self.datasets[2]
    self.df4 = self.datasets[3]
    self.df5 = self.datasets[4]

    cleaning(self)
    self.button.text = 'Raccogliendo\ni dati'
    self.button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    self.window.add_widget(self.button)

def warningbox(self):
    
    self.warn_box = FloatLayout(size_hint=(0.82, 0.42),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
    
    warnbord1 = Button(text='',
                       size_hint=(1, 1),
                       pos_hint={'center_x': 0.5, 'center_y': 0.5},
                       background_normal = '',
                       background_color = 'red')

    self.warn_box.add_widget(warnbord1)
    

    warnbord2 = Button(text='',
                       size_hint=(0.99, 0.99),
                       pos_hint={'center_x': 0.5, 'center_y': 0.5},
                       background_normal = '',
                       background_color = colors['label'])

    self.warn_box.add_widget(warnbord2)
    
    
    self.warnlabel = Label(text='',
                           color = colors['text'],
                           size_hint=(0.99, 0.8),
                           text_size = (self.window.size[0]*0.75, None),
                           pos_hint={'center_x': 0.5, 'center_y': 0.6})

    self.warn_box.add_widget(self.warnlabel)

    bbcolor = [0.682, 0.239, 0.341, 1.0]
    
    self.warnback = Button(text='Ok', size_hint=(0.4, 0.3),
                           pos_hint={'center_x': 0.5, 'center_y': 0.2},
                           font_size = 40, color = colors['text'],
                           background_normal = '', background_color = bbcolor)
    self.warn_box.add_widget(self.warnback)
    
    self.bupdate = Button(text='Aggiorna', size_hint=(0.2, 0.2),
                          pos_hint={'center_x': 0.25, 'center_y': 0.2},
                          font_size = 40, color = colors['text'],
                          background_normal = '', background_color = bbcolor)

    self.bskip = Button(text='Non ora', size_hint=(0.2, 0.2),
                        pos_hint={'center_x': 0.75, 'center_y': 0.2},
                        font_size = 40, color = colors['text'],
                        background_normal = '', background_color = bbcolor)

    
