##Constans
THROUGHPUT_OBJECTIVE = "Throughput*"
LATENCY_FATHER = "Latency Distribution"
LATENCY_OBJECTIVE = "Average Latency (milliseconds)"

#########################
#####  PATH INFO  #######
#########################

###Tells the program to adjust the path so it will fit the format. To give an absolute path set as false and set absolute path in DIRECTORIES and the rest of the fields as = "". You can also decide to only specify COMMON_SUFFIX or ROOT_DIR
ADJUST_PATH = True 

###Modify DATA_STRINGS to contain the desired objectives
OBJECTIVES = [THROUGHPUT_OBJECTIVE, [LATENCY_FATHER, LATENCY_OBJECTIVE]]

###Modify ROOT_DIR where to look for folders.
ROOT_DIRS = ["Testing/BarTesting/test/tt1", "Testing/BarTesting/test/tt2", "Testing/BarTesting/test/tt1"]

###The directories where your plotting files are contained
DIRECTORIES = {
    1 : ["test1", "test2", "test3"], 
    2 : ["test1", "test2", "test3"],
    3 : ["test1", "test2", "test3"]
}

#Give the corresponding bar names from DIRECTOIRES
BAR_NAMES = ["DBTune", "PGTune", "OLTP-Bench", "te", "32", "312", "312321", "321321", "32321", "312213"] 

###The suffix file path or just file ending. * is a wild card and means any character. 
COMMON_SUFFIX = {
    1 : ["Hypermapper/*output.csv", "results/*file.@.summary"],
}


#########################
#####  PLOT INFO  #######
#########################

###Figure titles correspond to objectives. 
TITLES = ["Throughput (wikipedia)", "Latency"]

###Output folder for images. Set as None to save manually
SAVE_FOLDER = "OutputFolder/BarOutput"

###Whatever to plot the bar plot in log10 or not
LOG_10 = False

######################
#####  COLORS  #######
######################

###Generation of random colors, precedence given to COLORS need to set to None for seed to be generated.
COLOR_SEED = None

###Define your own colors in a list, must be matplotlib compatible. Precedence given above COLOR_SEED. 
COLORS = ["blue", "red", "sandybrown", "aliceblue", "darkgoldenrod", "teal", "orange", "pink", "grey", "purple", "brown"] 
