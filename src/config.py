import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DBNAME'),
        'host': 'localhost',
        'port': 27017,
        'username': os.environ.get('MONGO_USERNAME'),
        'password': os.environ.get('MONGO_PASSWORD'),
        'authentication_source': os.environ.get('MONGO_AUTH_SOURCE')
    }
