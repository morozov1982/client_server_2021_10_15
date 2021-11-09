""" Лаунчер """

from subprocess import Popen, CREATE_NEW_CONSOLE

PROCESS = []

while True:
    ACTION = input('Выберите действие:\n'
                   'q - выход,\n'
                   's - запустить сервер и клиенты,\n'
                   'x - закрыть все окна\n>>> ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))

        for _ in range(2):
            PROCESS.append(Popen('python client.py -m send', creationflags=CREATE_NEW_CONSOLE))

        for _ in range(5):
            PROCESS.append(Popen('python client.py -m listen', creationflags=CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()  # ;-)
            VICTIM.kill()           # ;-)
