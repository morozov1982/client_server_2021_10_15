""" Лаунчер """

from subprocess import Popen, CREATE_NEW_CONSOLE

PROCESSES = []  # теперь во множественном числе

while True:
    ACTION = input('Выберите действие:\n'
                   'q - выход,\n'
                   's - запустить сервер и клиенты,\n'
                   'x - закрыть все окна\n>>> ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        # почти копипаста, немного подсократил за счёт from import
        PROCESSES.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
        PROCESSES.append(Popen('python client.py -n test1', creationflags=CREATE_NEW_CONSOLE))
        PROCESSES.append(Popen('python client.py -n test2', creationflags=CREATE_NEW_CONSOLE))
        PROCESSES.append(Popen('python client.py -n test3', creationflags=CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()  # ;-)
            VICTIM.kill()           # ;-)
