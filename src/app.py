from flask import Flask, render_template
from mongoengine import connect
from routes.adm1 import adm1_bp
from routes.adm2 import adm2_bp
from routes.adm3 import adm3_bp
from routes.watershed import watershed_bp
from routes.waterpoint import waterpoint_bp
from routes.typecontent import typecontent_bp
from routes.wpcontent import wpcontent_bp
from routes.wscontent import wscontent_bp
from config import config
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)



app.register_blueprint(adm1_bp)
app.register_blueprint(adm2_bp)
app.register_blueprint(adm3_bp)
app.register_blueprint(watershed_bp)
app.register_blueprint(waterpoint_bp)
app.register_blueprint(typecontent_bp)
app.register_blueprint(wpcontent_bp)
app.register_blueprint(wscontent_bp)



if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])