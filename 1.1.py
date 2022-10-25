question1 = input('Введите название вакансии: ')
question2 = input('Введите описание вакансии: ')
question3 = int(input('Введите требуемый опыт работы (лет): '))
question4 = int(input('Введите нижнюю границу оклада вакансии: '))
question5 = int(input('Введите верхнюю границу оклада вакансии: '))
question6 = input('Есть ли свободный график (да / нет): ')
question7 = input('Является ли данная вакансия премиум-вакансией (да / нет): ')


def print_bool(question):
    if question == 'да':
        print('True (bool)')
    else:
        print('False (bool)')


print(question1 + ' (' + type(question1).__name__ + ')')
print(question2 + ' (' + type(question2).__name__ + ')')
print(str(question3) + ' (' + type(question3).__name__ + ')')
print(str(question4) + ' (' + type(question4).__name__ + ')')
print(str(question5) + ' (' + type(question5).__name__ + ')')
print_bool(question6)
print_bool(question7)
