import os
from tkinter.ttk import Style
import pandas as pd
import json 

# Map log files from common_logs
dic_all = {}
all_params = {}
suf = len(".log")
def readFile(filname):
    lines = open("common_logs/" +filname, "r").readlines()
    all_params[filname] = set()
    for line in lines:
        if "[CTEST][GET-PARAM]" in line:
            for ind, j in enumerate(line):
                # print(line[ind:ind+len('[CTEST][GET-PARAM]')])
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
            if want[-1] == "\n":
                want = want[:-1]
            # print(want)
            
            curr = all_params[filname]
            curr.add(want)
            all_params[filname] = curr
        

all = os.walk("common_logs")
all_files = [x[2] for x in all][0]
for i in all_files:
    print(i)
    if i[-3:] != "log":
        continue
    readFile(i)

print(all_params)

new_dict_for_dump = {}
for i in all_params.keys():
    if len(list(all_params[i])) != 0:
        new_dict_for_dump[i[:-suf]] = list(all_params[i])


with open("result/map.json", "w") as outfile:
    json.dump(new_dict_for_dump, outfile, indent=2)

# df = pd.DataFrame()
# lines = open('data/test.log', "r").readlines()
# dic_all = {}
# all_params = {}
# key = ''
# name = ''
# start_flag = False
# for line in lines:
#     line = line.strip("\n")
#     start = 0
#     if "Running" in line:
#         name = line[len('[INFO] Running '):]
#     if "[CTEST][GET-PARAM]" in line and start_flag == True:
#         for ind, j in enumerate(line):
#             # print(line[ind:ind+len('[CTEST][GET-PARAM]')])
#             if line[ind:ind+len('[CTEST][GET-PARAM]')] == "[CTEST][GET-PARAM]":
#                 start = ind+len('[CTEST][GET-PARAM] ')
#         line2 = line[start:]
#         line2 = line2.lstrip()
#         print("=====")
#         li = line2.split(' ')
#         want = ''
#         if len(li) < 2:
#             want = li[0]
#         if len(li) == 2:
#             want = li[0]
#         print(want)
        
#         curr = all_params[key]
#         curr.add(want)
#         all_params[key] = curr
     
#     if "[TestName]" in line:
#         start_flag = True
#         key = line[11:]
#         all_params[key] = set()

# new_dict_for_dump = {}
# for i in all_params.keys():
#     new_dict_for_dump[i] = list(all_params[i])


# dic_all[name] = new_dict_for_dump
# with open("result/config_Test.json", "w") as outfile:
#     json.dump(dic_all, outfile, indent=2)