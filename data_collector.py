import dotenv
import os
import datetime
import time
import concurrent.futures
# Python 3 import
from xmlrpc.client import Server
from database import get_database, get_connection

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env"))

class Arrival(object):

    @staticmethod
    def save(arrivals):
        database = get_database()
        conn = get_connection(database)
        cursor = conn.cursor()
        args_str = b','.join(
            cursor.mogrify(
                b'''(
                    %(tempo_attesa)s,
                    %(tempo_attesa_secondi)s,
                    %(distanza_fermate)s,
                    %(linea)s,
                    %(id_palina)s,
                    %(nome_palina)s,
                    %(collocazione)s,
                    %(capolinea)s,
                    %(in_arrivo)s,
                    %(a_capolinea)s,
                    %(created_at)s
                )''',
                arrival
            ) for arrival in arrivals
        )
        cursor.execute(
            b'''
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
            ) VALUES
            ''' + args_str
        )
        conn.commit()
        conn.close()

DEV_KEY = os.environ.get('DEV_KEY')

def get_palina(palina, token):
    server = Server('http://muovi.roma.it/ws/xml/paline/7')
    timestamp = datetime.datetime.utcnow()
    res = server.paline.Previsioni(token, palina, 'it')
    risposta = res['risposta']
    arrivals = []
    arr = {'nome': risposta['nome'], 'collocazione': risposta['collocazione']}
    arr['created_at'] = timestamp
    for p in risposta['primi_per_palina']:
        for a in p['arrivi']:
            arr['linea'] = a.get('linea')
            arr['tempo_attesa'] = a.get('tempo_attesa')
            arr['tempo_attesa_secondi'] = a.get('tempo_attesa_secondi')
            arr['distanza_fermate'] = a.get('distanza_fermate')
            arr['id_palina'] = a.get('id_palina')
            arr['nome_palina'] = a.get('nome_palina')
            arr['collocazione'] = a.get('collocazione')
            arr['capolinea'] = a.get('capolinea')
            arr['in_arrivo'] = bool(a.get('in_arrivo'))
            arr['a_capolinea'] = bool(a.get('a_capolinea'))
            arrivals.append(arr)
    return arrivals

def all_paline():
    database = get_database()
    conn = get_connection(database)
    cursor = conn.cursor()
    cursor.execute('SELECT stop_code FROM paline')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return [r[0] for r in rows]

palina_list = all_paline()
s1 = Server('http://muovi.roma.it/ws/xml/autenticazione/1')
token = s1.autenticazione.Accedi(DEV_KEY, '')

workers=int(os.environ.get('THREAD_NUMBER'))
while True:
    start_time = time.time()
    arrivals = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_palina = {
            executor.submit(get_palina, palina, token): palina
            for palina in palina_list
        }
        for future in concurrent.futures.as_completed(future_to_palina):
            palina = future_to_palina[future]
            try:
                arrivals += future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (palina, exc))
    Arrival.save(arrivals)
    end_time = time.time()
    minimum_delta = int(os.environ.get('PULL_FREQUENCY'))
    if end_time - start_time < minimum_delta:
        time.sleep(minimum_delta - (end_time - start_time))
    break
