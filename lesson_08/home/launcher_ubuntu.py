"""
It is a launcher for starting subprocesses for server and clients of two types: senders and listeners.
for more information:
https://stackoverflow.com/questions/67348716/kill-process-do-not-kill-the-subprocess-and-do-not-close-a-terminal-window
"""

import os
import sys
import signal
from subprocess import Popen
from time import sleep


PYTHON_PATH = sys.executable
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_subprocess(file_with_args):
    sleep(0.2)
    file_full_path = f'{PYTHON_PATH} {BASE_PATH}/{file_with_args}'
    args = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", file_full_path]
    return Popen(args, preexec_fn=os.setpgrp)


process = []

while True:
    INPUT_TEXT = 'Выберите действие:\n'\
                 'q - выход,\n'\
                 's - запустить сервер и клиенты,\n'\
                 'x - закрыть все окна\n>>> '
    action = input(INPUT_TEXT)

    if action == 'q':
        break
    elif action == 's':
        process.append(get_subprocess('server.py'))

        for _ in range(2):
            process.append(get_subprocess('client.py -m send'))

        for _ in range(2):
            process.append(get_subprocess('client.py -m listen'))

    elif action == 'x':
        while process:
            victim = process.pop()                # ;-)
            os.killpg(victim.pid, signal.SIGINT)  # ;-)
