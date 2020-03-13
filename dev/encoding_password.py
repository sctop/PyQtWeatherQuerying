from urllib.parse import quote
import json

content = r'!"#$%&' + r"'()+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~" + "\n"
dict1 = {}
dict2 = {}
for i in range(len(content)):  # 字符-编号
    dict1[content[i]] = i
for i in range(len(content)):  # 编号-字符
    dict2[str(i)] = content[i]


def encoding(name):
    with open(name, encoding="utf-8", mode="r") as file:
        content = json.load(file)
    new = []
    for i in content:
        temp = quote(i)
        temp2 = ""
        for i in temp:
            temp2 += dict2[str(dict1[i] + 1)]
        new.append(temp2)
    with open(name, encoding="UTF-8", mode="w") as file:
        json.dump(new, file, indent=4, ensure_ascii=False)


encoding("../password.json")
