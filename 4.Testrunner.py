import importlib.util
import json
import os
import os.path
import sys
from pathlib import Path

import pandas as pd

spec = importlib.util.spec_from_file_location(
    name="my_module",  # note that ".test" is not a valid module name
    location="3.generate_value.py",
)
generate_value = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_value)

ctest_file = "../kylin/core-common/src/main/resources/ctest.properties"
working_dir = "../kylin"
git_link = "https://github.com/apache/kylin"
sha = "63f9ac6bcd0db005f10935d88747d39fc0819ab7"


def run_ctest(module_name, test_name, config_parameter, config_value):
    inject(config_parameter, config_value)
    if module_name == "query":
        command = "mvn -pl " + module_name + " test -Dtest=" + test_name
    else:
        command = "mvn -pl core-" + module_name + " test -Dtest=" + test_name
    os.chdir(working_dir)
    print("[ctest]--> change dir to " + working_dir)
    print("[ctest]--> run command : " + command)
    with os.popen(command) as output:
        if "[INFO] BUILD SUCCESS\n" in output.readlines():
            result = "PASS"
        else:
            result = "FAIL"
    if result == "PASS":
        print("[ctest]--> " + config_parameter + " " + config_value + " " + " " + "\033[32m" + result + "\033[0m")
    elif result == "FAIL":
        print("[ctest]--> " + config_parameter + " " + config_value + " " + " " + "\033[31m" + result + "\033[0m")
    return result


def file_is_exist(path):
    my_file = Path(path)
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
    file_name = 'config_result/' + module_name + "_result.csv"
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
            print("[ctest]--> current is " + str(idx) + " test, " + str(progress) + "% finished.")
            print("")
            idx = idx + 1
            fp.write("%s\n" % lines)
        print('Done')


def inject(name, config_value):
    if str(config_value) == "nan":
        config_value = " "
    with open(ctest_file, 'w') as fp:
        print("[ctest]--> ctest file at : " + ctest_file)
        print("[ctest]--> inject parameter: " + name + " = " + str(config_value))
        fp.write(name + " =" + config_value)


def delete():
    print("clear ctest File at " + ctest_file)
    os.remove(ctest_file)
    f = open(ctest_file, "w")
    f.close()


def main():
    if len(sys.argv) != 2:
        print(''' usage: python3 4.Testrunner.py + module name''')
        return 0
    print("[ctest]--> Working on Module: " + sys.argv[1])
    print("[ctest]--> Generate the Configuration Test value: ")
    # check the file exist
    # running test
    run_all_ctest(sys.argv[1])


if __name__ == "__main__":
    module = "common"
    # testName = "KylinServerDiscoveryTest#test"
    # param = "kylin.job.remote-cli-password"
    # value = ""
    # run_ctest(module, testName, param, value)
    # file_generate("1")
    # run_all_ctest("core-common")
    # mydf = file_generate("common")
    # print(mydf)
    main()
    # my_file = 'config_result/generated_common_vals_example.csv'
    # mydf = pd.read_csv(my_file, sep=',', engine='python')
    # value = mydf[mydf.CONFIG_PARAMETER == "kylin.job.remote-cli-password"]["VALUE"].head(1)
    # print(value)
    # inject(param, np.NaN)
