import copy

###for testing
#import ConfigHandling.BarHandling.test_plot_config as config

from ConfigHandling.BarHandling import config
from ConfigHandling import config_handling
from ConfigHandling.config_handling import __Config_Handler

def flatten_n_extract_ending(l):
    new_list = []

    for sub_list in l:
        if type(sub_list) is list:
            item = sub_list[-1]
        else:
            item = sub_list
        
        new_list.append(item)

    return new_list

class Bar_Config_Handler(__Config_Handler):
    def __init__(self):
        super().__init__(config)

    def generate_title_keys(self):
        new_store = {}
        titles = super().objective_info()["objectives"]
        bar_names = super().file_info()["bar_names"]

        amount_of_bars = super().amount_of_bars()
        valid_bar_names = bar_names[0 : amount_of_bars]

        for title in titles:
            new_store[title] =  valid_bar_names

        return new_store

    ###Overrides
    def generate_objective_info(self):
        objective_info = {}
        objective_info["objective_paths"] = config.OBJECTIVES
        
        objectives_flatt = flatten_n_extract_ending(objective_info["objective_paths"])
        objective_info["objectives"] = self.titles_or_objectives(objectives_flatt)

        return objective_info

    ###Overrides
    def generate_file_info(self):
        file_info = super().generate_file_info()
        file_info["bar_names"] = config_handling.into_list(config.BAR_NAMES)

        return file_info

    def titles_or_objectives(self, objectives):
        titles = config.TITLES

        if titles:
            max_titles = len(objectives)
            return titles[0 : max_titles]
        else:
            return objectives

