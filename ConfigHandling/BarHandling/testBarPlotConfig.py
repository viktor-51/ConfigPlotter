##Constans
THROUGHPUT_OBJECTIVE = "Throughput*"
LATENCY_FATHER = "Latency Distribution"
LATENCY_OBJECTIVE = "Average Latency (milliseconds)"

DBTUNE_ROOT = "/home/viktor/Skolan/master_thesis/db-tune-bench/plotting/dbtune"
PGTUNE_ROOT ="/home/viktor/Skolan/master_thesis/db-tune-bench/plotting/pgtune"
OLTP_ROOT = "/home/viktor/Skolan/master_thesis/db-tune-bench/plotting/oltp"

###Tells the program to adjust the path so it will fit the format. To give an absolute path set as false and set absolute path in DIRECTORIES and the rest of the fields as = "". You can also decide to only specify COMMON_SUFFIX or ROOT_DIR
ADJUST_PATH = True 

###Generation of random colors, precedence given to COLORS need to set to None for seed to be generated.
COLOR_SEED = None

###Define your own colors in a list, must be matplotlib compatible. Precedence given above COLOR_SEED. 
COLORS = ["blue", "red", "sandybrown", "aliceblue", "darkgoldenrod", "teal", "orange", "pink", "grey", "purple", "brown"] 

###Modify DATA_STRINGS to contain the desired objectives
OBJECTIVES = [THROUGHPUT_OBJECTIVE, [LATENCY_FATHER, LATENCY_OBJECTIVE]]

###Modify ROOT_DIR where to look for folders.
ROOT_DIRS = "test/tt2"

###The directories where your plotting files are contained
DIRECTORIES = {
    1 : "test1",
    2 : "test2",
    3 : "test3",
    4 : "test1",
    5 : "test2",
    6 : "test3",
    7 : "test1",
    8 : "test2",
    9 : "test3",
}

#Give the corresponding bar names from DIRECTOIRES
BAR_NAMES = ["DBTune", "PGTune", "OLTP-Bench", "te", "32", "312", "312321", "321321", "32321", "312213"] 

###The suffix file path or just file ending. * is a wild card and means any character. 
COMMON_SUFFIX = {
    1 : ["Hypermapper/*output.csv", "results/*file.@.summary"],
}

###Figure titles correspond to objectives. 
TITLES = ["Throughput (wikipedia)", "Latency"]

###Output folder for images. Set as None to save manually
SAVE_FOLDER = "outputImages"

