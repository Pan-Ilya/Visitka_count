import os
import re
from math import ceil, floor
import formats as fo
import openpyxl
import datetime

filename_pattern = r'(?P<date>\d{2}-\d{2}).*?' \
                   r'(?P<size>\d+[xXхХ]\d+).*?' \
                   r'(?P<density>\d{3})_' \
                   r'(?P<lam>\w{2,3}\d\+\d)?.*?' \
                   r'(?P<quantity>[\d ]{3,}).*?' \
                   r'(?P<file_format>\.pdf)'


def main():
    path_to_files: str = input('Укажите путь к директории где расположены плотные макеты (250, 300, 350): ')
    folder_names_with_files: list = make_folders_list(path_to_files)

    # if not folder_names_with_files:
    #     print('[-] По указанному адресу нету папок с плотными макетами.')
    # else:
    #     print(f'\n[+] Путь корректный.\nНачинаю считать макеты...\n{"=" * 35}')

    filenames_to_print: list = make_files_list(folder_names_with_files)
    incorrect_files = list()

    for filename in filenames_to_print:
        incorrect_files = list()

        if not re.findall(filename_pattern, filename):
            incorrect_files.append(filename)
            continue


def make_folders_list(path_to_files: str) -> list:
    folders_list = list()
    folders_pattern = r'(?i)(GL|MAT|NON|SOFT|UF) ?(1\+0|1\+1)?(?=$)'

    content = os.scandir(path_to_files)
    for obj in content:
        if obj.is_dir() and re.match(folders_pattern, obj.name):
            folders_list.append(obj)

    return folders_list


def make_files_list(folders_name: list) -> list:
    files_list = list()

    for folder in folders_name:
        for element in os.walk(folder):
            if element[2]:
                files_list.extend(element[2])

    return files_list


# a = make_folders_list('D:\Праця\Тест программы')
# for el in a:
#     print(el)
#     print(type(el))
main()
