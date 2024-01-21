from display.window_config import Page, CustomButton
from gitconnect.gitset import repopath

class InfoPage(Page):

    def __init__(self):
        path = f'https://raw.githubusercontent.com/{repopath}/main/Readme.md'
        with open(path, 'r') as file:
            self.text= file.read()
        
    def informating(self, screen):
        self.cleaning(screen)

        infolayout = CustomButton(
            category='button',
            text = self.text,
            pos_hint=(0.2, 0.2),
            size_hint=(0.6, 0.6)
        )

        infobackbutton = CustomButton(
            category='bbutton',
            text = 'Ok',
            
        )

        screen.window.add_widget(infolayout)
        backbutton = self.window.add_widget(Button(text='back'), on_press=self.go_back())

def go_back():
    clean
    self.step2()
    
    

