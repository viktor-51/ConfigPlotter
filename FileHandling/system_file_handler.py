import os

import glob

from SearchHandling import search_handler
from ExceptionHandling import exception

NO_VERBOSE, NO_ADJUST_PATH = False, False

def adjust_faulty_path_combine(path_variables):
    path_variables = adjust_faulty_path(path_variables)

    return "".join(path_variables)

def adjust_faulty_path(path_variables):
    end_idx = len(path_variables) - 1

    for idx, path_variable in enumerate(path_variables):
        first = idx == 0
        last = idx == end_idx

        path_variables[idx] = adjust_faulty_path_variable(path_variable, first = first, last = last)

    return path_variables

def adjust_faulty_path_variable(path_variable, first = False, last = False):
    str_len = len(path_variable)

    if last and path_variable[-1] == "/":
        path_variable = path_variable[0 : str_len - 1]
    elif not last and path_variable[-1] != "/":
        path_variable = path_variable + "/"

    str_len = len(path_variable)

    if path_variable[0] == "/" and not first:
        path_variable = path_variable[1 : str_len]

    return path_variable


def read(file_path, verbose, adjust_path = True):
    if adjust_path:
        file_path = adjust_faulty_path_combine(file_path)

    with open(file_path) as summary_file:
        if verbose: print("loading {}".format(file_path))

        summary_string = summary_file.read() 

    return summary_string

def find_all_at_root(root, suffix, adjust_path):
    def sorting_func(string):
        span = search_handler.span("[0-9]+", string)
        str_int = string[span[0] : span[1]]

        return int(str_int)

    if adjust_path:
        orginal_root = adjust_faulty_path_variable(root[0], first = True)
        middel_part = adjust_faulty_path_variable(root[1])
    
        root = orginal_root + middel_part

    path_pattern = "**/" + suffix 

    found_paths = glob.glob(path_pattern, root_dir = root, recursive = True)
    
    sorted_paths = iter(sorted(sorted(found_paths), key = sorting_func))
    
    all_paths = []
    previous_directory = None 

    sub_files_counted = False
    idx = 0 
    while True:
        try:
            next_path = sorted_paths.__next__()
        except StopIteration:
            break
            
        next_directory = os.path.dirname(next_path)

        if previous_directory is None:
            previous_directory = next_directory 

        elif next_directory != previous_directory:
            sub_files_counted = True
            idx = 0

            previous_directory = next_directory 

        full_path = root + next_path
        
        if sub_files_counted:
            all_paths[idx].append(full_path)
        else:
            local_paths = [full_path]
            all_paths.append(local_paths)

        idx += 1
   
    return all_paths 

def find_n_files(dir_path_pattern, n = 1, find_all = False):
    dir_path, pattern = os.path.split(dir_path_pattern)

    found_files = list(sorted(os.listdir(path = dir_path)))
    matches = search_handler.find_n_matches(pattern, found_files, True, n = n, find_all = find_all)
    exception.raise_exception_if_none_or_empty(matches, dir_path_pattern, "FileNotFoundError")

    found_paths = []
    for match in matches:
        found_path = dir_path + "/" + match
        found_paths.append(found_path)
    
    return found_paths

def find_all(file_path, adjust_path = True):
    if adjust_path:
        file_path = adjust_faulty_path_combine(file_path)
   
    return find_n_files(file_path, find_all = True) 

def find_all_dirs(root, dir_pattern, adjust_path = True):
    if adjust_path:
        root = adjust_faulty_path_variable(root, first = True)
        dir_pattern = adjust_faulty_path_variable(dir_pattern)

    root_len = len(root)

    dir_pattern = dir_pattern[0 : -1]
    dir_path_pattern = root + dir_pattern 

    found_paths = find_n_files(dir_path_pattern, find_all = True)

    found_dirs = []
    for found_path in found_paths:
        found_dir = found_path[root_len : ] 
        found_dirs.append(found_dir)
    
    return found_dirs

def find_n_read_file(file_path, adjust_path = True):
    if adjust_path:
        file_path = adjust_faulty_path_combine(file_path)

    found_path = find_n_files(file_path, n = 1)[0]
    
    return read(found_path, True, adjust_path = False)
    
def to_file_ending(path):
    return path.split(".")[-1]

def get_file_type(file_ending, expected_types):
    for file_type in expected_types:
        if file_type in file_ending:
            return file_type
    
    exception.look_up_err(file_ending)

def create_dirs_at_root(root, directory_names):
    created_paths = []

    for directory_name in directory_names:
        path = root + "/" + directory_name
        exception.do_print_if_exception(os.makedirs, (FileExistsError, ), ["folder already exist: {}".format(path)], lambda : None, [path]) 

        created_paths.append(path)
    return created_paths

