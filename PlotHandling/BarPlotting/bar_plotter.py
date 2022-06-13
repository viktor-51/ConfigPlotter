import numpy as NP

import matplotlib.pyplot as plt

from PlotHandling import plot_handler

MAX_FIGURES = 10

def plot(info_handler):
    plot_info = info_handler.get_all()

    plot_handler.plot_figures_several(plot_info["bar_info"], plot_bar, MAX_FIGURES)
    print("\n**** Showing maximum of {} first figures **** \n\n**** Rest of the images can be found in the specified save_folder *****".format(MAX_FIGURES))
    plt.show()

def plot_bar(heights, error_lengths, title, bar_names, colors, text_colors, background_colors, amount_of_bars, log, save_folder):
    fig = plt.figure(figsize = plot_handler.FIGURE_SIZE)

    heights, error_lengths = log_if_log(log, heights, error_lengths)
    
    bars = plt.bar(bar_names, heights, yerr = error_lengths, align = "center", color = colors, alpha=0.7, capsize = 10, ecolor = 'black', edgecolor = "teal")

    set_values_on_bars(bars, text_colors, background_colors, amount_of_bars)

    plot_handler.save_and_set_title(fig, title, log, save_folder)
    
    
def set_values_on_bars(bars, text_colors, background_colors, amount_of_bars, shift = True):
    if amount_of_bars > 9:
        return

    x_shift = -0.23 
    height_weight = 0.2 - pol_func(amount_of_bars)
    margin = 0.01

    max_height = get_max_height(bars)
    if max_height == 0:
        return None

    y_shift = max_height * height_weight

    font_size = 40 / (amount_of_bars ** (1/2))


    for idx, rectangle_obj in enumerate(bars.patches):
        height = rectangle_obj.get_height()

        height_percentage_of_max = height / max_height

        if height_percentage_of_max > height_weight + margin:
            x_bar = rectangle_obj.get_x()

            if shift:
                x_text = x_bar - x_shift
                y_text = height - y_shift
            
            if height < 1:
                str_precission = f"{height :.2f}"
            if height > 10000:
                str_precission = f"{height :.2e}"
            else:
                str_precission = f"{height :.0f}"

            text_obj = plt.text(x_text, y_text, str_precission, ha='center', va='bottom', fontsize = font_size, color = text_colors[idx], backgroundcolor = background_colors[idx])

def pol_func(x):
    a = -7 / 225
    b = 8 / 225
    c = - 1 / 450

    return a + b*x + c*(x ** 2)

def get_max_height(bars):
    max_height = 0

    for rectangle_obj in bars.patches:
        next_height = rectangle_obj.get_height()

        if next_height > max_height:
            max_height = next_height

    return max_height

def log_if_log(log, *all_values):
    log_values = []

    if log:
        for values in all_values:
            value = [1 if value == 0 else value for value in values]
            log_values.append(NP.log(value))

        return log_values
    else:
        return all_values


