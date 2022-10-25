import csv
import math
import re
from prettytable import PrettyTable
from prettytable import ALL

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


def append_correct_input(splitting_char):
    list = []
    for i in input().split(splitting_char):
        if i != '':
            list.append(i)
    return list


def check_filters(filters):
    if len(filters) == 1:
        print("Формат ввода некорректен")
        exit()
    if len(filters) != 0 and filters[0] not in list(dic_naming.values()):
        print("Параметр поиска некорректен")
        exit(0)


name = input()
filters = append_correct_input(': ')
check_filters(filters)
numbers = append_correct_input(' ')
columns = append_correct_input(', ')


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


translator = {
"AZN": "Манаты",
"BYR": "Белорусские рубли",
"EUR": "Евро",
"GEL": "Грузинский лари",
"KGS": "Киргизский сом",
"KZT": "Тенге",
"RUR": "Рубли",
"UAH": "Гривны",
"USD": "Доллары",
"UZS": "Узбекский сум",
"noExperience": "Нет опыта",
"between1And3": "От 1 года до 3 лет",
"between3And6": "От 3 до 6 лет",
"moreThan6": "Более 6 лет",
"True": "Без вычета налогов",
"False": "С вычетом налогов",
"Без вычета налогов": "Да",
"С вычетом налогов": "Нет"
}

correct_sequence = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']
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


def check_file(file):
    if len(file) == 0:
        print("Пустой файл")
        exit()
    elif len(file) == 1:
        print("Нет данных")
        exit()


def add_more_fields(vacancy):
    vacancy['Нижняя граница вилки оклада'] = get_nice_number(vacancy['Нижняя граница вилки оклада'])
    vacancy['Верхняя граница вилки оклада'] = get_nice_number(vacancy['Верхняя граница вилки оклада'])
    published_data = vacancy['Дата и время публикации вакансии'].split('T')[0].split('-')
    data_published = f'{published_data[2]}.{published_data[1]}.{published_data[0]}'
    salary_info = f'{vacancy["Нижняя граница вилки оклада"]} - {vacancy["Верхняя граница вилки оклада"]} ({vacancy["Идентификатор валюты оклада"]}) ({vacancy["Оклад указан до вычета налогов"]})'
    vacancy['Оклад'] = salary_info
    vacancy['Дата публикации вакансии'] = data_published


def get_vacancy_dict(row: []) -> dict:
    vacancy = dict()
    for i in range(0, len(fields)):
        field = dic_naming[fields[i]]
        vacancy[field] = delete_spaces(delete_tags(row[i]))
        if vacancy[field] in translator:
            vacancy[field] = translator[vacancy[field]]
            if field == 'Премиум-вакансия':
                vacancy[field] = translator[vacancy[field]]
    add_more_fields(vacancy)
    return vacancy


def csv_reader(file_name) -> []:
    with open(file_name, encoding="utf-8-sig") as test:
        unpacker = csv.reader(test)
        data = []
        length = 0
        for row in unpacker:
            if length < len(row):
                length = len(row)
            if '' not in row and length == len(row):
                data.append(row)
        check_file(data)
        global fields
        fields = data[0]
        return data[1:]


def view_on_table_decorator(func):
    def view_on_table(name):
        data_vacancies = func(name)
        number_vacancy = 0
        for vacancy in data_vacancies:
                if filter_vacancy(vacancy, filters):
                    number_vacancy += 1
                    row = [number_vacancy] + get_correct_fields(vacancy)
                    my_table.add_row(row)
        if number_vacancy == 0:
            print("Ничего не найдено")
            exit()
        correct_table = get_correct_table(data_vacancies)
        return correct_table

    return view_on_table


@view_on_table_decorator
def csv_parser(file_name):
    reader = csv_reader(file_name)
    data_all_vacancies = []
    for j in range(0, len(reader)):
        new_vacancy = get_vacancy_dict(reader[j])
        data_all_vacancies.append(new_vacancy)
    return data_all_vacancies


def get_correct_fields(vacancy):
    correct_fields = []
    for field in correct_sequence:
        if len(vacancy[field]) > 100:
            vacancy[field] = f'{vacancy[field][0:100]}...'
        correct_fields.append(vacancy[field])
    return correct_fields


def filter_vacancy(vacancy, filters) -> bool:
    if len(filters) == 0:
        return True
    filter_field = filters[0]
    filters = filters[1].split(', ')
    if filter_field == 'Навыки':
        skills = vacancy[filter_field].split('\n')
        for skill in filters:
            if skill not in skills:
                return False
            if skill == filters[-1]:
                return True
    elif filter_field == 'Оклад':
        salary = int(delete_spaces(filters.pop()))
        return int(vacancy['Нижняя граница вилки оклада'].replace(' ', '')) <= salary <= int(vacancy['Верхняя граница вилки оклада'].replace(' ', ''))
    else:
        return vacancy[filter_field] == filters.pop()


def get_correct_table(data_vacancies):
    start = 0
    end = len(data_vacancies)
    output_fields = my_table.field_names
    if len(numbers) == 1:
        start = int(numbers[0]) - 1
    elif len(numbers) > 1:
        start = int(numbers[0]) - 1
        end = int(numbers[1]) - 1

    if len(columns) > 0:
        output_fields = ['№'] + columns

    return my_table.get_string(start=start, end=end, fields=output_fields)


print(csv_parser(name))