from kivy.uix.button import Button
from display.window_config import colors
import numpy as np

def new_button(text, label=False):
    if label:
        fonts = 45
    else:
        fonts = 40
    button = Button(text = str(text), 
                    font_size = fonts, 
                    color = colors['text'], 
                    background_color = colors['label'])
    return button

def proba_string(df, match, index):
    proba_label = f'{np.round(df.iloc[match, index]*100, 1)} %'
    return proba_label