from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy import utils
from kivy.core.text import LabelBase, DEFAULT_FONT

colors = {
    'label': utils.get_color_from_hex('#23395d'),
    'text': utils.get_color_from_hex('#ffffff'),
    'background': utils.get_color_from_hex('#afeeee')
}

LabelBase.register(DEFAULT_FONT, "display/fonts/calibri/calibri.ttf")

def applayout(self):      

    self.gfgshead = GridLayout(size_hint=(0.8, 0.05), pos_hint={'center_x': .55, 'center_y': .95}, cols=8)

    self.gflab = GridLayout(size_hint=(0.8, 0.1), pos_hint={'center_x': .55, 'center_y': .87}, cols=8)

    self.gslab = GridLayout(size_hint=(0.8, 0.1), pos_hint={'center_x': .55, 'center_y': .77}, cols=8)


    self.gglab = GridLayout(size_hint=(0.4, 0.1), pos_hint={'center_x': .27, 'center_y': .53}, cols=2)

    self.gghead = GridLayout(size_hint=(0.4, 0.05), pos_hint={'center_x': .27, 'center_y': .61}, cols=2)


    self.uolab = GridLayout(size_hint=(0.4, 0.1), pos_hint={'center_x': .73, 'center_y': .53}, cols=2)

    self.uohead = GridLayout(size_hint=(0.4, 0.05), pos_hint={'center_x': .73, 'center_y': .61}, cols=2)


    self.teamh = Button(size_hint=(0.1, 0.09), pos_hint={'center_x': .08, 'center_y': .87},
                            font_size = 40, color = colors['text'], background_color = colors['label'])

    self.teama = Button(size_hint=(0.1, 0.09), pos_hint={'center_x': .08, 'center_y': .77},
                            font_size = 40, color = colors['text'], background_color = colors['label'])


    self.ox2head = GridLayout(size_hint=(0.5, 0.05), pos_hint={'center_x': .5, 'center_y': .40}, cols=3)

    self.ox2lab = GridLayout(size_hint=(0.5, 0.1), pos_hint={'center_x': .5, 'center_y': .32}, cols=3)


    self.prec = Button(size_hint=(0.3, 0.1), pos_hint={'center_x': .25, 'center_y': .1},
                              text='Precedente', font_size = 60, color = colors['text'], background_color = colors['label'])

    self.suc = Button(size_hint=(0.3, 0.1), pos_hint={'center_x': .75, 'center_y': .1},
                              text='Successivo', font_size = 60, color = colors['text'], background_color = colors['label'])

    self.gfgsdesc = Button(text='GOL', font_size = 50, color = colors['text'], size_hint=(0.1, 0.05),
                      pos_hint={'center_x': .08, 'center_y': .95}, background_color = colors['label'])

    self.partita = 0