import os
import re
from math import ceil, floor
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
        # filename выглядит след. образом   12-10_ClientName_937664_89x49_4+4_250_GL1+1_1SVERL3_1000.pdf

        if not re.findall(right_filename_pattern, filename):
            incorrect_files.append(filename)
            continue

        date, _, size, _, density, lam, quantity, _ = re.findall(right_filename_pattern, filename)[0]

        # Вычисляю ключи, по которым смогу обратиться к словарю formats для нахождения нужной ячейки
        key_date: int = get_date_key(date)
        key_density: int = int(density)
        key_lam: str = lam.upper() if lam else 'NON'
        key_quantity: int = get_quantity_key(quantity)

        # Вычисляю значение, которое будет внесено в таблицу-шаблон Excel
        value_size = tuple(int(n) for n in re.findall(r'\d+', size))
        value_quantity = int(quantity.replace(' ', ''))
        value_filename = 0  # Реализовать ф-цию или ф-ции которые считают вес макета в местах.

        index = 0  # get_table_index() - Далее делаем ф-цию которая получит индекс ячейки в Excel документе.

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


def get_quantity_key(quantity: str) -> int:
    result = int(quantity.replace(' ', ''))

    return 1000 if result > 500 else 500


def calculate_format(file_size: tuple) -> int or float:
    width, height = file_size
    width = (width / 89, width / 49)
    height = (height / 49, height / 89)
    result = max(width[0] * height[0], width[1] * height[1])

    return floor(result) if result > 1 else 1 if result > 0.5 else 0.5
