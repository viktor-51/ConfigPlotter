import functools

import numpy as NP

import matplotlib.pyplot as plt
import matplotlib.colors as colors

from FileHandling import system_file_handler

from PlotHandling import plot_handler
from PlotHandling.BarPlotting import bar_plotter

MAX_FIGURES = 1

NO_LOG_10 = False

def make_colors(names):
    new_cmaps = []

    for name in names:
        cmap = plt.get_cmap(name)
        new_cmap = colors.LinearSegmentedColormap.from_list(
            'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=0.4, b=1), 
            cmap(NP.linspace(0.4, 1, 100))
        )
        
        new_cmaps.append(new_cmap)

    return new_cmaps

CMAP_NAMES = ["Blues", "Reds", "Greens", "Purples", "Greys", "YlOrBr"]
COLOR_MAPS = make_colors(CMAP_NAMES) 

COLORS = ["orange", "sienna", "cyan"]

def plot(info_handler):
    scatter_plotter_1D = functools.partial(plot_several_1D, plot_scatter_several_1D)  
    scatter_plotter_3D = plot_scatter_several_3D
    line_plotter = functools.partial(plot_several_1D, plot_line_several)  

    plot_data = info_handler.get_all()
    
    font = {'family' : 'normal', 'weight' : 'bold', 'size' : 22}

    plt.rc('font', **font)

    plot_handler.plot_figures_several(
        plot_data["time_line"], line_plotter, MAX_FIGURES
    )
    plot_handler.plot_figures_several(
        plot_data["euc_equal_workloads"], line_plotter, MAX_FIGURES
    )
    plot_handler.plot_figures_several(
        plot_data["euc_different_workloads"], line_plotter, MAX_FIGURES
    )
    plot_handler.plot_figures_several(
        plot_data["scatter_info"], scatter_plotter_3D, MAX_FIGURES
    )
    plot_handler.plot_figures_several(
        plot_data["scatter_mean_info"], scatter_plotter_3D, MAX_FIGURES
    )
    plot_handler.plot_figures_several(
        plot_data["manhattan_info"], scatter_plotter_3D, MAX_FIGURES
    )
    
    print("\n**** Showing maximum of {} first figures(Not 1D plots) **** \n\n**** Rest of the images can be found in the specified save_folder *****".format(MAX_FIGURES * 3))
    
    plt.show()

def plot_scatter_several_3D(
    values, title, axis_names, legend_title, save_folder, legend_labels
):
    fig = plt.figure(figsize = plot_handler.FIGURE_SIZE)
    axis = fig.add_subplot(111, projection='3d')
    
    values = NP.array(values)
    amount_rows, amount_columns = values.shape[0 : 2] 
    color = NP.linspace(0, 1, amount_columns)
    
    print("shape under", values.shape)
    for idx in range(0, amount_rows):
        next_values = values[idx]
        plot_scatter_3D(next_values, axis, color, COLOR_MAPS[idx], legend_labels[idx])
        
    axis.legend(title = legend_title, fontsize = 'small')
    plot_handler.set_axes_data(axis, axis_names, dim_3 = True)
    plot_handler.save_and_set_title(fig, title, NO_LOG_10, save_folder)
    
    return fig

def plot_scatter_3D(values, axis, color, color_map, label):
    axis.scatter(values[:, 0], values[:, 1], values[:, 2], c = color, cmap = color_map, label = label)

