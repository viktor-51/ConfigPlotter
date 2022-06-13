from FileHandling import system_file_handler

from PlotHandling.plot_info_handler import Plot_Info_Handler

from PlotHandling.DistancePlotting.line_info import Line_Info 
from PlotHandling.DistancePlotting.distance_info import Distance_Info

class Distance_Info_Handler(Plot_Info_Handler):
    SAVE_DIRS_LINE = ["Timeline", "EuclideanIterations", "EuclideanWorkload"]
    SAVE_DIRS_SCATTER = ["Manhattan", "Values", "Mean"]

    FILE_IDX_LINE = {"time_line" : 0 , "euc_equal_workloads" : 1, "euc_different_workloads" : 2}
    FILE_IDX_SCATTER = {"manhattan_info" : 0 , "scatter_info" : 1, "scatter_mean_info" : 2}

    def __init__(self, config):
        plot_info = config.plot_info()
        save_folder = plot_info["save_folder"]
        
        SAVE_DIRS_LINE = ["LinePlots/" + next_path for next_path in self.SAVE_DIRS_LINE]
        SAVE_DIRS_SCATTER = ["ScatterPlots/" + next_path for next_path in self.SAVE_DIRS_SCATTER]
    
        self.save_paths_line = system_file_handler.create_dirs_at_root(save_folder, SAVE_DIRS_LINE)
        self.save_paths_scatter = system_file_handler.create_dirs_at_root(save_folder, SAVE_DIRS_SCATTER)
        
        super().__init__()

    def assign_distance_info_1D(self, name, *distance_parameters):
        idx = self.FILE_IDX_LINE[name]
        save_path = self.save_paths_line[idx]

        self.plot_infos[name] = Distance_Info(*distance_parameters, save_path)

    def assign_distance_info_3D(self, name, *distance_parameters):
        idx = self.FILE_IDX_SCATTER[name]
        save_path = self.save_paths_scatter[idx]

        self.plot_infos[name] = Distance_Info(*distance_parameters, save_path)

    def assign_line_info(self, name, *line_parameters, time = None):
        idx = self.FILE_IDX_LINE[name]
        save_path = self.save_paths_line[idx]

        self.plot_infos[name] = Line_Info(*line_parameters, save_path, time = time)

