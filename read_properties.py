import os
import pandas as pd

# Read properties from kylin default config
df = pd.DataFrame(columns =['variable', 'value'])
lines = open('data/kylin-defaults.properties', "r").readlines()
for line in lines:
    line = line.strip("\n")
    if "=" in line and line[0] != '#':
        print(line)
        q = pd.DataFrame([line.split('=', 1)],columns =['variable', 'value'])
        print(q)
        df = pd.concat([df, q])

df.to_csv('result/all_default_properties.csv')