def plot_several_1D(
    plot_function, values, title, axis_names, legend_title, save_folder, 
    time_axis, *function_parameters
):
    x_locs = None
    values = NP.array(values)

    print("shape under", values.shape)
    amount_rows, amount_columns, amount_figures = values.shape[0 : 3]

    if time_axis == None:
        vline_variables = None

        x_legend = "iteration" 
        x_locs = NP.linspace(0, amount_columns - 1, amount_columns)
        
        x_values = x_locs 
    else:
        vline_variables = {"amount_iterations" : 10}

        x_legend = "seconds" 
        x_values = NP.around(time_axis)

    figures, all_1D_axes = create_n_figures(amount_figures, x_locs = x_locs)
    plot_function(
        all_1D_axes, amount_rows, amount_figures, x_values, values, 
        vline_variables, *function_parameters
    )
            
    for idx in range(0, amount_figures):
        next_axis = all_1D_axes[idx]     
        next_axis.legend(title = legend_title)

        next_axis_name = [x_legend, axis_names[idx]]
        plot_handler.set_axes_data(next_axis, next_axis_name, dim_3 = False)
        
        next_figure = figures[idx]

        plt.close(next_figure)
        plot_handler.save_and_set_title(
            next_figure, title + ", " + axis_names[idx], NO_LOG_10, save_folder
        )

    return figures[0]

def plot_scatter_several_1D(axis, amount_rows, amount_figures, x_values, y_values, legend_labels):
    for idx in range(0, amount_rows):
        next_y_values = y_values[idx]

        plot_scatter_1D(x_values[idx], next_y_values, axis, amount_figures, legend_labels[idx])

def plot_scatter_1D(x_values, y_values, axis, stop, label):
    for idx in range(0, stop):
        axis[idx].scatter(x_values, y_values[:, idx], label = label)

def create_n_figures(size, x_locs = None):
    figures = []
    axis = []

    for _ in range(0, size):
        next_figure = plt.figure(figsize = plot_handler.FIGURE_SIZE)
        
        if x_locs is not None: plt.xticks(x_locs)

        plt.axis()
        next_axis = next_figure.get_axes()[0] 

        figures.append(next_figure)
        axis.append(next_axis)

    return figures, axis

def plot_line_several(
    axis, amount_rows, amount_figures, x_values, y_values, vline_variables, 
    std_values, legend_labels
):
    std_values = NP.array(std_values) 
    
    for idx in range(0, amount_figures):
        next_y_values, next_stds = y_values[:, :, idx], std_values[:, :, idx]

        plot_line(
            x_values, next_y_values, next_stds, axis[idx], amount_rows, 
            legend_labels, vline_variables
        )

def plot_line(
    x_values, y_values, std_values, axis, stop, labels, vline_variables
):
    positiv_multiplex = 1.05
    negativ_multiplex = 0.95
    
    if vline_variables is not None:
        highest_limit = NP.max(NP.add(y_values, std_values)) 
        lowest_limit  = NP.min(NP.subtract(y_values, std_values)) 

        highest_limit *= positiv_multiplex if NP.sign(highest_limit) == 1 else negativ_multiplex 
        lowest_limit *= negativ_multiplex if NP.sign(lowest_limit) == 1 else positiv_multiplex 

        x_len = len(x_values)
        split_size = int(x_len / vline_variables["amount_iterations"])
        
        iteration_x_pos = [] 
        warmup_x_pos = [] 
        for selection in range(0, x_len, split_size):
            iteration_x_pos.append(x_values[selection])
            warmup_x_pos.append(x_values[selection + 30])

        axis.vlines(
            iteration_x_pos, highest_limit, lowest_limit, 
            color="green", label="iteration_border", linestyles = "dotted",
            linewidth = 4
        )
        axis.vlines(
            warmup_x_pos, highest_limit, lowest_limit, color="#764AF1",
            label="warmup_zone", linestyles="dotted", linewidth = 4
        )
    
    for idx in range(0, stop):
        next_y_values = y_values[idx]
        next_stds_values = std_values[idx]

        lower_limit = NP.subtract(next_y_values, next_stds_values)
        upper_limit = NP.add(next_y_values, next_stds_values) 
        axis.fill_between(
            x_values, lower_limit, y2 = upper_limit, alpha = 0.3
        )

        axis.tick_params(axis='both', which='major', labelsize=20)

        axis.plot(
            x_values, next_y_values, label = labels[idx], markersize = 100,
            linewidth = 5
        )

