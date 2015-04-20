import dotenv
import os
import datetime
import psycopg2
import urlparse
# Python 2 import
from xmlrpclib import Server

try:
    PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env"))
except Exception:
    pass

def get_database():
    # url format: postgresql://username:password@host:port/database
    settings = {}
    result = urlparse.urlparse(
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

def save(line, minutes, created_at):
    print line, minutes, created_at
    database = get_database()
    conn = get_connection(database)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO arrivals (line, minutes, created_at) VALUES (%s, %s, %s);',
        (line, minutes, created_at)
    )
    conn.commit()
    conn.close()

DEV_KEY = os.environ.get('DEV_KEY')

s1 = Server('http://muovi.roma.it/ws/xml/autenticazione/1')
s2 = Server('http://muovi.roma.it/ws/xml/paline/7')

token = s1.autenticazione.Accedi(DEV_KEY, '')

now = datetime.datetime.utcnow()
rome_now = now + datetime.timedelta(hours=2)

res = s2.paline.Previsioni(token, '71427', 'it')
for p in res['risposta']['primi_per_palina']:
    print 'Arrivi: ', len(p)
    for a in p['arrivi']:
        line = a['linea']
        if 'nessun_autobus' in a:
            minutes = None
        else:
            minutes = a['tempo_attesa']

        save(line, minutes, rome_now)
