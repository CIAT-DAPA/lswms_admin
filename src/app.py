from flask import Flask, render_template
from mongoengine import connect
from config import Config
from routes.adm1 import adm1_bp
from routes.adm2 import adm2_bp

app = Flask(__name__)
app.config.from_object(Config)
connect(
    db=app.config['MONGODB_SETTINGS']['db'],
    host=app.config['MONGODB_SETTINGS']['host'],
    port=app.config['MONGODB_SETTINGS']['port'],
    username=app.config['MONGODB_SETTINGS']['username'],
    password=app.config['MONGODB_SETTINGS']['password'],
    authentication_source=app.config['MONGODB_SETTINGS']['authentication_source']
)

app.register_blueprint(adm1_bp)
app.register_blueprint(adm2_bp)



if __name__ == '__main__':
    app.run()
