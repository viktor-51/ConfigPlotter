###Tells the program to adjust the path so it will fit the format. To give an absolute path set as false and set absolute path in DIRECTORIES and the rest of the fields as = "". You can also decide to only specify COMMON_SUFFIX or ROOT_DIR
ADJUST_PATH = True 

###Modify ROOT_DIR where to look for folders.
ROOT = "InputFolder/DistancePlotting/non_optimized_files"
FIRST = ROOT + "/first" 
SECOND = ROOT + "/second"
THIRD = ROOT + "/third"
FOURTH = ROOT + "/fourth"
FIFTH = ROOT + "/fifth"
SIXTH = ROOT + "/sixth"
SEVENTH = ROOT + "/seventh"

ROOT_DIRS = [FIRST, SECOND]

###The directories where your plotting files are contained
STRUCT_DIRECTORIES = ["wikipedia", "chbenchmark"]
DIRECTORIES = {
    1 : STRUCT_DIRECTORIES,
    2 : STRUCT_DIRECTORIES
    #3 : STRUCT_DIRECTORIES,
    #4 : STRUCT_DIRECTORIES,
    #5 : STRUCT_DIRECTORIES
}

###The suffix file path or just file ending. * is a wild card and means any character. Can only be one value in distance plotting
COMMON_SUFFIX = "*.csv"

###Figure titles, correspond to extraction order 
TITLES = ["CPU-Usage", "Disk-Usage", "Memory-Usage", "Net-Usage", "Swap-Memory"]

### Workload names
WORKLOAD_NAMES = ["Wikipedia", "CH-BenCHmark"]

AXIS_NAMES = {
    1 : [
        "load_1min", "load_5min", "load_15min", "nice", "idle", "irq",
        "softirq", "steal", "guest", "guest_nice", "user(post)", "system(post)",
        "iowait(post)", "interrupts", "soft_interupts",
        "ctx_switches_vol(post)", "ctx_switches_invol(post)", "num_fds(post)",
        "cpu_frequency", "cpu_percent", "time(s)"
    ],
    2 : [
        "read_time", "write_time", "read_merged_count", "write_merged_count",
        "busy_time", "read_count(post)", "write_count(post)",
        "read_bytes(post)", "write_bytes(post)", "read_chars(post)",
        "write_chars(post)", "time(s)"
    ],
    3 : [
        "buffers", "cached", "shared", "slab", "rss(post)", "vms(post)",
        "shared(post)", "text(post)", "lib(post)", "data(post)", "dirty(post)",
        "mem_percent(post)", "time(s)"
    ],
    4 : [
        "bytes_sent", "bytes_recv", "packets_sent", "packets_recv", "errin",
        "errout", "dropin", "dropout", "time(s)"
    ],
    5 : [
        "swap_used", "swap_free", "swap_percent", "sin", "sout", "time(s)"
    ]
}

###Output folder for images. Set as None to save manually
SAVE_FOLDER = "OutputFolder/DistanceOutput/wikipedia_chbenchmark"

###Whatever to plot the bar plot in log10 or not
LOG_10 = True 

###################
######COLORS#######
###################


###Generation of random colors, precedence given to COLORS need to set to None for seed to be generated.
COLOR_SEED = None

###Define your own colors in a list, must be matplotlib compatible. Precedence given above COLOR_SEED. 
COLORS = ["blue", "red", "sandybrown", "aliceblue", "darkgoldenrod", "teal", "orange", "pink", "grey", "purple", "brown"] 
