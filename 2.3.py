import csv
import re
import math

class Vacancy:
    Middle_Salary = 0
    Name = ''
    Employer_Name = ''
    Area_Name = ''

    def __init__(self, middle_salary, name, employer_name, area_name):
        self.Middle_Salary = middle_salary
        self.Name = name
        self.Employer_Name = employer_name
        self.Area_Name = area_name


def get_correct_word(input_str, enter_type):
    repeats = ["раз", "раза", "раз"]
    rubles = ["рубль", "рубля", "рублей"]
    vac = ["вакансия", "вакансии", "вакансий"]
    skills = ["скилла", "скиллов", "скиллов"]
    cities = ["города", "городов", "городов"]
    current_mass = repeats
    if enter_type == "Rubles":
        current_mass = rubles
    elif enter_type == "Vac":
        current_mass = vac
    elif enter_type == "Skills":
        current_mass = skills
    elif enter_type == "Cities":
        current_mass = cities
    inputInt = int(input_str)
    last2Int = int(input_str[-2:])
    lastInt = int(input_str[-1])
    if (last2Int < 12 or last2Int > 14) and (lastInt >= 2 and lastInt <= 4):
        return current_mass[1]
    if last2Int != 11 and lastInt == 1:
        return current_mass[0]
    return current_mass[2]


def DeleteTags(line: str):
    if line.find("\n") != -1:
        return line
    new_field = re.sub(r"\<[^>]*\>", '', line)
    new_field = re.sub(r'\s+', ' ', new_field).strip()
    return new_field


def DeleteSpace(line: str):
    arr = line.split(' ')
    new_line = ''
    for word in arr:
        if word != '':
            new_line += word + ' '
    return new_line


def ClearLine(line: []):
    new_line = []
    for e in line:
        new_e = e.replace('\n', '## ')
        new_line.append(DeleteSpace(DeleteTags(new_e)))
    return new_line


def IsVoidFieldInLine(line_split):
    for field in line_split:
        if field == "":
            return True
    return False


def GetIndexs(line):
    indexs =dict()
    indexs['salary_from'] = line.index('salary_from')
    indexs['salary_to'] = line.index('salary_to')
    indexs['employer_name'] = line.index('employer_name')
    indexs['name'] = line.index('name')
    indexs['area_name'] = line.index('area_name')
    indexs['salary_currency'] = line.index('salary_currency')
    indexs['skills'] = line
    return indexs


def Refesh(new_props, all_props):
    for new_prop in new_props:
        try:
            all_props[new_prop] += 1
        except:
            all_props[new_prop] = 1
    return all_props


def PrintHighOrLowSalaries(middle_salaries, vacancies, typeSored):
    highOrLow = ''
    if typeSored == 'high':
        middle_salaries = sorted(middle_salaries, reverse=True)
        highOrLow = 'высокие'
    else:
        middle_salaries = sorted(middle_salaries, reverse=False)
        highOrLow = 'низкие'

    print(f'Самые {highOrLow} зарплаты:')
    printed = []
    for i in range(0, min(10, len(middle_salaries))):
        for vacancy in vacancies:
            if vacancy.Middle_Salary == middle_salaries[i] and  vacancy not in printed:
                printed.append(vacancy)
                print(f'    {i + 1}) {vacancy.Name.strip()} в компании "{vacancy.Employer_Name.strip()}" - {int(middle_salaries[i])} {get_correct_word(str(int(middle_salaries[i])), "Rubles")} (г. {vacancy.Area_Name})')
                break
    print()


def CalculateElements(all_elements):
    element_to_count = dict()
    for element in all_elements:
        element = element.strip()
        if element not in element_to_count:
            element_to_count[element] = 1
        else:
            element_to_count[element] += 1
    return element_to_count


