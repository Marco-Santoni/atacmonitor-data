import pandas as pd
import os
import dotenv
import database

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env"))

def is_a_palina(stop_code):
    return len(stop_code) == 5 and stop_code.isdigit()

df = pd.read_csv(
    'data/stops.txt',
    usecols=['stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon'],
    dtype={
        'stop_code': str,
        'stop_name': str,
        'stop_desc': str,
        'stop_lat': float,
        'stop_lon': float
    },
    quotechar='\"'
)
df = df.dropna(subset=['stop_code'])
df = df[df.apply(lambda x: is_a_palina(x['stop_code']), axis=1)]

db = database.get_database()
conn = database.get_connection(db)
cursor = conn.cursor()
cursor.execute('TRUNCATE paline')
for index, row in df.iterrows():
    cursor.execute(
        '''
        INSERT INTO paline (stop_code, stop_name, stop_desc, stop_lat, stop_lon)
        values (%s, %s, %s, %s, %s)
        ''',
        (
            row['stop_code'],
            row['stop_name'],
            row['stop_desc'],
            row['stop_lat'],
            row['stop_lon']
        )
    )
conn.commit()
conn.close()
