import numpy as np

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

from gitconnect import retrieval
from display import window_config, window_obj

class MainApp(App):
    def build(self):
        self.window = FloatLayout()
        Window.clearcolor = window_config.colors['background']

        self.button = Button(text='Predici',
                      font_size = 60, color = window_config.colors['text'], bold = True,
                      size_hint=(0.4, 0.2),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      background_color = window_config.colors['label'])
        self.button.bind(on_press = self.homepage)
        self.window.add_widget(self.button)

        self.label = Button(text='',
                      halign = 'center',
                      font_size = 60, color = window_config.colors['text'], bold = True,
                      size_hint=(0.4, 0.2),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      background_color = window_config.colors['label'])

        return self.window


    def homepage(self, event):
        self.window.remove_widget(self.button)
        self.window.add_widget(self.label)
        self.label.text = 'Raccogliendo\ni dati'
        Clock.schedule_once(self.get_gitdata, 0.1)


    def get_gitdata(self, event):
        window_config.applayout(self)
        self.datasets = retrieval.retrieve()
        self.df1 = self.datasets[0]
        self.df2 = self.datasets[1]
        self.df3 = self.datasets[2]
        self.df4 = self.datasets[3]
        self.df5 = self.datasets[4]
        Clock.schedule_once(self.createcanvas, 0.1)


    def createcanvas(self, event):
        self.window.clear_widgets()

        objects = [self.gfgshead, self.gflab, self.gslab,
                         self.gglab, self.gghead, self.uolab,
                         self.uohead, self.ox2lab, self.ox2head,
                         self.teamh, self.teama, 
                         self.gfgsdesc, self.prec, self.suc]

        for obj in objects:
            self.window.add_widget(obj)

        self.prec.bind(on_press = self.backw)
        self.suc.bind(on_press = self.forw)

        Clock.schedule_once(self.initializecanvas, 0.1)

    def initializecanvas(self, event):
        for i in range(5):
            self.gfgshead.add_widget(window_obj.new_button(str(self.df1.columns[i]), label=True))
            self.gflab.add_widget(window_obj.new_button(''))
            self.gslab.add_widget(window_obj.new_button(''))

        for i in range(3):
            self.ox2head.add_widget(window_obj.new_button(['1', 'X', '2'][i], label=True))
            self.ox2lab.add_widget(window_obj.new_button(''))

        for i in range(2):
            self.gghead.add_widget(window_obj.new_button(self.df4.columns[i], label=True))
            self.gglab.add_widget(window_obj.new_button(''))

            self.uohead.add_widget(window_obj.new_button(self.df5.columns[i]+' 2.5', label=True))
            self.uolab.add_widget(window_obj.new_button(''))

        Clock.schedule_once(self.paintcanvas)

    def paintcanvas(self, event):

        self.teamh.text = self.df1.index[self.partita].split('-')[0][0:3].upper()
        self.teama.text = self.df1.index[self.partita].split('-')[1][0:3].upper()

        for i, but in enumerate(self.gflab.children):
            but.text = window_obj.proba_string(self.df1, self.partita, 4-i)

        for i, but in enumerate(self.gslab.children):
            but.text = window_obj.proba_string(self.df2, self.partita, 4-i)

        for i, but in enumerate(self.ox2lab.children):
            but.text = window_obj.proba_string(self.df3, self.partita, 2-i)

        for i, but in enumerate(self.gglab.children):
            but.text = window_obj.proba_string(self.df4, self.partita, 1-i)

        for i, but in enumerate(self.uolab.children):
            but.text = window_obj.proba_string(self.df5, self.partita, 1-i)


    def forw(self, event):
        self.partita += 1
        if self.partita > 9:
            self.partita = 0
        Clock.schedule_once(self.paintcanvas, 0.01)

    def backw(self, event):
        self.partita -= 1
        if self.partita < 0:
            self.partita = 9
        Clock.schedule_once(self.paintcanvas, 0.01)

if __name__ == '__main__':
    MainApp().run()
