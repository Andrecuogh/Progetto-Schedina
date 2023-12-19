def applayout(self):      

    self.gfgshead = GridLayout(size_hint=(0.8, 0.05), pos_hint={'center_x': .55, 'center_y': .95}, cols=8)

    self.gflab = GridLayout(size_hint=(0.8, 0.1), pos_hint={'center_x': .55, 'center_y': .87}, cols=8)

    self.gslab = GridLayout(size_hint=(0.8, 0.1), pos_hint={'center_x': .55, 'center_y': .77}, cols=8)


    self.gglab = GridLayout(size_hint=(0.4, 0.1), pos_hint={'center_x': .27, 'center_y': .53}, cols=2)

    self.gghead = GridLayout(size_hint=(0.4, 0.05), pos_hint={'center_x': .27, 'center_y': .61}, cols=2)


    self.uolab = GridLayout(size_hint=(0.4, 0.1), pos_hint={'center_x': .73, 'center_y': .53}, cols=2)

    self.uohead = GridLayout(size_hint=(0.4, 0.05), pos_hint={'center_x': .73, 'center_y': .61}, cols=2)


    self.teamh = Button(size_hint=(0.1, 0.09), pos_hint={'center_x': .08, 'center_y': .87},
                            font_size = 40, color = 'yellow', background_color = 'darkgreen')

    self.teama = Button(size_hint=(0.1, 0.09), pos_hint={'center_x': .08, 'center_y': .77},
                            font_size = 40, color = 'yellow', background_color = 'darkgreen')


    self.ox2head = GridLayout(size_hint=(0.5, 0.05), pos_hint={'center_x': .5, 'center_y': .40}, cols=3)

    self.ox2lab = GridLayout(size_hint=(0.5, 0.1), pos_hint={'center_x': .5, 'center_y': .32}, cols=3)


    self.prec = Button(size_hint=(0.3, 0.1), pos_hint={'center_x': .25, 'center_y': .1},
                              text='Precedente', font_size = 60, color = 'yellow', background_color = 'darkgreen')

    self.suc = Button(size_hint=(0.3, 0.1), pos_hint={'center_x': .75, 'center_y': .1},
                              text='Successivo', font_size = 60, color = 'yellow', background_color = 'darkgreen')

    self.gfgsdesc = Button(text='GOL', font_size = 50, color = 'yellow', size_hint=(0.1, 0.05),
                      pos_hint={'center_x': .08, 'center_y': .95}, background_color = 'darkgreen')

    self.partita = 0