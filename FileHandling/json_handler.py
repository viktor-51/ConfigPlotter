import sys

import json

from SearchHandling import search_handler
from ExceptionHandling import exception

def extract(result_text, objective_entity):
    escape_signs = True

    err = "LookupError"
    summary_data = json.loads(result_text)

    if type(objective_entity) is list:
        branch = summary_data

        for pattern_key in objective_entity:
            key = search_handler.search(pattern_key, branch.keys(), escape_signs)
            exception.raise_exception_if_none_or_empty(key, pattern_key, err)
            
            branch = branch[key]

        leaf_value = branch
    else:
        key = search_handler.search(objective_entity, summary_data.keys())
        exception.raise_exception_if_none_or_empty(key, objective_entity, err)

        leaf_value = summary_data[key]
    
    value_idx = None
    return leaf_value, value_idx
