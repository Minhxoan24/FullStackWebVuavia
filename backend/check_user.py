import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

email = os.getenv('TEST_EMAIL', 'minhxoandev@gmail.com')

print('Connecting to DB', DB_HOST, DB_PORT, DB_NAME, 'as', DB_USER)
try:
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT id, email FROM users WHERE email = %s', (email,))
    rows = cur.fetchall()
    if rows:
        print('Found users:')
        for r in rows:
            print(r)
    else:
        print('No user with email', email)
    cur.close()
    conn.close()
except Exception as e:
    print('DB error:', e)
    raise
