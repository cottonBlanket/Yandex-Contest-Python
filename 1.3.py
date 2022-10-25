def uncorrect():
    print('Данные некорректны, повторите ввод')


def input_this(question, answer_type):
    while True:
        answer = input(question)
        if answer_type == 'str' and len(answer):
            return answer
        if answer_type == 'int':
            try:
                answer = int(answer)
                return answer
            except:
                a = 1
        if answer_type == 'bool' and answer in ('да', 'нет'):
            return answer
        uncorrect()


question1 = input_this('Введите название вакансии: ', 'str')
question2 = input_this('Введите описание вакансии: ', 'str')
question3 = input_this('Введите требуемый опыт работы (лет): ', 'int')
question4 = input_this('Введите нижнюю границу оклада вакансии: ', 'int')
question5 = input_this('Введите верхнюю границу оклада вакансии: ', 'int')
question6 = input_this('Есть ли свободный график (да / нет): ', 'bool')
question7 = input_this('Является ли данная вакансия премиум-вакансией (да / нет): ', 'bool')

years = ("год" if 11 <= question3 <= 19 or question3 % 10 == 1 else
         "года" if 2 <= question3 % 10 <= 4 else
         "лет")

rubles = ''
average = int((question4 + question5) / 2)
i = average % 1000

if average % 100 != 11 and i == 1 :
    rubles = 'рубль'
elif i > 1 and i < 5 and not(average % 100 > 11 and average % 100 < 20):
    rubles = 'рубля'
else:
    rubles = 'рублей'


print(question1)
print('Описание: ' + question2)
print('Требуемый опыт работы: ' + str(question3) + ' ' + years)
print('Средний оклад: ' + str(average) + ' ' + rubles)
print('Свободный график: ' + question6)
print('Премиум-вакансия: ' + question7)
