import csv
import re

def DeleteTags(line: str):
    if line.find("\n") != -1:
        return line
    new_field = re.sub(r"\<[^>]*\>", '', line)
    new_field = re.sub(r'\s+', ' ', new_field)
    return new_field

def DeleteSpace(line: str):
    arr = line.strip().split(' ')
    new_line = ''
    for word in arr:
        if word != '':
            new_line += word + ' '
    return new_line


dic_naming = {'name': 'Название',
'description': 'Описание',
'key_skills': 'Навыки',
'experience_id': 'Опыт работы',
'premium': 'Премиум-вакансия',
'employer_name': 'Компания',
'salary_from': 'Нижняя граница вилки оклада',
'salary_to': 'Верхняя граница вилки оклада',
'salary_gross': 'Оклад указан до вычета налогов',
'salary_currency': 'Идентификатор валюты оклада',
'area_name': 'Название региона',
'published_at': 'Дата и время публикации вакансии'}


def csv_reader(file_name):
    with open(file_name, encoding="utf-8-sig") as test:
        unpacker = csv.reader(test)
        list = []
        l = 0
        for row in unpacker:
            if l < len(row):
                l = len(row)
            if '' not in row and l == len(row):
                list.append(row)
    csv_filer(list[1:], list[0])


def csv_filer(reader, list_naming):
    dict1 = dict()
    for j in range(0, len(reader)):
        for i in range(0, len(list_naming)):
            dict1[list_naming[i]] = reader[j][i]
        for i in dict1.keys():
            if dict1[i].lower() == 'false':
                dict1[i] = 'Нет'
            if dict1[i].lower() == 'true':
                dict1[i] = 'Да'
            dict1[i] = DeleteSpace(DeleteTags(dict1[i]).replace('\n', ', '))
        print_vacancies(dict1, dic_naming)
        print()

def print_vacancies(data_vacancies, dic_naming):
    for i in data_vacancies:
        print(f'{dic_naming[i]}: {data_vacancies[i]}')

name = input()
csv_reader(name)


