import numpy as np

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
        Window.clearcolor = [0.25, 0.8, 0, 1]

        self.button = Button(text='Predici',
                      font_size = 60, color = 'yellow', bold = True,
                      size_hint=(0.4, 0.2),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      background_color = 'darkgreen')
        self.button.bind(on_press = self.step0)
        self.window.add_widget(self.button)

        self.label = Button(text='',
                      halign = 'center',
                      font_size = 60, color = 'yellow', bold = True,
                      size_hint=(0.4, 0.2),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      background_color = 'darkgreen')

        return self.window


    def step0(self, event):
        self.window.remove_widget(self.button)
        self.window.add_widget(self.label)
        self.label.text = 'Raccogliendo\ni dati'
        Clock.schedule_once(self.step1, 0.1)


    def step1(self, event):
        window_config.applayout(self)
        self.datasets = retrieval.retrieve()
        self.df1 = self.datasets[0].iloc[0:10]
        self.df2 = self.datasets[0].iloc[11:21]
        self.df3 = self.datasets[1]
        self.df4 = self.datasets[2]
        self.df5 = self.datasets[3]
        Clock.schedule_once(self.step2, 0.1)


    def step2(self, event):
        self.window.remove_widget(self.button)
        self.window.clear_widgets()

        objects_clear = [self.gfgshead, self.gflab, self.gslab,
                         self.gglab, self.gghead, self.uolab,
                         self.uohead, self.ox2lab, self.ox2head]

        for obj in objects_clear:
            obj.clear_widgets()

        objects_add = [self.teamh, self.teama, self.gfgsdesc, self.prec, self.suc]

        objects = objects_clear + objects_add
        for obj in objects:
            self.window.add_widget(obj)

        self.prec.bind(on_press = self.backw)
        self.suc.bind(on_press = self.forw)

        Clock.schedule_once(self.step3, 0.1)

    def step3(self, event):
        for i in range(5):
            self.gfgshead.add_widget(window_obj.new_button(str(self.df1.columns[i])))
            self.gflab.add_widget(window_obj.new_button(
                window_obj.proba_string(self.df1, self.partita, i)))
            self.gslab.add_widget(window_obj.new_button(
                window_obj.proba_string(self.df2, self.partita, i)))

        for i in range(3):
            self.ox2head.add_widget(window_obj.new_button(['1', 'X', '2'][i]))
            self.ox2lab.add_widget(window_obj.new_button(
                window_obj.proba_string(self.df3, self.partita, i)))

        for i in range(2):
            self.gghead.add_widget(window_obj.new_button(self.df4.columns[i]))
            self.gglab.add_widget(window_obj.new_button(
                window_obj.proba_string(self.df4, self.partita, i)))

            self.uohead.add_widget(window_obj.new_button(self.df5.columns[i]))
            self.uolab.add_widget(window_obj.new_button(
                window_obj.proba_string(self.df5, self.partita, i)))

        self.teamh.text = self.df1.index[self.partita].split('-')[0][0:3].upper()
        self.teama.text = self.df1.index[self.partita].split('-')[1][0:3].upper()


    def forw(self, event):
        self.partita += 1
        if self.partita > 9:
            self.partita = 0
        Clock.schedule_once(self.step2, 0.01)

    def backw(self, event):
        self.partita -= 1
        if self.partita < 0:
            self.partita = 9
        Clock.schedule_once(self.step2, 0.01)

if __name__ == '__main__':
    MainApp().run()