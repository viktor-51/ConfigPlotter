from PlotHandling.plot_info_handler import Plot_Info_Handler
from PlotHandling.BarPlotting.bar_info import Bar_Info

class Bar_Info_Handler(Plot_Info_Handler):
    def __init__(self, config):
        self.save_path = config.plot_info()["save_folder"]
        
        super().__init__()
    
    def assign_bar_info(self, name, *bar_parameters):
        self.plot_infos[name] = Bar_Info(*bar_parameters, self.save_path)

