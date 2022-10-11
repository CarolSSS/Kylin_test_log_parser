import os
import json
from pathlib import Path
import csv

ctest_file = "../kylin/core-common/src/main/resources/ctest.properties"
working_dir = "../kylin"

def file_generate(test_name):
    json_file = open('./result/map.json')  # param_unset_getter_map path
    para_map = json.load(json_file)
    my_para = para_map[test_name]
    data = {}
    for i in my_para:
        data[i] = [[], []]
    with open("./result/" + test_name + '.csv', 'w') as fp:
        header = "REPO, SHA, CONFIG_PARAMETER, TEST_NAME, VALUE, TYPE(GOOD|BAD), EXPECTATION(PASS|FAIL)"
        fp.write("%s\n" % header)


def run_ctest(module_name, test_name, config_parameter, value):
    inject(config_parameter, value)
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
        print("[myctest]--> " + config_parameter + " " + value + " " + " " + "\033[32m"+result+"\033[0m")
    elif result == "FAIL":
        print("[myctest]--> " + config_parameter + " " + value + " " + " " + "\033[31m"+result+"\033[0m")
    return result


def file_is_exist(test_name):
    my_file = Path(test_name + ".json")
    return my_file.exists()


def run_all_ctest(git_link, sha, test_name, module_name):
    csv_output = []
    with open(test_name + '.json') as json_file:
        test_dict = json.load(json_file)
    os.chdir('../IDoCT/run_ctest')  # ctest function path
    for i in test_dict:
        config_parameter = i
        for j in range(len(test_dict[i][0])):
            value = test_dict[i][0][j]
            types = test_dict[i][1][j]
            result = run_ctest(module_name, test_name, config_parameter, value, )
            csv_output.append(git_link + ", " + sha + ", " + config_parameter + ", " + test_name + ", " + value + ", " +
                              types + ", " + result)
    print("")
    os.chdir('../../utils')  # result dir
    file_name = test_name + ".csv"
    with open(file_name, 'w+') as fp:
        header = "REPO, SHA, CONFIG_PARAMETER, TEST_NAME, VALUE, TYPE(GOOD|BAD), EXPECTATION(PASS|FAIL)"
        fp.write("%s\n" % header)
        for lines in csv_output:
            fp.write("%s\n" % lines)
        print('Done')


def inject(name, value):
    with open(ctest_file, 'w') as fp:
        print("ctest file at : " + ctest_file)
        print("inject parameter: " + name + " = " + value)
        fp.write(name + " =" + value)


def delete():
    print("clear ctest File at " + ctest_file)
    os.remove(ctest_file)
    f = open(ctest_file, "w")
    f.close()


if __name__ == "__main__":
    module = "core-common"
    testName = "KylinServerDiscoveryTest#test"
    param = "kylin.env.zookeeper-base-sleep-time"
    value = "5555"
    run_ctest(module, testName, param, value)
