import matplotlib.pyplot as plt

import numpy as NP

from FileHandling import CSV_handler
from PlotHandling.BarPlotting.bar_info_handler import Bar_Info_Handler 
from PlotHandling.DistancePlotting.distance_info_handler import Distance_Info_Handler

AXIS_0, AXIS_1, AXIS_2 = 0, 1, 2
    
PARTITION_SIZE = 3
NO_JUMP = NO_TIME = FLATTEN = False
JUMP = REDUCE_IF_EMPTY= True

def bar_data(extractor, bar_config_handler):
    AXIS_0, step_size_1 = 0, 1
    no_jump, REDUCE_IF_EMPTY, FLATTEN = False, True, True

    info_handler = Bar_Info_Handler(bar_config_handler)
    data_store = extractor.extract_file_data()
    
    print("**** Collected Data **** \n\n", data_store)

    titles = data_store.get_sub_keys()
    bar_names = data_store.all_axis_names()
    means = (
        data_store
        .means(AXIS_0, NO_JUMP, step_size = step_size_1)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )

    stds = (
        data_store
        .stds(AXIS_0, NO_JUMP, step_size = step_size_1)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )

    amount_names_each_axis = data_store.all_axis_lengths()

    info_handler.assign_bar_info(
        "bar_info", means, stds, titles, bar_names, amount_names_each_axis, bar_config_handler
    )

    return info_handler

