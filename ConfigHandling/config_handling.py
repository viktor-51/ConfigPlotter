import copy

def return_values_or_list(serializable):
    if type(serializable) is dict:
        return into_list(serializable.values())
    else:
        return into_list(serializable)

def assure_correct_size(value, size):
    value = into_list(value)
    new_list = copy.copy(value)
    
    start = len(value)

    for _ in range(start, size):
        new_list.append(value[start - 1])

    return new_list

def into_list(value):
    if type(value) is str:
        return [value]
    else:
        return list(value)


class __Config_Handler:

    def __init__(self, config):
        self.config = config
        
        color_seed = config.COLOR_SEED
        colors = config.COLORS

        self.color_info_map = {"seed" : color_seed, "colors" : colors}

        #Order matters here
        self.plot_info_map = self.generate_plot_info() 
        self.objective_info_map = self.generate_objective_info() 
        self.file_info_map = self.generate_file_info() 

        self.axis_name_store = self.generate_title_keys()

    def objective_info(self):
        return self.objective_info_map

    def file_info(self):
        return self.file_info_map

    def plot_info(self):
        return self.plot_info_map

    def color_info(self):
        return self.color_info_map

    def generate_objective_info(self):
        pass

    def generate_file_info(self):
        file_info_map = {}
        config = self.config

        file_info_map["adjust_path"] = config.ADJUST_PATH
        file_info_map["directories"] = return_values_or_list(config.DIRECTORIES)
        file_info_map["root_dirs"] = assure_correct_size(config.ROOT_DIRS, len(file_info_map["directories"]))
        file_info_map["common_suffix_list"] = self.dict_to_list(config.COMMON_SUFFIX)

        return file_info_map

    def generate_plot_info(self):
        plot_info_map = {}

        plot_info_map["save_folder"] = self.config.SAVE_FOLDER
        plot_info_map["log_10"] = self.config.LOG_10

        return plot_info_map
     
    def dict_to_list(self, values):
        objective_size = len(self.objective_info_map["objectives"])

        if type(values) is dict:
            new_list = []

            for key, value in values.items():
                size_corrected_value = assure_correct_size(value, objective_size)

                if type(key) is tuple:
                    for idx in key:
                        new_list.append(size_corrected_value)
                else:
                    new_list.append(size_corrected_value)
            return new_list
        else:
            return assure_correct_size([values], objective_size)
       
    def amount_of_bars(self):
        return len(self.file_info_map["directories"])

    def get_titles(self):
        pass
    
    def get_axis_names(self, key):
        return self.axis_name_store[key]
