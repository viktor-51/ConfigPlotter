import sys
import copy

import numpy as NP
from numpy import linalg as LA 

def shape_or_1(value):
    ndim  = NP.ndim(value)

    shape = NP.shape(value)
    if shape:
        partition_length = shape[ndim - 1]
        rows = shape[0]

        if len(shape) > 1:
            columns = shape[1]
            return rows, columns, partition_length
        else:
            return rows, 1, partition_length
    else:
        return 1, 1, 1
        
def append_lists_into_list(target, source):
    for idx, list_slot in enumerate(target):
        list_slot.append(source[idx])

def reshape(values, ndmin):
    return NP.array(values, ndmin = ndmin)

def handle_multi_3dim(
    ndim, current_partition_size, list_of_values,
    requested_partition_size, base_name, axis_names
):
    if ndim == 3:
        shape = list_of_values.shape

        partioned_values = []
        for idx, next_list in enumerate(list_of_values):
            next_value = handle_partition(
                current_partition_size, next_list, requested_partition_size,
                base_name, axis_names
            )

            if next_value != None:
                next_partition, axis_names_partitioned, partition_names = next_value 
                partioned_values.append(next_partition)
            else:
                return None

        return NP.array(partioned_values), axis_names_partitioned, partition_names
    else:
        return handle_partition(current_partition_size, list_of_values, requested_partition_size, base_name, axis_names)

def handle_partition(current_partition_size, list_of_values, requested_partition_size, base_name, axis_names):
    start = 0
    first_value = list_of_values[0]

    len_values = len(list_of_values)
    amount_partitions = current_partition_size - requested_partition_size + 1

    if amount_partitions > 1:
        start += 1
        all_partitions = NP.zeros((len_values, amount_partitions, requested_partition_size))

        partitions, axis_names_partitioned, partition_names = partition_fit(
            first_value, requested_partition_size, base_name = base_name,
            axis_names = axis_names
        )
        all_partitions[0, :, :] = partitions
    else:
        return None

    for idx in range(start, len_values):
        values = list_of_values[idx]

        partitions = partition_fit(values, requested_partition_size)
        all_partitions[idx, :, :] = partitions

    return all_partitions, axis_names_partitioned, partition_names

def partition_fit(elements, partition_size, base_name = None, axis_names = None):
    axis_names_partitioned = []
    partition_names = []

    steps = len(elements) - partition_size + 1
    generate_names = base_name and axis_names

    partitions = NP.zeros((steps, partition_size))


    for start in range(0, steps):
        stop = start + partition_size

        partitions[start, :] = elements[start : stop]
        
        if generate_names:
            axis_name_partition = axis_names[start : stop]
            axis_names_partitioned.append(axis_name_partition)

            partition_names.append(base_name + "_" + str(start))
    
    if generate_names:
        return partitions, axis_names_partitioned, partition_names
    else:
        return partitions

