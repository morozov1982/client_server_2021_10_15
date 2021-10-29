""" Unit-тесты для сервера """

import unittest

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CLIENTS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, PORT
from server import check_client_data


class TestServer(unittest.TestCase):
    """
    Класс с тестами server-а
    """
    ok_response = {RESPONSE: 200}
    error_response = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_check_ok(self):
        """ Корректный запрос """
        self.assertEqual(check_client_data(
            {ACTION: PRESENCE, TIME: 1.1, PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_response)

    def test_incorrect_check_ok(self):
        """ Некорректный запрос """
        self.assertNotEqual(check_client_data(
            {ACTION: PRESENCE, TIME: 1.1, PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_response)

    def test_no_action(self):
        """ Ошибка при отсутствии действия """
        self.assertEqual(check_client_data(
            {TIME: '1.1', PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_response)

    def test_wrong_action(self):
        """ Ошибка при неверном действии """
        self.assertEqual(check_client_data(
            {ACTION: "wrong", TIME: 1.1, PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_response)

    def test_no_time(self):
        """ Ошибка при отсутствии времени """
        self.assertEqual(check_client_data(
            {ACTION: PRESENCE, PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_response)

    def test_no_port(self):
        """ Ошибка при отсутствии порта """
        # вернёт 200 так как устанавливается порт по умолчанию
        self.assertEqual(check_client_data(
            {ACTION: PRESENCE, TIME: '1.2', USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_response)

    def test_no_user(self):
        """ Ошибка при отсутствии пользователя """
        self.assertEqual(check_client_data(
            {ACTION: PRESENCE, TIME: '1.2', PORT: DEFAULT_PORT}), self.error_response)

    def test_wrong_user(self):
        """ Ошибка при неверном пользователе """
        self.assertEqual(check_client_data(
            {ACTION: PRESENCE, TIME: '1.2', PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Бобёр Уасся'}}), self.error_response)

    def test_incorrect_wrong_user(self):
        """ Ошибка (некорректная) при неверном пользователе - высосаный из пальца пример ;-) """
        self.assertNotEqual(check_client_data(
            {ACTION: PRESENCE, TIME: '1.2', PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Бобёр Уасся'}}), self.ok_response)


if __name__ == '__main__':
    unittest.main()
