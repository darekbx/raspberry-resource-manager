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

login_manager.init_app(app)

from app import views, models, login_manager
