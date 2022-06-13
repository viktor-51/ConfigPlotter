from FileHandling import file_handler
from FileHandling import system_file_handler

from ExceptionHandling import exception

from DataHandling.data_store import Data_Store 
from DataHandling.data_extractor import __Data_Extractor

from FileHandling import CSV_handler

class Distance_Extractor(__Data_Extractor):
    
    def __init__(self, config_handler):
        objective_info = config_handler.objective_info()

        objectives = objective_info["objectives"]
        self.keys = objective_info["keys"]
        
        self.next_name_idx = 0

        data_storer = Data_Store(objectives, config_handler, True)

        file_info = config_handler.file_info()

        CSV = "csv"
        self.supported_file_types = [CSV]

        CSV_extractor = CSV_handler.extract_all

        extract_functions = {CSV : CSV_extractor}
        super().__init__(data_storer, config_handler, extract_functions, self.supported_file_types)
        

    ###Overrides
    def get_objective_values(self, current_root, middle_path, common_suffix):
        new_root = [current_root, middle_path]
        
        try:
            file_paths = system_file_handler.find_all_at_root(new_root, common_suffix, adjust_path = True)
        except FileNotFoundError as err:
            e_msg = "\n\nFailed to find any objective file in {} \n".format(err)
            print(e_msg)
            
            exception.want_to_quit()

        objective_values = super().get_value_from_text(self.supported_file_types[0], file_paths)  
        return objective_values

    ###Overrides
    def next_name(self):
        idx = self.next_name_idx
        next_name = self.keys[idx] 

        self.next_name_idx += 1

        return next_name

    ###Overrides
    def read_file(self, file_path):
        return file_handler.read(file_path, self.supported_file_types)
