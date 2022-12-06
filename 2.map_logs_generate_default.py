import os
from tkinter.ttk import Style
import pandas as pd
import json 
import const

# Map log files from common_logs
SUF_LEN = len(".log")
LOG = const.LOG_FILE
NAME = const.name

all_value = dict()
# LOG = "cube_logs"
# NAME = "cube"

def readFile(filename, all_value):
    lines = open(LOG + "/" + filename, "r").readlines()
    all_params[filename] = set()
    #SET
    set_list = set()
    for line in lines:
        if "[CTEST][GET-PARAM]" in line:
            for ind, j in enumerate(line):
                if line[ind:ind+len('[CTEST][GET-PARAM]')] == "[CTEST][GET-PARAM]":
                    start = ind+len('[CTEST][GET-PARAM] ')
            line2 = line[start:]
            line2 = line2.lstrip()
            # print("=====")
            li = line2.split(' ', 1)
            # print(line2)
            want = ''
            value = ''
            if len(li) <= 2:
                want = li[0]
                if len(li) != 1:
                    value = li[1]
            # print(want)
            if want[-1] == "\n":
                want = want[:-1]
            if len(li) != 1:
                if value[-1] == "\n":
                    value = value[:-1]
            # SET###
            if want in set_list:
                continue
            ########
            curr = all_params[filename]
            curr.add(want)
            all_params[filename] = curr
            # Get default values store
            curr2 = all_value.get(want, set())
            curr2.add(value)
            all_value[want] = curr2

        # SET
        if "[CTEST][SET-PARAM]" in line:
            for ind, j in enumerate(line):
                if line[ind:ind+len('[CTEST][SET-PARAM]')] == "[CTEST][SET-PARAM]":
                    start = ind+len('[CTEST][SET-PARAM] ')
            line2 = line[start:]
            line2 = line2.lstrip()
            # print("=====")
            li = line2.split(' ')
            want = ''
            if len(li) > 3:
                want = li[-3]
            else:
                print("ERORR!!!Notice Here")
                print(line2)
                print("+++++++++++++++++++")
                continue
            if want[-1] == "\n":
                want = want[:-1]
            set_list.add(want)
            # print(set_list)


all_params = {}
new_dict_for_dump = {}
all_value_for_dump = {}
all = os.walk(LOG)

# Call read file
all_files = [x[2] for x in all][0]
for i in all_files:
    if i[-3:] != "log":
        continue
    readFile(i, all_value)

# print(all_value)

# Clean result dictionary and eliminate tests with no configuration parameter called
for i in all_params.keys():
    if len(list(all_params[i])) != 0:
        new_dict_for_dump[i[:-SUF_LEN]] = list(all_params[i])

for i in all_value.keys():
    all_value_for_dump[i] = list(all_value[i])

# Parse to json
with open("result/"+NAME+"_map.json", "w") as outfile:
    json.dump(new_dict_for_dump, outfile, indent=2)

with open("result/"+NAME+"_default_value.json", "w") as outfile:
    json.dump(all_value_for_dump, outfile, indent=2)