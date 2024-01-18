# database.py
import psycopg2

def connect_to_postgres():
    return psycopg2.connect(user="root", password="s3cr3t", dbname="keycloak", host="localhost", port="5432")

def perform_postgres_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
