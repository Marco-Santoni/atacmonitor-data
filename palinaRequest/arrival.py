import os
from pymongo import MongoClient

def save(bus_arrival):
    client = MongoClient(os.environ['MONGODB_CONN_STRING'])
    db = client.test
    collection = db['arrivals']
    collection.insert(bus_arrival)


def process(atac_response):
    """
    Loads the response by ATAC API, loops over the first arrivals for each line. Then, stores the arrival.
    Input:
        atac_response: the json response by ATAC API
    """
    response = atac_response['risposta']
    for palina in response['primi_per_palina']:
        for bus_arrival in palina['arrivi']:
            save(bus_arrival)