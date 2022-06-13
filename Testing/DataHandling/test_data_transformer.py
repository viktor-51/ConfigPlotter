import unittest

import numpy as NP
from numpy import linalg as LA

from DataHandling import data_transformer

LIMIT = 0.00001
NO_JUMP = False

class Test_Data_Transformer(unittest.TestCase):
    
    values_11 = NP.array([NP.arange(4), NP.arange(4,8)])
    values_12 = NP.array([NP.arange(2, 8, 2), NP.arange(8, 14, 2)])
    values_21 = NP.array([NP.arange(2, 6), NP.arange(6, 10)])
    values_22 = NP.array([NP.arange(0, 6, 2), NP.arange(6, 12, 2)])
    values_31 = NP.array([NP.arange(4, 8), NP.arange(4)])
    values_32 = NP.array([NP.arange(8, 14, 2), NP.arange(2, 8, 2)])
    
    values_41 = NP.array([NP.arange(4), NP.arange(4,8)])
    values_42 = NP.array([NP.arange(2, 8, 2), NP.arange(8, 14, 2)])
    values_51 = NP.array([NP.arange(2, 6), NP.arange(6, 10)])
    values_52 = NP.array([NP.arange(0, 6, 2), NP.arange(6, 12, 2)])
    values_61 = NP.array([NP.arange(4, 8), NP.arange(4)])
    values_62 = NP.array([NP.arange(8, 14, 2), NP.arange(2, 8, 2)])


    store_1 = {0 : values_11, 1 : values_12}
    store_2 = {0 : values_21, 1 : values_22}
    store_3 = {0 : values_31, 1 : values_32}
    
    store_4 = {0 : values_41, 1 : values_42}
    store_5 = {0 : values_51, 1 : values_52}
    store_6 = {0 : values_61, 1 : values_62}


    data_store = {
        0 : store_1, 1 : store_2, 2 : store_3,
        3 : store_4, 4 : store_5, 5 : store_6
    }

    def check_if_all_equal(self, found_values, expected_values):
        all_values_was_equal = True
        for idx_outer, next_found_list in enumerate(found_values):
            for idx_inner, next_found in enumerate(next_found_list):
                next_expected = NP.array(expected_values[idx_outer][idx_inner])

                values_was_equal = ((NP.array(next_found) - next_expected) < LIMIT).all()
                all_values_was_equal &= values_was_equal
        
        self.assertTrue(all_values_was_equal)

    def test_transform_list(self):
        step_size = 1
        want_keys = False
        discard_other_keys = True 

        storage_funcs = [data_transformer.list_append, data_transformer.append_and_reset_list]
        sum_func = NP.sum

        found_sums = []
        data_transformer.transform_data_nested_store(
            self.data_store, found_sums, [], storage_funcs, sum_func, step_size,
            NO_JUMP, want_keys, discard_other_keys
        )

        expected_sums = NP.array([[28, 42], [44, 30], [28, 42], [28, 42], [44, 30], [28, 42]])
        all_zero_values = (expected_sums - NP.array(found_sums)) == 0
        
        equal = all_zero_values.all()

        self.assertTrue(equal)

    def test_transform_dict(self):
        step_size = 1
        want_keys = True
        discard_other_keys = True 

        storage_funcs = [data_transformer.set_store, data_transformer.append_and_reset_store]
        plus_func = lambda x : x + 5

        found_plus_dict = {}
        data_transformer.transform_data_nested_store(
            self.data_store, found_plus_dict, {}, storage_funcs, plus_func, step_size,
            NO_JUMP, want_keys, discard_other_keys
        )

        equal_1 = ((found_plus_dict[0][0] - (self.values_11 + 5)) == 0).all()
        equal_2 = ((found_plus_dict[0][1] - (self.values_12 + 5)) == 0).all()
        equal_3 = ((found_plus_dict[1][0] - (self.values_21 + 5)) == 0).all()
        equal_4 = ((found_plus_dict[1][1] - (self.values_22 + 5)) == 0).all()

        equals = [equal_1, equal_2, equal_3, equal_4]
        equal = all(equals)

        self.assertTrue(equal)

    def test_transform_dict_step_2(self):
        step_size = 2
        want_keys = True
        discard_other_keys = True 

        storage_funcs = [data_transformer.set_store, data_transformer.append_and_reset_store]

        plus_func = lambda x, y : x - y

        found_plus_dict = {}
        data_transformer.transform_data_nested_store(
            self.data_store, found_plus_dict, {}, storage_funcs, plus_func, step_size,
            NO_JUMP, want_keys, discard_other_keys
        )

        sub_1 = self.values_11 - self.values_21
        sub_2 = self.values_12 - self.values_22
        sub_3 = self.values_31 - self.values_41
        sub_4 = self.values_32 - self.values_42
        sub_5 = self.values_51 - self.values_61
        sub_6 = self.values_52 - self.values_62

        equal_1 = ((sub_1 - found_plus_dict[0][0]) == 0).all()
        equal_2 = ((sub_2 - found_plus_dict[0][1]) == 0).all()
        equal_3 = ((sub_3 - found_plus_dict[2][0]) == 0).all()
        equal_4 = ((sub_4 - found_plus_dict[2][1]) == 0).all()
        equal_5 = ((sub_5 - found_plus_dict[4][0]) == 0).all()
        equal_6 = ((sub_6 - found_plus_dict[4][1]) == 0).all()

        expected_len = 3
        self.assertEqual(len(found_plus_dict), expected_len)

        equals = [equal_1, equal_2, equal_3, equal_4, equal_5, equal_6]
        equal = all(equals)

        self.assertTrue(equal)

    def sub_add(self, found_store):
        iterations = range(0, len(found_store), 2)

        values = []
        for key in iterations:
            values_11 = self.data_store[key][0]
            values_12 = self.data_store[key][1]
            values_21 = self.data_store[key + 1][0]
            values_22 = self.data_store[key + 1][1]
            
            sub_1 = values_11 - values_21  
            add_1 = values_11 + values_21
            
            sub_2 = values_12 - values_22  
            add_2 = values_12 + values_22

            values.append([sub_1, sub_2])
            values.append([add_1, add_2])

        return values

    def is_correct(self, values, found_dict):
        equal = True

        for i in range(0, 6):
            equal_1 = ((values[i][0] - found_dict[i][0]) == 0).all()
            equal_2 = ((values[i][1] - found_dict[i][1]) == 0).all()

            equal &= equal_1 and equal_2 

        return equal 

    def test_transform_dict_step_2_no_reduce(self):
        step_size = 2
        want_keys = True
        discard_other_keys = False

        storage_funcs = [data_transformer.set_store_many, data_transformer.append_and_reset_store_many]

        plus_func = lambda x, y : NP.array([x - y, x + y])

        found_plus_dict = {}
        data_transformer.transform_data_nested_store(
            self.data_store, found_plus_dict, [{}, {}], storage_funcs, plus_func, step_size,
            NO_JUMP, want_keys, discard_other_keys
        )

        expected_values = self.sub_add(found_plus_dict)

        equal = self.is_correct(expected_values, found_plus_dict)

        expected_len = 6
        self.assertEqual(len(found_plus_dict), expected_len)

        self.assertTrue(equal)

    def test_transform_list_step_3(self):
        step_size = 3
        want_keys = False
        discard_other_keys = True 

        storage_funcs = [data_transformer.list_append, data_transformer.append_and_reset_list]
        sum_func = lambda x, y, z : NP.sum([x, y, z])

        found_sums = []
        data_transformer.transform_data_nested_store(
            self.data_store, found_sums, [], storage_funcs, sum_func, step_size, 
            NO_JUMP, want_keys, discard_other_keys
        )

        expected_sums = NP.array([[100, 114], [100, 114]])
        all_zero_values = (expected_sums - NP.array(found_sums)) == 0

        equal = all_zero_values.all()

        self.assertTrue(equal)

    def test_transform_list_step_all(self):
        step_size = 6
        want_keys = False
        discard_other_keys = True 

        storage_funcs = [data_transformer.list_append, data_transformer.append_and_reset_list]
        mean_func = lambda x, y, z, a, b, c : NP.mean([x, y, z, a, b, c], axis = 0)

        found_means = []
        data_transformer.transform_data_nested_store(
            self.data_store, found_means, [], storage_funcs, mean_func, step_size,  
            NO_JUMP, want_keys, discard_other_keys
        )

        expected_means = [[
            [[2, 3, 4, 5], [3.33333333, 4.33333333, 5.33333333, 6.33333333]],
            [[3.33333333, 5.33333333, 7.33333333],[5.33333333, 7.33333333, 9.33333333]]
        ]]
       
        self.check_if_all_equal(found_means, expected_means) 
        
    
    def test_transform_list_step_3_jump(self):
        step_size = 3
        should_jump = True
        want_keys = False
        discard_other_keys = True 

        storage_funcs = [data_transformer.list_append, data_transformer.append_and_reset_list]
        mean_func = lambda x, y, z : NP.mean([x, y, z], axis = 0)

        found_means = []
        data_transformer.transform_data_nested_store(
            self.data_store, found_means, [], storage_funcs, mean_func, step_size,  
            should_jump, want_keys, discard_other_keys 
        )

        expected_means = [
            [
                [[2, 3, 4, 5], [3.33333333, 4.33333333, 5.33333333, 6.33333333]],
                [[3.33333333, 5.33333333, 7.33333333], [5.33333333, 7.33333333, 9.33333333]]
            ],
            [
                [[2, 3, 4, 5], [3.33333333, 4.33333333, 5.33333333, 6.33333333]],
                [[3.33333333, 5.33333333, 7.33333333], [5.33333333, 7.33333333, 9.33333333]]
            ]
        ]
       
        self.check_if_all_equal(found_means, expected_means) 
        
    
