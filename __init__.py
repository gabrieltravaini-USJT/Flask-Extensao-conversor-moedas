from flask import Flask 
from.extensions import db,migrate
from.routes.cmBp import cmBp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(cmBp)
    
    return app