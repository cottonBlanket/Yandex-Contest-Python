import csv
import math
import re
from prettytable import PrettyTable
from prettytable import ALL


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

correct_sequence = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']
# correct_sequence_in_russian = ['№']
# for field in correct_sequence:
#     correct_sequence_in_russian.append(dic_naming[field])
data_all_vacancies = {}
my_table = PrettyTable()
my_table.field_names = ['№'] + correct_sequence
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
    for j in range(0, len(reader)):
        dict1 = dict()
        for i in range(0, len(list_naming)):
            dict1[dic_naming[list_naming[i]]] = reader[j][i]
        for i in dict1.keys():
            dict1[i] = DeleteSpace(DeleteTags(dict1[i]))
            if len(dict1[i]) > 100:
                dict1[i] = f'{dict1[i][0:100]}...'
        formatter(dict1)
        data_all_vacancies[j + 1] = dict1
    view_on_table(data_all_vacancies)


def formatter(row):
    row[dic_naming['premium']] = bools[row[dic_naming['premium']].lower()]
    row[dic_naming['salary_gross']] = bools[row[dic_naming['salary_gross']].lower()]
    row[dic_naming['salary_currency']] = currencies[row[dic_naming['salary_currency']]]
    row[dic_naming['experience_id']] = experience[row[dic_naming['experience_id']]]
    salary_gross = ''
    if row[dic_naming['salary_gross']] == 'Да': salary_gross = 'Без вычета налогов'
    elif row[dic_naming['salary_gross']] == 'Нет': salary_gross = 'С вычетом налогов'
    row[dic_naming['salary_from']] = get_nice_number(row[dic_naming['salary_from']])
    row[dic_naming['salary_to']] = get_nice_number(row[dic_naming['salary_to']])
    published_data = row[dic_naming['published_at']].split('T')[0].split('-')
    data_published = f'{published_data[2]}.{published_data[1]}.{published_data[0]}'
    salary_info = f'{row[dic_naming["salary_from"]]} - {row[dic_naming["salary_to"]]} ({row[dic_naming["salary_currency"]]}) ({salary_gross})'
    row[dic_naming['salary_info']] = salary_info
    row[dic_naming['data_published']] = data_published


def get_correct_fields(vacancy):
    correct_fields = []
    for field in correct_sequence:
        correct_fields.append(vacancy[field])
    return correct_fields


def view_on_table(data_vacancies):
    for vacancy in data_vacancies:
        row = [vacancy] + get_correct_fields(data_vacancies[vacancy])
        my_table.add_row(row)
    correct_table = get_correct_table(data_vacancies)

    print(correct_table)


def get_correct_table(data_vacancies):
    start = 0
    end = len(data_vacancies)
    output_fields = my_table.field_names
    if len(numbers) == 1:
        start = int(numbers[0]) - 1
    elif len(numbers) > 1:
        start = int(numbers[0]) - 1
        end = int(numbers[1]) - 1

    if len(fields) > 0:
        output_fields = ['№'] + fields

    return my_table.get_string(start=start, end=end, fields=output_fields)


def append_correct_input(splitting_char):
    list = []
    for i in input().split(splitting_char):
        if i != '':
            list.append(i)
    return list

name = input()
#filters = append_correct_input(': ')
numbers = append_correct_input(' ')
fields = append_correct_input(', ')

csv_reader(name)



