import requests
page = requests.get("https://kylin.apache.org/docs30/install/configuration.html")
import re
import pandas as pd

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())

# print(list(soup.children))
all_li =[]
mydivs = soup.findAll('code',{"class": "highlighter-rouge"})
last = None
flag = False
for div in mydivs: 
    # if (div["class"] == "highlighter-rouge"):
    if div.parent != last:
        if flag == False:
            if(div.parent.parent.find_previous('p')):
                if (div.parent.parent.find_previous('p').text == 'This section introduces Kylin Deployment related configuration.'):
                    flag = True
        if flag:
            all_li.append(div.parent)
    last = div.parent

all_para = {}
all_descriptions = {}
for i in all_li:
    if i.name != 'li':
        continue
    para = i.findAll('code',{"class": "highlighter-rouge"})[0].string
    # Not interested in this case
    if para[-2:] ==".*":
        continue
    
    if "=" in para:
        all_parts = para.split("=")
        curr = all_para.get(all_parts[0],set())
        # If '=' inside
        para = all_parts[0]
        curr.add(all_parts[1])
    else:
        curr = all_para.get(para,set())
    print(para)

    # Add all highlighted
    for j in i.findAll('code',{"class": "highlighter-rouge"})[1:]:
        curr.add(j.string)
    # print(i.text)
    all_texts = i.text.split(':', 2)
    # There is content
    description = ''
    # print(i)
    if len(all_texts) > 1:
        description = i.text.split(':', 2)[1].strip()
        for j in i.findAll('em'):
            curr.add(j.string)
        all_default = re.split("default value is ", description)
        for i in all_default[1:]:
            raw = re.split(" ", i)[0]
            if raw[-1] =='.' or raw[-1] ==',':
                raw = raw[:-1]
            if raw[-1] ==')':
                raw = raw.split("(")[0]
                print(raw)
            
            curr.add(raw)
            print(raw)

    all_para[para] = curr

    all_descriptions[para] = description
    print("====")


# print(all_para)
    # print(para)
    # print()
    # for j in i.findAll('code',{"class": "highlighter-rouge"}):
    #     print(j.string)
    # print("===")
print(len(all_li))
#/html/body/div/div/div[1]/div/div/article/ul[9]/li[1]/code

# print(soup.findNext("h3",{"id": "kylin-deploy"}))
#document.querySelector("#pjax > article > ul:nth-child(42) > li:nth-child(1)")
all_para_li = {}
for i in all_para.keys():
    all_para_li[i] = list(all_para[i])

import json
with open("all_paras.json", "w") as outfile:
    json.dump(all_para_li, outfile, indent=2)

with open("all_paras_descriptions.json", "w") as outfile:
    json.dump(all_descriptions, outfile, indent=2)

tsv_dump = {"name":[], "val":[], "description":[]}
for i in all_para.keys():
    if len(all_para_li[i]) == 0:
        val = ""
    else:
        val = all_para_li[i][0]
    tmp = tsv_dump["name"]
    tmp.append(i)
    tsv_dump["name"] = tmp

    tmp = tsv_dump["val"]
    tmp.append(val)
    tsv_dump["val"] = tmp

    tmp = tsv_dump["description"]
    tmp.append(all_descriptions[i])
    tsv_dump["description"] = tmp

df = pd.DataFrame(tsv_dump)

df.to_csv("kylin-common-default.tsv",sep="\t",index=False,header=False)