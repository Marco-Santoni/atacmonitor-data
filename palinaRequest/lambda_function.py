import datetime
import json
import os
from xmlrpc.client import Server
import arrival

def lambda_handler(event, context):
    """
    Input:
        event: {
            'body': {
                'id_palina': id_palina,
                'token': authentication_token
            }
        }
    """
    body = event['body']
    print('Request for palina {}'.format(body['id_palina']))
    server = Server(os.environ['PALINA_URL'], use_builtin_types=True)
    ts = datetime.datetime.utcnow()
    res = server.paline.Previsioni(body['token'], body['id_palina'], 'it')
    arrival.process(res, ts)
    return {
        'statusCode': 200,
        'body': 'DONE'
    }
