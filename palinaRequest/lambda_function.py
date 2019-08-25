import datetime
import json
import os
from xmlrpc.client import Server, Fault
import arrival

def invalid_palina(err):
    return {
        'statusCode': 200,
        'body': 'INVALID PALINA'
    }

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
    try:
        res = server.paline.Previsioni(body['token'], body['id_palina'], 'it')
    except Fault as err:
        if err.faultCode == 803:
            return invalid_palina(err)
        else: raise
    arrival.process(res, ts)
    return {
        'statusCode': 200,
        'body': 'DONE'
    }
