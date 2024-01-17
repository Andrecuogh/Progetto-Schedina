import numpy as np

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, RoundedRectangle

from display.window_config import colors, colorbar, cleaning


def pagelayout(self):

    self.gfgshead = GridLayout(size_hint=(0.8, 0.05), pos_hint={'center_x': .55, 'center_y': .85},
                               cols=5, spacing = [2, 2])
    
    self.gfgsdesc = Button(text='GOL', font_size = 40, color = colors['text'], size_hint=(0.1, 0.05),
                           pos_hint={'center_x': .08, 'center_y': .85},
                           background_color = colors['label'],background_normal = '',)
    
    self.gflab = GridLayout(size_hint=(0.8, 0.095), pos_hint={'center_x': .55, 'center_y': .77},
                            cols=5, spacing = [2, 2])
    
    self.gslab = GridLayout(size_hint=(0.8, 0.095), pos_hint={'center_x': .55, 'center_y': .67},
                            cols=5, spacing = [2, 2])
    
    
    self.gglab = GridLayout(size_hint=(0.4, 0.1), pos_hint={'center_x': .27, 'center_y': .46},
                            cols=2, spacing = [2, 2])
    
    self.gghead = GridLayout(size_hint=(0.4, 0.05), pos_hint={'center_x': .27, 'center_y': .54},
                             cols=2, spacing = [2, 2])
    
    
    self.uolab = GridLayout(size_hint=(0.4, 0.1), pos_hint={'center_x': .73, 'center_y': .46},
                            cols=2, spacing = [2, 2])
    
    self.uohead = GridLayout(size_hint=(0.4, 0.05), pos_hint={'center_x': .73, 'center_y': .54},
                             cols=2, spacing = [2, 2])
    
    
    self.ox2head = GridLayout(size_hint=(0.5, 0.05), pos_hint={'center_x': .5, 'center_y': .33},
                              cols=3, spacing = [2, 2])
    
    self.ox2lab = GridLayout(size_hint=(0.5, 0.1), pos_hint={'center_x': .5, 'center_y': .25},
                             cols=3, spacing = [2, 2])
    
    
    self.teamh = Button(size_hint=(0.1, 0.09), pos_hint={'center_x': .08, 'center_y': .77},
                        font_size = 40, color = colors['text'],
                        background_normal = '', background_color = colors['label'])
    
    self.teama = Button(size_hint=(0.1, 0.09), pos_hint={'center_x': .08, 'center_y': .67},
                        font_size = 40, color = colors['text'],
                        background_normal = '',background_color = colors['label'])

def navigation(self):
    
    wind_size = self.window.size

    self.prec = Label(size_hint=(0.26, 0.1), pos_hint={'x': 0.09, 'y': 0.05},
                       text='Precedente', font_size = 45, color = colors['text'])
    self.suc = Label(size_hint=(0.26, 0.1), pos_hint={'x': 0.65, 'y': 0.05},
                      text='Successivo', font_size = 45, color = colors['text'])
    self.home = Label(size_hint=(0.1, 0.08), pos_hint={'x': 0.45, 'y': 0.06},
                       text='Home', font_size = 35, color = colors['text'])


    prec_p = (self.prec.pos_hint['x']*wind_size[0]-5,
              self.prec.pos_hint['y']*wind_size[1]-5)

    suc_p = (self.suc.pos_hint['x']*wind_size[0]-5,
             self.suc.pos_hint['y']*wind_size[1]-5)

    home_p = (self.home.pos_hint['x']*wind_size[0],
              self.home.pos_hint['y']*wind_size[1])

    prec_s = (self.prec.size_hint[0]*wind_size[0]+10,
              self.prec.size_hint[1]*wind_size[1]+10)

    suc_s = (self.suc.size_hint[0]*wind_size[0]+10,
             self.suc.size_hint[1]*wind_size[1]+10)

    home_s = (self.home.size_hint[0]*wind_size[0],
              self.home.size_hint[1]*wind_size[1])
    
    r,g,b,a = colors['label']
    
    with self.window.canvas:
        Color(r, g, b, a)
        Ellipse(pos=prec_p, size=prec_s)
        Ellipse(pos=suc_p, size=suc_s)
        RoundedRectangle(pos=home_p, size=home_s)

def initializecanvas(self):

    self.page = 'Major'
    self.partita = 0
    cleaning(self)

    pagelayout(self)
    navigation(self)


    objects = [self.gfgshead, self.gfgsdesc, self.gflab, self.gslab,
               self.gglab, self.gghead,
               self.uolab,self.uohead,
               self.ox2lab, self.ox2head,
               self.teamh, self.teama,
               self.prec, self.suc, self.home]

    for obj in objects:
        self.window.add_widget(obj)
    
    for i in range(5):
        self.gfgshead.add_widget(new_button(str(self.df1.columns[i]), label=True))
        self.gflab.add_widget(new_button(''))
        self.gslab.add_widget(new_button(''))

    for i in range(3):
        self.ox2head.add_widget(new_button(['1', 'X', '2'][i], label=True))
        self.ox2lab.add_widget(new_button(''))

    for i in range(2):
        self.gghead.add_widget(new_button(self.df4.columns[i], label=True))
        self.gglab.add_widget(new_button(''))

        self.uohead.add_widget(new_button(self.df5.columns[i]+' 2.5', label=True))
        self.uolab.add_widget(new_button(''))

def paintcanvas(self):

    self.teamh.text = self.df1.index[self.partita].split('-')[0][0:3].upper()
    self.teama.text = self.df1.index[self.partita].split('-')[1][0:3].upper()

    for i, but in enumerate(self.gflab.children):
        but.text = proba_string(self.df1, self.partita, 4-i)
        but.background_color = colorbar[int(self.df1.iloc[self.partita, 4-i]*100)]

    for i, but in enumerate(self.gslab.children):
        but.text = proba_string(self.df2, self.partita, 4-i)
        but.background_color = colorbar[int(self.df2.iloc[self.partita, 4-i]*100)]

    for i, but in enumerate(self.ox2lab.children):
        but.text = proba_string(self.df3, self.partita, 2-i)
        but.background_color = colorbar[int(self.df3.iloc[self.partita, 2-i]*100)]

    for i, but in enumerate(self.gglab.children):
        but.text = proba_string(self.df4, self.partita, 1-i)
        but.background_color = colorbar[int(self.df4.iloc[self.partita, 1-i]*100)]

    for i, but in enumerate(self.uolab.children):
        but.text = proba_string(self.df5, self.partita, 1-i)
        but.background_color = colorbar[int(self.df5.iloc[self.partita, 1-i]*100)]


def new_button(text, label=False):
    button = Button(text = str(text), 
                    color = colors['text'],
                    background_normal = '')
    if label:
        button.font_size = 45
        button.background_color = colors['label']
    else:
        button.font_size = 40
        button.background_color = colors['button']
    
    return button


def proba_string(df, match, index):
    proba_label = f'{np.round(df.iloc[match, index]*100, 1)} %'
    return proba_label 
