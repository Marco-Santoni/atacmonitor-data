import json
import os
from xmlrpc.client import Server
import boto3

def get_id_palina_list():
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName="palinaList",
        InvocationType='RequestResponse'
    )
    response = json.loads(response['Payload'].read().decode("utf-8"))
    return response['body']

def lambda_handler(event, context):
    id_palina_list = get_id_palina_list()
    s1 = Server(os.environ['ATAC_AUTH_URL'], use_builtin_types=True)
    token = s1.autenticazione.Accedi(os.environ['ATAC_DEV_KEY'], os.environ['ATAC_ID_UTENTE'])
    client = boto3.client('lambda')
    for id_palina in id_palina_list:
        client.invoke(
            FunctionName="palinaRequest",
            InvocationType='Event',
            Payload=json.dumps(
                {
                    'body': {
                        'id_palina': id_palina,
                        'token': token
                    }
                }
            )
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('DONE')
    }
