import numpy as np
from numpy import random 

import matplotlib.colors as mcolors
    
###Colors
color_keys = np.array(list(mcolors.CSS4_COLORS.keys()))
amount_of_colors = color_keys.size

def set_within_limits(color_value):
    if color_value > 1:
        color_value = 0
    elif color_value < 0:
        color_value = 1

    return color_value
    
def get_n_color_keys(N, seed):
    rng = np.random.default_rng(seed)
    indexes = rng.choice(amount_of_colors, size = N, replace = False)
    
    new_color_keys = list(color_keys[ [indexes] ])

    return new_color_keys

def color_to_rgb(color):
    tp = type(color)

    if tp is np.str_ or tp is str: 
       color = mcolors.to_rgb(color)

    return color

class Color_Handler:
    def __init__(self, config = None, create_n_colors = None, seed = None, colors = None):
        if config:
            color_info = config.color_info()    

            colors = color_info["colors"]
            seed = color_info["seed"]

        if colors:
            self.colors = colors
        else:
            self.colors = get_n_color_keys(create_n_colors, seed)
            print("\n The following colors was choosen: \n\n {} \n".format(self.colors))

    def get_colors(self):
        return self.colors

    def shifted_colors(self, shift = 0.3):
        shifted_colors = []

        for color in self.get_colors():
            rgb_color = color_to_rgb(color)

            shifted_color = tuple(np.array(rgb_color) + shift)
            adjusted_color = list(map(set_within_limits, shifted_color))

            shifted_colors.append(adjusted_color)

        return Color_Handler(colors = shifted_colors)

