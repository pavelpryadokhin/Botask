# Структура квиза
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Что делает следующий код? \ndef a(b, c, d): \n   pass',
        'options': [
            'Определяет список и инициализирует его', 'Определяет функцию, которая ничего не делает',
            'Определяет функцию, которая передает параметры', 'Определяет пустой класс'
        ],
        'correct_option': 1
    },
    {
        'question': 'Что выведет следующая программа? \n a = [1,2,3,None,(),[],] \n print(len(a))',
        'options': ['Syntax Error', '4', '5', '6'],
        'correct_option': 3
    },
    {
        'question': 'Что выведет следующий код? \n d = lambda p: p * 2 \n t = lambda p: p * 3 \n x = 2 \n x = d(x) \n x = t(x) \n x = d(x) \n print(x)',
        'options': ['7', '12', '24', '36'],
        'correct_option': 2
    },
    {
        'question': 'Что выведет следующий фрагмент кода? \n x = 4.5 \n y = 2 \n print(x // y)',
        'options': ['2.0', '2.25', '9.0', '20.25'],
        'correct_option': 0
    },
    {
        'question': "Что будет напечатано? \n kvps = {'user','bill', 'password','hillary'} \n print(kvps['password'])",
        'options': ['bill', 'password', 'hillary', 'Ничего. TypeError.'],
        'correct_option': 3
    },
    {
        'question': 'Что будет напечатано? \n name = "snow storm" \n print("%s" % name[6:8])',
        'options': ['st', 'sto', 'to', 'Syntax Error'],
        'correct_option': 2
    },
    {
        'question': 'Какой результат будет у следующего кода? \ndef func(x): \n   return x * 2 \nfunc(3) + func(4)',
        'options': ['11', '14', '7', 'Неопределённый'],
        'correct_option': 1
    },
    {
        'question': 'Что будет напечатано? \n a = [1, 2, 3] \n b = a \n b.append(4) \n print(a)',
        'options': ['[1, 2, 3]', '[1, 2, 3, 4]', 'TypeError', 'None'],
        'correct_option': 1
    }

]
