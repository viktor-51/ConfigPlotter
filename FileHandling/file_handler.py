import sys

import os

from FileHandling import system_file_handler
from ExceptionHandling import exception

KEY_CHAR = '@'

def read(path, expected_file_types):
    result_text, file_type = None, None
    
    try: 
        file_ending = system_file_handler.to_file_ending(path)
        temp1 = system_file_handler.get_file_type(file_ending, expected_file_types)

        temp2 = system_file_handler.read(path, adjust_path = False) 

        file_type = temp1
        result_text = temp2

    except FileNotFoundError as err:
        err_msg = "\nThe following path could not be found {}\n\n".format(err)
        print(err_msg)

        exception.want_to_quit()

    except LookupError as err:
        err_msg = "\nThe following file type is not supported {} ".format(err)
        print(err_msg)
        
        exception.want_to_quit()
        
    return result_text, file_type


def search_read(root_dir, middle_path, suffix, expected_file_types, adjust_path, idx = None):
    result_text, file_type = None, None

    if idx != None:
        suffix = set_as_idx(suffix, idx)

    if adjust_path:
        file_variable = [root_dir, middle_path, suffix]
    else: 
        file_variable = root_dir + middle_path + suffix

    try: 
        temp1 = system_file_handler.find_n_read_file(file_variable, adjust_path)

        file_ending = system_file_handler.to_file_ending(suffix)
        temp2 = system_file_handler.get_file_type(file_ending, expected_file_types)

        result_text = temp1
        file_type = temp2

    except FileNotFoundError as err:
        specification = "\n root: {} \n dir: {} \n suffix: {}".format(root_dir, middle_path, suffix)
        fields = "\n\nThe fields you had an error in is defined in config.py \n\nThe field names are: \n root_dir: ROOT_DIR \n directory: DIRECTORIES \n suffix: COMMON_SUFFIX "

        e_messages = [specification, fields]

        err_msg = "\nThe following path could not be found {}. \n\nSpecified as: {} {} \n\n".format(err, *e_messages)
        print(err_msg)

        exception.want_to_quit()

    except LookupError as err:
        err_msg = "\nThe following file type is not supported {} ".format(err)
        print(err_msg)
        
        exception.want_to_quit()
        
    return result_text, file_type

def set_as_idx(suffix, idx):
    if idx == 0:
        return suffix.replace(".@", "")
    else:
        return suffix.replace(KEY_CHAR, str(idx))


