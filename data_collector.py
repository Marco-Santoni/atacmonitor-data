import dotenv
import os
import datetime
import psycopg2
import urllib.parse
import time
# Python 3 import
from xmlrpc.client import Server

try:
    PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env"))
except Exception:
    pass

def get_database():
    # url format: postgresql://username:password@host:port/database
    settings = {}
    result = urllib.parse.urlparse(
        os.environ.get('DATABASE_URL')
    )
    settings['name'] = result.path[1:] or ''
    settings['username'] = result.username or ''
    settings['host'] = result.hostname or ''
    settings['password'] = result.password or ''
    settings['port'] = result.port or ''
    return settings

def get_connection(database):
    return psycopg2.connect(
        "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (
            database['name'],
            database['username'],
            database['host'],
            database['password'],
            database['port']
        )
    )

def save(arrival):
    database = get_database()
    conn = get_connection(database)
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO arrivals (
            tempo_attesa,
            tempo_attesa_secondi,
            distanza_fermate,
            linea,
            id_palina,
            nome_palina,
            collocazione,
            capolinea,
            in_arrivo,
            a_capolinea,
            created_at
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
        ''',
        (
            arrival.tempo_attesa,
            arrival.tempo_attesa_secondi,
            arrival.distanza_fermate,
            arrival.linea,
            arrival.id_palina,
            arrival.nome_palina,
            arrival.collocazione,
            arrival.capolinea,
            arrival.in_arrivo,
            arrival.a_capolinea,
            arrival.created_at
        )
    )
    conn.commit()
    conn.close()

class Arrival(object):

    def __init__(self, nome, collocazione):
        self.nome = nome #
        self.collocazione = collocazione #
        self.tempo_attesa = None
        self.tempo_attesa_secondi = None
        self.distanza_fermate = None
        self.linea = None #
        self.id_palina = None
        self.nome_palina = None
        self.collocazione = None
        self.capolinea = None
        self.in_arrivo = None
        self.a_capolinea = None
        self.created_at = None

DEV_KEY = os.environ.get('DEV_KEY')

s1 = Server('http://muovi.roma.it/ws/xml/autenticazione/1')
s2 = Server('http://muovi.roma.it/ws/xml/paline/7')

token = s1.autenticazione.Accedi(DEV_KEY, '')

while True:
    for palina in ['70638', '72074', '70200']:
        timestamp = datetime.datetime.utcnow()
        res = s2.paline.Previsioni(token, palina, 'it')
        risposta = res['risposta']
        arr = Arrival(risposta['nome'], risposta['collocazione'])
        arr.created_at = timestamp
        for p in risposta['primi_per_palina']:
            for a in p['arrivi']:
                arr.linea = a.get('linea')
                arr.tempo_attesa = a.get('tempo_attesa')
                arr.tempo_attesa_secondi = a.get('tempo_attesa_secondi')
                arr.distanza_fermate = a.get('distanza_fermate')
                arr.id_palina = a.get('id_palina')
                arr.nome_palina = a.get('nome_palina')
                arr.collocazione = a.get('collocazione')
                arr.capolinea = a.get('capolinea')
                arr.in_arrivo = bool(a.get('in_arrivo'))
                arr.a_capolinea = bool(a.get('a_capolinea'))

                save(arr)
    time.sleep(int(os.environ.get('PULL_FREQUENCY')))
