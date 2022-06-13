import copy
import unittest

import numpy as NP
from numpy import linalg as LA

from DataHandling import axis_store
from DataHandling.axis_store import Axis_Store

from Testing.DataHandling import dummy_config_handler

VALUES = [[[4, 2, 3], [1, 2, 3], [5, 7, 8]], [[4, 5, 6], [7, 8, 9], [9, 8, 3]]]
TIME_VALUES = [
    [[4, 2, 3, 1], [1, 2, 3, 2], [5, 7, 8, 3]],
    [[4, 5, 6, 1], [7, 8, 9, 2], [9, 8, 3, 3]]
]


AXIS_0 = 0

TITLE = "test1"
VALUES_BEFORE = [5, 4, 3, 5]
VALUES_AFTER = [[5, 4, 3, 5]]
STORE_HAVE_TIME_AXIS = False
TIME_AXIS = None
AMOUNT_ROWS = len(VALUES_AFTER)
PARTITION_LENGTH = 4
AXIS_NAMES = dummy_config_handler.AXIS_NAMES_1
INITIAL_NDIM = 2
NDIM = 2
PARAMETERS = [
    TITLE, VALUES_AFTER, STORE_HAVE_TIME_AXIS, TIME_AXIS, PARTITION_LENGTH,
    AXIS_NAMES, INITIAL_NDIM, NDIM
]
CALL_NAMES_INIT = [
    "title_key", "values", "have_time_axis", "time_axis", "partition_length",
    "axis_names", "initial_ndim", "ndim"
] 

NO_TIME_AXIS = NO_REDUCE = False
REDUCE = HAVE_TIME_AXIS = True

