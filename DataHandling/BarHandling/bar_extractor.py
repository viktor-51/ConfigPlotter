from ExceptionHandling import exception

from DataHandling.data_store import Data_Store  
from FileHandling import CSV_handler
from FileHandling import json_handler 

from DataHandling.data_extractor import __Multiple_File_Extractor

err_msg_to_few_names = "\n\n To few bar names are specifed. Provide more bar names in config.py in field BAR_NAMES. Excpeted at least {} \n"

class Bar_Extractor(__Multiple_File_Extractor):
    NO_TIME_AXIS = False

    def __init__(self, config_handler):
        objective_info = config_handler.objective_info()
        self.objective_paths = objective_info["objective_paths"]
        objectives = objective_info["objectives"]

        data_storer = Data_Store(objectives, config_handler, self.NO_TIME_AXIS)

        file_info = config_handler.file_info()

        self.bar_names = file_info["bar_names"]
       
        CSV = "csv"
        SUMMARY = "summary"
        JSON = "json"

        supported_types = [CSV, SUMMARY, JSON]

        CSV_extractor = CSV_handler.extract_object
        json_extractor = json_handler.extract

        extract_functions = {CSV : CSV_extractor, SUMMARY : json_extractor, JSON : json_extractor}

        super().__init__(data_storer, config_handler, extract_functions, supported_types)
        
        self.next_name_idx = 0
        self.wanted_bars = len(self.directories)
        exception.longer_then(self.bar_names, self.directories, err_msg_to_few_names.format(self.wanted_bars))
    
    ###Overrides
    def next_name(self):
        idx = self.next_name_idx % self.wanted_bars 
        next_name = self.bar_names[idx] 

        self.next_name_idx += 1

        return next_name

    ###Overrides
    def get_objective_values(self, current_root, middle_path, common_suffix):
        objective_values = []

        for idx, objective_path in enumerate(self.objective_paths):
            path_suffix = common_suffix[idx]

            result_text, file_type = super().read_file(current_root, middle_path, path_suffix)
            
            if result_text:
                try:
                    objective_value, optimal_idx = super().get_value_from_text(file_type, result_text, objective_path)
                    
                    objective_values.append(objective_value)
                    super().set_optimal_idx(optimal_idx)
                except LookupError as err:
                    err_msg = "\n\n The objective could not be found: {} \n".format(err)
                    print(err_msg)

                    exception.want_to_quit()

                    return None
            
        return objective_values

