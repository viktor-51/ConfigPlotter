from io import StringIO

import numpy as NP
import pandas 

from SearchHandling import search_handler
from ExceptionHandling import exception
from DataHandling.axis_store import Axis_Store

NUMPY, NO_NUMPY = True, False 

def extract_object(result_text, objective):
    escape_signs = True

    data_frame = pandas.read_csv(StringIO(result_text))
    
    key = search_handler.search(objective, data_frame.keys(), escape_signs)
    exception.raise_exception_if_none_or_empty(key, objective, "LookupError")

    negate = data_frame[key][1] < 0

    if negate:
        max_idx = data_frame[key].idxmin()
        result = -data_frame[key][max_idx]
    else:
        max_idx = data_frame[key].idxmax()
        result = data_frame[key][max_idx]
   
    max_idx = max_idx
    return result, max_idx 

def extract(path):
    data_frame = pandas.read_csv(path)

    return data_frame.to_numpy()

def extract_all(all_paths):
    reduce_if_empty, no_time = True, False

    all_values = []
    for paths in all_paths:
        init = True

        for path in paths:
            values_array = extract(path)[0 : 110]

            if init:
                axis_store = Axis_Store("value_appender", values_array, no_time)
                init = False
            else:
                axis_store.add(values_array)

        all_values.append(axis_store.values_list(no_time, reduce_if_empty))
    
    return all_values 

def create_files(paths, headers, data = None):
    for idx, next_path in enumerate(paths):
        next_header = headers[idx]

        if data is None:
            create_file(next_path, next_header)
        else:
            create_file(next_path, next_header, data[idx])

def create_file(path, header, data = None):
    data_frame = create_data_frame(data, columns = header)

    data_frame.to_csv(path_or_buf = path, mode = 'w', index = False)

def append(path, data):
    data_frame = create_data_frame(data)

    data_frame.to_csv(
        path_or_buf = path, mode = 'a', header = False, index = False
    )

def headers_from_files(paths):
    headers = []

    for path in paths:
        headers.append(header_from_file(path))

    return headers

def header_from_file(path):
    data_frame = load_file(path, NO_NUMPY)

    return list(data_frame.columns)

def load_files(paths, to_numpy):
    all_data = []

    for next_path in paths:
        all_data.append( load_file(next_path, to_numpy) )

    return all_data

def load_file(path, to_numpy):
    if to_numpy == True:
        return pandas.read_csv(path).to_numpy()
    else:
        return pandas.read_csv(path)

def create_data_frame(data, columns = None):
    if data is None:
        data_array = None
    else:
        data_array = NP.array(data, ndmin = 2)

    data_frame = pandas.DataFrame(
        data = data_array, columns = columns, index = None
    )

    return data_frame

def all_values_at_column(paths, column_name):
    requested_data = []

    for path in paths:
        data_frame = load_file(path, NO_NUMPY)

        requested_data.append(list(data_frame[column_name]))

    return requested_data

def all_data_as_columns(paths):
    first = True
    all_data = None

    all_headers = []
    for path in paths:
        data_frame = load_file(path, NO_NUMPY)

        headers = data_frame.columns
        old_shape = data_frame.shape

        local_array = NP.zeros((old_shape[1], old_shape[0]))
        for idx, header in enumerate(headers):
            all_headers.append(header)
            local_array[idx, :] = data_frame[header].to_numpy()

        if first:
            all_data = local_array
            first = False
        else:
           all_data = NP.append(all_data, local_array, axis = 0)

    return all_data.tolist(), all_headers