def PrintTopSkills(all_skills):
    all_skills = CalculateElements(all_skills);
    counts_of_mentions = sorted(all_skills.values(), reverse=True)
    count_of_skill = len(all_skills.values())
    print(f'Из {count_of_skill} {get_correct_word(str(count_of_skill), "Skills")}, самыми популярными являются:')
    printed_skills = []
    for i in range(0, min(len(counts_of_mentions), 10)):
        for skill in all_skills:
            if all_skills[skill] == counts_of_mentions[i] and  i < len(counts_of_mentions) and skill not in printed_skills:
                printed_skills.append(skill)
                print(f'    {i + 1}) {skill.strip()} - упоминается '
                        f'{counts_of_mentions[i]} {get_correct_word(str(counts_of_mentions[i]), "p")}')
                break
    print()


def DeleteSmallCities(all_cities, vacancies_count):
    border = math.floor(0.01 * vacancies_count)
    big_cities = {}
    for city in all_cities:
        if all_cities[city] >= border:
            big_cities[city] = all_cities[city]
    return big_cities

def DetermineCitiesWithBigSalary(all_cities, vacancies):
    middle_salaries_in_cities = {}
    vacancies_count_in_cities = {}
    for city in all_cities:
        sum_middle_salaries = 0
        vacancies_count_in_city = 0
        for vacancy in vacancies:
            if vacancy.Area_Name == city:
                if vacancy.Area_Name == city:
                    sum_middle_salaries += vacancy.Middle_Salary
                    vacancies_count_in_city += 1
                if vacancies_count_in_city >= 1:
                    middle_salaries_in_cities[vacancy.Area_Name] = int(sum_middle_salaries/vacancies_count_in_city)
    return middle_salaries_in_cities



def PrintTopCities(all_cities, vacancies):
    all_cities = CalculateElements(all_cities)
    vacancies_counts = len(vacancies)
    all_cities_count = len(all_cities)
    all_cities = DeleteSmallCities(all_cities, vacancies_counts)
    middle_salaries_in_cities = DetermineCitiesWithBigSalary(all_cities, vacancies)
    middle_salaries = sorted(middle_salaries_in_cities.values(), reverse=True)
    print(f'Из {all_cities_count} {get_correct_word(str(len(all_cities)), "Cities")}, самые высокие средние ЗП:')
    printed_cities = []
    for i in range(0, min(len(middle_salaries), 10)):
        for city in middle_salaries_in_cities:
            if middle_salaries[i] == middle_salaries_in_cities[city] and city not in printed_cities:
                printed_cities.append(city)
                print(f'    {i + 1}) {city} - средняя зарплата {int(middle_salaries[i])} {get_correct_word(str(int(middle_salaries[i])), "Rubles")} ({all_cities[city]} {get_correct_word(str(all_cities[city]), "Vac")})')
                break


#'vacancies.csv'
name = input()
with open(name,  encoding="utf-8-sig") as test:
    file = csv.reader(test)
    first_line = ''
    countColumns = 0
    all_skills = []
    all_cities = []
    middle_salaries = []
    vacancies = []
    flag = True
    list = []
    l = 0
    for line in file:
        if flag:
            flag = False
            first_line = line
            countColumns = len(line)
        else:
            if len(line) < countColumns or IsVoidFieldInLine(line) or line[first_line.index('salary_currency')] != 'RUR':
                continue
            line = ClearLine(line)
            middle_salary = math.floor((float(line[first_line.index('salary_to')]) + float(line[first_line.index('salary_from')])) / 2)
            middle_salaries.append(middle_salary)
            area_name = line[first_line.index('area_name')][0: len(line[first_line.index('area_name')]) - 1]
            vacancies.append(Vacancy(middle_salary,
                                     line[first_line.index('name')],
                                     line[first_line.index('employer_name')],
                                     area_name))
            all_skills.extend(line[first_line.index('key_skills')].split('## '))
            all_cities.append(area_name)

    PrintHighOrLowSalaries(middle_salaries, vacancies, 'high')
    PrintHighOrLowSalaries(middle_salaries, vacancies, 'low')
    PrintTopSkills(all_skills)
    PrintTopCities(all_cities, vacancies)



