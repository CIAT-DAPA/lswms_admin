# database.py
import psycopg2
import os
name_db = os.getenv('USERS_DB_NAME', 'prueba2key')
user = os.getenv('USERS_DB_USER', 'root')
passw = os.getenv('USERS_DB_PASS', 's3cr3t')
def connect_to_postgres():
    return psycopg2.connect(user=user, password=passw, dbname=name_db, host="localhost", port="5432")

def perform_postgres_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
