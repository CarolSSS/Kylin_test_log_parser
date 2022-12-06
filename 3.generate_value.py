import sys
import pandas as pd
import json
import const


def db_generate(module_name):
    git_link = "https://github.com/apache/kylin"
    sha = "63f9ac6bcd0db005f10935d88747d39fc0819ab7"
    file_path = './result/{}_map.json'.format(module_name)
    map_file = open(file_path)
    para_map = json.load(map_file)
    db = []
    header = ["REPO", "SHA", "CONFIG_PARAMETER", "TEST_NAME", "VALUE", "TYPE(GOOD|BAD)", "EXPECTATION(PASS|FAIL)"]
    for test_name in para_map:
        for i in para_map[test_name]:
            output = [git_link, sha,  i,   test_name,  "  ", " ", " "]
            db.append(output)
    db = pd.DataFrame(db, columns=header)
    return db


def auto_generate(module_name):
    # Opening JSON file
    with open('result/{}_default_value.json'.format(module_name)) as json_file:
        data = json.load(json_file)
    with open('all_paras.json') as json_file:
        data2 = json.load(json_file)
    for i in data2.keys():
        if i in data:
            data[i] = list(set(data[i] + data2[i]))
        else:
            data[i] = data2[i]
    # All configs value
    all_keys = data.keys()

    df = db_generate(module_name)
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
                    if (type(j) == type(1.0)):
                        curr = all_generate.get(i, set())
                        # curr.add((j, "GOOD"))
                        curr.add((0, "GOOD"))
                        curr.add((0.5, "GOOD"))
                        # curr.add((20.5, "GOOD"))
                    elif i[-(len("ratio") + 1):] == "ratio" or i[-(len("coefficient") + 1):] == "coefficient":
                        # curr.add((-10, "BAD"))
                        curr.add((0.9, "GOOD"))
                        curr.add((0.1, "GOOD"))
                    elif i[-(len("second") + 1):] == "second" or i[-(len("seconds")+ 1):] == "seconds":
                        curr.add((-300, "BAD"))
                        curr.add((0, "GOOD"))
                        # curr.add((0.1, "GOOD"))
                        curr.add((500, "GOOD"))
                    elif (j == 256 or j == 512 or j == 1024 or j == 2048):
                        curr = all_generate.get(i, set())
                        curr.add((512, "GOOD"))
                        # curr.add((1024, "GOOD"))
                        # curr.add((2048, "GOOD"))
                        curr.add((-100, "BAD"))    
                    else:
                        curr = all_generate.get(i, set())
                        # curr.add((500, "GOOD"))
                        curr.add((0, "GOOD"))
                        # curr.add((600000, "GOOD"))
                        curr.add((-300, "BAD"))
                    all_generate[i] = curr
                # true false
                elif j == 'true' or j == 'false':
                    curr = all_generate.get(i, set())
                    curr.add(('true', "GOOD"))
                    curr.add(('false', "GOOD"))
                    all_generate[i] = curr
                elif j == 'TRUE' or j == 'FALSE':
                    curr = all_generate.get(i, set())
                    curr.add(('TRUE', "GOOD"))
                    curr.add(('FALSE', "GOOD"))
                    all_generate[i] = curr
                # Prefix string
                elif len(j) > 1 and j[-1] == '_':
                    curr = all_generate.get(i, set())
                    curr.add((j, "GOOD"))
                    curr.add(('KYLIN_', "GOOD"))
                    # curr.add(('HELLO_', "BAD"))
                    all_generate[i] = curr
                # Whether this env is a Dev, QA, or Prod environment
                elif j == 'Dev' or j == 'QA' or j == 'Prod':
                    curr = all_generate.get(i, set())
                    # curr.add((j, "GOOD"))
                    curr.add(('Dev', "GOOD"))
                    curr.add(('QA', "GOOD"))
                    curr.add(('Prod', "GOOD"))
                    all_generate[i] = curr
                # directory
                elif '/kylin' in j:
                    curr = all_generate.get(i, set())
                    curr.add((j, "GOOD"))
                    curr.add(('/kylin/whatever', "BAD"))
                    curr.add(('/Nahhhhhh', "BAD"))
                    all_generate[i] = curr
                # Owner-tag
                elif '@kylin.apache.org' in j:
                    curr = all_generate.get(i, set())
                    curr.add((j, "GOOD"))
                    curr.add(('whoami@kylin.apache.org', "GOOD"))
                    curr.add(('kylin@kylin.apache.org', "GOOD"))
                    all_generate[i] = curr
                elif j == "query" or j == "all" or j == "job":
                    curr = all_generate.get(i, set())
                    curr.add(("query" "GOOD"))
                    curr.add(('all"', "GOOD"))
                    curr.add(('job', "GOOD"))
                    # curr.add(('VERYBADVAL', "BAD"))
                    all_generate[i] = curr
                # Manually check here
                else:
                    curr = all_generate.get(i, set())
                    curr.add((j, "GOOD"))
                    curr.add(('obviously-bad-value', "BAD"))
                    # curr.add((' ', "MANUAL"))
                    print(i)
                    all_generate[i] = curr

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
                new_df = pd.concat([new_df, pd.DataFrame(curr).T], axis=0, ignore_index=True)
                # print(new_df)

    new_df.to_csv('config_result/generated_{}_vals.csv'.format(module_name))


if __name__ == "__main__":
    auto_generate(const.MODULE_NAME)
