import os
import re
from math import ceil
import formats as fo
import openpyxl
import datetime

right_filename_pattern = r'(?i)' \
                         r'(?P<date>\d{2}-\d{2}).*?' \
                         r'(?P<OrderID>\d+)_' \
                         r'(?P<size>\d+[xх]\d+)_' \
                         r'(?P<color>\d\+\d).*?' \
                         r'(?P<density>\d{3})_' \
                         r'(?P<lam>[a-z]{2,3}\d\+\d)?.*?' \
                         r'(?P<quantity>[\d ]{3,}).*?' \
                         r'(?P<file_format>\.pdf)'


def main():
    path: str = input('Укажите путь к директории где расположены плотные макеты (250, 300, 350): ')
    filenames_to_print: list = get_filenames_to_print(path)

    incorrect_files = list()

    for filename in filenames_to_print:

        if not re.findall(right_filename_pattern, filename):
            incorrect_files.append(filename)
            continue

        date, _, size, _, density, lam, quantity, _ = re.findall(right_filename_pattern, filename)[0]

        # Вычисляю ключи, по которым смогу обратиться к словарю formats для нахождения нужной ячейки
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
    folders_pattern = r'(?i)(GL|MAT|NON|UF) ?(1\+0|1\+1)?(?=$)'

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
        exit(0)
    else:
        print(f'\n[+] Путь корректный.\nНачинаю считать макеты...\n{"=" * 35}')


def get_filenames_to_print(path: str) -> list:
    folders_list = create_folders_list(path)
    check_folders(folders_list)
    files_list = create_files_list(folders_list)

    return files_list


def str_to_date(file_date: str) -> datetime:
    current_year = datetime.datetime.today().strftime("%y")

    return datetime.datetime.strptime(f'{current_year}-{file_date}', '%y-%m-%d').date()


def get_tomorrow_date() -> list:
    if datetime.datetime.today().strftime('%a') == 'Fri':
        tomorrow = [
            (datetime.datetime.today() + datetime.timedelta(1)).date(),
            (datetime.datetime.today() + datetime.timedelta(3)).date()
        ]
    else:
        tomorrow = [(datetime.datetime.today() + datetime.timedelta(1)).date()]

    return tomorrow


def get_date_key(file_date: str) -> int:
    file_date = str_to_date(file_date)
    tomorrow = get_tomorrow_date()

    if file_date in tomorrow:
        key = 24
    elif file_date > max(tomorrow):
        key = 48
    else:
        raise ValueError('Указана уже прошедшая дата файла.')

    return key
