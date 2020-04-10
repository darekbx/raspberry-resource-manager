from app import app
from flask import render_template

from app import models

@app.route('/')
def index():
	
	users = models.User.query.all()

	return render_template('index.html', name="{0}".format(len(users)))