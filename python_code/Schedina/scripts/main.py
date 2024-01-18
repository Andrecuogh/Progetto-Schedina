import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from display import homepage, matchday_page, major_page, window_config


class MainApp(App):
        
    def build(self):
        self.window = FloatLayout(size=(1000, 750))
        window_config.cleaning(self)
        homepage.initializing(self)
        self.button.bind(on_press = self.get_forecasts)
        self.archivio.bind(on_press = self.chooseday)
        
        if homepage.no_updated:
            self.raise_warn(homepage.line, update=True)
            self.ask_upd = True
        
        return self.window
    

    def goto_updlink(self, event):
        import webbrowser
        webbrowser.open(homepage.upd_link)
        Clock.schedule_once(self.remove_warn_box, 1)
        

    def chooseday(self, event):
        matchday_page.list_matchdays(self)
        for b in self.daygrid.children:
            b.bind(on_press=self.get_forecasts)


    def get_forecasts(self, event):
            
        if event.text == 'Predici':
            self.button.text = 'Raccogliendo i dati'
            homepage.loading(self, str(matchday_page.lday+1))
            window_config.cleaning(self, canvas=False)
            Clock.schedule_once(self.createcanvas, 2)

                
        elif int(event.text) < 6:
            self.raise_warn(matchday_page.warning_text)
                
        else:
            homepage.loading(self, event.text)
            Clock.schedule_once(self.createcanvas, 2)
            

    def raise_warn(self, warn_text, fontsize = 50, update=False):

        self.warnlabel.text = warn_text
        self.warnlabel.font_size = fontsize
        self.warnback.bind(on_press = self.remove_warn_box)
        self.window.add_widget(self.warn_box)

        if update:
            self.warn_box.remove_widget(self.warnback)
            self.warn_box.add_widget(self.bupdate)
            self.warn_box.add_widget(self.bskip)
            self.bupdate.bind(on_press = self.goto_updlink)
            self.bskip.bind(on_press = self.remove_warn_box)

    def remove_warn_box(self, event):
        self.window.remove_widget(self.warn_box)
        if self.ask_upd:
            self.warn_box.remove_widget(self.bupdate)
            self.warn_box.remove_widget(self.bskip)
            self.warn_box.add_widget(self.warnback)
            self.ask_upd = False

    def createcanvas(self, event):

        if not self.first:
            major_page.initializecanvas(self)
            self.first = True

        major_page.paintcanvas(self)
        self.prec.bind(on_touch_down = self.backw)
        self.suc.bind(on_touch_down = self.forw)
        self.home.bind(on_touch_down = self.backhome)


    def forw(self, event, touch):
        
        if event.collide_point(*touch.pos):
            self.partita += 1
            if self.partita > 9:
                self.partita = 0
            Clock.schedule_once(self.createcanvas, 0.01)

    def backw(self, event, touch):
        if event.collide_point(*touch.pos):
            self.partita -= 1
            if self.partita < 0:
                self.partita = 9
            Clock.schedule_once(self.createcanvas, 0.01)

    def backhome(self, event, touch):
        if event.collide_point(*touch.pos):
            window_config.cleaning(self)
            homepage.initializing(self)
            self.button.bind(on_press = self.get_forecasts)
            self.archivio.bind(on_press = self.chooseday)
        

if __name__ == '__main__':
    MainApp().run()