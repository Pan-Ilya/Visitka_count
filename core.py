import os
import re
from math import ceil
import formats as fo
import openpyxl
import datetime

right_filename_pattern = r'(?P<date>\d{2}-\d{2}).*?' \
                         r'(?P<size>\d+[xXхХ]\d+).*?' \
                         r'(?P<density>\d{3})_' \
                         r'(?P<lam>\w{2,3}\d\+\d)?.*?' \
                         r'(?P<quantity>[\d ]{3,}).*?' \
                         r'(?P<file_format>\.pdf)'


def main():
    path: str = input('Укажите путь к директории где расположены плотные макеты (250, 300, 350): ')
    folder_names_with_files: list = create_folders_list(path)
    check_folders(folder_names_with_files)
    filenames_to_print: list = create_files_list(folder_names_with_files)
    incorrect_files = list()

    for filename in filenames_to_print:

        if not re.findall(right_filename_pattern, filename):
            incorrect_files.append(filename)
            continue

        date, size, density, lam, quantity, _ = re.findall(right_filename_pattern, filename)[0]
        date = 0  # get_date() - Реализовать ф-цию формирующую дату (24 или 48)
        size = tuple(int(n) for n in re.findall(r'\d+', size))
        density = 0
        lam = 0
        quantity = int(quantity.replace(' ', ''))
        total_value = 0  # Реализовать ф-цию или ф-ции которые считают вес макета в местах.

        index = 0  # get_table_index() - Далее делаем ф-цию которая получит индекс ячейки в Excel документе.
        # Берет во внимание параметры выше и словарь с индексами из файла formats.py

        # Затем записываем значение total_value в таблицу - Excel по указанному index-у.
        # На этом основной цикл программы окончен.

    # Далее записываем в ячейку А1 таблицы Excel текущую дату.
    # После чего записываем все имена неопознанных файлов из списка incorrect_files в таблицу Excel начиная
    # с ячейки А40 и ниже (А41, А42, А43 ...)

    # Далее можно вывести информативные принты о статусе работы.
    # Сохраняем полученный Excel документ под новым именем. Таким образом оставляя шаблон template.xlsx всегда чистым.
    # Добавляем финальный принт об успешном выполнении работы.


def create_folders_list(path: str) -> list:
    folders_list = list()
    content = os.scandir(path)
    folders_pattern = r'(?i)(GL|MAT|NON|SOFT|UF) ?(1\+0|1\+1)?(?=$)'

    for obj in content:
        if obj.is_dir() and re.match(folders_pattern, obj.name):
            folders_list.append(obj)

    return folders_list


def create_files_list(folder_names_list: list) -> list:
    files_list = list()

    for folder_name in folder_names_list:
        for dirpath, dirnames, filenames in os.walk(folder_name):
            if filenames:
                files_list.extend(filenames)

    return files_list


def check_folders(folder_names: list) -> None:
    if not folder_names:
        print('[-] По указанному адресу нету папок с плотными макетами.')
    else:
        print(f'\n[+] Путь корректный.\nНачинаю считать макеты...\n{"=" * 35}')
