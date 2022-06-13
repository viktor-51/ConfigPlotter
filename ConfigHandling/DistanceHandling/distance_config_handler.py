from ConfigHandling.DistanceHandling import config
from ConfigHandling import config_handling 
from ConfigHandling.config_handling import __Config_Handler

class Distance_Config_Handler(__Config_Handler): 
    def __init__(self):
        super().__init__(config)

    def generate_title_keys(self):
        new_store = {}
        titles = super().objective_info()["objectives"]

        for idx, value in enumerate(config.AXIS_NAMES.values()):
            title = titles[idx]
            new_store[title] = value

        return new_store

    ###Overrides
    def generate_objective_info(self):
        objective_info = {}
        objective_info["objectives"] = config.TITLES
        objective_info["keys"] = list(range(0, len(config.DIRECTORIES) * 2))
        
        return objective_info

    ###Overrides
    def generate_plot_info(self):
        file_info = super().generate_plot_info()
        file_info["workload_names"] = config.WORKLOAD_NAMES

        return file_info

    ###Overrides
    def dict_to_list(self, values):
        return [values]
