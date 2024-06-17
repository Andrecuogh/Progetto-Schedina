import numpy as np
from kivy.utils import get_color_from_hex

col_list = [64, 134, 104]

colorbar1 = np.column_stack([np.linspace(x * 1.75, x, 50) / 255 for x in col_list])
colorbar2 = np.column_stack([np.linspace(x, x * 0.8, 50) / 255 for x in col_list])
colorbar = np.concatenate((colorbar1, colorbar2))

colors1 = {
    "button": get_color_from_hex("#334b53"),
    "label": get_color_from_hex("#26383e"),
    "label_pressed": get_color_from_hex("#1E2C31"),
    "background": get_color_from_hex("#80BDD1"),
    "warning": [0.682, 0.239, 0.341, 1.0],
    "utilbar": get_color_from_hex("#e8f7ca"),
    "tutorial": get_color_from_hex("#FA8072"),
    "transparent": (0, 0, 0, 0),
    "colorbar": colorbar,
}
