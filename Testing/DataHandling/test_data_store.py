import copy

import unittest

from tabulate import tabulate

import numpy as NP

from DataHandling.data_store import Data_Store 
from DataHandling.axis_store import Axis_Store

from Testing.DataHandling import dummy_config_handler

VALUE_2D_0 = [ 
    [[0, 2, 4, 6], [12, 2, 10, 2], [4, 2, 8, 2]],       
    [[10, 2], [4, 2]] 
]

VALUE_2D_1 = [  
    [[4, 2, 2, 0], [4, 2, 6, 8]],       
    [[6, 8], [4, 10], [2, 6]]
]

VALUE_2D_2 = [  
    [[4, 10, 6, 2], [6, 0, 2, 8], [8, 2, 10, 14]],       
    [[2, 2]]
]

VALUE_2D_3 = [ 
    [[0, 2, 4, 6], [12, 2, 10, 2], [4, 2, 8, 2]],       
    [[10, 2], [4, 2]] 
]

### Maybe one value to much for axis_names, but its the time axis not sure
VALUES_TIME_0 = [ 
    [
        [[0, 2, 4, 6, 1], [12, 2, 10, 2, 2]],
        [[12, 2, 10, 2, 1], [4, 2, 8, 2, 2]],
        [[4, 2, 8, 2, 1], [1, 9, 10, 8, 2]]
    ], 
    [[10, 2, 1], [4, 2, 1]] 
]

VALUES_TIME_1 = [ 
    [
        [[1, 3, 5, 7, 1], [13, 3, 11, 3, 2]],
        [[13, 3, 11, 3, 1], [5, 3, 9, 3, 2]],
        [[5, 3, 9, 3, 1], [2, 10, 11, 9, 2]]
    ],       
    [[11, 3, 1], [5, 3, 1]] 
]

VALUES_2D = [VALUE_2D_0, VALUE_2D_1, VALUE_2D_2, VALUE_2D_3]

LIMIT = 0.0000001

AMOUNT_SUB_STORES, MAX_PARTITION_SIZE = 2, 3
SUB_KEYS = list(dummy_config_handler.name_store.keys())[0 : 2]

value_from_key = {
    0 : [3, 4], 1 : [8, 9], 2 : [30, -20], 3 : [5, 5], 4 : [4, 5], 5 : [4, 1]
}
value_len = len(value_from_key)

AXIS_0 = 0
NO_FLATTEN = NO_REDUCE = NO_JUMP = NO_TIME_AXIS = False
JUMP = STEP_MAX = TIME_AXIS = REDUCE = True

