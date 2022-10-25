import csv
import re

file = input()
with open(file,  encoding="utf-8-sig") as test:
    unpacker = csv.reader(test)
    list = []
    l = 0
    for row in unpacker:
        if l < len(row):
            l = len(row)
        if '' not in row and l == len(row):
            list.append(row)

keys = list[0]
values = list[1:]


def DeleteTags(line: str):
    if line.find("\n") != -1:
        return line
    new_field = re.sub(r"\<[^>]*\>", '', line)
    new_field = re.sub(r'\s+', ' ', new_field).strip()
    return new_field

def DeleteSpace(line: str):
    arr = line.strip().split(' ')
    new_line = ''
    for word in arr:
        if word != '':
            new_line += word + ' '
    return new_line


dict1 = dict()
for j in range(0, len(values)):
    for i in range(0, len(keys)):
        dict1[keys[i]] = values[j][i]
    for i in dict1.keys():
        dict1[i] = DeleteSpace(DeleteTags(dict1[i]).replace('\n', ', '))
        print("{0}: {1}".format(i, dict1[i]))
    print()
