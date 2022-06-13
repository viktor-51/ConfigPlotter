import sys

from ExceptionHandling import exception

from FileHandling import file_handler
from FileHandling import system_file_handler


def get_value_in_range(l, idx):
        if len(l) <= idx:
            return l[-1]
        else: 
            return l[idx]

class __Data_Extractor:
    def __init__(self, data_storer, config_handler, extract_functions, supported_types):
        self.data_storer = data_storer
        file_info = config_handler.file_info()

        self.root_dirs = file_info["root_dirs"]
        self.directories = file_info["directories"]
        self.common_suffix_list = file_info["common_suffix_list"]
        self.adjust_path = file_info["adjust_path"]

        self.extract_functions = extract_functions

        self.supported_types = supported_types

    def next_name(self):
        pass

    def extract_file_data(self):
        adjust_path = self.adjust_path

        for idx, file_entity in enumerate(self.directories): 
            current_root = self.root_dirs[idx]
            common_suffix = get_value_in_range(self.common_suffix_list, idx)
            
            if type(file_entity) is list:
                for sub_idx, middle_path in enumerate(file_entity):
                    name = self.next_name()
                    self.extract(name, current_root, middle_path, common_suffix, adjust_path)
            else:
                name = self.next_name()
                self.extract(name, current_root, file_entity, common_suffix, adjust_path)

            
        print("\n\n ***DONE*** \n")
        return self.data_storer

    def extract(self, name, current_root, middle_path, common_suffix, adjust_path):
        try:
            found_dirs = system_file_handler.find_all_dirs(current_root, middle_path, adjust_path = True)
        except FileNotFoundError as err:
            e_msg = "\n\nFailed to find the directory specified in DIRECTORY as {} \n".format(err)
            print(e_msg)

            exception.want_to_quit()

        for middle_path in found_dirs:
            objective_values = self.get_objective_values(current_root, middle_path, common_suffix)
            
            self.add_values_to_store(name, objective_values)
                    
    def add_values_to_store(self, name, objective_values):
        self.data_storer.add_all_to_key(name, objective_values)
    
    def get_objective_values(self, current_root, middle_path, common_suffix):
        pass 

    def read_file(self, current_root, middle_path, path_suffix):
        return file_handler.search_read(current_root, middle_path, path_suffix, self.supported_types, self.adjust_path)

    def get_value_from_text(self, file_type, *args):
        extract_function = self.extract_functions[file_type] 

        try:
            return_values = extract_function(*args)
        except LookupError as err:
            err_msg = "\n\n The objective could not be found: {} \n".format(err)
            print(err_msg)

            exception.want_to_quit()

            return None
                
        return return_values

class __Multiple_File_Extractor(__Data_Extractor):
    def __init__(self, data_storer, config_handler, extract_functions, supported_types):
        self.found_first_file = False 
        self.first_index = None

        super().__init__(data_storer, config_handler, extract_functions, supported_types)
    
    #overrides
    def read_file(self, current_root, middle_path, path_suffix):
        if self.found_first_file:
            return file_handler.search_read(current_root, middle_path, path_suffix, self.supported_types, self.adjust_path, idx = self.first_index)
        else:
            return super().read_file(current_root, middle_path, path_suffix)

    #overrides
    def set_optimal_idx(self, idx):
        if not self.found_first_file:
            self.found_first_file = True
            self.first_index = idx
    
