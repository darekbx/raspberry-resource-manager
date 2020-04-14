from app import app
from app.forms import LoginForm, RegisterForm
from app import models, login_manager, db
from flask import g, render_template, redirect
from flask_login import current_user, login_user, logout_user, login_required

import os
from os.path import expanduser
import hashlib

@app.route('/')
@app.route('/dir/<dir>')
@login_required
def index(dir = None):
	parent_directory = expanduser("~") + app.config['RESOURCES-DIRECTORY']
	if dir is None:
		dir = "/"
	content = os.listdir(parent_directory + dir)
	return render_template('index.html', content = content)

@login_manager.user_loader
def load_user(user_id):
	return models.User.query.get(user_id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/settings")
@login_required
def settings():
	return "TODO"

@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect("/")
	elif models.User.query.first() is not None:
		form = LoginForm()
		if form.validate_on_submit():
			user = models.User.query.filter_by(name=form.name.data).first()
			if user is not None and user.verify_password(form.password.data):
				login_user(user)
				return redirect("/")
		return render_template('login.html', form=form)
	else:
		return redirect("/register")

@app.route('/register', methods=["GET", "POST"])
def register():
	one_user = app.config['ONE_USER']
	if not one_user or models.User.query.count() == 0:
		form = RegisterForm()
		if form.validate_on_submit():
			name = form.name.data
			password = hashlib.md5(form.password.data.encode())
			db.session.add(models.User(name=name, password=password.hexdigest()))
			db.session.commit()
			return redirect("/login")
		return render_template('register.html', form=form)
	else:
		return redirect("/login")
