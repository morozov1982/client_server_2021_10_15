"""Модуль pyyaml_examples"""

# Внимание!!! Нужно устанавливать!
# $ pip3 install pyyaml
import yaml

# считываем данные
with open('data_read.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print(F_N_CONTENT)

# изменяем форматирование записи
ACTION_LIST = ['msg_1', 'msg_2', 'msg_3']
TO_LIST = ['account_1', 'account_2', 'account_3']
AS_SET = {1, 2, 2, 3}
DATA_DICT = {'action': ACTION_LIST, 'to': TO_LIST, 'names': AS_SET}
DATA_TO_YAML = {'action': ACTION_LIST, 'to': TO_LIST, 'names': AS_SET, 'names_d': DATA_DICT}

with open('data_write.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False)

with open('data_write.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print(F_N_CONTENT)


