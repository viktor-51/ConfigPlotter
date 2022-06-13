from DataHandling import data_handler
from DataHandling.BarHandling.bar_extractor import Bar_Extractor
from ConfigHandling.BarHandling.bar_config_handler import Bar_Config_Handler

from DataHandling.DistanceHandling.distance_extractor import Distance_Extractor
from ConfigHandling.DistanceHandling.distance_config_handler import Distance_Config_Handler

from PlotHandling.DistancePlotting import distance_plotter
from PlotHandling.BarPlotting import bar_plotter


if __name__ == '__main__':
    choice = input("\n\n1: bar plotter \n\n2: distance plotter \n\n: ")
    choice = int(choice)

    if choice == 1:
        print("\n *** Running bar plotter *** \n")
        
        bar_config_handler = Bar_Config_Handler()
        extractor = Bar_Extractor(bar_config_handler)

        info_handler = data_handler.bar_data(extractor, bar_config_handler) 
        bar_plotter.plot(info_handler)
    
    elif choice == 2:
        print("\n *** Running distance plotter *** \n")

        distance_config_handler = Distance_Config_Handler()
        extractor = Distance_Extractor(distance_config_handler)
        
        info_handler = data_handler.distance_data(extractor, distance_config_handler) 
        distance_plotter.plot(info_handler)

