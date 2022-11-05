import csv
import math
import re
from prettytable import PrettyTable
from prettytable import ALL


#static methods#
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


def get_nice_number(num):
    num = float(num)
    num = math.floor(num)
    num = '{0:,}'.format(num).replace(',', ' ')
    return num


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

correct_sequence = ['Название', 'Описание', 'Навыки', 'Опыт работы',
                    'Премиум-вакансия', 'Компания', 'Оклад', 'Название региона',
                    'Дата публикации вакансии']

is_reversed_translate = {
    "Да": True,
    "Нет": False,
    "": False
}

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

is_reversed_translate = {
    "Да": True,
    "Нет": False,
    "": False
}

experience_sorted_dict = {
    "Нет опыта": "a",
    "От 1 года до 3 лет": "aa",
    "От 3 до 6 лет": "aaa",
    "Более 6 лет": "aaaa",
}

currency_to_rub = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055,
}


class Salary:
    currency_to_rub = {"Манаты": 35.68,
                       "Белорусские рубли": 23.91,
                       "Евро": 59.90,
                       "Грузинский лари": 21.74,
                       "Киргизский сом": 0.76,
                       "Тенге": 0.13,
                       "Рубли": 1,
                       "Гривны": 1.64,
                       "Доллары": 60.66,
                       "Узбекский сум": 0.0055, }

    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def convert_to_rub(self, currency):
        value = Salary.currency_to_rub[currency]
        return ((self.salary_from + self.salary_to) / 2) * value


class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary: Salary, area_name,
                 published_at):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class InputConect:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.filters = self.append_correct_input(': ', 'Введите параметр фильтрации: ')
        self.sorting_field = input('Введите параметр сортировки: ').strip()
        self.is_reversed = input('Обратный порядок сортировки (Да / Нет): ')
        self.numbers = self.append_correct_input(' ', 'Введите диапазон вывода: ')
        self.columns = self.append_correct_input(', ', 'Введите требуемые столбцы: ')
        self.check_filters()
        self.check_sorting_parameters()

    @classmethod
    def append_correct_input(cls, splitting_char, output_txt):
        correct = []
        for i in input(output_txt).split(splitting_char):
            if i != '':
                correct.append(i)
        return correct

    def check_filters(self):
        if len(self.filters) == 1:
            print("Формат ввода некорректен")
            exit()
        if len(self.filters) != 0 and self.filters[0] not in list(dic_naming.values()):
            print("Параметр поиска некорректен")
            exit()

    def check_sorting_parameters(self):
        if self.sorting_field not in correct_sequence and self.sorting_field != "":
            print('Параметр сортировки некорректен')
            exit()
        if self.is_reversed not in is_reversed_translate:
            print('Порядок сортировки задан некорректно')
            exit()

    @classmethod
    def sorted_skills(cls, data_vacancies, is_reverse) -> list:
        sorted_data = sorted(data_vacancies, key=lambda v: len(v['Навыки'].split('\n')), reverse=is_reverse)
        return sorted_data

    @classmethod
    def sorted_salary(cls, data_vacancies, is_reverse) -> list:
        sorted_data = sorted(data_vacancies, key=lambda v:
        (float(v['Нижняя граница вилки оклада'].replace(' ', '')) * currency_to_rub[v['Идентификатор валюты оклада']]
         + float(v['Верхняя граница вилки оклада'].replace(' ', '')) * currency_to_rub[
             v['Идентификатор валюты оклада']]) / 2,
                             reverse=is_reverse)
        return sorted_data

    @classmethod
    def sorted_published_data(cls, data_vacancies, is_reverse) -> list:
        sorted_data = sorted(data_vacancies, key=lambda v:
        float(v['Дата и время публикации вакансии']
              .replace('+0300', '').replace('T', '').replace('-', '').replace(':', '')), reverse=is_reverse)
        return sorted_data

    @classmethod
    def sorted_experience(cls, data_vacancies, is_reverse) -> list:
        sorted_data = sorted(data_vacancies, key=lambda v: experience_sorted_dict[v['Опыт работы']], reverse=is_reverse)
        return sorted_data

    def sort_vacancies(self, data_vacancies) -> list:
        if self.sorting_field == "":
            return data_vacancies

        is_reverse = is_reversed_translate[self.is_reversed]
        try:
            this_sorted_func = sorted_func[self.sorting_field]
            return this_sorted_func(data_vacancies, is_reverse)
        except:
            sorted_data = sorted(data_vacancies, key=lambda v: v[self.sorting_field], reverse=is_reverse)
            return sorted_data

    def filter_vacancy(self, vacancy) -> bool:
        filter_field = self.filters[0]
        filters = self.filters[1].split(', ')
        if filter_field == 'Навыки':
            skills = vacancy[filter_field].split('\n')
            for skill in filters:
                if skill not in skills:
                    return False
                if skill == filters[-1]:
                    return True
        elif filter_field == 'Оклад':
            salary = int(delete_spaces(filters.pop()))
            return int(vacancy['Нижняя граница вилки оклада'].replace(' ', '')) <= salary <= int(
                vacancy['Верхняя граница вилки оклада'].replace(' ', ''))
        else:
            return vacancy[filter_field] == filters.pop()

    def filter_vacancies(self, data_vacancies) -> list:
        if len(self.filters) == 0:
            return data_vacancies
        filtered_data = list(filter(lambda v: self.filter_vacancy(v), data_vacancies))
        if len(filtered_data) == 0:
            print("Ничего не найдено")
            exit()
        return filtered_data

    def view_on_table(self, data_vacancies):
        my_table = PrettyTable()
        my_table.field_names = ['№'] + correct_sequence
        my_table.max_width = 20
        my_table.hrules = ALL
        my_table.align = 'l'
        data_vacancies = self.filter_vacancies(data_vacancies)
        data_vacancies = self.sort_vacancies(data_vacancies)
        for vacancy in list(data_vacancies):
            row = [data_vacancies.index(vacancy) + 1] + self.get_correct_fields(vacancy)
            my_table.add_row(row)
        correct_table = self.get_correct_table(data_vacancies, my_table)
        return correct_table

    def get_correct_table(self, data_vacancies, table):
        start = 0
        end = len(data_vacancies)
        output_fields = table.field_names
        if len(self.numbers) == 1:
            start = int(self.numbers[0]) - 1
        elif len(self.numbers) > 1:
            start = int(self.numbers[0]) - 1
            end = int(self.numbers[1]) - 1

        if len(self.columns) > 0:
            output_fields = ['№'] + self.columns

        return table.get_string(start=start, end=end, fields=output_fields)

    @classmethod
    def get_correct_fields(cls, vacancy):
        correct_fields = []
        for field in correct_sequence:
            if len(vacancy[field]) > 100:
                vacancy[field] = f'{vacancy[field][0:100]}...'
            correct_fields.append(vacancy[field])
        return correct_fields


