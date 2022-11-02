import pandas as pd
import json
 
# Opening JSON file
with open('result/common_default_value.json') as json_file:
    data = json.load(json_file)
# All configs value
all_keys = data.keys()

df = pd.read_csv('config_result/common.csv', sep=', ', engine='python')
new_df = pd.DataFrame()
# All parameters
all_paras = df['CONFIG_PARAMETER']

# Generated values for each parameter
all_generate = {}

for i in all_paras:
    if i not in all_keys:
        print("error, not found" + i)
    else:
        # Checking all values that have been appeared in our code
        for j in data[i]:
            # Number
            if j.isnumeric():
                print("num")
                print(j)
                curr = all_generate.get(i,set())
                curr.add(('some-value',"BAD"))
                curr.add((-300,"BAD"))
                curr.add((0,"GOOD"))
                curr.add((0.1,"GOOD"))
                curr.add((100,"GOOD"))
                curr.add((600000,"GOOD"))
                all_generate[i] = curr
            # Prefix string
            if len(j) > 1 and j[-1] == '_':
                print("prefix")
                curr = all_generate.get(i, set())
                curr.add(('KYLIN_',"GOOD"))
                curr.add(('HELLO_',"BAD"))
        print(data[i])
print(data)
# print(df['CONFIG_PARAMETER'])