class Test_Axis_Store(unittest.TestCase):
       
    def make_2_stores(self):
        value_1_start = [3, 4, 5]
        value_2_start = [6, 7, 8]
        
        axis_store_1 = Axis_Store(TITLE, value_1_start, NO_TIME_AXIS)
        axis_store_2 = Axis_Store(TITLE, value_2_start, NO_TIME_AXIS)

        value_both = [2, 2, 2]
        axis_store_1.add(value_both)
        axis_store_2.add(value_both)
        
        return axis_store_1, axis_store_2

    def make_3_stores(self):
        values_1 = VALUES_AFTER  
        values_2 = [9, 8, 2, 3]
        values_3 = [4, 5, 6, 7]
        
        axis_store_1 = self.axis_store
        axis_store_2 = Axis_Store("test_mean_store", values_2, NO_TIME_AXIS)
        axis_store_3 = Axis_Store("test_mean_store", values_3, NO_TIME_AXIS)
        
        v1_v2 = NP.append(values_1, [values_2], axis = 0)
        v1_v2_v3 = NP.append(v1_v2, [values_3], axis = 0).tolist()

        stores = [axis_store_1, axis_store_2, axis_store_3]

        return v1_v2_v3, stores
    
    def make_axis_stores(self, values_start, values_add):
        axis_stores = []
        values = []

        for next_values in values_add:
            new_axis_store = Axis_Store(
                TITLE, values_start, NO_TIME_AXIS, axis_names = AXIS_NAMES
            )
            new_axis_store.add_all(next_values, AXIS_0)

            axis_stores.append(new_axis_store)

            next_insert_value = copy.copy(next_values) 
            next_insert_value.insert(0, values_start)

            values.append(next_insert_value)

        values.insert(0, VALUES_AFTER)
        return axis_stores, values
    
    def check_all_stores_equal_to_range_in_values(self, values_add, stores, expected_range):
        for idx, next_values in enumerate(values_add):
            next_store = stores[idx]
            
            expected_values = NP.array(next_values)[0 : expected_range].tolist()
            self.assertEqual(next_store.values_list(NO_TIME_AXIS, NO_REDUCE), expected_values)

    def setUp(self):
        self.axis_store = Axis_Store(
            TITLE, VALUES_BEFORE, NO_TIME_AXIS,
            partition_length = PARTITION_LENGTH, axis_names = AXIS_NAMES
        )
        self.time_store = Axis_Store("time_store", TIME_VALUES, HAVE_TIME_AXIS)

    ###NON class tests
    def test_reshape(self):
        ndmin = self.axis_store.all_parameters()["ndim"]
        v1 = [1, 4, 5]
        expected_1 = [[1, 4, 5]]

        found_value_1 = axis_store.reshape(v1, ndmin).tolist()

        self.assertEqual(found_value_1, expected_1)
        
        v2 = [[1, 3, 10]]
        expected_2 = [[1, 3, 10]]
        
        found_value_2 = axis_store.reshape(v2, ndmin).tolist()

        self.assertEqual(found_value_2, expected_2)

        v3 = 1
        expected_3 = [[1]]

        found_value_3 = axis_store.reshape(v3, ndmin).tolist()

        self.assertEqual(found_value_3, expected_3)

    ###class tests
    def test_create_new_axis_store(self):
        axis = 1

        new_values = NP.array([[3, 4], [5, 6]]) 
        new_axis_store = self.axis_store.create_new_axis_store(new_values, axis = axis)
        
        expected_values = new_values.tolist()
        found_values = new_axis_store.values_list(NO_TIME_AXIS, NO_REDUCE)
        self.assertEqual(found_values, expected_values)
    
    def test_create_new_axis_store_reshape(self):
        axis_store = Axis_Store(TITLE, 1, NO_TIME_AXIS, axis_names = AXIS_NAMES)
        axis = 1
        through_list = False

        new_values = NP.array([3, 4]) 
        new_axis_store = axis_store.create_new_axis_store(new_values, axis = axis)
        
        expected_values = NP.reshape(new_values, (2, 1)).tolist()
        found_values = new_axis_store.values_numpy(through_list).tolist()
        self.assertEqual(found_values, expected_values)
    
    def test_get_title(self):
       found_title = self.axis_store.get_title()

       self.assertEqual(found_title, TITLE)
    
    def test_values_append(self):
        values, stores = self.make_3_stores()

        expected_values = [[values[0]], [values[1]], [values[2]]]
        
        append_store = stores[0].values_append(stores[1], stores[2], reduce_dim = False)
        found_values = append_store.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertEqual(found_values, expected_values)

    def test_values_append_reduce(self):
        expected_values, stores = self.make_3_stores()

        append_store = stores[0].values_append(stores[1], stores[2], reduce_dim = True)
        found_values = append_store.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertEqual(found_values, expected_values)

    def test_values_numpy(self):
        through_list = True
        found_values = self.axis_store.values_numpy(through_list)
       
        self.assertEqual(found_values.tolist(), VALUES_AFTER)
               
    def test_values_list(self):
        found = self.axis_store.values_list(NO_TIME_AXIS, NO_REDUCE)
       
        self.assertEqual(found, VALUES_AFTER)

    def test_extract_time_axis(self):
        found_values, found_time = self.time_store.extract_time_axis(NP.array(TIME_VALUES))

        expected_values = VALUES 
        expected_time = [[[1], [2], [3]], [[1], [2], [3]]]
       
        self.assertEqual(found_values.tolist(), expected_values)
        self.assertEqual(found_time.tolist(), expected_time)

    def test_get_time_axis(self):
        found = self.time_store.time_axis_list()
        expected = [[1, 2, 3], [1, 2, 3]]
       
        self.assertEqual(found, expected)
        
        found = self.time_store.time_axis_numpy().tolist()
        expected = [[[[1], [2], [3]], [[1], [2], [3]]]]
        
        self.assertEqual(found, expected)

    def test_include_time_axis(self):
        expected_time = [TIME_VALUES] 
        found_time = self.time_store.include_time_axis().tolist()
       
        self.assertEqual(found_time, expected_time)
      
        no_time_store = self.time_store.drop_time()
        expected_no_time = [VALUES]
        
        found_no_time = no_time_store.include_time_axis().tolist()
        self.assertEqual(found_no_time, expected_no_time)

    def test_drop_time_axis(self):
        no_time_store = self.time_store.drop_time()

        found = no_time_store.time_axis_list()
        expected = None 
       
        self.assertEqual(found, expected)

    def test_values_list_reduce(self):
        expected = VALUES
        reduce_store = Axis_Store(
            "get_values_reduce", [[[expected]]], NO_TIME_AXIS
        )
        found = reduce_store.values_list(NO_TIME_AXIS, REDUCE)
       
        self.assertEqual(found, expected)

    def test_get_partition_length(self):
        found_partition_length = self.axis_store.get_partition_length()

        self.assertEqual(found_partition_length, PARTITION_LENGTH)

    def test_get_amount_rows(self):
        found_values_length = self.axis_store.get_amount_rows()
       
        self.assertEqual(found_values_length, AMOUNT_ROWS)

    def test_get_axis_names(self):
        found_axis_names = self.axis_store.get_axis_names()
        
        self.assertEqual(found_axis_names, AXIS_NAMES)

    def test_all_parameters(self):
        found_paramters = self.axis_store.all_parameters(numpy = False)
        
        found_parameter_keys = list(found_paramters.keys())
        found_parameter_values = list(found_paramters.values())

        self.assertCountEqual(found_parameter_keys, CALL_NAMES_INIT)
        self.assertCountEqual(found_parameter_values, PARAMETERS)

    def test_get_amount_columns(self):
        expected_columns = NP.shape(NP.array(VALUES_AFTER))[1]

        found_columns = self.axis_store.get_amount_columns()

        self.assertEqual(found_columns, expected_columns)

    def test_copy(self):
        old_parameters = self.axis_store.all_parameters()

        axis_store_copy = self.axis_store.copy()
        copy_parameters = axis_store_copy.all_parameters()

        self.assertEqual(copy_parameters, old_parameters)

        old_values = self.axis_store.values_list(NO_TIME_AXIS, NO_REDUCE)
        axis_store_copy.add([4, 3, 2, 20])

        copy_values = axis_store_copy.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertNotEqual(copy_values, old_values)
   
    def test_drop(self):
        drop_amount_1, drop_amount_2, axis_1, axis_2 = 1, 2, 1, 2

        expected_ax_0 = [[4, 5, 6, 1], [7, 8, 9, 2], [9, 8, 3, 3]]
        found_ax_0 = (
            self
            .time_store
            .drop(drop_amount_1, AXIS_0 + 1)
            .values_list(REDUCE, HAVE_TIME_AXIS)
        ) 

        self.assertEqual(found_ax_0, expected_ax_0)
        
        expected_ax_1 = [[5, 7, 8, 3], [9, 8, 3, 3]]

        found_ax_1 = (
            self
            .time_store
            .drop(drop_amount_2, axis_1 + 1)
            .values_list(REDUCE, HAVE_TIME_AXIS)
        )
        
        self.assertEqual(found_ax_1, expected_ax_1)
        
        expected_ax_2 = [[[3, 1], [3, 2], [8, 3]], [[6, 1], [9, 2], [3, 3]]]
        found_ax_2 = (
            self
            .time_store
            .drop(drop_amount_2, axis_2 + 1)
            .values_list(REDUCE, HAVE_TIME_AXIS)
        )

        self.assertEqual(found_ax_2, expected_ax_2)

    def test_reduce_if_empty(self):
        expected_values = VALUES_AFTER
        
        reduce_store = Axis_Store("test reduce", VALUES_AFTER, NO_TIME_AXIS)
        found_values = (
            reduce_store
            .reduce_if_empty()
            .values_list(NO_TIME_AXIS, NO_REDUCE)
        )
        
        self.assertEqual(found_values, expected_values)

    def test_reduce_if_empty_deep(self):
        values = VALUES

        reduce_store = Axis_Store("reduce_store", [[values]], NO_TIME_AXIS)
        expected = [values]
        
        found = reduce_store.reduce_if_empty().values_list(NO_TIME_AXIS, NO_REDUCE)
        
        self.assertEqual(found, expected)

    def test_reduce(self):
        values = [VALUES]
        
        reduce_store = Axis_Store("reduce_store", values, NO_TIME_AXIS)
        expected = [[[4, 2, 3], [1, 2, 3], [5, 7, 8], [4, 5, 6], [7, 8, 9], [9, 8, 3]]]
        
        found = reduce_store.reduce_at_pivot().values_list(NO_TIME_AXIS, NO_REDUCE)
        
        self.assertEqual(found, expected)

    def test_reduce_time_axis(self):
        expected_values = [[[4, 2, 3], [1, 2, 3], [5, 7, 8], [4, 5, 6], [7, 8, 9], [9, 8, 3]]]
        expected_times = [[[1], [2], [3], [4], [5], [6]]]
        
        reduced_store = self.time_store.reduce_at_pivot()
        
        found_values = reduced_store.values_list(NO_TIME_AXIS, NO_REDUCE)
        found_times = reduced_store.time_axis_numpy().tolist()

        self.assertEqual(found_values, expected_values)
        self.assertEqual(found_times, expected_times)

    def test_add(self):
        axis_store = Axis_Store("test_add", 4, NO_TIME_AXIS)
        
        axis_store.add(10)
        expected_values_1 = [4, 10]

        found_values_1 = axis_store.values_list(NO_TIME_AXIS, NO_REDUCE)
        self.assertCountEqual(found_values_1, expected_values_1)
        
        new_l = [4, 3, 2, 20, 50, 70]
        self.axis_store.add(new_l)

        added_values_expected = [4, 3, 2, 20]
        expected_values_2 = copy.copy(VALUES_AFTER)
        expected_values_2.append(added_values_expected)

        found_values_2 = self.axis_store.values_list(NO_TIME_AXIS, NO_REDUCE)
        self.assertCountEqual(found_values_2, expected_values_2)
    
    def test_add_all(self):
        axis_store = Axis_Store("test_add_all", 4, NO_TIME_AXIS)

        axis_store.add_all([10, 4, 5, 6], AXIS_0)
        expected_values = [4, 10, 4, 5, 6]

        found_values = axis_store.values_list(NO_TIME_AXIS, NO_REDUCE)
        self.assertCountEqual(found_values, expected_values)
       
    def test_add_stores(self):
        expected_values, stores = self.make_3_stores()

        other_stores = stores[1 : 3]

        added_store = stores[0].add_stores(other_stores)
       
        found_values = added_store.values_list(NO_TIME_AXIS, NO_REDUCE)
        self.assertCountEqual(found_values, expected_values)
    
    def test_assigns_axis_values_from_config_handler(self):
        axis_store_1 = Axis_Store(TITLE, VALUES_BEFORE, NO_TIME_AXIS, config_handler = dummy_config_handler)
        axis_names_1 = axis_store_1.get_axis_names()
        
        self.assertEqual(axis_names_1, AXIS_NAMES)

        axis_store_2 = Axis_Store("test2", VALUES_BEFORE, NO_TIME_AXIS, config_handler = dummy_config_handler)
        axis_names_2 = axis_store_2.get_axis_names()

        self.assertEqual(axis_names_2, dummy_config_handler.AXIS_NAMES_2)

    def test_same_length(self):
        expected_range = 1

        values_start = [20, 40, 9, 8]
        values_add = [[[30, 60, 7, 6], [9, 2, 1, 0]]]

        axis_stores_send, values_fixed = self.make_axis_stores(values_start, values_add)

        axis_stores_found = self.axis_store.same_length_store(*axis_stores_send, axis = AXIS_0)
        self.check_all_stores_equal_to_range_in_values(values_fixed, axis_stores_found, expected_range)
    
    def test_same_length_4D(self):
        value_1 = VALUES
        value_2 = [[[4, 2, 3], [3, 2, 1]], [[-4, -5, -6], [1, 0, -1]]]
        
        expected_1 = [[[[4, 2, 3], [1, 2, 3]], [[4, 5, 6], [7, 8, 9]]]]
        expected_2 = [[[[4, 2, 3], [3, 2, 1]], [[-4, -5, -6], [1, 0, -1]]]]

        store_1 = Axis_Store("4D", value_1, NO_TIME_AXIS)
        store_2 = Axis_Store("4D", value_2, NO_TIME_AXIS)
        store_3 = Axis_Store("4D", value_1, NO_TIME_AXIS)

        axis_stores_found = store_1.same_length_store(store_2, store_3, axis = 2)

        self.assertEqual(axis_stores_found[0].values_list(NO_TIME_AXIS, NO_REDUCE), expected_1)
        self.assertEqual(axis_stores_found[1].values_list(NO_TIME_AXIS, NO_REDUCE), expected_2)
        self.assertEqual(axis_stores_found[2].values_list(NO_TIME_AXIS, NO_REDUCE), expected_1)
    
    def test_same_length_time_axis(self):
        value_1 = [[[4, 2, 3, 1], [1, 2, 3, 2], [5, 7, 8, 3]], [[4, 5, 6, 4], [7, 8, 9, 5], [9, 8, 3, 6]]]
        value_2 = [[[4, 2, 3, 7], [3, 2, 1, 8]], [[-4, -5, -6, 9], [1, 0, -1, 10]]]
        
        expected_values_1 = [[[[4, 2, 3], [1, 2, 3]], [[4, 5, 6], [7, 8, 9]]]]
        expected_values_2 = [[[[4, 2, 3], [3, 2, 1]], [[-4, -5, -6], [1, 0, -1]]]]
        
        expected_time_1 = [[[[1], [2]], [[4], [5]]]]
        expected_time_2 = [[[[7], [8]], [[9], [10]]]]

        store_1 = Axis_Store("4D", value_1, HAVE_TIME_AXIS) 
        store_2 = Axis_Store("4D", value_2, HAVE_TIME_AXIS)

        axis_stores_found = store_1.same_length_store(store_2, axis = 2)

        self.assertEqual(axis_stores_found[0].values_list(NO_TIME_AXIS, NO_REDUCE), expected_values_1)
        self.assertEqual(axis_stores_found[1].values_list(NO_TIME_AXIS, NO_REDUCE), expected_values_2)
        
        self.assertEqual(axis_stores_found[0].time_axis_numpy().tolist(), expected_time_1)
        self.assertEqual(axis_stores_found[1].time_axis_numpy().tolist(), expected_time_2)

    def test_same_length_multi(self):
        expected_range = 1

        values_start = [20, 40, 9, 8]
        v_add_1 = [[30, 60, 7, 6], [9, 2, 1, 0]]
        v_add_2 = [[30, 60, 7, 6], [9, 2, 1, 0], [4, 5, 6, 7]]
        v_add_3 = [[30, 60, 7, 6]]
        v_add_4 = [[30, 60, 7, 6], [9, 2, 1, 0], [1, 2, 3 ,4], [5, 6, 7, 8]]
        v_add_5 = [[30, 60, 7, 6], [9, 2, 1, 0]]

        values_add = [v_add_1, v_add_2, v_add_3, v_add_4, v_add_5]
        axis_stores_send, values_fixed = self.make_axis_stores(values_start, values_add)

        axis_stores_found = self.axis_store.same_length_store(*axis_stores_send, axis = AXIS_0)
        self.check_all_stores_equal_to_range_in_values(values_fixed, axis_stores_found, expected_range)
    
    def test_partition(self):
        values_2 = [1, 2, 3, 4]
        self.axis_store.add(values_2)

        partition_size = 3
        partition_stores = self.axis_store.partition(partition_size)

        expected_partions = 2
        self.assertEqual(len(partition_stores), expected_partions)

        expected_values_1 = [[5, 4, 3], [1, 2, 3]]
        expected_values_2 = [[4, 3, 5], [2, 3, 4]]

        store_1 = partition_stores[0]
        store_2 = partition_stores[1]

        found_values_1 = store_1.values_list(NO_TIME_AXIS, NO_REDUCE)
        found_values_2 = store_2.values_list(NO_TIME_AXIS, NO_REDUCE)
        
        self.assertCountEqual(found_values_1, expected_values_1)
        self.assertCountEqual(found_values_2, expected_values_2)

        expected_title_1 = TITLE + "_0"
        expected_title_2 = TITLE + "_1"

        found_title_1 = store_1.get_title()
        found_title_2 = store_2.get_title()

        self.assertEqual(found_title_1, expected_title_1)
        self.assertEqual(found_title_2, expected_title_2)

        found_expected_axis_names_1 = ["1", "2", "3"]
        found_expected_axis_names_2 = ["2", "3", "4"]

        found_axis_names_1 = store_1.get_axis_names()
        found_axis_names_2 = store_2.get_axis_names()

        self.assertEqual(found_axis_names_1, found_expected_axis_names_1)
        self.assertEqual(found_axis_names_2, found_expected_axis_names_2)
    
    def test_subtract(self):
        axis_store_1, axis_store_2 = self.make_2_stores()

        value_1 = [[3, 4, 5], [2, 2, 2]]
        value_2 = [[6, 7, 8], [2, 2, 2]]

        expected_manhattan = (NP.array(value_1) - NP.array(value_2)).tolist()
        
        found_manhattan = axis_store_1.subtract(axis_store_2, AXIS_0).tolist()
        self.assertEqual(found_manhattan, expected_manhattan)
        
    def test_subtract_stores(self):
        axis_store_1, axis_store_2 = self.make_2_stores()
        
        value_1 = [[3, 4, 5], [2, 2, 2]]
        value_2 = [[6, 7, 8], [2, 2, 2]]

        expected_manhattan = (NP.array(value_1) - NP.array(value_2)).tolist()
        
        manhattan_store = axis_store_1.subtract_stores(axis_store_2, AXIS_0)
        found_manhattan = manhattan_store.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertEqual(found_manhattan, expected_manhattan)
    
    def test_euclidean_axis_0(self):
        axis_store_1, axis_store_2 = self.make_2_stores()

        value_1 = [[3, 4, 5], [2, 2, 2]]
        value_2 = [[6, 7, 8], [2, 2, 2]]

        expected_euclidean = [LA.norm(NP.array(value_1) - NP.array(value_2), axis = AXIS_0).tolist()]
        
        euclidean_store = axis_store_1.euclidean(axis_store_2, AXIS_0, AXIS_0)
        found_euclidean = euclidean_store.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertEqual(found_euclidean, expected_euclidean)

    def test_euclidean_axis_1(self):
        axis = 1
        
        axis_store_1, axis_store_2 = self.make_2_stores()

        value_1 = [[3, 4, 5], [2, 2, 2]]
        value_2 = [[6, 7, 8], [2, 2, 2]]
        
        expected_euclidean = [LA.norm(NP.array(value_1) - NP.array(value_2), axis = axis).tolist()]
        
        euclidean_store = axis_store_1.euclidean(axis_store_2, axis, AXIS_0)
        found_euclidean = euclidean_store.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertEqual(found_euclidean, expected_euclidean)
        
    def test_mean(self):
        expected_mean = [NP.mean(VALUES_AFTER, axis = AXIS_0).tolist()]
        found_mean = self.axis_store.mean(AXIS_0)

        self.assertEqual(found_mean, expected_mean)

    def test_mean_stores(self):
        v1_v2_v3, stores = self.make_3_stores()
        expected_means = [NP.mean(v1_v2_v3, axis = 0).tolist()]

        other_stores = stores[1 : 3]

        mean_store = stores[0].mean_stores(*other_stores, axis = AXIS_0)
        found_means = mean_store.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertEqual(found_means, expected_means)

    def test_mean_stores_4D(self):
        value_1 = [[[4, 2, 3], [1, 2, 3]], [[4, 5, 6], [7, 8, 9]]]
        value_2 = [[[4, 2, 3], [3, 2, 1]], [[-4, -5, -6], [1, 0, -1]]]

        expected_means = [[[[4, 2, 3], [2, 2, 2]], [[0, 0, 0], [4, 4, 4]]]]

        store_1 = Axis_Store("4D", value_1, NO_TIME_AXIS)
        store_2 = Axis_Store("4D", value_2, NO_TIME_AXIS)

        mean_store = store_1.mean_stores(store_2, axis = AXIS_0)
        found_means = mean_store.values_list(NO_TIME_AXIS, NO_REDUCE)

        self.assertEqual(found_means, expected_means)

    def test_std(self):
        axis = 0

        expected_std = [NP.std(VALUES_AFTER, axis = axis).tolist()]
        found_std = self.axis_store.std(axis)

        self.assertEqual(found_std , expected_std)
    
    def test_std_stores(self):
        v1_v2_v3, stores = self.make_3_stores()
        expected_stds = [NP.std(v1_v2_v3, axis = 0).tolist()]

        other_stores = stores[1 : 3]

        std_store = stores[0].std_stores(*other_stores, axis = AXIS_0)
        found_stds = std_store.values_list(NO_TIME_AXIS, NO_REDUCE) 

        self.assertEqual(found_stds, expected_stds)
 
if __name__ == '__main__':
    unittest.main()
