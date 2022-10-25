import csv
import math
import re
from prettytable import PrettyTable
from prettytable import ALL
import os


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
    return new_line.strip()


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
'published_at': 'Дата и время публикации вакансии',
'data_published': 'Дата публикации вакансии',
'salary_info': 'Оклад'}

currencies = {
"AZN": "Манаты",
"BYR": "Белорусские рубли",
"EUR": "Евро",
"GEL": "Грузинский лари",
"KGS": "Киргизский сом",
"KZT": "Тенге",
"RUR": "Рубли",
"UAH": "Гривны",
"USD": "Доллары",
"UZS": "Узбекский сум"}

experience = {
"noExperience": "Нет опыта",
"between1And3": "От 1 года до 3 лет",
"between3And6": "От 3 до 6 лет",
"moreThan6": "Более 6 лет" }

bools = {
    "true": "Да",
    "false": "Нет",
}

correct_sequence = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_info', 'area_name', 'data_published']
correct_sequence_in_russian = ['№']
for field in correct_sequence:
    correct_sequence_in_russian.append(dic_naming[field])
data_all_vacancies = []
my_table = PrettyTable()
my_table.field_names = correct_sequence_in_russian
my_table.max_width = 20
my_table.hrules = ALL
my_table.align = 'l'


def get_nice_number(num):
    num = float(num)
    num = math.floor(num)
    num = '{0:,}'.format(num).replace(',', ' ')
    return num


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
        if len(list) == 0:
            print("Пустой файл")
            return
        elif len(list) == 1:
            print("Нет данных")
            return
    csv_filer(list[1:], list[0])


def csv_filer(reader, list_naming):
    dict1 = dict()
    for j in range(0, len(reader)):
        for i in range(0, len(list_naming)):
            dict1[list_naming[i]] = reader[j][i]
        for i in dict1.keys():
            dict1[i] = DeleteSpace(DeleteTags(dict1[i]))
            if len(dict1[i]) > 100: dict1[i] = f'{dict1[i][0:100]}...'
        data = formatter(dict1)
        data.insert(0, j + 1)
        data_all_vacancies.append(data)
    view_on_table(data_all_vacancies)


def formatter(row):
    row['premium'] = bools[row['premium'].lower()]
    row['salary_gross'] = bools[row['salary_gross'].lower()]
    row['salary_currency'] = currencies[row['salary_currency']]
    row['experience_id'] = experience[row['experience_id']]
    salary_gross = ''
    if row['salary_gross'] == 'Да': salary_gross = 'Без вычета налогов'
    elif row['salary_gross'] == 'Нет': salary_gross = 'С вычетом налогов'
    row['salary_from'] = get_nice_number(row['salary_from'])
    row['salary_to'] = get_nice_number(row['salary_to'])
    published_data = row['published_at'].split('T')[0].split('-')
    data_published = f'{published_data[2]}.{published_data[1]}.{published_data[0]}'
    salary_info = f'{row["salary_from"]} - {row["salary_to"]} ({row["salary_currency"]}) ({salary_gross})'
    row.pop('salary_from')
    row.pop('salary_to')
    row.pop('salary_currency')
    row.pop('salary_gross')
    row.pop('published_at')
    result = list(row.values())
    result.insert(6, salary_info)
    result.append(data_published)
    return result


def view_on_table(data_vacancies):
    for vacancy in data_vacancies:
        my_table.add_row(vacancy)
    print(my_table)


name = input()
csv_reader(name)



