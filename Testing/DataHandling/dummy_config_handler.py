AXIS_NAMES_1 = ["1", "2", "3", "4"]
AXIS_NAMES_2 = ["1", "6"]
AXIS_NAMES_3 = ["7", "8", "9", "10", "11", "12"]

name_store = {
    "test1" : AXIS_NAMES_1,
    "test2" : AXIS_NAMES_2,
    "test3" : AXIS_NAMES_3
}

def get_axis_names(key):
    return name_store[key]
