import functools

import copy

import numpy as NP

from tabulate import tabulate

from DataHandling import data_transformer
from DataHandling.axis_store import Axis_Store

class Data_Store:
    STEP_SIZE_1, STEP_SIZE_2 = 1, 2
    NO_JUMP = False
    WANT_KEYS = DISCARD_OTHER_KEYS = INCLUDE_TIME_AXIS = True
    
    def append_key(self, store, key, value):
        if key in store:
            store[key].append(value)
        else:
            store[key] = [key, value]

    def axis_store_add(self, store, key, value):
        store[key].add(value)
   
    def store_add_new_axis_store(self, sub_store, sub_key, value):
        sub_store[sub_key] = Axis_Store(
            sub_key, value, self.have_time_axis,
            config_handler = self.config_handler
        )

    def __init__(
        self, sub_keys, config_handler, have_time_axis, key_store = None
    ):
        self.sub_keys = sub_keys
        self.config_handler = config_handler
        self.have_time_axis = have_time_axis

        self.count_sub_keys = len(sub_keys) 

        if key_store:
            self.key_store = key_store
        else:
            self.key_store = {}


    ###Overrides object class __str__
    def __str__(self):
        reduce_if_empty = True
        storage_funcs = [self.append_key, data_transformer.nothing]
        

        get_values_func = functools.partial(
            Axis_Store.values_list, include_time = self.INCLUDE_TIME_AXIS,
            reduce_if_empty = reduce_if_empty
        )
        
        headers = self.get_key_store(keys = True)
        headers.insert(0, "sub_headers")
        
        formated_dict = {}
        self.transform_data(
            [], formated_dict, storage_funcs, get_values_func, self.STEP_SIZE_1,
            self.NO_JUMP, self.WANT_KEYS, self.DISCARD_OTHER_KEYS
        )

        return tabulate(formated_dict.values(), headers = headers)
    
    def values_list(self, include_time, reduce_if_empty, flatten):
        aggregator_func = self.list_transformtation
        return self.values_getter(
            aggregator_func, include_time, reduce_if_empty, flatten
        )

    def values_dict(self, reduce_if_empty):
        aggregator_func = self.dict_transformation
        return self.values_getter(
            aggregator_func, False, reduce_if_empty, False
        )

    def values_getter(
        self, aggregator_func, include_time, reduce_if_empty, flatten
    ):
        if flatten:
            flatten_op = data_transformer.flatten_op
        else:
            flatten_op = None

        values_list_func = functools.partial(
            Axis_Store.values_list, include_time = include_time,
            reduce_if_empty = reduce_if_empty
        )
        all_values = aggregator_func(
            values_list_func, self.STEP_SIZE_1, self.NO_JUMP, flatten_op
        )
        
        return all_values 

    def flip_order(self):
        new_keys = [None]

        def flip_func(container, *x):
            new_keys = list(range(0, len(x)))
            new_sub_store = dict(zip(new_keys, x))
            
            container[0] = new_keys
            return new_sub_store 

        flip_func = functools.partial(flip_func, new_keys)

        add_func = data_transformer.set_store

        storage_funcs = [add_func, data_transformer.nothing]

        step_size = self.amount_keys()

        flipped_values_store = {} 
        self.transform_data(
            {}, flipped_values_store, storage_funcs, flip_func, step_size, 
            self.NO_JUMP, self.WANT_KEYS, self.DISCARD_OTHER_KEYS
        )
         
        return Data_Store(
            new_keys[0], self.config_handler, self.have_time_axis, 
            key_store=flipped_values_store
        )

    def create_data_store(self, key_store):
        return Data_Store(
            self.get_sub_keys(), self.config_handler, self.have_time_axis,
            key_store = key_store
        )

    def keys(self):
        return data_transformer.get_key_store(self.key_store, keys=True)

    def amount_keys(self):
        return len(self.keys())

    def amount_sub_stores(self):
        return self.count_sub_keys

    def get_key_store(self, keys=False, values=False, items=False):
        return data_transformer.get_key_store(
            self.key_store, keys=keys, values=values, items=items
        )

    def get_sub_keys(self):
        return self.sub_keys
    
    def do_func_on_axis_names(self, target, axis_func, store_func):
        sub_store = list(self.get_key_store(values = True))[0]

        for axis_store in sub_store.values():
            axis_names = axis_func(axis_store) 
            store_func(target, axis_names)
    
    def all_axis_names(self):
        axis_names_list = [] 
        append_func = data_transformer.list_append
        get_axis_func = Axis_Store.get_axis_names

        self.do_func_on_axis_names(axis_names_list, get_axis_func, append_func)
        return axis_names_list
 
    def all_axis_lengths(self):
        axis_lengths_list = [] 
        append_op_func = functools.partial(
            data_transformer.list_append_n_op, len
        )
        get_axis_func = Axis_Store.get_axis_names

        self.do_func_on_axis_names(
            axis_lengths_list, get_axis_func, append_op_func
        )
        return axis_lengths_list

    def time_axis(self):
        time_axis_list = [] 
        append_func = data_transformer.list_append
        get_func = Axis_Store.time_axis_list

        self.do_func_on_axis_names(time_axis_list, get_func, append_func)
        return time_axis_list 
    
    def add_all_to_key(self, key, values):
        add = self.axis_store_add
        add_missing = self.store_add_new_axis_store
        how_to_store = [add, add_missing]
        
        self.add_all_to_key_given_store(
            self.key_store, key, self.get_sub_keys(), values, how_to_store
        )

    def add_all_to_key_given_store(
        self, key_store, key, sub_keys, values, how_to_store
    ):
        if values: 
            if key in key_store:
                sub_store = key_store[key]
                
                for idx, sub_key in enumerate(sub_keys):
                    how_to_store[0](sub_store, sub_key, values[idx])
            else:
                new_sub_store = {}
                for idx, sub_key in enumerate(sub_keys):
                    how_to_store[1](new_sub_store, sub_key, values[idx])
                
                key_store[key] = new_sub_store

    def add_axis_stores(self, store, key, sub_keys, axis_stores):
        storage_function = data_transformer.set_store 
        how_to_store = [storage_function, storage_function]
        
        self.add_all_to_key_given_store(
            store, key, sub_keys, axis_stores, how_to_store
        )

    def drop(self, drop_amount, axis):
        drop_func = functools.partial(
            Axis_Store.drop, drop_amount=drop_amount, axis=axis
        )

        drop_store = self.dict_transformation(
            drop_func, self.STEP_SIZE_1, self.NO_JUMP
        )
        
        return self.create_data_store(drop_store) 

    def set_partition_size(self, max_amount_values_per_element):
        sub_keys = []
        modified_store = {}

        for idx, (key, sub_store) in enumerate(self.get_key_store(items = True)):
            for sub_key, axis_store in sub_store.items():
                partition_stores = axis_store.partition(
                    max_amount_values_per_element
                )
                
                partition_sub_keys = []
                partition_sub_keys = [
                    partition_store.get_title() 
                    for partition_store 
                    in partition_stores
                ]

                if idx == 1:
                    sub_keys += partition_sub_keys

                self.add_axis_stores(
                    modified_store, key, partition_sub_keys, partition_stores
                )

        new_data_handler = Data_Store(
            sub_keys, self.config_handler, self.have_time_axis,
            key_store = modified_store
        )
        return new_data_handler
    
    def set_same_length(self, axis, step_size = 2, step_size_max = False):
        add_func = data_transformer.set_store_many 
        reset_add = data_transformer.append_and_reset_store_many

        storage_funcs = [add_func, reset_add]

        same_size_func = functools.partial(
            Axis_Store.same_length_store, axis = axis
        )
        
        if step_size_max:
            step_size = self.amount_keys()

        same_length_store = {}
        storage_sub_dicts = [{} for _ in range(0, step_size)]
        self.transform_data(
            same_length_store, storage_sub_dicts, storage_funcs, same_size_func,
            step_size, self.NO_JUMP, self.WANT_KEYS, not self.DISCARD_OTHER_KEYS
        )
        
        return self.create_data_store(same_length_store)
   
    def drop_time(self):
        drop_func = Axis_Store.drop_time
        time_dropped_store = self.dict_transformation(
            drop_func, self.STEP_SIZE_1, self.NO_JUMP
        )

        return self.create_data_store(time_dropped_store)

    def reduce_if_empty(self):
        reduce_func = Axis_Store.reduce_if_empty
        reduced_store = self.dict_transformation(
            reduce_func, self.STEP_SIZE_1, self.NO_JUMP
        )

        return self.create_data_store(reduced_store)

    def reduce_at_pivot(self):
        reduce_func = Axis_Store.reduce_at_pivot
        reduced_store = self.dict_transformation(
            reduce_func, self.STEP_SIZE_1, self.NO_JUMP
        )

        return self.create_data_store(reduced_store)
    
    def means(self, axis, should_jump, step_size = 1, step_size_max = False):
        if step_size_max:
            amount_keys = self.amount_keys()
            step_size = amount_keys / 2 if should_jump else amount_keys

        mean_func = functools.partial(Axis_Store.mean_stores, axis = axis) 
        
        mean_dict = self.dict_transformation(mean_func, step_size, should_jump)
        mean_store = self.create_data_store(mean_dict)

        return mean_store 
    
    def stds(self, axis, should_jump, step_size = 1, step_size_max = False):
        if step_size_max:
            amount_keys = self.amount_keys()
            step_size = amount_keys / 2 if should_jump else amount_keys

        std_func = functools.partial(Axis_Store.std_stores, axis = axis)
        
        stds_dict  = self.dict_transformation(std_func, step_size, should_jump)
        stds_store = self.create_data_store(stds_dict)

        return stds_store 

    def subtract(self, axis):
        sub_func = functools.partial(
            Axis_Store.subtract_stores, auxiliary_axis = axis
        )

        sub_store = self.dict_transformation(
            sub_func, self.STEP_SIZE_2, self.NO_JUMP
        )
        
        return self.create_data_store(sub_store)

    def euclideans(self, functional_axis, auxiliary_axis, jump):
        euclidean_construct = Axis_Store.euclidean
        euclidean_func = functools.partial(
            euclidean_construct, functional_axis = functional_axis,
            auxiliary_axis = auxiliary_axis
        )

        euc_store = self.dict_transformation(
            euclidean_func, self.STEP_SIZE_2, jump
        )
        
        return self.create_data_store(euc_store)

    def list_transformtation(self, axis_func, step_size, should_jump, op = None):
        append_reset_func = data_transformer.append_and_reset_list
       
        if op is not None:
            append_func = functools.partial(
                data_transformer.list_append_n_op, op
            )
        else:
            append_func = data_transformer.list_append

        storage_funcs = [append_func, append_reset_func]
        
        values = []
        self.transform_data(
            values, [], storage_funcs, axis_func, step_size, should_jump, 
            not self.WANT_KEYS, self.DISCARD_OTHER_KEYS
        )
        
        return values
        
    ###Does not use op for anything as of now
    def dict_transformation(
        self, axis_func, step_size, should_jump, key_store = None, op = None
    ):
        add_func = data_transformer.set_store
        reset_func = data_transformer.append_and_reset_store

        storage_funcs = [add_func, reset_func]

        values = {} 
        self.transform_data(
            values, {}, storage_funcs, axis_func, step_size, should_jump,
            self.WANT_KEYS, self.DISCARD_OTHER_KEYS, key_store = key_store
        )
        
        return values

    def transform_data(
        self, storage_1, storage_2, storage_funcs, axis_func, step_size, 
        should_jump, want_keys, discard_other_keys, key_store = None
    ):
        if not key_store:
            key_store = self.get_key_store()

        data_transformer.transform_data_nested_store(
            key_store, storage_1, storage_2, storage_funcs, axis_func, 
            step_size, should_jump, want_keys, discard_other_keys
        )
