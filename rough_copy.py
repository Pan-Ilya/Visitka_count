import os
import re
from math import ceil
import formats as fo
import openpyxl
import datetime

# date_format = "%m-%d"  # strftime("%m-%d")
today = datetime.datetime.today().strftime('%Y-%m-%d')  # "%Y-%m-%d_%H-%M-%S"

excel_file = openpyxl.load_workbook('template.xlsx')
sheet = excel_file.active
directory = input('Укажите путь к директории где расположены плотные макеты (250, 300, 350): ')
content = os.scandir(directory)

folders_pattern = r'(?i)(GL|MAT|NON|SOFT|UF) ?(1\+0|1\+1)?(?=$)'
folders = list()

for obj in content:
    if obj.is_dir() and re.match(folders_pattern, obj.name):
        folders.append(obj)

if not folders:
    print('[-] По указанному адресу нету папок с плотными макетами.')
else:
    print(f'\n[+] Путь корректный.\nНачинаю считать макеты...\n{"=" * 35}')

pdfs_lists = list()

for folder in folders:
    for el in os.walk(folder):
        if el[2]:
            pdfs_lists.extend(el[2])

incorrect_files = list()
pdf_pattern = r'(?P<date>\d{2}-\d{2}).*?' \
              r'(?P<size>\d+[xXхХ]\d+).*?' \
              r'(?P<density>\d{3})_' \
              r'(?P<lam>\w{2,3}\d\+\d)?.*?' \
              r'(?P<quantity>[\d ]{3,}).*?' \
              r'(?P<file_format>\.pdf)'

for pdf in pdfs_lists:
    if not re.findall(pdf_pattern, pdf):
        incorrect_files.append(pdf)
        continue

    date, size, density, lam, quantity, file_format = re.findall(pdf_pattern, pdf)[0]
    size = tuple(int(n) for n in re.findall(r'\d+', size))
    quantity = quantity.replace(' ', '')

    current_year = datetime.datetime.today().strftime("%y")
    # tomorrow = (datetime.datetime.today() + datetime.timedelta(1)).date()

    if datetime.datetime.today().strftime('%a') == 'Fri':
        tomorrow = [
            (datetime.datetime.today() + datetime.timedelta(1)).date(),
            (datetime.datetime.today() + datetime.timedelta(3)).date()
        ]
    else:
        tomorrow = [(datetime.datetime.today() + datetime.timedelta(1)).date()]
    pdf_date = datetime.datetime.strptime(f'{current_year}-{date}', '%y-%m-%d').date()

    if pdf_date in tomorrow:
        date = 24
    elif pdf_date > max(tomorrow):
        date = 48
    else:
        incorrect_files.append(pdf)
        continue

    if fo.standard_formats.get(size) or fo.standard_formats.get(size[::-1]):
        value = fo.standard_formats.get(size) if fo.standard_formats.get(size) else fo.standard_formats.get(size[::-1])
    else:
        value = fo.calculate_format(size)

    total_value = value * ceil(int(quantity) / 1000) if int(quantity) > 500 else value

    quantity = 1000 if int(quantity) > 500 else 500
    density = int(density)
    lam = lam.upper() if lam else 'NON'

    if fo.structure.get(density, {}).get(lam, {}).get(quantity, {}).get(date, False):
        index = fo.structure.get(density).get(lam).get(quantity).get(date)
        if sheet[index].value is None:
            sheet[index] = total_value
        else:
            sheet[index] = sheet[index].value + total_value
    else:
        incorrect_files.append(pdf)

sheet['A1'] = today
for i, file_name in enumerate(incorrect_files, 40):
    sheet[f'A{i}'] = file_name

print(f'[+] Создаю файл с просчётом...\n{"=" * 35}')
excel_file.save(f'{today}_result.xlsx')
print('[+] Программа отработала успешно.')
