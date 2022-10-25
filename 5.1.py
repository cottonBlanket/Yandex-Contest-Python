import csv
import re
from var_dump import var_dump


name = input('Введите название файла: ')
filters = input('Введите параметр фильтрации: ')
sorting_field = input('Введите параметр сортировки: ')
is_reversed = input('Обратный порядок сортировки (Да / Нет): ')
numbers = input('Введите диапазон вывода: ')
columns = input('Введите требуемые столбцы: ')

class Salary:
    def __init__(self,  salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary : Salary, area_name, published_at):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = []

    def add_vacancy(self, vacancy: Vacancy):
        self.vacancies_objects.append(vacancy)


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

def get_vacancy(row: []) -> Vacancy:
    row = list(map(lambda x: delete_spaces(delete_tags(x)), row))
    salary = Salary(row[6], row[7], row[8], row[9])
    vacancy = Vacancy(row[0], row[1], row[2].split('\n'), row[3], row[4], row[5], salary, row[10], row[11])
    return vacancy


def check_file(file):
    if len(file) == 0:
        print("Пустой файл")
        exit()


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


def csv_parser(file_name):
    data_set = DataSet(file_name)
    data_set.file_name = file_name
    reader = csv_reader(file_name)
    for row in reader:
        data_set.add_vacancy(get_vacancy(row))
    return data_set


var_dump(csv_parser(name))
