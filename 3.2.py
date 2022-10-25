import csv
import math
import re

def delete_tags(line: str):
    if line.find("\n") != -1:
        return line
    new_field = re.sub(r"\<[^>]*\>", '', line)
    new_field = re.sub(r'\s+', ' ', new_field)
    return new_field


def delete_spaces(line: str):
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
    csv_filer(list[1:], list[0])


def csv_filer(reader, list_naming):
    dict1 = dict()
    for j in range(0, len(reader)):
        for i in range(0, len(list_naming)):
            dict1[list_naming[i]] = reader[j][i]
        for i in dict1.keys():
            dict1[i] = DeleteSpace(DeleteTags(dict1[i]).replace('\n', ', '))
        print_vacancies(dict1, dic_naming)
        print()


def print_vacancies(data_vacancies, dic_naming):
    formatter(data_vacancies)
    for i in correct_sequence:
        print(f'{dic_naming[i]}: {data_vacancies[i]}')


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
    row['salary_info'] = f'{row["salary_from"]} - {row["salary_to"]} ({row["salary_currency"]}) ({salary_gross})'
    published_data = row['published_at'].split('T')[0].split('-')
    row['data_published'] = f'{published_data[2]}.{published_data[1]}.{published_data[0]}'
    row.pop('salary_from')
    row.pop('salary_to')
    row.pop('salary_currency')
    row.pop('salary_gross')
    row.pop('published_at')


name = input()
csv_reader(name)

