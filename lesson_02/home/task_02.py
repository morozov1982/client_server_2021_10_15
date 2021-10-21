"""
2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
Для этого:
    a. Создать функцию write_order_to_json(), в которую передается 5 параметров —
       товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
       Функция должна предусматривать запись данных в виде словаря в файл orders.json.
       При записи данных указать величину отступа в 4 пробельных символа;
    b. Проверить работу программы через вызов функции write_order_to_json()
       с передачей в нее значений каждого параметра.
"""
import json
import os
from datetime import datetime

DATA_DIR_NAME = 'data'
OUTPUT_FILE_NAME = 'orders.json'
OUTPUT_FILE_PATH = os.path.join(DATA_DIR_NAME, OUTPUT_FILE_NAME)
JSON_INDENT = 4
current_date = datetime.today().strftime("%d-%m-%Y")


def write_order_to_json(item, quantity, price, buyer, date):
    current_order = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    """Записывает данные в виде словаря в orders.json"""
    with open(OUTPUT_FILE_PATH, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as file:
        json_data['orders'].append(current_order)
        json.dump(json_data, file, indent=JSON_INDENT, ensure_ascii=False)


write_order_to_json('бобёр', '16', '5000', 'строитель плотин', current_date)
write_order_to_json('хомяк', '4', '15', 'отец ревущего ребёнка', current_date)