def distance_data(extractor, distance_config_handler):
    workload_names = distance_config_handler.plot_info()["workload_names"]
    workload_variables = [next_name for next_name in workload_names]

    
    info_handler = Distance_Info_Handler(distance_config_handler)
    
    data_store = (
        extractor
        .extract_file_data()
    )
    
    sub_keys = data_store.get_sub_keys()
    axis_titles = data_store.all_axis_names()
    
    time_axis_store = data_store.reduce_at_pivot()
    
    time_values = time_axis_store.time_axis()
    mean_values = (
        time_axis_store
        .means(AXIS_0, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
    
    std_values = (
        time_axis_store
        .stds(AXIS_0, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
   
    legend_time_line = workload_variables

    info_handler.assign_line_info(
        "time_line", mean_values, std_values, sub_keys, axis_titles,
        '', legend_time_line, time = time_values 
    )

    data_store_NO_TIME = (
        data_store
        .drop_time()
        .drop(32, AXIS_2)
    )
    
    diff_euclidean_handler = (
        data_store_NO_TIME.euclideans(AXIS_2, AXIS_1, NO_JUMP)
    )
    
    diff_per_iteration_mean = (
        diff_euclidean_handler
        .means(AXIS_0, NO_JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )

    diff_per_iteration_stds = (
        diff_euclidean_handler
        .stds(AXIS_0, NO_JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )

    diff_per_iterations_title = (
        "Euclidean distance between workload, {} and {}".format(*workload_names)
    )
    diff_per_iterations_label = [""]
    
    info_handler.assign_line_info(
        "euc_different_workloads", diff_per_iteration_mean, 
        diff_per_iteration_stds, sub_keys, axis_titles, 
        diff_per_iterations_title, diff_per_iterations_label 
    )
    
    euc_equal_label_title = (
        "Euclidean distance between the workloads themself, {} and {}"
        .format(*workload_names)
    )

    equal_euclidean_handler = (
        data_store_NO_TIME
        .euclideans(AXIS_2, AXIS_1, JUMP)
    )
    
    euc_equal_mean = (
        equal_euclidean_handler
        .means(AXIS_0, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )

    euc_equal_stds = (
        equal_euclidean_handler
        .stds(AXIS_0, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )

    euc_equal_labels = workload_variables 
    
    info_handler.assign_line_info(
        "euc_equal_workloads", euc_equal_mean, euc_equal_stds, sub_keys, 
        axis_titles, euc_equal_label_title, euc_equal_labels 
    )

    scatter_legend_title = "Repetition = r"
    
    partition_3_store = (
        data_store_NO_TIME
        .means(AXIS_1, NO_JUMP)
        .reduce_if_empty()
        .set_partition_size(PARTITION_SIZE)
    )
    
    partitioned_titles = partition_3_store.get_sub_keys()
    partitioned_axis_labels = partition_3_store.all_axis_names() 
    
    scatter_values = (
        partition_3_store
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
    
    for n in scatter_values:
        n.pop()
        n.pop()

    scatter_legend = []
    for i in range(0, 3):
        str1 = "r = " + str(i + 1) + ", " + workload_variables[0] 
        str2 = "r = " + str(i + 1) + ", " + workload_variables[1] 

        scatter_legend.append(str1)
        scatter_legend.append(str2)
    
    info_handler.assign_distance_info_3D(
        "scatter_info", scatter_values, partitioned_titles, partitioned_axis_labels, 
         scatter_legend_title, scatter_legend
    ) 
    
    scatter_values_mean = (
        partition_3_store 
        .means(AXIS_0, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
    
    scatter_legend_title_mean = "Mean of repetitions"
    scatter_legend_mean = workload_variables

    info_handler.assign_distance_info_3D(
        "scatter_mean_info", scatter_values_mean, partitioned_titles, partitioned_axis_labels, 
        scatter_legend_title_mean, scatter_legend_mean
    ) 
    
    manhattan_values_mean = (
        partition_3_store 
        .subtract(AXIS_0) 
        .means(AXIS_0, NO_JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
    
    manhattan_legend_title = "manhattan distance"
    manhattan_labels = [""]

    info_handler.assign_distance_info_3D(
        "manhattan_info", manhattan_values_mean, partitioned_titles,
        partitioned_axis_labels, manhattan_legend_title, manhattan_labels
    )
   
    data_store_pivoted = (
        data_store
        .drop_time()
        .drop(32, AXIS_2)
        .reduce_at_pivot()
    )

    iteration_mean_data = (
        data_store_NO_TIME
        ### mean of points
        .means(AXIS_2, JUMP, step_size_max = True)
        ### mean of workloads
        .means(AXIS_1, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
    
    iteration_std_data = (
        data_store_NO_TIME 
        .stds(AXIS_2, JUMP, step_size_max = True)
        .means(AXIS_1, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
    
    print_data(
        data_store_pivoted, iteration_mean_data, iteration_std_data, 
        euc_equal_mean, euc_equal_stds, diff_per_iteration_mean, 
        diff_per_iteration_stds, axis_titles
    )
    return info_handler 
    

def print_data(
    data_store, iteration_mean_data, iteration_std_data,
    category_euclidean_iteration_data_self_mean, 
    category_euclidean_iteration_data_self_std, 
    category_euclidean_iteration_data_other_mean,
    category_euclidean_iteration_data_other_std, axis_labels
):

    mean_values = (
        data_store
        .means(AXIS_0, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )
    
    std_values = (
        data_store
        .stds(AXIS_0, JUMP, step_size_max = True)
        .flip_order()
        .values_list(NO_TIME, REDUCE_IF_EMPTY, FLATTEN)
    )

    dependent_data, independent_data = process(
        mean_values, std_values, iteration_mean_data, iteration_std_data,
        category_euclidean_iteration_data_self_mean, 
        category_euclidean_iteration_data_self_std, 
        category_euclidean_iteration_data_other_mean,
        category_euclidean_iteration_data_other_std, axis_labels
    )
    
    header_dependent = [
        "metric", "distance", "variance_inner", "variance_outer", 
        "intermingling"
    ]

    all_data_dependent = []
    for key, value_dict in dependent_data.items():
        next_data = []
        next_data.append(key)

        next_data.extend(value_dict.values())
        all_data_dependent.append(next_data)

    CSV_handler.create_file(
        "test_test_do_not_remove.csv", header_dependent, 
        data=all_data_dependent
    )

    header_independent = [
        "metric", "distance", "variance", "bias", "growth", "growth_variance"
    ]

    all_data_independent_1 = []
    all_data_independent_2 = []
    for key, value_dict in independent_data.items():
        next_data_1 = []
        next_data_2 = []
        next_data_1.append(key)
        next_data_2.append(key)
        
        for value_list in value_dict.values():
            next_data_1.append(value_list[0])
            next_data_2.append(value_list[1])
        
        all_data_independent_1.append(next_data_1)
        all_data_independent_2.append(next_data_2)

    CSV_handler.create_file(
        "test_test_do_not_remove_in_1.csv", header_independent, 
        data=all_data_independent_1
    )

    CSV_handler.create_file(
        "test_test_do_not_remove_in_2.csv", header_independent, 
        data=all_data_independent_2
    )
def process(
    category_mean_data, category_std_data,
    iteration_mean_data, iteration_std_data,
    category_euclidean_iteration_data_self_mean, 
    category_euclidean_iteration_data_self_std, 
    category_euclidean_iteration_data_other_mean, 
    category_euclidean_iteration_data_other_std, all_axis_category_labels
):  
    categorized_data_dependent = {}
    categorized_data_independent = {}
    for idx, workload_mean_data in enumerate(category_mean_data):
        w1_m, w2_m = NP.array(workload_mean_data)[0 : 2]
        nbr_columns = w1_m.shape[-1]

        w1_s, w2_s = NP.array(category_std_data[idx])[0 : 2]
                
        m_i = NP.array(iteration_mean_data[idx])
        s_i = NP.array(iteration_std_data[idx])

        euc_m_self = NP.array(
            category_euclidean_iteration_data_self_mean[idx]
        )
        euc_s_self = NP.array(
            category_euclidean_iteration_data_self_std[idx]
        )
        euc_m_other = NP.array(
            category_euclidean_iteration_data_other_mean[idx][0]
        ) 
        euc_s_other = NP.array(
            category_euclidean_iteration_data_other_std[idx][0]
        )

        nbr_iterations = euc_m_other.shape[0]
        
        axis_category_labels = all_axis_category_labels[idx]
        for idx in range(0, nbr_columns):
            points_w1_m = w1_m[:, idx]
            points_w2_m = w2_m[:, idx]
            ps_w1_s = w1_s[:, idx]
            ps_w2_s = w2_s[:, idx]
            next_label = axis_category_labels[idx]
            
            mean_1 = NP.mean(points_w1_m)
            mean_2 = NP.mean(points_w2_m)
            
            largest = max(mean_1, mean_2)
            smallest = min(mean_1, mean_2) 

            match (mean_1, mean_2):
                case (0, 0):
                    var_1 = NP.mean(ps_w1_s)
                    var_2 = NP.mean(ps_w2_s) 
                    
                    distance_factor = 0
                    
                case (x, 0):
                    var_1 = NP.mean(ps_w1_s) / x
                    var_2 = NP.mean(ps_w2_s) 
                    
                    distance_factor = largest

                case (0, y):
                    var_1 = NP.mean(ps_w1_s) 
                    var_2 = NP.mean(ps_w2_s) / y
                    
                    distance_factor = largest

                case (x, y):
                    var_1 = NP.mean(ps_w1_s) / x
                    var_2 = NP.mean(ps_w2_s) / y
                    
                    distance_factor = largest / smallest
                        
            dist_mean = abs(mean_1 - mean_2)

            if dist_mean != 0:
                inner_variance = NP.std(points_w1_m - points_w2_m) / dist_mean
            else:
                inner_variance = 0
            
            outer_variance_high = NP.sum(
                euc_s_other[:, idx] / euc_m_other[:, idx]
            ) 
            outer_variance = outer_variance_high / nbr_columns 

            less_inds = points_w1_m < points_w2_m
            bigger_inds = ~less_inds

            less_contacts = (
                points_w1_m[less_inds] 
                + ps_w1_s[less_inds] 
                >= points_w2_m[less_inds] 
                - ps_w2_s[less_inds]
            )
            bigger_contacts = (
                points_w1_m[bigger_inds] 
                - ps_w1_s[bigger_inds] 
                <= points_w2_m[bigger_inds] 
                + ps_w2_s[bigger_inds]
            )
            
            total_contacts = NP.sum(less_contacts) + NP.sum(bigger_contacts)
            contact_percentage = total_contacts / len(points_w1_m)

            categorized_data_dependent[next_label] = categorize_dependent(
                distance_factor, contact_percentage, inner_variance, 
                outer_variance
            )

            biases = []
            growth = []
            g_variance = []

            for idx_w, w_m_i in (
                enumerate(m_i)
            ):
                first_m, rest_m = w_m_i[0, idx], w_m_i[1 :, idx]
                first_s = s_i[idx_w, 0, idx]

                
                if first_s > 0:
                    bias = NP.mean(NP.abs(rest_m - first_m)) / first_s  
                else:
                    bias = NP.mean(NP.abs(rest_m - first_m)) 
                
                biases.append(bias)

                mean_values = euc_m_other[:, idx]
                
                length = len(mean_values)
                indexes = NP.arange(0, length)
                oned = NP.vstack([indexes, NP.ones(length)]).T
                
                (coeficient, c), residual = (
                    NP.linalg.lstsq(oned, mean_values, rcond=None)[0 : 2]
                )
                total_mean_growth = coeficient * 10
                average_dist_from_line = (residual ** (1/2)) / length

                if first_m != 0:
                    growth.append(total_mean_growth / mean_values[0])
                else:
                    growth.append(total_mean_growth)
                    
                """ 
                if next_label == 'load_5min':
                    print(total_mean_growth / first_m)
                    print(first_m)
                    a = b
                """

                if total_mean_growth != 0:
                    g_variance.append(
                        average_dist_from_line / total_mean_growth
                    )
                else:
                    g_variance.append(average_dist_from_line)
            
            values_to_be_categorized = {
                "distance" : [distance_factor] * 2, 
                "variance" : [var_1, var_2], 
                "bias" : biases, "growth" : growth, 
                "growth_variance" : g_variance 
            }
            categorized_data_independent[next_label] = categorize_independent(
                values_to_be_categorized 
            )

    return categorized_data_dependent, categorized_data_independent

def categorize_dependent(
    distance_factor, total_contacts, inner_variance, outer_variance
):
    match distance_factor:
        case x if x >= 1.8:
            distance_label = "high"
        case x if x >= 1.5:
            distance_label = "medium"
        case 0:
            distance_label = "0"
        case _:
            distance_label = "low"
    
    match inner_variance:
        case x if x >= 0.5:
            inner_label = "very high"
        case x if x >= 0.3:
            inner_label = "high"
        case x if x >= 0.1:
            inner_label = "medium"
        case 0:
            inner_label = "0"
        case _:
            inner_label = "low"

    match outer_variance:
        case x if x >= 0.5:
            outer_label = "very high"
        case x if x >= 0.3:
            outer_label = "high"
        case x if x >= 0.1:
            outer_label = "medium"
        case _:
            outer_label = "low"

    match total_contacts:
        case 0:
            contact_label = "non"
        case x if x <= 0.01:
            contact_label = "low" 
        case x if x <= 0.05:
            contact_label = "medium" 
        case x if x <= 0.1:
            contact_label = "high" 
        case _:
            contact_label = "very high" 

    return {
        "distance" : distance_label, "variance_inner" : inner_label, 
        "variance_outer" : outer_label, "intermingling" : contact_label
    }
        
        
def categorize_independent(all_values):
    collected_data = {}
    for label, values_list in all_values.items():
        for value in values_list:
            match label:
                
                case "distance" :
                    match value:
                        case x if x >= 1.8:
                            value_label = "high"
                        case x if x >= 1.5:
                            value_label = "medium"
                        case 0:
                            value_label = "0"
                        case _:
                            value_label = "low"

                case "variance" : 
                    match value:
                        case x if x >= 0.5:
                            value_label = "very high"
                        case x if x >= 0.3:
                            value_label = "high"
                        case x if x >= 0.1:
                            value_label = "medium"
                        case _:
                            value_label = "low"
        
                case "bias" : 
                    match value:
                        case x if x >= 1:
                            value_label = "high"
                        case x if x >= 0.5:
                            value_label = "medium"
                        case _:
                            value_label = "low"
        
                case "growth" : 
                    match value:
                        case x if x >= 2:
                            value_label = "+very high"
                        case x if x >= 1:
                            value_label = "+high"
                        case x if x >= 0.5:
                            value_label = "+medium"
                        case x if x >= 0:
                            value_label = "+low"
                        case x if x >= -0.5:
                            value_label = "-low"
                        case x if x >= -1:
                            value_label = "-medium"
                        case x if x >= -2:
                            value_label = "-high"
                        case _:
                            value_label = "-very high"
     
                case "growth_variance" : 
                    match value:
                        case x if x >= 0.5:
                            value_label = "very high"
                        case x if x >= 0.3:
                            value_label = "high"
                        case x if x >= 0.1:
                            value_label = "medium"
                        case _:
                            value_label = "low"
                case _ :
                    print("\nfailed to match warning\n")
            
            if label in collected_data:
                collected_data[label].append(value_label)
            else:
                collected_data[label] = [value_label]
    
    return collected_data
  





