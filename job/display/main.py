import webbrowser
import urllib.request as urlr

import sys
import os
if os.getcwd().split('/')[-1] == 'display':
    os.chdir('../..')
sys.path.append(os.getcwd())

import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from app_utils.window_config import AppConfigurer
from homepage.homepage import Homepage
from matchday_page.matchday_page import MatchdayPage
from major_page.major_page import MajorPage
from transversal.utilbar import Infos
from set_up_kivy.config_var import VERSION, PATH


class MainApp(App):
    def build(self):
        self.curr_version = VERSION
        self.read_txt()

        self.window = FloatLayout()

        self.app_con = AppConfigurer()
        self.app_con.custom_init()
        self.colors = self.app_con.paint()

        self.hp = Homepage()
        self.mdp = MatchdayPage(self.lat_matchday)
        self.mjp = MajorPage()
        self.ip = Infos()

        self.hp.cleaning(self)
        self.hp.initializing(self)
        self.button.bind(on_press=self.get_forecasts)
        self.archivio.bind(on_press=self.chooseday)
        self.bindutils()

        if self.app_con.check_update(self.curr_version):
            self.raise_warn(self.app_con.line, update=True)
            self.hp.ask_upd = True

        return self.window

    def read_txt(self):
        file = urlr.urlopen(
            f"https://raw.githubusercontent.com/Andrecuogh/Progetto-Schedina/main/set_up/config_app.txt"
            )
        lines = file.read().decode().split('\n')
        self.lat_matchday = int(lines[1].split(" = ")[1])

    def bindutils(self):
        self.quitting.bind(on_press=self.stop)
        self.info.bind(on_press=self.infopage)

    def infopage(self, event):
        self.ip.informating(self)
        self.infobackbutton.bind(on_press=self.infoback)

    def infoback(self, event):
        self.window.remove_widget(self.infolayout)
        self.window.remove_widget(self.infobackbutton)

    def get_forecasts(self, event):
        if event.text == "Predici":
            self.button.text = "Raccogliendo i dati"
            self.hp.loading(self, str(self.lat_matchday + 1))
            self.hp.cleaning(self, canvas=False)
            self.window.add_widget(self.button)
            Clock.schedule_once(self.createcanvas, 2)

        elif int(event.text) < 6:
            self.raise_warn(self.mdp.warning_text)

        else:
            self.hp.loading(self, event.text)
            Clock.schedule_once(self.createcanvas, 2)

    def goto_updlink(self, event):
        webbrowser.open(self.app_con.upd_link)
        Clock.schedule_once(self.remove_warn_box, 1)

    def chooseday(self, event):
        self.mdp.list_matchdays(self)
        for b in self.daygrid.children:
            b.bind(on_press=self.get_forecasts)
        self.bindutils()

    def raise_warn(self, warn_text, fontsize=50, update=False):
        self.warnlabel.text = warn_text
        self.warnlabel.text_size = (self.window.size[0] * 0.75, None)
        self.warnlabel.font_size = fontsize
        self.warnback.bind(on_press=self.remove_warn_box)
        self.window.add_widget(self.warn_box)

        if update:
            self.warnlabel.text_size = (self.window.size[0] * 7.5, None)
            self.warn_box.remove_widget(self.warnback)
            self.warn_box.add_widget(self.bupdate)
            self.warn_box.add_widget(self.bskip)
            self.bupdate.bind(on_press=self.goto_updlink)
            self.bskip.bind(on_press=self.remove_warn_box)

    def remove_warn_box(self, event):
        self.window.remove_widget(self.warn_box)
        if self.hp.ask_upd:
            self.warn_box.remove_widget(self.bupdate)
            self.warn_box.remove_widget(self.bskip)
            self.warn_box.add_widget(self.warnback)
            self.hp.ask_upd = False

    def createcanvas(self, event):
        if not self.hp.first:
            self.mjp.initializecanvas(self)
            self.hp.first = True

        self.mjp.paintcanvas(self)
        self.prec.bind(on_touch_down=self.backw)
        self.suc.bind(on_touch_down=self.forw)
        self.home.bind(on_touch_down=self.backhome)
        self.bindutils()

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
            self.mjp.cleaning(self)
            self.hp.initializing(self)
            self.hp.first = False
            self.button.bind(on_press=self.get_forecasts)
            self.archivio.bind(on_press=self.chooseday)
            self.bindutils()


if __name__ == "__main__":
    MainApp().run()
