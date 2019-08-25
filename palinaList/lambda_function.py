import boto3
import csv
import os

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    obj = s3.Object(
        os.environ['ROME_GTFS_BUCKET'],
        os.environ['ROME_GTFS_FILE']
    )
    in_memory_file = obj.get()['Body'].read().decode('utf-8')
    fl = csv.reader(in_memory_file.splitlines(), delimiter=',')
    cnt = 0
    id_palina_list = []
    for row in fl:
        if cnt > 0:
            id_palina_list.append(row[0])
        cnt += 1
    return {
        'statusCode': 200,
        'body': id_palina_list
    }
