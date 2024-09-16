import numpy as np
from kivy.utils import get_color_from_hex

col_list = [34, 114, 64]

colorbar1 = np.column_stack([np.linspace(x * 1.75, x, 50) / 255 for x in col_list])
colorbar2 = np.column_stack([np.linspace(x, x * 0.8, 50) / 255 for x in col_list])
colorbar = np.concatenate((colorbar1, colorbar2))

colors1 = {
    "primary": get_color_from_hex("#3480ae"),
    "secondary": get_color_from_hex("#34ae62"),
    "background": get_color_from_hex("#acd0e6"),
    "on_background": get_color_from_hex("#8ebfdd"),
    "utilbar": get_color_from_hex("#193d53"),
    "navigationbar": get_color_from_hex("#225472"),
    "navigationbarpressed": get_color_from_hex("#193d53"),
    "label": get_color_from_hex("#225472"),
    "data": get_color_from_hex("#34ae62"),
    "highlighted": get_color_from_hex("#90832b"),
    "presplash": get_color_from_hex("#225472"),
    "tutorialbackground": get_color_from_hex("#225472"),
    "tutorialforth": get_color_from_hex("#34ae62"),
    "tutorialback": get_color_from_hex("#3480ae"),
    "tutorialpages": get_color_from_hex("#34ae62"),
    "transparent": (0, 0, 0, 0),
    "results": {
        "win": get_color_from_hex("#90832b"),
        "draw": get_color_from_hex("#3480ae"),
        "loss": get_color_from_hex("#ae3443"),
    },
    "colorbar": colorbar,
}
