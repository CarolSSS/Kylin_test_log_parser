import os
from pickle import TRUE

all = os.walk("../kylin/core-common/src/test/java/org/apache/kylin/common")
# sub1 = [x[2] for x in all]
all_tests = []
match_dir = []
THRESHOLD = len('Test.java')
for x in all:
    testname = x[2]
    dir = x[0]
    dir_cleaned = dir[3:].replace("/", ".") + "."
    for i in testname:
        if len(i) - THRESHOLD < 0:
            continue
        if i[len(i) - THRESHOLD:] != 'Test.java':
            continue
        else:
            match_dir.append(dir +"/"+ i)
            fullName = dir_cleaned+i[:len(i) - 5]
            all_tests.append(fullName)

print(all_tests)

print(match_dir)

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
                        # print(i)
                        curr = all_tests[ind] +"#"+ words[:-2]
                        all_names.append(curr)
                        # curr_command = "mvn -pl core-common test -Dtest="
                        # all_commands.append()

            test_detected = False



with open("common_test_names.txt", "w") as output:
    for row in all_names:  
        output.write(row +'\n')

with open("common_commands.txt", "w") as output:
    for row in all_names:
        # Need to change for other module
        curr = "mvn -pl core-common test -Dtest=" + row[len("kylin.core-common.src.test.java."):] + " -Dcheckstyle.skip=true"
        output.write(curr + '\n')

# print(sub1)