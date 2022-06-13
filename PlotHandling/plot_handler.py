import numpy as NP

import matplotlib.pyplot as plt

from PlotHandling.color_handler import Color_Handler

FIGURE_SIZE = (16, 8)
FIGURE_SAVE_SIZE = (16, 9)
SAVE_DPI = 200

def save_and_set_title(fig, title, log, save_folder):
    set_title(fig, title, log)
    save(fig, title, save_folder)

def save(fig, folder_name, save_folder):
    if save_folder:
        print("\n SAVING figure ")
        fig.set_size_inches(FIGURE_SAVE_SIZE, forward=False)
        fig.savefig(save_folder + "/" + folder_name, dpi = SAVE_DPI)

def set_title(fig, title, log):
    if log:
        fig.suptitle(title + " (plotted in log_10)", fontsize = 'xx-large')
    else:
        fig.suptitle(title, fontsize = 'xx-large')

def set_axes_data(axis, axis_names, dim_3 = None):
    fontsize = 'xx-large'

    if dim_3:
        label_pad = 20
        axis.set_zlabel(
            "z, " + axis_names[2], labelpad = label_pad, fontsize = fontsize
        )
    else:
        label_pad = 4

    axis.set_xlabel(
        "x, " + axis_names[0], fontsize = fontsize, labelpad = label_pad
    )
    axis.set_ylabel(
        "y, " + axis_names[1], fontsize = fontsize, labelpad = label_pad
    )


def plot_figures_several(plot_info, plot_function, show_limit):
    runs = plot_info.amount_of_runs()

    for run_number in runs:
        fig = plot_function(*plot_info.get_values(run_number))

        if run_number >= show_limit:
            plt.close(fig)




