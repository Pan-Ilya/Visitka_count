import os
import re
from math import ceil
import formats as fo
import openpyxl
import datetime


def main():
    path: str = input('Укажите путь к директории где расположены плотные макеты (250, 300, 350): ')
    folder_names_with_files: list = create_folders_list(path)
    pass


def create_folders_list(path: str) -> list:
    folders_list = list()
    content = os.scandir(path)
    folders_pattern = r'(?i)(GL|MAT|NON|SOFT|UF) ?(1\+0|1\+1)?(?=$)'

    for obj in content:
        if obj.is_dir() and re.match(folders_pattern, obj.name):
            folders_list.append(obj)

    return folders_list

