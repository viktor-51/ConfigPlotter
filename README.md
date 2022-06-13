# Intro #

A simple plotter which makes bar plots of the statistics produced by **OLTP-Bench**, developed to support **DBTune**. The plotter plots information stored in the data directories produced by DBTune or any other software. The plotter reads a number of these data files in order to aggregate the data. The plotter then produce one bar plot per objective. A bar in the bar plot contains the aggregated mean value for a given objective and the standard deviation.

# Limitations #

Can only handle json and csv format. 

# How to Use #
The program is run by

```
python barPlotter.py
```

## Specifying Path ##

In the configuration file **config.py** there are three fields for specifying which files you want to aggregate. These are:

1. ROOT_DIRS
2. DIRECTORIES
3. COMMON_SUFFIX

These three fields will together generate paths to the data files used to create the bar plots, in the form of 

```
ROOT_DIRS/DIRECTORIES/COMMON_SUFFIX
``` 
### ROOT_DIRS ###

This is where the directories containing your plotting data lay. 

```
ROOT_DIRS = “/mnt/data/” 

where for DBTune /mnt/data/ will contain directories like 

2020-01-13_12-14-13
```
If you have seperated your directories into several root folders you many want to specify a list.  

```
ROOT_DIRS = [“plottingDir/DBTune”, “plottingDir/PGTune”, “plottingDir/OLTP-Bench”]
```

### DIRECTORIES ###

A list of folders for the plotter to aggregate data from. By default DBTune names these as the date and time the optimization started. The following example would collect from three benchmark runs.
```
DIRECTORIES = [[“2020-01-13_12-14-13”, “2022-05-13_12-14-13”], “2021-02-13_12-14-13”]
```
Were the folders placed within the nested array **[“2020-01-13_12-14-13”, “2022-05-13_12-14-13”]** is aggregated into one single bar. 

**Important** if you have specified **ROOT_DIRS** as a list of more then one item then each item in **DIRECTORIES** will increment **ROOT_DIRS**.

An alternative way of definining directories is: 

```
DIRECTORIES = {
  1 : [“2020-01-13_12-14-13”, “2022-05-13_12-14-13”], 
  2 : “2021-02-13_12-14-13”
}
```


The regex "*" can also be used in directories. Every matched file will be placed in a list for example:

```
folder_contains = "1-12, 2-12, 3-12, 4-13"

DIRECTORIES = "*-12"

```

This would match [1-12, 2-12, 3-12], but not 4-13. The new list is the same thing as writing.

```
DIRECTORIES = [[1-12, 2-12, 3-12]]
```

**NOTE:** That the list is nested. 

### BAR_NAMES ###

A list of bar names. The index correspond to the items in **DIRECTORIES**. For a nested array one name is given only. So with the same example as in **DIRECTORIES**

```
BAR_NAMES = ["First name", "Second name"] 

"First name" -> [“2020-01-13_12-14-13”, “2022-05-13_12-14-13”]

"Second name" -> “2021-02-13_12-14-13”
```

### COMMON_SUFFIX ###

**COMMON_SUFFIX** is appended to each string in **DIRECTORIES**. This specifies the relation between the data file and the folder names given in **DIRECTORIES**. 

```
COMMON_SUFFIX = ["*output.csv", "results/outputfile.@.summary"]
```

Please note that this is a **common** suffix for all files in **DIRECTORIES**, i.e we assume all data files are stored in the same way.

Placing several file names in **COMMON_SUFFIX** lets the program extract several objectives. 

In **COMMON_SUFFIX** we can use the wild card * to substitute any combination of letters including nothing. E.g "*output.csv" would match.

```
dsadassada21313--12313123213.output.csv
output.csv
```
The **@** sign has a special meaning and is replaced with the index corresponding to the **optimal** value in the first file in **COMMON_SUFFIX**, e.g "*output.csv". For example a .csv file with the objective optimal value at index 43 at run one and 50 at run 2 would yield 
```
results/outputfile.43.summary
results/outputfile.50.summary
```

If we have specified a **list** for **ROOT_DIRS** then we may want to specify a suffix for each root directory.
```
COMMON_SUFFIX = {
1 : ["*output.csv", "results/outputfile.@.summary"],
(2, 3) : "*.summary" 
}
```

Here we have defined the **COMMON_SUFFIX** for three seperate roots.  

## Objectives ##
An objective is one of the field names or columns in the data file and which we want plotted. 

Each objective will have its own plot.
These objectives are specified in the field **OBJECTIVES**

**Each objective** corresponds to an entry in **COMMON_SUFFIX** if both are **equal** length. If not, then its assumed that the file specified by the last suffix in **COMMON_SUFFIX** contains all the last objectives in **OBJECTIVES**. 

### OBJECTIVES ### 

Here we specify the objectives we want in the bar plots. The example below would aggregate data and produce two plots, one for throughput[ANY CHARACTER], and one for average latency.
```
OBJECTIVES = ["Throughput*", ["Parent to Latency", "Average Latency (milliseconds)"]]

COMMON_SUFFIX = ["*output.csv", "results/outputfile.@.summary"]
```
If we have a **json** file we may need to define nested objectives. These are specified as an array within the **OBJECTIVES** field. In our example the .summary file is actually an json file and here "Average Latency (milliseconds)" is nested one step.

Also here in the **OBJECTIVES** field we can specify * to match any character. 

## Colors ##
### COLORS ###
Your own colors can be defined in the field **COLORS**. Note that the colors must follow matplotlib standard. 

```
COLORS = ["blue", "red", "sandybrown", "aliceblue", "darkgoldenrod", "teal", "orange", "pink", "grey", "purple", "brown"]
```

To many colors is not a problem. 

### COLOR_SEED ###
You can also set a random seed to get some insperation on colors, the colors are printed in standard output. 

```
COLOR_SEED = 20
```

## Misc ##
### Adjust Path ###
By default the program adjust the path to fit

```
ROOT_DIR/DIRECTORIES/COMMON_SUFFIX
``` 
You can turn this off by setting

```
ADJUST_PATH = False
```

Now you can specify the absolute path in ***DIRECTORIES*** for each file. ***ROOT_DIR*** and ***COMMON_SUFFIX*** will still work as usual if you define them. So by this construct you could for example specify ***ROOT_DIR*** and then from ***ROOT_DIR*** have the rest of the path for each file in ***DIRECTORIES***. 
