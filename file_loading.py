from urllib.parse import unquote
import json

content = r'!"#$%&' + r"'()+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~" + "\n"
dict1 = {}
dict2 = {}
for i in range(len(content)):  # 字符-编号
    dict1[content[i]] = i
for i in range(len(content)):  # 编号-字符
    dict2[str(i)] = content[i]

def decoding(name):
    with open(name, encoding="UTF-8", mode="r") as file:
        content = json.load(file)
    new = []
    for i in content:
        new.append(unquote(unquote(i)))
    return new


def decoding_password(name):
    with open(name, encoding="UTF-8", mode="r") as file:
        content = json.load(file)
    new = []
    for i in content:
        temp2 = ""
        for c in i:
            temp2 += dict2[str(dict1[c] - 1)]
        temp = unquote(temp2, encoding="UTF-8")
        new.append(temp)
    return new
