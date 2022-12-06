#!/bin/bash


#!/bin/bash

function run() {
    # python3 0.read_properties.py
    # python3 1.generate_all_tests.py
    # cd ../kylin
    # sh ../Kylin_test_log_parser/commands/tool_commands.sh
    # cd ../Kylin_test_log_parser
    # python3 2.map_logs_generate_default.py
    # python3 3.generate_value.py
    # python3 4.Testrunner.py
    echo "$project"_commands.sh
}

project=$1
function main() {
    if [ -z $project ]
    then
      echo 1
    else
      echo $project
      run        
    fi
}

main