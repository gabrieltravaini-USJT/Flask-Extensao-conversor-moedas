from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# instanciando os objetos
db = SQLAlchemy()
migrate = Migrate()

