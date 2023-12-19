from kivy.uix.button import Button

def new_button(text):
    button = Button(text = str(text), 
                    font_size = 50, 
                    color = 'yellow', 
                    background_color = 'darkgreen')
    return button

def proba_string(df, match, index):
    proba_label = f'{np.round(df.iloc[match, index]*100, 1)} %'
    return proba_label