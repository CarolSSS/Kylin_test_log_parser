import pandas as pd
import json
 
MODULE = 'common'
# Opening JSON file
with open('result/{}_default_value.json'.format(MODULE)) as json_file:
    data = json.load(json_file)
# All configs value
all_keys = data.keys()

df = pd.read_csv('config_result/{}.csv'.format(MODULE), sep=', ', engine='python')
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
                # print("num")
                # print(j)
                curr = all_generate.get(i,set())
                curr.add((j,"GOOD"))
                curr.add(('some-value',"BAD"))
                curr.add((-300,"BAD"))
                curr.add((0,"GOOD"))
                curr.add((0.1,"GOOD"))
                curr.add((100,"GOOD"))
                curr.add((600000,"GOOD"))
                all_generate[i] = curr
            # true false
            elif j == 'true' or j == 'false':
                curr = all_generate.get(i,set())
                curr.add(('true',"GOOD"))
                curr.add(('false',"GOOD"))
                all_generate[i] = curr
            # Prefix string
            elif len(j) > 1 and j[-1] == '_':
                print("prefix")
                curr = all_generate.get(i, set())
                curr.add((j,"GOOD"))
                curr.add(('KYLIN_',"GOOD"))
                curr.add(('HELLO_',"BAD"))
                all_generate[i] = curr
            # Whether this env is a Dev, QA, or Prod environment
            elif j == 'Dev' or j == 'QA' or j == 'Prod':
                curr = all_generate.get(i, set())
                curr.add((j,"GOOD"))
                curr.add(('Dev',"GOOD"))
                curr.add(('QA',"GOOD"))
                curr.add(('Prod',"GOOD"))
                all_generate[i] = curr
            # directory
            elif '/kylin' in j:
                curr = all_generate.get(i, set())
                curr.add((j,"GOOD"))
                curr.add(('/kylin/whatever',"BAD"))
                curr.add(('/Nahhhhhh',"BAD"))
                all_generate[i] = curr
            # Owner-tag
            elif '@kylin.apache.org' in j: 
                curr = all_generate.get(i, set())
                curr.add((j,"GOOD"))
                curr.add(('whoami@kylin.apache.org',"GOOD"))
                curr.add(('kylin@kylin.apache.org',"GOOD"))
                all_generate[i] = curr
            else:
                curr = all_generate.get(i, set())
                curr.add((j,"GOOD"))
                curr.add(('obviously-bad-value',"BAD"))
                all_generate[i] = curr

new_df = pd.DataFrame()

new_df = pd.DataFrame()

for i in all_generate.keys():
    # All config parameters data row
    all_cols = df[df['CONFIG_PARAMETER'].isin([i])].reset_index(drop=True)
    # print(all_cols)
    for j in range(len(all_cols)):
        curr = all_cols.loc[j]
        for k in all_generate[i]:
            # print(k)
            curr['VALUE'] = k[0]
            curr['TYPE(GOOD|BAD)'] = k[1]
            new_df = pd.concat([new_df, pd.DataFrame(curr).T], axis = 0, ignore_index= True)
            # print(new_df)

new_df.to_csv('config_result/generated_{}_vals.csv'.format(MODULE))
# print(all_generate)
# print(df['CONFIG_PARAMETER'])