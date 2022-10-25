question1 = input('Введите название вакансии: ')
question2 = input('Введите описание вакансии: ')
question3 = int(input('Введите требуемый опыт работы (лет): '))
question4 = int(input('Введите нижнюю границу оклада вакансии: '))
question5 = int(input('Введите верхнюю границу оклада вакансии: '))
question6 = input('Есть ли свободный график (да / нет): ')
question7 = input('Является ли данная вакансия премиум-вакансией (да / нет): ')


years = ("год" if 11 <= question3 <= 19 or question3 % 10 == 1 else
         "года" if 2 <= question3 % 10 <= 4 else
         "лет")

rubles = ''
average = int((question4 + question5) / 2)
i = average % 1000

if average % 100 != 11 and i == 1 :
    rubles = 'рубль'
elif i > 1 and i < 5 and not (average % 100 > 11 and average % 100 < 20):
    rubles = 'рубля'
else:
    rubles = 'рублей'


print(question1)
print('Описание: ' + question2)
print('Требуемый опыт работы: ' + str(question3) + ' ' + years)
print('Средний оклад: ' + str(average) + ' ' + rubles)
print('Свободный график: ' + question6)
print('Премиум-вакансия: ' + question7)
