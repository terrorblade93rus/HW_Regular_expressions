from pprint import pprint
import csv
import re
from collections import defaultdict

# Чтение адресной книги в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

# Функция для нормализации телефонного номера
def normalize_phone(phone):
    # Ищем основной номер и, если есть, добавочный номер
    match = re.match(r"(\+?[78]|8)?\s*\(?(\d{3})\)?\s*[-]?\s*(\d{3})\s*[-]?\s*(\d{2})\s*[-]?\s*(\d{2})(.*)", phone)
    
    if match:
        # Извлекаем части номера
        country_code = "+7"
        area_code = match.group(2)
        first_part = match.group(3)
        second_part = match.group(4)
        third_part = match.group(5)
        extension = match.group(6)

        # Форматируем основной номер
        formatted_phone = f"{country_code}({area_code}){first_part}-{second_part}-{third_part}"

        # Если есть добавочные цифры, находим их и добавляем в нужном формате
        ext_match = re.search(r"(\d{4})", extension)
        if ext_match:
            formatted_phone += f" доб.{ext_match.group(0)}"

        return formatted_phone

    # Если номер не подходит под формат, возвращаем как есть
    return phone



# TODO 1: выполнение пунктов 1-3
# Словарь для объединения дублирующихся записей
contacts_dict = defaultdict(lambda: [""] * 7)

# Обработка контактов
for contact in contacts_list[1:]:
    # Объединяем ФИО в одно поле и разбиваем его
    full_name = " ".join(contact[:3]).split()
    lastname, firstname, surname = full_name + [""] * (3 - len(full_name))
    key = f"{lastname} {firstname}"

    # Заполняем данные, оставляя уже существующие поля, если они есть
    contacts_dict[key][0] = lastname
    contacts_dict[key][1] = firstname
    contacts_dict[key][2] = surname or contacts_dict[key][2]
    contacts_dict[key][3] = contact[3] or contacts_dict[key][3]  # Организация
    contacts_dict[key][4] = contact[4] or contacts_dict[key][4]  # Должность
    contacts_dict[key][5] = normalize_phone(contact[5] or contacts_dict[key][5])  # Телефон
    contacts_dict[key][6] = contact[6] or contacts_dict[key][6]  # Email

# Преобразуем результат обратно в список для записи
contacts_list = [contacts_list[0]] + list(contacts_dict.values())

# TODO 2: Сохранение получившихся данных в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

pprint(contacts_list)