class Axis_Store:
    MINIMUM_NDIM = 2
    CLASS_TYPE = "axis store"
    THROUGH_LIST = True 
    NO_TIME_AXIS = NO_REDUCE = NOT_THROUGH_LIST = False
    AXIS_0, AXIS_1 = 0, 1
    
    TRUTH_STATMENT = {type(None) : 0, int : 1}

    def __init__(
        self, title_key, given_values, have_time_axis, time_axis = None, 
        partition_length = None, config_handler = None, axis_names = None, 
        initial_ndim = None, ndim = None
    ):
        self.title_key = title_key
            
        suggested_initial_ndim = NP.array(given_values).ndim
        wanted_ndim = suggested_initial_ndim + 1

        suggested_ndim = max(wanted_ndim, self.MINIMUM_NDIM)
        
        assignment_map_ndim = {0 : [wanted_ndim, suggested_ndim], 1 : [ndim, ndim], 2 : [initial_ndim, ndim]}
        
        assignment_value = self.TRUTH_STATMENT[type(initial_ndim)] + self.TRUTH_STATMENT[type(ndim)] 
        self.initial_ndim, self.ndim = assignment_map_ndim[assignment_value]

        reshaped_values = reshape(given_values, self.ndim) 

        if have_time_axis:
            self.values, self.time_axis = self.extract_time_axis(reshaped_values)
        else:
            self.values, self.time_axis = reshaped_values, time_axis

        self.amount_rows, self.amount_columns, self.partition_length = shape_or_1(self.values)

        if partition_length:
            self.partition_length = partition_length 

        if axis_names:
            self.axis_names = axis_names
        elif config_handler:
            self.axis_names = config_handler.get_axis_names(title_key)
        else:
            self.axis_names = None

    ###Overrides
    def __str__(self):
        include_time = True
        string = (
            self.CLASS_TYPE 
            + " : " 
            + str(self.values_list(include_time, self.NO_REDUCE)) 
        )

        return string

    def get_title(self):
        return self.title_key

    def values_numpy(self, through_list):
        if through_list:
            found_list = self.__values_list(self.values)
            return NP.array(found_list)
        else:
            return self.values

    def values_list(self, include_time, reduce_if_empty):
        
        if include_time:
            values = self.include_time_axis()
        else:
            values = self.values

        if reduce_if_empty:
            keep_struct = False
            
            values, _, _ = self.__flatten_if_empty(
                values, keep_struct
            )

        return self.__values_list(values)

    def __values_list(self, values):
        initial_ndim = True
        shape_len = len(values.shape)

        if shape_len > 1 and self.get_ndim(initial_ndim = initial_ndim) == 1:
            return values[:, 0].tolist()
        else:
            return values.tolist()
   
    def time_axis_numpy(self):
        return self.time_axis

    def time_axis_list(self):
        time_axis = self.time_axis_numpy()

        if time_axis is None:
            return None
        else: 
            flattened_axis, _, _ = self.__flatten_if_empty(time_axis, keep_struct = False)
            return flattened_axis.tolist()

    def get_partition_length(self):
        return self.partition_length

    def get_amount_rows(self):
        return self.amount_rows
    
    def get_axis_names(self):
        return self.axis_names
   
    def get_amount_columns(self):
        return self.amount_columns

    def get_ndim(self, initial_ndim = False):
        if initial_ndim:
            return self.initial_ndim
        else:
            return self.ndim

    def shape(self):
        return self.values_numpy(self.NOT_THROUGH_LIST).shape
   
    def extract_time_axis(self, time_and_values):
        shape = time_and_values.shape 
        
        last_index = len(shape) - 1 
        last_index_size = shape[-1] - 1

        values = NP.take(time_and_values, NP.arange(0, last_index_size), axis = last_index)
        time_axis = NP.take(time_and_values, [last_index_size], axis = last_index)
        
        return values, time_axis 

    def include_time_axis(self):
        values = self.values_numpy(self.NOT_THROUGH_LIST)
        time_axis = self.time_axis_numpy()
        
        if time_axis is None:
            return values 
        else:
            return self.merge_values_last_axis(values, time_axis)

    def merge_values_last_axis(self, target, source):
            last_idx = len(target.shape) - 1

            merged_values = NP.append(target, source, axis = last_idx)
            return merged_values 

    def drop_time(self):
        old_parameters = self.all_parameters(
            name_constructor_compatible = True, numpy = True
        )
        old_parameters["time_axis"] = None

        return Axis_Store(**old_parameters)

    def reduce_if_empty(self, keep_struct = True):
        new_values, reduction, try_include_time = self.__flatten_if_empty(
            self.include_time_axis(), keep_struct
        )

        return self.create_new_axis_store(
            new_values, self.AXIS_0, try_include_time_axis = try_include_time,
            reduce_ndim = reduction 
        )

    def __flatten_if_empty(self, values, keep_struct = True):
        try_include_time = False
        shape = values.shape
        shape_len = len(shape)

        if 0 in shape:
            reduction = shape_len - 1
            return NP.array([]), reduction, try_include_time
        
        try_include_time = True
        new_values = NP.squeeze(values)
        len_new_shape = len(new_values.shape)

        reduction = shape_len - len_new_shape

        should_restore = False
        if keep_struct:
            found_1 = False
            for next_shape in shape:
                if found_1 and next_shape != 1:
                    should_restore = True
                elif next_shape != 1:
                    break
                else:
                    found_1 = True

            if should_restore: 
                new_values = NP.array([new_values])
                reduction -= 1 
        
        if len_new_shape == 0:
            new_values = NP.array([new_values])

        return new_values, reduction, try_include_time

    def reduce_at_pivot(self):
        include_time = False

        ndim_before = self.get_ndim()
        reduced_store = self.reduce_if_empty(keep_struct = False)
        ndim_after = reduced_store.get_ndim()
        
        if ndim_after <= self.MINIMUM_NDIM:
            return reduced_store

        values = reduced_store.values_numpy(self.NOT_THROUGH_LIST)
        time_axis = reduced_store.time_axis_numpy()
        
        shape = values.shape
        
        pivot_value = shape[0] * shape[1]
        
        new_shape = [pivot_value] + list(shape[2 :])
        
        new_values = NP.reshape(values, new_shape)
        dim_reduction = 0 if ndim_before > ndim_after else 1
        
        if time_axis is not None:
            include_time = True

            reduced_time_axis = self.reduce_time_axis(time_axis)
            new_values = self.merge_values_last_axis(new_values, reduced_time_axis)

        return reduced_store.create_new_axis_store(
            new_values, self.AXIS_0, try_include_time_axis = include_time, reduce_ndim = dim_reduction
        )

    def reduce_time_axis(self, time_axis):
        shape = time_axis.shape
        
        pivot_value = shape[0] * shape[1]
        new_shape = [pivot_value] + list(shape[2 :])

        last_value = 0
        reduced_time_axis = None 

        for idx, time_values in enumerate(time_axis):
            time_values += last_value

            if idx == 0:
                reduced_time_axis = time_values
            else:
                reduced_time_axis = NP.append(reduced_time_axis, time_values, axis = 0)

            last_value = time_values.flatten()[-1] 
        
        return reduced_time_axis    

    def create_new_axis_store(
        self, new_values, axis, try_include_time_axis=False, time_axis=None,
        reduce_ndim=None
    ):
        new_values = NP.array(new_values, ndmin = 2)

        amount_columns_current = self.get_amount_columns()
        ndim = self.get_ndim(initial_ndim = True) 

        new_length = new_values.shape[1]
        
        if amount_columns_current == 1 and axis == 1 and new_length > 1 and ndim == 1:
            new_values = NP.reshape(new_values, (new_length, 1))

        old_parameters = self.all_parameters(
            name_constructor_compatible = True, numpy = True
        )
        old_parameters["given_values"] = new_values 
        
        if try_include_time_axis:
            old_parameters["time_axis"] = None
            if self.time_axis_numpy() is None:
                old_parameters["have_time_axis"] = False
            else:
                old_parameters["have_time_axis"] = True
        else:
            if time_axis is not None:
                old_parameters["time_axis"] = time_axis
                old_parameters["have_time_axis"] = True

        if reduce_ndim is not None:
            old_parameters["ndim"] = max(2, old_parameters["ndim"] - reduce_ndim)

        return Axis_Store(**old_parameters)

    def all_parameters(self, name_constructor_compatible = False, numpy = False):
        if name_constructor_compatible:
            values_id = "given_values"
        else:
            values_id = "values"

        parameter_dict = {
            "title_key" : self.get_title(),
            "have_time_axis" : False,
            "time_axis" : self.time_axis_numpy(),
            "partition_length" : self.get_partition_length(),
            "axis_names" : self.get_axis_names(),
            "initial_ndim" : self.get_ndim(initial_ndim = True),
            "ndim" : self.get_ndim()
        }

        if numpy:
            parameter_dict[values_id] = (
                self
                .values_numpy(self.NOT_THROUGH_LIST).copy() 
            )
        else:
            parameter_dict[values_id] = (
                self
                .values_list(self.NO_TIME_AXIS, self.NO_REDUCE) 
            )

        return parameter_dict
    
    def copy(self):
        old_parameters = self.all_parameters(name_constructor_compatible = True, numpy = True)
        return Axis_Store(**old_parameters)

    def values_append(self, *other_stores, reduce_dim):
        stores = (self, ) + other_stores
        
        values = []
        for store in stores:
            next_value = store.values_list(self.NO_TIME_AXIS, self.NO_REDUCE)

            if reduce_dim:
                next_value = next_value[0]

            values.append(next_value)
        
        return self.create_new_axis_store(values, self.AXIS_0)

    def add(self, value):
        dim_adjusted_val = reshape(value, self.get_ndim())

        same_length_stores = self.same_length_store(
            self.create_new_axis_store(value, self.AXIS_1), axis = self.AXIS_1
        )

        values_source = same_length_stores[0].values_numpy(self.NOT_THROUGH_LIST)
        values_append = same_length_stores[1].values_numpy(self.NOT_THROUGH_LIST)
        
        new_values = NP.append(values_source, values_append, axis = self.AXIS_0)
        self.values = new_values

        self.amount_rows += 1

    def add_all(self, values, axis):
        for value in values:
            self.add(value)
    
    def add_stores(self, other_stores):
        new_store = self.copy()

        for store in other_stores:
            new_store.add(store.values_numpy(self.NOT_THROUGH_LIST))

        return new_store

    def drop(self, drop_amount, axis):
        values = self.include_time_axis()

        new_values = NP.delete(values, range(0, drop_amount), axis)
        return self.create_new_axis_store(new_values, axis, try_include_time_axis = True) 
        
    def partition(self, requested_partition_length):
        have_axis_store = False

        partition_succeeded = handle_multi_3dim(
            self.get_ndim(), self.get_partition_length(), self.values, requested_partition_length, self.title_key, self.axis_names
        )

        if partition_succeeded != None:
            partitions, axis_names_partitioned, partition_names = partition_succeeded 
        else:
            return [self] 

        axis_stores = []
        for idx, axis_names in enumerate(axis_names_partitioned):
            if self.get_ndim() == 3:
                list_idx = idx % self.get_amount_rows()
                values = partitions[list_idx, :, idx, :]
            else:
                values = partitions[:, idx, :]

            title_key = partition_names[idx]

            axis_store = Axis_Store(
                title_key, values, have_axis_store, partition_length = requested_partition_length,
                axis_names = axis_names, ndim = self.get_ndim()
            )
            axis_stores.append(axis_store)

        return axis_stores

    def same_length_store(self, *other_axis_stores, axis):
        other_axis_stores = list(other_axis_stores)
        other_axis_stores.insert(0, self)

        min_length_axis = -1
        for next_store in other_axis_stores:
            axis_length = next_store.shape()[axis]

            if min_length_axis == -1:
                min_length_axis = axis_length
            else:
                min_length_axis = min(min_length_axis, axis_length)
        
        new_axis_stores = []
        for next_store in other_axis_stores:
            indencies = NP.linspace(
                0, min_length_axis - 1, min_length_axis, dtype = "int64"
            )
            
            next_values = next_store.values_numpy(self.NOT_THROUGH_LIST)

            new_values = NP.take(next_values, indencies, axis = axis)
            
            new_axis_store = next_store.create_new_axis_store(new_values, axis)
            new_axis_stores.append(new_axis_store)

        return new_axis_stores

    def subtract(self, other_store, auxiliary_axis):
        store_1, store_2 = self.same_length_store(other_store, axis = auxiliary_axis)
        manhattan_values = store_1.values_numpy(self.NOT_THROUGH_LIST) - store_2.values_numpy(self.NOT_THROUGH_LIST)

        return manhattan_values
   
    def subtract_stores(self, other_store, auxiliary_axis):
        manhattan_values = self.subtract(other_store, auxiliary_axis)

        return self.create_new_axis_store(manhattan_values, auxiliary_axis) 

    def euclidean(self, other_store, functional_axis, auxiliary_axis):
        manhattan_values = self.subtract(other_store, auxiliary_axis)
        euclidean_values = LA.norm(manhattan_values, axis = functional_axis)

        return self.create_new_axis_store(euclidean_values, functional_axis)

    def mean(self, axis):
        values = NP.array(NP.mean(self.values_numpy(self.NOT_THROUGH_LIST), axis = axis), ndmin = 2)
        return self.__values_list(values)

    def mean_stores(self, *other_stores, axis):
        added_store = self.add_stores(other_stores)
        mean_values = added_store.mean(axis = axis)

        return self.create_new_axis_store(mean_values, axis)

    def std(self, axis):
        values = NP.array(NP.std(self.values_numpy(self.NOT_THROUGH_LIST), axis = axis), ndmin = 2)
        return self.__values_list(values)
    
    def std_stores(self, *other_stores, axis):
        added_store = self.add_stores(other_stores)
        std_values = added_store.std(axis = axis)
        
        return self.create_new_axis_store(std_values, axis)

