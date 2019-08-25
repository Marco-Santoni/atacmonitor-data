import unittest
from xmlrpc.client import Server
from unittest.mock import patch
import os

from lambda_function import lambda_handler

class TestPalinaRequest(unittest.TestCase):
 
    def setUp(self):
        s1 = Server(os.environ['ATAC_AUTH_URL'], use_builtin_types=True)
        token = s1.autenticazione.Accedi(os.environ['ATAC_DEV_KEY'], os.environ['ATAC_ID_UTENTE'])
        self.event = {
            'body': {
                'token': token,
                'id_palina': '10037'
            }
        }
        self.context = None

    @patch('arrival.process', autospec=True)
    def test_lambda_handler(self, mock_arrival_process):
        lambda_handler(self.event, self.context)
        res = mock_arrival_process.call_args[0][0]
        assert('id_richiesta' in res)

if __name__ == '__main__':
    unittest.main()