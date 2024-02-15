from flask import Flask
from mongoengine import connect
from routes.adm1 import adm1_bp
from routes.adm2 import adm2_bp
from routes.adm3 import adm3_bp
from routes.watershed import watershed_bp
from routes.waterpoint import waterpoint_bp
from routes.typecontent import typecontent_bp
from routes.wpcontent import wpcontent_bp
from routes.wscontent import wscontent_bp
from routes.home import home_bp
from routes.login import login_bp
from routes.alerts import alerts_bp
from routes.weekly import weekly_bp
from models.models import User
from models.database import connect_to_postgres, perform_postgres_query
from config import config
import os
import flask_login
import psycopg2
name_db = os.getenv('USERS_DB_NAME', 'prueba2key')
user = os.getenv('USERS_DB_USER', 'root')
passw = os.getenv('USERS_DB_PASS', 's3cr3t')
app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_username(user_id)

app.register_blueprint(adm1_bp)
app.register_blueprint(adm2_bp)
app.register_blueprint(adm3_bp)
app.register_blueprint(watershed_bp)
app.register_blueprint(waterpoint_bp)
app.register_blueprint(typecontent_bp)
app.register_blueprint(wpcontent_bp)
app.register_blueprint(wscontent_bp)
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(weekly_bp)
def connect_to_postgres():
    return psycopg2.connect(user=user, password=passw, dbname=name_db, host="localhost", port="5432")



def perform_postgres_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected to MongoDB")

    # Conexión a PostgreSQL
    postgres_connection = connect_to_postgres()
    print("Conectado a PostgreSQL")

    postgres_connection.close()

    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])
