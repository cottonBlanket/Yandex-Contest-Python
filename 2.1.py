import csv
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

print(keys)
print(values)
