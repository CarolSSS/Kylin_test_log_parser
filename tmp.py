import pandas as pd

li = []
with open('commands/common_test_names.txt') as f:
    lines = f.readlines()

for i in lines:
    li.append(i[:-1])


print(li)