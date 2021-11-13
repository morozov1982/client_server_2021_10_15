""" Unit-тесты клиента """

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_PORT, PORT
from client import request_user, get_server_response


class TestClient(unittest.TestCase):
    """
    Класс с тестами client-а
    """

    def test_request_user(self):
        """ Тест корректного запроса о присутствии клиента """
        test = request_user()
        test[TIME] = 1.1  # возьму из примера, зачем усложнять ;-)
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, PORT: DEFAULT_PORT, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_incorrect_request_user(self):
        """ Тест некорректного запроса о присутствии клиента """
        test = request_user()
        test[TIME] = 1.1
        self.assertNotEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_request_user_port(self):
        """ Тест указания порта в запросе о присутствии клиента """
        test = request_user()
        test[TIME] = 1.1
        self.assertIn(PORT, test)

    def test_request_user_port_value(self):
        """ Тест значения порта в запросе о присутствии клиента """
        test = request_user()
        test[TIME] = 1.1
        self.assertEqual(test[PORT], DEFAULT_PORT)

    def test_server_response_200(self):
        """ Тест корректного разбора ответа от сервера (200) """
        self.assertEqual(get_server_response({RESPONSE: 200}), '200 : OK')

    def test_incorrect_server_response_200(self):
        """ Тест некорректного разбора ответа от сервера (200) """
        self.assertNotEqual(get_server_response({RESPONSE: 200}), '400 : Bad Request')

    def test_server_response_400(self):
        """ Тест корректного разбора (400) """
        self.assertEqual(get_server_response({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_incorrect_server_response_400(self):
        """ Тест некорректного разбора (400) """
        self.assertNotEqual(get_server_response({RESPONSE: 400, ERROR: 'Bad Request'}), '200 : OK')

    def test_no_response(self):
        """ Тест исключения без поля RESPONSE """
        self.assertRaises(ValueError, get_server_response, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
