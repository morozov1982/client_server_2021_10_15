"""
1. Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV.
Для этого:
    a. Создать функцию get_data(), в которой в цикле осуществляется
       перебор файлов с данными, их открытие и считывание данных.
       В этой функции из считанных данных необходимо
       с помощью регулярных выражений извлечь значения параметров
       «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
       Значения каждого параметра поместить в соответствующий список.
       Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
       В этой же функции создать главный список для хранения данных отчета — например,
       main_data — и поместить в него названия столбцов отчета в виде списка:
       «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
       Значения для этих столбцов также оформить в виде списка
       и поместить в файл main_data (также для каждого файла);
    b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
       В этой функции реализовать получение данных через вызов функции get_data(),
       а также сохранение подготовленных данных в соответствующий CSV-файл;
    c. Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import os
import re

from chardet import detect

DATA_DIR_NAME = 'data'
OUTPUT_FILE_NAME = 'main_data.csv'
HEADERS = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']


def find_value(content, phrase):
    result = re.search(phrase + ":(.*)\n", content)
    return result.groups()[0].strip() or None


def get_encoded_content(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        file_encoding = detect(file_content)['encoding']
        return file_content.decode(file_encoding)


def get_data(file_names):
    main_data = [HEADERS]
    # os_prod_list, os_name_list, os_code_list, os_type_list - не пригодились

    for list_num, file_name in enumerate(file_names, 1):
        main_data.append([])
        file_path = os.path.join(DATA_DIR_NAME, file_name)

        encoded_content = get_encoded_content(file_path)

        for header in HEADERS:
            value = find_value(encoded_content, header)
            main_data[list_num].append(value)

    return main_data


def write_to_csv(csv_link):
    file_names = os.listdir(DATA_DIR_NAME)
    data = get_data(file_names)
    with open(csv_link, 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        for row in data:
            file_writer.writerow(row)


write_to_csv(OUTPUT_FILE_NAME)


# ну и потренируемся в чтении ;-)
with open(OUTPUT_FILE_NAME, 'r', encoding='utf-8') as file:
    READER = csv.reader(file)
    for row in READER:
        print(row)
