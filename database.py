import psycopg2
import urllib.parse
import os
import dotenv

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env"))

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
