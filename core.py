import os
import re
from math import ceil, floor
import formats as fo
import patterns
import openpyxl
import datetime
import time


def main():
    path: str = input('Укажите путь к директории где расположены плотные макеты (250, 300, 350):\n')

    try:
        filenames_to_print: list = get_filenames_to_print(path)
        incorrect_files = list()
    except FileNotFoundError as fne:
        print(f'[-] {fne}')
        finish_program(code=1, time_sleep=3)

    try:
        excel_file = openpyxl.load_workbook('template.xlsx')
        sheet = excel_file.active
    except FileNotFoundError:
        print('[-] Отсутствует файл - шаблон Excel.')
        finish_program(code=1, time_sleep=3)

    for filename in filenames_to_print:
        # filename выглядит след. образом:
        # 12-10_ClientName_937664_89x49_4+4_250_GL1+1_1SVERL3_1000.pdf

        try:
            check_filename(filename)
            date, _, size, _, density, lam, quantity, _ = re.findall(patterns.right_filename_pattern, filename)[0]
            # 12-10 _ 89x49  _  250   GL1+1   1000    _

            # Вычисляю ключи, по которым смогу обратиться к словарю template_cells_structure для нахождения имени
            # нужной ячейки.
            key_date: int = get_date_key(date)
            key_density: int = int(density)
            key_lam: str = lam.upper() if lam else 'NON'
            key_quantity: int = 1000 if get_quantity(quantity) > 500 else 500

            # Вычисляю значение, которое будет внесено в ту самую ячейку таблицы - шаблона Excel.
            filename_total_space: int = get_filename_total_space(size, quantity)

            # Достаю имя ячейки из словаря template_cells_structure и записываю в таблицу - шаблон Excel значение.
            index: str = Index.get_index(den=key_density,
                                         lam=key_lam,
                                         quan=key_quantity,
                                         dat=key_date)
            Index.add_value(sheet=sheet,
                            index=index,
                            value=filename_total_space)
        except ValueError:
            incorrect_files.append(filename)

    Index.place_date(sheet=sheet, index='A1')
    Index.add_incorrect_files(sheet=sheet,
                              index='A40',
                              filenames=incorrect_files)

    print(f'[+] Создаю файл с просчётом...\n{"=" * 35}')
    excel_file.save(f'{get_today_date("%Y-%m-%d")}_result.xlsx')
    print('[+] Программа отработала успешно.')
    finish_program(code=0, time_sleep=3)


def create_folders_list(path: str) -> list:
    folders_list = list()
    content = os.scandir(path)

    for obj in content:
        if obj.is_dir() and re.match(patterns.folders_pattern, obj.name):
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
        finish_program(code=0, time_sleep=3)
    else:
        print(f'\n[+] Путь корректный.\nНачинаю считать макеты...\n{"=" * 35}')


def check_filename(filename: str) -> None:
    if not re.findall(patterns.right_filename_pattern, filename):
        raise ValueError('Имя файла не соответствует шаблону.')


def get_filenames_to_print(path: str) -> list:
    folders_list = create_folders_list(path)
    check_folders(folders_list)
    files_list = create_files_list(folders_list)

    return files_list


def get_today_date(date_format: str) -> str:
    return datetime.datetime.today().strftime(date_format)  # Пример date_format - '%Y-%m-%d'


def str_to_date(file_date: str) -> datetime:
    current_year = get_today_date("%y")

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


def get_quantity(quantity: str) -> int:
    return int(quantity.replace(' ', ''))


def calculate_space(file_size: tuple) -> int or float:
    '''Позволяет высчитать место занимаемое в визитках для изделия
    произвольного формата.'''

    width, height = file_size
    width = (width / 89, width / 49)
    height = (height / 49, height / 89)
    result = max(width[0] * height[0], width[1] * height[1])

    return floor(result) if result > 1 else 1 if result > 0.5 else 0.5


def get_filename_total_space(size: str, quantity: str) -> int:
    '''Считает место, которое занимает макет с учётом тиража.
    Если к нам зашла визитка тиражом 5 000 вернёт значение 1х5 = 5.'''

    space = get_filename_space(size)
    quantity = get_quantity(quantity)

    return space * ceil(quantity / 1000) if quantity > 500 else space


def get_filename_space(size: str) -> int:
    '''Считает место, которое занимает макет без учёта тиража.
    Если к нам зашла визитка, вернёт значение 1.'''

    size = tuple(sorted(int(n) for n in re.findall(patterns.digits_only, size)))

    if fo.standard_formats.get(size):
        filename_space = fo.standard_formats.get(size)
    else:
        filename_space = calculate_space(size)

    return filename_space


class Index:
    '''Класс для извлечения ячеек из словаря dict_with_cells и записи данных в таблицу - шаблон Excel.'''

    __dict_with_cells = fo.template_cells_structure

    def __new__(cls, *args, **kwargs):
        raise ValueError("Нельзя создавать объекты данного класса.")

    @classmethod
    def get_index(cls, *, den: int, lam: str, quan: int, dat: int) -> str:
        if cls.__dict_with_cells.get(den, {}).get(lam, {}).get(quan, {}).get(dat, False):
            return cls.__dict_with_cells[den][lam][quan][dat]
        raise ValueError("Один из переданных ключей не корректный.")

    @classmethod
    def add_value(cls, *, sheet: 'Worksheet', index: str, value: int) -> None:
        if sheet[index].value is None:
            sheet[index] = value
        else:
            sheet[index] = sheet[index].value + value

    @staticmethod
    def place_date(*, sheet: 'Worksheet', index: str) -> None:
        sheet[index] = get_today_date('%Y-%m-%d')

    @staticmethod
    def add_incorrect_files(*, sheet: 'Worksheet', index: str, filenames: list) -> None:
        column = re.findall(patterns.letters_only, index)[0]
        row = int(re.findall(patterns.digits_only, index)[0])

        for i, file_name in enumerate(filenames, row):
            sheet[f'{column}{i}'] = file_name


def finish_program(*, code: int, time_sleep: int) -> None:
    code = 1 if code >= 1 else 0
    time.sleep(time_sleep)
    exit(code)


if __name__ == '__main__':
    main()
