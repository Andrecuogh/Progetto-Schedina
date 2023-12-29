from kivy.uix.button import Button

def readme(self, event):
    self.clean_window()
    with open('../../../README.md', 'r') as file:
        data = file.read()
    self.window.add_widget(Layout)
    self.window.add_text(data)
    backbutton = self.window.add_widget(Button(text='back'), on_press=self.go_back())

def go_back():
    clean
    self.step2()
    
    

