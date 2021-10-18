"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""

first_string = 'разработка'
second_string = 'администрирование'
third_string = 'protocol'
forth_string = 'standard'

encoded_first = first_string.encode(encoding='utf-8')
encoded_second = second_string.encode(encoding='utf-8')
encoded_third = third_string.encode(encoding='utf-8')
encoded_forth = forth_string.encode(encoding='utf-8')

decoded_first = encoded_first.decode(encoding='utf-8')
decoded_second = encoded_second.decode(encoding='utf-8')
decoded_third = encoded_third.decode(encoding='utf-8')
decoded_forth = encoded_forth.decode(encoding='utf-8')

print(f'{"="*50}\n\t{first_string=}\n{"-"*35}\n{encoded_first=}\n{decoded_first=}\n{"*"*50}')
print(f'{"="*50}\n\t{second_string=}\n{"-"*35}\n{encoded_second=}\n{decoded_second=}\n{"*"*50}')
print(f'{"="*50}\n\t{third_string=}\n{"-"*35}\n{encoded_third=}\n{decoded_third=}\n{"*"*50}')
print(f'{"="*50}\n\t{forth_string=}\n{"-"*35}\n{encoded_forth=}\n{decoded_forth=}\n{"*"*50}')
