import os
import json
from pathlib import Path

import numpy as np
import pandas as pd
import datetime

# to
ctest_file = "../kylin/core-common/src/main/resources/ctest.properties"
working_dir = "../kylin"
git_link = "https://github.com/apache/kylin"
sha = "63f9ac6bcd0db005f10935d88747d39fc0819ab7"


# TODO
# finished file gnerate function
# finish run all test function


def file_generate(file_path):
    file_path = './result/common_map.json'
    module_name = "core-common"
    json_file = open(file_path)
    para_map = json.load(json_file)
    csv_output = []
    with open("./config_result/" + module_name + '.csv', 'w') as fp:
        header = "REPO, SHA, CONFIG_PARAMETER, TEST_NAME, VALUE, TYPE(GOOD|BAD), EXPECTATION(PASS|FAIL)"
        fp.write("%s\n" % header)
        for test_name in para_map:
            for i in para_map[test_name]:
                output = git_link + ", " + sha + ", " + i + ", " + test_name + ", " + " " + ", " + "GOOD"
                fp.write("%s\n" % output)


def run_ctest(module_name, test_name, config_parameter, config_value):
    inject(config_parameter, config_value)
    command = "mvn -pl " + module_name + " test -Dtest=" + test_name
    print(command)
    os.chdir(working_dir)
    print("change dir to " + working_dir)
    print("run command : " + command)
    with os.popen(command) as output:
        if "[INFO] BUILD SUCCESS\n" in output.readlines():
            result = "PASS"
        else:
            result = "FAIL"
    if result == "PASS":
        print("[myctest]--> " + config_parameter + " " + config_value + " " + " " + "\033[32m" + result + "\033[0m")
    elif result == "FAIL":
        print("[myctest]--> " + config_parameter + " " + config_value + " " + " " + "\033[31m" + result + "\033[0m")
    return result


def file_is_exist(test_name):
    my_file = Path(test_name + ".json")
    return my_file.exists()


def run_all_ctest(module_name):
    # need to change to csv files
    # finished the file generate first
    csv_output = []
    file = 'config_result/generated_{}_vals.csv'.format(module_name)
    df = pd.read_csv(file, sep=',', engine='python')
    df = df.fillna(value=" ")
    idx = 0.0
    print("")
    file_name = 'config_result/' + module_name + ".csv"
    with open(file_name, 'w+') as fp:
        header = "REPO, SHA, CONFIG_PARAMETER, TEST_NAME, VALUE, TYPE(GOOD|BAD), EXPECTATION(PASS|FAIL)"
        fp.write("%s\n" % header)
        for index, row in df.iterrows():
            row["EXPECTATION(PASS|FAIL)"] = "FAIL"
            test_name = row["TEST_NAME"]
            config_parameter = row["CONFIG_PARAMETER"]
            config_value = row["VALUE"]
            result = run_ctest(module_name, test_name, config_parameter, config_value)
            lines = git_link + ", " + sha + ", " + config_parameter + ", " + test_name + ", " + \
                    config_value + ", " + row["TYPE(GOOD|BAD)"] + ", " + result
            csv_output.append(lines)
            progress = float(idx / len(df)) * 100
            print("[myctest]--> current is " + str(idx) + " test, " + str(progress) + "% finished.")
            idx = idx + 1
            fp.write("%s\n" % lines)
        print('Done')


def inject(name, config_value):
    if str(config_value) == "nan":
        config_value = " "
    with open(ctest_file, 'w') as fp:
        print("ctest file at : " + ctest_file)
        print("inject parameter: " + name + " = " + str(config_value))
        fp.write(name + " =" + config_value)


def delete():
    print("clear ctest File at " + ctest_file)
    os.remove(ctest_file)
    f = open(ctest_file, "w")
    f.close()


if __name__ == "__main__":
    # module = "core-common"
    # testName = "KylinServerDiscoveryTest#test"
    param = "kylin.job.remote-cli-password"
    # value = ""
    # run_ctest(module, testName, param, value)
    # file_generate("1")
    run_all_ctest("core-common")
    # my_file = 'config_result/generated_core-common_vals.csv'
    # mydf = pd.read_csv(my_file, sep=',', engine='python')
    # value = mydf[mydf.CONFIG_PARAMETER == "kylin.job.remote-cli-password"]["VALUE"].head(1)
    # print(value)
    # inject(param, np.NaN)
