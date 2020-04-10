from flask import Flask

from app.configuration import Configuration

from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

configuration = Configuration().load()

app = Flask(__name__)
app.config.update(configuration)

db = SQLAlchemy(app)

from app import views, models