class Test_Data_Store(unittest.TestCase):
    
    def get_value(self, key):
        return value_from_key[key]

    def get_value_double(self, key_1, wanted_length):
        step_size = 2
        key_2 = (key_1 + 1) % value_len

        values_1 = []
        values_2 = []
        runs = range(0, wanted_length, step_size)

        for _ in runs:
            values_1 = values_1 + value_from_key[key_1][0 : wanted_length]
            values_2 = values_2 + value_from_key[key_2][0 : wanted_length]
            wanted_length -= 2

        values = [values_1, values_2]
        return values

    def get_value_triple(self, key_1, wanted_length):
        step_size = 2
        key_2 = (key_1 + 1) % value_len
        key_3 = (key_1 + 2) % value_len

        values_1 = []
        values_2 = []
        values_3 = []
        runs = range(0, wanted_length, step_size)

        for _ in runs:
            values_1 = values_1 + value_from_key[key_1][0 : wanted_length]
            values_2 = values_2 + value_from_key[key_2][0 : wanted_length]
            values_3 = values_3 + value_from_key[key_3][0 : wanted_length]
            wanted_length -= 2

        values = [[values_1, values_2], [values_1, values_3]]
        return values

    def create_multi_store(self):
        data_store_multi = Data_Store(SUB_KEYS, dummy_config_handler, NO_TIME_AXIS)

        data_store_multi.add_all_to_key("0", VALUES_2D[0])
        data_store_multi.add_all_to_key("1", VALUES_2D[1])
        data_store_multi.add_all_to_key("2", VALUES_2D[2])
        data_store_multi.add_all_to_key("3", VALUES_2D[3])

        return data_store_multi

    def check_if_all_equal(self, found_values, expected_values):
        all_values_was_equal = True
        for idx_outer, next_found_list in enumerate(found_values):
            for idx_inner, next_found in enumerate(next_found_list):
                next_expected = expected_values[idx_outer][idx_inner]
                
                values_was_equal = (NP.abs(NP.subtract(next_found, next_expected)) < LIMIT).all()
                
                all_values_was_equal &= values_was_equal
        
        self.assertTrue(all_values_was_equal)

    def add_to_key_simple(self, keys, get_function, wanted_values = None, args = None):
        if not wanted_values:
            wanted_values = keys

        for idx, key in enumerate(keys):
            value_key = wanted_values[idx]
            
            if args:
                value = get_function(value_key, *args)
            else:
                value = get_function(value_key)

            self.data_store.add_all_to_key(key, value)

    def run_simple_two_keys(self):
        self.add_to_key_simple(["0", "1"], self.get_value, wanted_values = [0, 1])
    
    def run_simple_three_keys(self):
        self.add_to_key_simple(["0", "0", "1"], self.get_value, wanted_values = [0, 2, 1])

    def setUp(self):
        self.data_store = Data_Store(SUB_KEYS, dummy_config_handler, NO_TIME_AXIS)

        self.time_store = Data_Store(SUB_KEYS, dummy_config_handler, TIME_AXIS)
        self.time_store.add_all_to_key(0, VALUES_TIME_0)

    def test_keys(self):
        self.run_simple_two_keys()

        expected_keys = ["0", "1"]

        found_keys = self.data_store.keys()
        self.assertEqual(found_keys, expected_keys)

    def test_amount_sub_stores(self):
        found_amount_sub_stores = self.data_store.amount_sub_stores()
        expected_amount_sub_stores = AMOUNT_SUB_STORES

        self.assertEqual(found_amount_sub_stores, expected_amount_sub_stores)

    def test__str__(self):
        self.run_simple_two_keys()
        
        headers = ["sub_headers", "0", "1"]
        str_values = [["test1", [3], [8]], ["test2", [4], [9]]]
        expected_str = tabulate(str_values, headers = headers)
        
        found_str = str(self.data_store)
        
        self.assertEqual(found_str, expected_str)

    def test_get_sub_keys(self):
        self.run_simple_two_keys()
        
        expected_sub_keys = ["test1", "test2"]
        found_sub_keys = self.data_store.get_sub_keys()

        self.assertEqual(found_sub_keys, expected_sub_keys)
    
    def test_axis_names_easy(self):
        self.run_simple_two_keys()

        ax_names_1 = dummy_config_handler.AXIS_NAMES_1
        ax_names_2 = dummy_config_handler.AXIS_NAMES_2

        expected_axis_names = [ax_names_1, ax_names_2]  
        
        found_axis_names = self.data_store.all_axis_names()
        self.assertEqual(found_axis_names, expected_axis_names)
      
    def test_axis_partioned_easy(self):
        values_1 = [[4, 5, 6, 7], [8, 9]]
        values_1_1 = [[-1, -2, -3, -4], [-8, -9]]
        values_2 = [[1, 2, 3, 4], [5, 6]]

        self.data_store.add_all_to_key("0", values_1)
        self.data_store.add_all_to_key("0", values_1_1)
        self.data_store.add_all_to_key("1", values_2)

        ax_names_1 = dummy_config_handler.AXIS_NAMES_1
        ax_names_2 = dummy_config_handler.AXIS_NAMES_2

        partioned_names = [ax_names_1[0:3], ax_names_1[1:4], ax_names_2]  
        
        data_store_3 = self.data_store.set_partition_size(3)

        found_axis_names = data_store_3.all_axis_names()
        self.assertEqual(found_axis_names, partioned_names)

    def test_axis_lengths(self):
        self.run_simple_two_keys()

        ax_names_1 = dummy_config_handler.AXIS_NAMES_1
        ax_names_2 = dummy_config_handler.AXIS_NAMES_2

        expected_axis_lengths = [len(ax_names_1), len(ax_names_2)]  
        
        found_axis_lengths = self.data_store.all_axis_lengths()
        self.assertEqual(found_axis_lengths, expected_axis_lengths)
      
    def test_axis_partioned_hard(self):
        data_store_more_axis = Data_Store(list(dummy_config_handler.name_store.keys()), dummy_config_handler, NO_TIME_AXIS)

        values_1 = [[4, 5, 6, 7], [8, 9], [10, 11, 12, 13, 14, 15]]
        values_1_1 = [[-1, -2, -3, -4], [-8, -9], [10, 11, 12, 13, 14, 15]]
        values_2 = [[1, 2, 3, 4], [5, 6], [10, 11, 12, 13, 14, 15]]

        data_store_more_axis.add_all_to_key("0", values_1)
        data_store_more_axis.add_all_to_key("0", values_1_1)
        data_store_more_axis.add_all_to_key("1", values_2)

        ax_names_1 = dummy_config_handler.AXIS_NAMES_1
        ax_names_2 = dummy_config_handler.AXIS_NAMES_2
        ax_names_3 = dummy_config_handler.AXIS_NAMES_3

        ax_names_3_partitioned = [ax_names_3[0:3], ax_names_3[1:4], ax_names_3[2:5], ax_names_3[3:6]]

        partioned_names = [ax_names_1[0:3], ax_names_1[1:4], ax_names_2] + ax_names_3_partitioned  
        
        data_store_3 = data_store_more_axis.set_partition_size(3)

        found_axis_names = data_store_3.all_axis_names()
        self.assertEqual(found_axis_names, partioned_names)

    def test_values(self):
        self.run_simple_two_keys()
        
        expected_values = [[[3], [4]], [[8], [9]]]

        found_values = self.data_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)

        self.assertEqual(found_values, expected_values)
    
    def test_time_axis(self):
        expected = [[[1, 2], [1, 2], [1, 2]], [1, 1]]
        found = self.time_store.time_axis()

        self.assertEqual(found, expected)
    
    def test_drop_time(self):
        expected = [None, None] 
        found = self.time_store.drop_time().time_axis()

        self.assertEqual(found, expected)
   
    def test_reduce_at_pivot(self):
        expected_values = [ 
            [[0, 2, 4, 6, 1], [12, 2, 10, 2, 2], [12, 2, 10, 2, 3], [4, 2, 8, 2, 4], [4, 2, 8, 2, 5], [1, 9, 10, 8, 6]],       
            [[10, 2, 1], [4, 2, 2]] 
        ]
        expected_time = [[1, 2, 3, 4, 5, 6], [1, 1]]
       
        reduced_store = self.time_store.reduce_at_pivot()
        
        found_values = reduced_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        found_time = reduced_store.time_axis()

        self.assertEqual(found_time, expected_time)

    def test_flip_order_one_store(self):
        
        self.add_to_key_simple(["0", "0"], self.get_value, wanted_values = [0, 2])

        expected_keys = SUB_KEYS 
        expected_sub_keys = [0]

        ### Flip performed on : [[[[3], [30]], [[4], [-20]]]]
        expected_values = [[[3, 30]], [[4, -20]]]
        flipped_store = self.data_store.flip_order()
        
        found_keys = flipped_store.get_key_store(keys = True)
        found_sub_keys = flipped_store.get_sub_keys()
        found_values = flipped_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)

        self.assertEqual(found_keys, expected_keys)
        self.assertEqual(found_sub_keys, expected_sub_keys)
        self.assertEqual(found_values, expected_values)

    def test_flip_order(self):
        self.run_simple_three_keys()

        expected_keys = SUB_KEYS 
        expected_sub_keys = [0, 1]
        ### Flip performed on : [[[[3], [30]], [[4], [-20]]], [[[8]], [[9]]]]
        expected_values = [[[3, 30], [8]], [[4, -20], [9]]]
        
        flipped_store = self.data_store.flip_order()

        found_keys = flipped_store.get_key_store(keys = True)
        found_sub_keys = flipped_store.get_sub_keys()
        found_values = flipped_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)

        self.assertEqual(found_keys, expected_keys)
        self.assertEqual(found_sub_keys, expected_sub_keys)
        self.assertEqual(found_values, expected_values)

    def test_flatten(self):
        values = [[[[[5, 4, 3]]]], [[[[6, 7, 8]]]]]
        data_store = Data_Store(SUB_KEYS, dummy_config_handler, NO_TIME_AXIS)
        data_store.add_all_to_key(0, values)

        expected = [[[[5, 4, 3]], [[6, 7, 8]]]]
        flatten_store = data_store.reduce_if_empty() 

        found = flatten_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN) 

        self.assertEqual(found, expected)
    
    def test_flip_flatten(self):
        values_1 = [[[[[5, 4, 3]]]], [[[[6, 7, 8]]]]]
        values_2 = [[[[[3, 2, 1]]]], [[[[9, 8, 7]]]]]
        data_store = Data_Store(SUB_KEYS, dummy_config_handler, NO_TIME_AXIS)
        data_store.add_all_to_key(0, values_1)
        data_store.add_all_to_key(1, values_2)

        expected_1 = [[[5, 4, 3]], [[3, 2, 1]]]
        expected_2 = [[[6, 7, 8]], [[9, 8, 7]]]

        expected = [expected_1, expected_2]
        flatten_flip_store = data_store.reduce_if_empty().flip_order() 

        found = flatten_flip_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN) 

        self.assertEqual(found, expected)

    def test_add_all_to_key(self):
        keys = ["0", "0", "1"]
        wanted_values = [0, 1, 0]
        self.add_to_key_simple(keys, self.get_value, wanted_values = wanted_values)

        values_1 = [3, 4]
        values_2 = [8, 9]

        sub_value_store_1 = {sub_key : [values_1[idx]] for idx, sub_key in enumerate(SUB_KEYS)}
        sub_value_store_1["test1"].append(8)
        sub_value_store_1["test2"].append(9)

        sub_value_store_2 = {sub_key : [values_1[idx]] for idx, sub_key in enumerate(SUB_KEYS)}
        
        expected_struct = {
            "0" : sub_value_store_1,
            "1" : sub_value_store_2
        }

        found_struct = self.data_store.values_dict(NO_REDUCE)
        self.assertEqual(found_struct, expected_struct)

    def test_add_all_to_key_many(self):
        values = [[i for i in range(0, 20)] for j in range(0, 400)]
        sent_values = [values, values]

        self.data_store.add_all_to_key("5", sent_values)

        sub_value_store = {sub_key : [sent_values[idx]] for idx, sub_key in enumerate(SUB_KEYS)}
        expected_struct = {
            "5" : sub_value_store
        }

        found_struct = self.data_store.values_dict(NO_REDUCE)
        
        self.assertEqual(found_struct, expected_struct)

    def test_add_axis_stores(self):
        axis_store_1 = Axis_Store("test1", [3], NO_TIME_AXIS, config_handler = dummy_config_handler) 
        axis_store_2 = Axis_Store("test2", [3], NO_TIME_AXIS, config_handler = dummy_config_handler) 
        axis_store_3 = Axis_Store("test3", [3], NO_TIME_AXIS, config_handler = dummy_config_handler) 
        
        sub_keys_1 = ["test1", "test2"]
        sub_keys_2 = ["test3"]

        expected_axis_stores_1 = [axis_store_1, axis_store_2]
        expected_axis_stores_2 = [axis_store_3]

        store = {}

        self.data_store.add_axis_stores(store, "0", sub_keys_1, expected_axis_stores_1)
        self.data_store.add_axis_stores(store, "1", sub_keys_2, expected_axis_stores_2)

        found_axis_stores_1 = list(store["0"].values())
        self.assertEqual(found_axis_stores_1, expected_axis_stores_1)
        
        found_axis_stores_2 = list(store["1"].values())
        self.assertEqual(found_axis_stores_2, expected_axis_stores_2)

    def test_set_max_partition_size(self):
        keys = ["0", "0", "1"]
        wanted_values = [2, 3, 1]
        self.add_to_key_simple(keys, self.get_value_double, wanted_values = wanted_values, args = [4])
        
        values1_1 = self.get_value_double(2, 4)
        values_11 = values1_1[0][0 : 3]
        values_12 = values1_1[0][1 : 4]
        values_13 = values1_1[1][0 : 3]
        values_14 = values1_1[1][1 : 4]

        sub_value_store_1 = {} 
        sub_value_store_1["test1_0"] = [values_11]
        sub_value_store_1["test1_1"] = [values_12]
        sub_value_store_1["test2_0"] = [values_13] 
        sub_value_store_1["test2_1"] = [values_14] 

        values1_2 = self.get_value_double(3, 4)
        values_15 = values1_2[0][0 : 3]
        values_16 = values1_2[0][1 : 4]
        values_17 = values1_2[1][0 : 3]
        values_18 = values1_2[1][1 : 4]

        sub_value_store_1["test1_0"].append(values_15)
        sub_value_store_1["test1_1"].append(values_16)
        sub_value_store_1["test2_0"].append(values_17)
        sub_value_store_1["test2_1"].append(values_18) 

        values2_1 = self.get_value_double(1, 4)
        values_21 = values2_1[0][0 : 3]
        values_22 = values2_1[0][1 : 4]
        values_23 = values2_1[1][0 : 3]
        values_24 = values2_1[1][1 : 4]

        sub_value_store_2 = {} 
        sub_value_store_2["test1_0"] = [values_21]
        sub_value_store_2["test1_1"] = [values_22]
        sub_value_store_2["test2_0"] = [values_23] 
        sub_value_store_2["test2_1"] = [values_24]

        expected_struct = {
            "0" : sub_value_store_1,
            "1" : sub_value_store_2
        }

        data_max_3 = self.data_store.set_partition_size(MAX_PARTITION_SIZE)
        found_struct = data_max_3.values_dict(NO_REDUCE)

        self.assertEqual(found_struct, expected_struct)

    def test_set_same_length(self):
        value_from_key = {0 : [3, 4], 1 : [8, 9], 2 : [30, -20], 3 : [5, 5], 4 : [4, 5], 5 : [4, 1]}

        keys = ["0", "0", "0", "a", "a", "2", "2", "2", "hat", "hat"]
        wanted_values = [2, 3, 4, 1, 2, 1, 5, 5, 4, 3]
        self.add_to_key_simple(keys, self.get_value, wanted_values = wanted_values)

        ###same length performed on [[[30, 5, 4], [-20, 5, 5]], [[8, 30], [9, -20]], [[8, 4, 4], [9, 1, 1]], [[4, 5], [5, 5]]] 
        expected_format = [[[30, 5], [-20, 5]], [[8, 30], [9, -20]], [[8, 4], [9, 1]], [[4, 5], [5, 5]]] 
        same_length_handler = self.data_store.set_same_length(axis = 0)

        found_values = same_length_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        self.assertEqual(found_values, expected_format)

        expected_keys = ["0", "a", "2", "hat"]
        found_keys = same_length_handler.get_key_store(keys = True)

        self.assertEqual(found_keys, expected_keys)

    
    def test_subtract(self):
        keys = ["0", "0", "0", "1", "1"]
        wanted_values = [2, 3, 1, 2, 1]
        self.add_to_key_simple(keys, self.get_value, wanted_values = wanted_values)

        ### sub performed on [
        ###     [[[30], [5]], [[-20], [5]]],
        ###     [[[30], [8]], [[-20], [9]]]
        ### ]
        expected_format = [[[0, -3], [0, -4]]]
        sub_handler = self.data_store.subtract(AXIS_0)

        found_values = sub_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        self.assertEqual(found_values, expected_format)

    def test_subtract_multi(self):
        keys = ["0", "0", "0", "1", "1", "2", "2", "2", "3", "3"]
        wanted_values = [2, 3, 4, 1, 2, 1, 5, 5, 4, 3]
        self.add_to_key_simple(keys, self.get_value, wanted_values = wanted_values)

        ### sub performed on [[[30, 5], [-20, 5]], [[8, 30], [9, -20]], [[8, 4], [9, 1]], [[4, 5], [5, 5]]]
        expected_format = [[[22, -25], [-29, 25]], [[4, -1], [4, -4]]]
        sub_handler = self.data_store.subtract(axis = AXIS_0)

        found_values = sub_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        self.assertEqual(found_values, expected_format)

    def test_drop(self):
        axis_1, axis_2, drop_amount = 1, 2, 2
        
        self.time_store.add_all_to_key(1, VALUES_TIME_1)
        
        expected_ax_0 = [ 
            [
                [[4, 2, 8, 2, 1], [1, 9, 10, 8, 2]],       
                []
            ],
            [ 
                [[5, 3, 9, 3, 1], [2, 10, 11, 9, 2]],       
                [] 
            ]
        ]

        dropped_store = self.time_store.drop(drop_amount, AXIS_0 + 1)
        found_ax_0 = dropped_store.values_list(TIME_AXIS, REDUCE, NO_FLATTEN)
        
        self.assertEqual(found_ax_0, expected_ax_0)

        expected_ax_1 = [
            [
                [], 
                [1, 1]
            ],
            [
                [],
                [1, 1]
            ]
        ]

        dropped_store = self.time_store.drop(drop_amount, axis_1 + 1)
        found_ax_1 = dropped_store.values_list(TIME_AXIS, REDUCE, NO_FLATTEN)
        
        self.assertEqual(found_ax_1, expected_ax_1)

    def test_euclideans_easy_ax0(self):
        keys = ["0", "0", "0", "1", "1"]
        wanted_values = [2, 3, 1, 2, 1]
        self.add_to_key_simple(keys, self.get_value, wanted_values = wanted_values)

        #euclidean performed on [[[0], [3]], [[0], [4]]]
        expected_euclideans = [[[3], [4]]]
        euclidean_handler = self.data_store.euclideans(AXIS_0, AXIS_0, NO_JUMP)

        found_values = euclidean_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        self.assertEqual(found_values, expected_euclideans)

    def test_euclideans_easy_ax1(self):
        auxiliary_axis = AXIS_0
        functional_axis = 1

        keys = ["0", "0", "0", "1", "1"]
        wanted_values = [2, 3, 1, 2, 1]
        self.add_to_key_simple(keys, self.get_value, wanted_values = wanted_values)
        
        expected_euclideans = [[[0, 3], [0, 4]]]
        euclidean_handler = self.data_store.euclideans(functional_axis, auxiliary_axis, NO_JUMP)

        found_values = euclidean_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        self.assertEqual(found_values, expected_euclideans)

    def test_euclideans_heavy_ax0(self):
        keys = ["0", "0", "0", "1", "1"]
        wanted_values = [2, 3, 0, 2, 4]
        self.add_to_key_simple(keys, self.get_value_double, wanted_values = wanted_values, args = [2])
        
        #euclidean performed on [(sub_store_0)[0, 0], [1, 0]], (sub_store_1)[[0, 0], [0, 4]]
        expected_euclideans = [[[[1, 0]], [[0, 4]]]]
        euclidean_handler = self.data_store.euclideans(AXIS_0, AXIS_0, NO_JUMP)

        found_values = euclidean_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        self.assertEqual(found_values, expected_euclideans)

    def test_euclideans_multi_sub_stores(self):
        keys = ["0", "0", "0", "1", "1", "2", "2", "2", "3", "3"]
        wanted_values = [2, 3, 4, 1, 2, 1, 5, 5, 4, 3]
        self.add_to_key_simple(keys, self.get_value, wanted_values = wanted_values)

        ###euclidean performed on [[[30, 5], [-20, 5]]], [[8, 30], [9, -20]]], [[8, 4], [9, 1]], [[4, 5], [5, 5]]] 
        #### Note: in axis_store each value is represented as a nest list, e.g [30], [5], ......
        expected_format = [[[33.301651610693426], [38.28837943815329]], [[4.123105625617661], [5.656854249492381]]]
        euclidean_handler = self.data_store.euclideans(AXIS_0, AXIS_0, NO_JUMP)

        found_values = euclidean_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        self.assertEqual(found_values, expected_format)

    def test_euclideans_multi(self):
        keys = ["0", "0", "0", "1", "1", "2", "2", "2", "3", "3"]
        wanted_values = [2, 3, 4, 1, 2, 1, 5, 5, 4, 3]
        self.add_to_key_simple(keys, self.get_value_double, wanted_values = wanted_values, args = [2])
        
        ###euclidean performed on [
        ### [[[30, -20], [5, 5]], [[5, 5], [4, 5]]], 
        ### [[[8, 9], [30, -20]], [[30, -20], [5, 5]]],
        ### [[[8, 9], [4, 1]], [[30, -20], [3, 4]]],
        ### [[[4, 5], [5, 5]], [[4, 1], [4, 5]]]
        ### ]
        expected_euclideans = NP.array([
            [[[33.30165161, 38.28837944]], [[25.01999201, 25]]],
            [[[4.12310563, 5.65685425]], [[26.01922366, 21.02379604]]]
        ])
        euclidean_handler = self.data_store.euclideans(AXIS_0, AXIS_0, NO_JUMP)

        found_values = NP.array(euclidean_handler.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN))
        
        less_then = (expected_euclideans - found_values) < LIMIT 
        correct = less_then.all()

        self.assertTrue(correct)
    
    def test_euclideans_multi_jump(self):
        data_store_multi = self.create_multi_store() 
        
        expected = [
            [[[7.21110255, 8.24621125, 8.24621125, 7.21110255]], [[8, 0]]],
            [[[8.94427191, 0, 4.47213595, 8.48528137]], [[[4, 6]]]], 
        ]

        euclidean_store = (
            data_store_multi 
            .set_same_length(1, step_size_max = STEP_MAX) 
        )
        
        euclidean_store = euclidean_store.euclideans(1, AXIS_0, JUMP) 
        found = euclidean_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        
        self.check_if_all_equal(found, expected)
    
    def test_means(self):
        self.run_simple_three_keys()

        expected_means = [[[16.5], [-8]], [[8], [9]]]
        mean_store = self.data_store.means(AXIS_0, NO_JUMP)
        
        found_means = mean_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)

        self.assertEqual(found_means, expected_means)
    
    def test_means_2(self):
        data_store_multi = self.create_multi_store() 
        step_size = 2
        
        expected_means_1 = [
            [
                [2, 2, 3, 3],
                [8, 2, 8, 5]
            ], 
            [
                [8, 5],
                [4, 6]
            ]
        ]
        
        expected_means_2 = [
            [
                [2, 6, 5, 4],
                [9, 1, 6, 5],
                [6, 2, 9, 8]
            ],    
            [
                [6, 2]
            ]
        ]
        
        expected_means = [expected_means_1, expected_means_2]

        data_store_same_length = data_store_multi.set_same_length(axis = 1, step_size = step_size)
        mean_store = data_store_same_length.means(AXIS_0, NO_JUMP, step_size = step_size)
        
        found_means = mean_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        
        self.check_if_all_equal(found_means, expected_means)

    def test_means_all(self):
        data_store_multi = self.create_multi_store() 

        expected_means_1 = [
            [2, 4, 4, 3.5],
            [8.5, 1.5, 7, 5] 
        ]
        expected_means_2 = [[7, 3.5]]
        
        expected_means = [[expected_means_1, expected_means_2]]

        data_store_same_length = data_store_multi.set_same_length(axis = 1, step_size_max = STEP_MAX)
        mean_store = data_store_same_length.means(AXIS_0, NO_JUMP, step_size_max = STEP_MAX)
        
        found_means = mean_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        
        self.check_if_all_equal(found_means, expected_means)

    def test_means_all_jump(self):
        data_store_multi = self.create_multi_store() 
        
        expected_means_1 = [
            [[2, 6, 5, 4],
            [9, 1, 6, 5]], 
            [[6, 2]]
        ]
        expected_means_2 = [
            [[2., 2., 3., 3.],
            [8., 2., 8., 5.]],
            [[8., 5.]]
        ]
        
        expected_means = [expected_means_1, expected_means_2]

        data_store_same_length = data_store_multi.set_same_length(axis = 1, step_size_max = STEP_MAX)
        mean_store = data_store_same_length.means(AXIS_0, JUMP, step_size_max = STEP_MAX)
        
        found_means = mean_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)

        self.check_if_all_equal(found_means, expected_means)

    def test_stds(self):
        self.run_simple_three_keys()
        
        expected_stds = [[[13.5], [12]], [[0], [0]]]
        stds_store = self.data_store.stds(AXIS_0, NO_JUMP)
        
        found_stds = stds_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)

        self.assertEqual(found_stds, expected_stds)

    def test_stds_2(self):
        data_store_multi = self.create_multi_store() 
        step_size = 2 
        
        expected_stds_1 = [
            [
                [2, 0, 1, 3],
                [4, 0, 2, 3]
            ], 
            [
                [2, 3],
                [0, 4]
            ]
        ]
        
        expected_stds_2 = [
            [
                [2, 4, 1, 2],
                [3, 1, 4, 3],
                [2, 0, 1, 6]
            ],    
            [
                [4, 0]
            ]
        ]
    

        expected_stds = [expected_stds_1, expected_stds_2]

        data_store_same_length = data_store_multi.set_same_length(axis = 1, step_size = step_size)
        stds_store = data_store_same_length.stds(AXIS_0, NO_JUMP, step_size = step_size)
        
        found_stds = stds_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        
        self.check_if_all_equal(found_stds, expected_stds)

    def test_stds_all(self):
        data_store_multi = self.create_multi_store() 
        
        expected_stds_1 = [
            [2, 3.46410162, 1.41421356, 2.59807621],
            [3.57071421, 0.8660254, 3.31662479, 3]
        ]
        expected_stds_2 = [[3.31662479, 2.59807621]]

        expected_stds = [[expected_stds_1, expected_stds_2]]

        data_store_same_length = data_store_multi.set_same_length(axis = 1, step_size_max = STEP_MAX)
        stds_store = data_store_same_length.stds(AXIS_0, NO_JUMP, step_size_max = STEP_MAX)
        
        found_stds = stds_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        
        self.check_if_all_equal(found_stds, expected_stds)
        
    def test_stds_all_jump(self):
        data_store_multi = self.create_multi_store() 
        
        expected_stds_1 = [
            [[2., 4., 1., 2.],
            [3., 1., 4., 3.]],
            [[4., 0.]]
        ]
        expected_stds_2 = [
            [[2., 0., 1., 3.],
            [4., 0., 2., 3.]],
            [[2., 3.]]
        ]

        expected_stds = [expected_stds_1, expected_stds_2]

        data_store_same_length = data_store_multi.set_same_length(axis = 1, step_size_max = STEP_MAX)
        stds_store = data_store_same_length.stds(AXIS_0, JUMP, step_size_max = STEP_MAX)
        
        found_stds = stds_store.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)
        
        self.check_if_all_equal(found_stds, expected_stds)
        
    def test_partioned_whole(self):
        data_store_multi = self.create_multi_store()
        partition_size = 3
        
        ax_names_1 = dummy_config_handler.AXIS_NAMES_1
        ax_names_2 = dummy_config_handler.AXIS_NAMES_2

        partioned_names = [ax_names_1[0:3], ax_names_1[1:4], ax_names_2]  
        
        data_store_3 = data_store_multi.set_partition_size(partition_size)

        found_axis_names = data_store_3.all_axis_names()
        self.assertEqual(found_axis_names, partioned_names)
        
        part11 = [[[0,2,4], [12,2,10], [4,2,8]]]
        part12 = [[[2,4,6], [2,10,2], [2,8,2]]]
        part13 = [VALUE_2D_0[1]]

        partition_1 = [part11, part12, part13]

        part21 = [[[4,2,2], [4,2,6]]]
        part22 = [[[2,2,0], [2,6,8]]]
        part23 = [VALUE_2D_1[1]]
        
        partition_2 = [part21, part22, part23]

        part31 = [[[4,10,6], [6,0,2], [8,2,10]]]
        part32 = [[[10,6,2], [0,2,8], [2,10,14]]]
        part33 = [VALUE_2D_2[1]]

        partition_3 = [part31, part32, part33]

        partition_4 = partition_1

        expected_values = [partition_1, partition_2, partition_3, partition_4]
        found_values = data_store_3.values_list(NO_TIME_AXIS, NO_REDUCE, NO_FLATTEN)

        self.assertEqual(found_values, expected_values)
    
  
