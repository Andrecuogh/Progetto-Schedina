from transversal.utilbar import UtilBar

class Page():

    def __init__(self):
        self.page = None

    def cleaning(self, screen, canvas=True):
        if canvas:
            screen.window.canvas.clear()
        screen.window.clear_widgets()

        UtilBar().draw(screen)