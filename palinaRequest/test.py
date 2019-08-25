import unittest
from xmlrpc.client import Server, Fault
from unittest.mock import patch
import os

from lambda_function import lambda_handler

class TestPalinaRequest(unittest.TestCase):
 
    def setUp(self):
        s1 = Server(os.environ['ATAC_AUTH_URL'], use_builtin_types=True)
        self.token = s1.autenticazione.Accedi(os.environ['ATAC_DEV_KEY'], os.environ['ATAC_ID_UTENTE'])
        self.event = {
            'body': {
                'token': self.token,
                'id_palina': '10037'
            }
        }
        self.context = None

    @patch('arrival.process', autospec=True)
    def test_lambda_handler(self, mock_arrival_process):
        lambda_handler(self.event, self.context)
        res = mock_arrival_process.call_args[0][0]
        assert('id_richiesta' in res)

    @patch('arrival.process', autospec=True)
    def test_palina_not_exists(self, mock_arrival_process):
        missing_palina = {
            'body': {
                'token': self.token,
                'id_palina': 'FOO_PALINA'
            }
        }
        with self.assertRaises(Fault):
            lambda_handler(missing_palina, self.context)

if __name__ == '__main__':
    unittest.main()