sorted_func = {
        'Навыки': InputConect.sorted_skills,
        'Оклад': InputConect.sorted_salary,
        'Дата публикации вакансии': InputConect.sorted_published_data,
        'Опыт работы': InputConect.sorted_experience
    }


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.fields = []
        self.vacancies_objects = []

    @classmethod
    def add_more_fields(cls, vacancy):
        vacancy['Нижняя граница вилки оклада'] = get_nice_number(vacancy['Нижняя граница вилки оклада'])
        vacancy['Верхняя граница вилки оклада'] = get_nice_number(vacancy['Верхняя граница вилки оклада'])
        published_data = vacancy['Дата и время публикации вакансии'].split('T')[0].split('-')
        data_published = f'{published_data[2]}.{published_data[1]}.{published_data[0]}'
        salary_info = f'{vacancy["Нижняя граница вилки оклада"]} - {vacancy["Верхняя граница вилки оклада"]} ' \
                      f'({vacancy["Идентификатор валюты оклада"]}) ({vacancy["Оклад указан до вычета налогов"]})'
        vacancy['Оклад'] = salary_info
        vacancy['Дата публикации вакансии'] = data_published

    def get_vacancy_dict(self, row: []) -> dict:
        vacancy = dict()
        for i in range(0, len(self.fields)):
            field = dic_naming[self.fields[i]]
            vacancy[field] = delete_spaces(delete_tags(row[i]))
            if vacancy[field] in translator:
                vacancy[field] = translator[vacancy[field]]
                if field == 'Премиум-вакансия':
                    vacancy[field] = translator[vacancy[field]]
        self.add_more_fields(vacancy)
        return vacancy

    def csv_reader(self, file_name) -> []:
        with open(file_name, encoding="utf-8-sig") as test:
            unpacker = csv.reader(test)
            data = []
            length = 0
            for row in unpacker:
                if length < len(row):
                    length = len(row)
                if '' not in row and length == len(row):
                    data.append(row)
            self.check_file(data)
            self.fields = data[0]
            return data[1:]

    @classmethod
    def check_file(cls, file):
        if len(file) == 0:
            print("Пустой файл")
            exit()
        elif len(file) == 1:
            print("Нет данных")
            exit()

    def csv_parser(self):
        reader = self.csv_reader(self.file_name)
        data_all_vacancies = []
        for row in reader:
            new_vacancy = self.get_vacancy_dict(row)
            data_all_vacancies.append(new_vacancy)
        return data_all_vacancies


input_data = InputConect()
new_data_set = DataSet(input_data.file_name)
print(input_data.view_on_table(new_data_set.csv_parser()))
