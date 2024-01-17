import numpy as np

from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.gridlayout import GridLayout

col_list = [64, 134, 104]
colorbar1 = np.column_stack([np.linspace(x*1.75, x, 50)/255 for x in col_list])
colorbar2 = np.column_stack([np.linspace(x, x*0.8, 50)/255 for x in col_list])
colorbar = np.concatenate((colorbar1, colorbar2))

colors = {
    'button': get_color_from_hex('#334b53'),
    'label': get_color_from_hex('#26383e'),
    'text': get_color_from_hex('#ffffff'),
    'background': get_color_from_hex('#80BDD1')
}

LabelBase.register(DEFAULT_FONT, "display/fonts/calibri/calibri.ttf", fn_bold="display/fonts/calibri/calibrib.ttf")

def utilbar(self):
    wind_size = self.window.size
    self.utilbar = GridLayout(pos_hint={'x': 0.02, 'y': 0.92},
                              size_hint=(0.96, 0.06),
                              cols = 3, spacing = [20, 0])

    tutorial = ToggleButton(text = 'Tutorial', font_size=50, bold = True,
                      background_normal = '', background_color = colors['label'])
    self.utilbar.add_widget(tutorial)
    
    info = Button(text = 'About', font_size=50, bold = True,
                  background_normal = '', background_color = colors['label'])
    self.utilbar.add_widget(info)

    quitting = Button(text = 'Quit', font_size=50, bold = True,
                      background_normal = '', background_color = colors['label'])
    self.utilbar.add_widget(quitting)

    self.window.add_widget(self.utilbar)
    

def cleaning(self, canvas=True):
    if canvas:
        self.window.canvas.clear()
    self.window.clear_widgets()

    wind_size = self.window.size
    r,g,b,a = colors['text']
    
    with self.window.canvas:
        Color(r, g, b, a)
        RoundedRectangle(pos=[wind_size[0]*0.01, wind_size[1]*0.91],
                         size=[wind_size[0]*0.98, wind_size[1]*0.08])

    utilbar(self)
