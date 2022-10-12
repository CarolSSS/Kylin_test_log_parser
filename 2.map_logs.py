import os
from tkinter.ttk import Style
import pandas as pd
import json 

# Map log files from common_logs
SUF_LEN = len(".log")
COMMON_LOG_FILE = "common_logs"
NAME = "common"

# COMMON_LOG_FILE = "cube_logs"
# NAME = "cube"

def readFile(filename):
    lines = open(COMMON_LOG_FILE + "/" + filename, "r").readlines()
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
            li = line2.split(' ')
            want = ''
            
            if len(li) < 2:
                want = li[0]
            if len(li) == 2:
                want = li[0]
            # print(want)
            if want[-1] == "\n":
                want = want[:-1]
            # SET###
            if want in set_list:
                continue
            ########
            curr = all_params[filename]
            curr.add(want)
            all_params[filename] = curr

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
all = os.walk(COMMON_LOG_FILE)

# Call read file
all_files = [x[2] for x in all][0]
for i in all_files:
    if i[-3:] != "log":
        continue
    readFile(i)

# Clean result dictionary and eliminate tests with no configuration parameter called
for i in all_params.keys():
    if len(list(all_params[i])) != 0:
        new_dict_for_dump[i[:-SUF_LEN]] = list(all_params[i])

# Parse to json
with open("result/"+NAME+"_map.json", "w") as outfile:
    json.dump(new_dict_for_dump, outfile, indent=2)