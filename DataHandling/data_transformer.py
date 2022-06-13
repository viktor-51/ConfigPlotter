import copy

import numpy as NP

def get_key_store(key_store, keys = False, values = False, items = False):
    if items or (values and keys):
        return list(key_store.items())
    elif keys:
        return list(key_store.keys())
    elif values:
        return list(key_store.values())
    else:
        return key_store

def get_sub_stores(key_store, keys, start_idx, step_size, should_jump, discard_other_keys):
    jump_size = 2 if should_jump else 1 
    
    indencies = NP.arange(
        start_idx, start_idx + step_size * jump_size, jump_size, dtype = "int64"
    ) 

    used_keys = []
    sub_stores = []
    for idx in indencies:
        next_key = keys[idx]
        used_keys.append(next_key)

        sub_store = key_store[next_key]
        sub_stores.append(sub_store)

    if discard_other_keys:
        used_keys = used_keys[0]

    return used_keys, sub_stores

def get_axis_values(sub_key, sub_stores):
    axis_values = []

    for sub_store in sub_stores:
        axis_value = sub_store[sub_key]
        
        axis_values.append(axis_value)
    
    return axis_values

def create_as_many_as(value, length):
    return [value for _ in range(0, length)]

def transform_data_nested_store(
    key_store, storage_1, storage_2, storage_funcs, axis_func, batch_size, should_jump, 
    want_keys, discard_other_keys
):
    
    keys = get_key_store(key_store, keys = True)
    keys_len = len(keys)

    runs = keys_len
    idx = 0

    while runs > 0:
        next_keys, sub_stores = get_sub_stores(key_store, keys, idx, batch_size, should_jump, discard_other_keys)
        runs -= batch_size 
        idx += 1 if should_jump else batch_size

        for sub_key in sub_stores[0].keys():
            axis_values = get_axis_values(sub_key, sub_stores)
            
            values = axis_func(*axis_values)

            if want_keys:
                if not discard_other_keys:
                    sub_keys = create_as_many_as(sub_key, len(values))
                else: 
                    sub_keys = sub_key

                storage_funcs[0](storage_2, sub_keys, values)
            else:
                storage_funcs[0](storage_2, values)

        if want_keys:
            storage_funcs[1](storage_1, next_keys, storage_2)
        else:
            storage_funcs[1](storage_1, storage_2)

def list_append(target, value):
    target.append(value)
    
def list_append_n_op(func, target, value):
    list_append(target, func(value))

def append_and_reset_list(target, source):
    copied_source = copy.deepcopy(source)
    target.append(copied_source)

    source.clear()

def set_store(target, key, value):
    target[key] = value 

def set_store_many(targets, keys, values):
    for idx, key in enumerate(keys):
        targets[idx][key] = values[idx]

def append_and_reset_store(target, key, source):
    target[key] = copy.deepcopy(source)
    source.clear()

def append_and_reset_store_many(target, keys, sources):
    for idx, source in enumerate(sources):
        next_key = keys[idx]

        target[next_key] = copy.deepcopy(source)
        source.clear()

def nothing(target, keys, source):
    pass

def flatten_op(value):
    return value[0]
