import os

import sys

sys.path.insert(0, '/home/viktor/Skolan/master_thesis/db-tune-bench/jonas-vik/plotter')
from FileHandling import system_file_handler as sf

mixed_folder = "./split_equal/"

adjust_path = False
#optimized_root = 
pattern = "*[0-9]*/"

repetitions = ["first", "second"]
names = ["wikipedia"]

optimization_root = "./optimization_files"
non_optimization_root = "./non_optimized_files"

def create_paths(root, middles, suffixes, runs, step_size):
    it_str = "/iteration_"
    generated_paths = []
    
    for middle in middles:
        middle_paths = []

        for suffix in suffixes:
            suffix_paths = []

            for i in range(0, runs, step_size):
                next_it_str = it_str + str(i)
                new_path = root + "/" + middle + "/" + suffix + next_it_str
                
                suffix_paths.append(new_path)
            
            middle_paths.append(suffix_paths)

        generated_paths.append(middle_paths)

    return generated_paths

def save_paths(paths, workload_idx):
    for repetition_paths in paths:
        for workload_paths in repetition_paths:
            for i, next_path in enumerate(workload_paths):
                #remove .  optimization_files and iteration_x
                non_root_path = next_path.split("/")[2 : -1]
                folder_specification = "/".join(non_root_path)
                
                new_iteration = "/iteration_" + str(i)
                new_dir = mixed_folder + folder_specification + workload_idx + new_iteration
                
                print(new_dir)
                os.system("sudo mkdir -p {}".format(new_dir))

                os.system("sudo cp -r {} {}".format(next_path + "/*", new_dir))


optimization_paths = create_paths(optimization_root, repetitions, names, 21, 5)
non_optimization_paths = create_paths(non_optimization_root, repetitions, names, 5, 1)

save_paths(optimization_paths, "_0")
save_paths(non_optimization_paths, "_1")

