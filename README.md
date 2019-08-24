﻿# Многочлены

Версия 1.0
Автор: Пискунова Виктория (victory13.99@gmail.com)

## Описание
Сравнивает 2 многочлена над полем комплексных чисел (многочлены от нескольких переменных, заданных в математической форме). Программа преобразует введённые строки к многочлену, выполняет математические операции (+, -, *, / (только на число, т.к. над полем комплексных чисел), ^ (степень должна быть натуральной или 0)), сообщает об ошибке при вводе (и её позиции), если такая была, или выводит результат сравнения. А так же различает в кодах выхода равенство многочленов (0), неравенство многочленов (1), синтаксические ошибки (2).
#### Запуск приложения
Каждый многочлен должен быть введён в двойных кавычках, если строка начинается со знака "-", то перед ним должен стоять пробел. Переменной может быть любая буква латинского алфавита за исключением j, которая обозначает мнимую единицу в комплексном числе.

CLI: python main.py "(x^2 * y^4 - 4y^2x + 4)" "(xy^2 - 2)(xy^2 - 2)"

## Состав
#### Модули приложения
- polynom.py - класс многочлена, каждый многочлен представляет собой словарь с переменными в ключах, и с коэффициентами в значениях
- polynom_parser.py - класс парсера, в котором реализованы преобразованный алгоритм Дейкстры, упрощающий вычисление, и функция, преобразующая запись из постфиксной формы в многочлен с поиском ошибок в записи.
- main.py - файл запуска
- /tests - тесты