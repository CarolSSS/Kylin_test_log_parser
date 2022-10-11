import os

# Use bash common_commands to write all test logs to common_logs file
all = os.walk("../kylin/core-common/src/test/java/org/apache/kylin/common")
PRE_LEN = len("../")
SUF_LEN = len(".java")
THRESHOLD = len('Test.java')
MODULE_NAME = "core-common"
LOG_FILE = "common_logs"

all_tests = []
match_dir = []

for x in all:
    testname = x[2]
    dir = x[0]
    dir_cleaned = dir[PRE_LEN:].replace("/", ".") + "."
    for i in testname:
        if len(i) - THRESHOLD < 0:
            continue
        if i[len(i) - THRESHOLD:] != 'Test.java':
            continue
        else:
            match_dir.append(dir +"/"+ i)
            fullName = dir_cleaned + i[:len(i) - SUF_LEN]
            all_tests.append(fullName)

all_names = []
all_commands = []
for ind, i in enumerate(match_dir):
    test_detected = False
    lines = open(i, "r").readlines()
    for line in lines:
        line = line.strip("\n")
        if '@Test' in line:
            test_detected = True
        elif test_detected:
            for words in line.split(" "):
                if len(words) > 2:
                    if words[-2:] == "()":
                        curr = all_tests[ind] +"#"+ words[:-2]
                        all_names.append(curr)
            test_detected = False

with open("commands/common_test_names.txt", "w") as output:
    for row in all_names:  
        output.write(row +'\n')

with open("commands/common_commands.txt", "w") as output:
    for row in all_names:
        # Need to change for other module here
        row_slice = row[len("kylin.core-common.src.test.java."):]
        full_dir = "../" + "Kylin_test_log_parser" +"/"+ LOG_FILE +"/" + row_slice
        curr = "mvn -pl "+ MODULE_NAME + " test -Dtest=" + row_slice + " -Dcheckstyle.skip=true"
        curr = curr + " 2>&1 | Tee "+full_dir + ".log"
        output.write(curr + '\n')
