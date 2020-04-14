from flask import Flask

from app.configuration import Configuration

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

configuration = Configuration().load()

app = Flask(__name__)
app.config.update(configuration)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()

from app.models import User
db.create_all()
db.session.commit()

login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models, login_manager
