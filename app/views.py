from app import app
from app.forms import LoginForm, RegisterForm
from app import models, login_manager, db
from flask import g, render_template, redirect 
from flask import send_file
from flask_login import current_user, login_user, logout_user, login_required
from dateutil.parser import parse

import time, datetime as dt
import os
from os.path import expanduser
import hashlib

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

@app.route('/download')
@app.route('/dir/<dir>')
@login_required
def file_download(file_to_download, dir = None):
	parent_directory = expanduser("~") + app.config['RESOURCES-DIRECTORY']
	if dir is None:
		dir = "/"
	parent_dir = parent_directory + dir
	path = parent_dir + file_to_download
	return send_file(path)

@app.route('/')
@app.route('/dir/<dir>')
@login_required
def index(dir = None):
	parent_directory = expanduser("~") + app.config['RESOURCES-DIRECTORY']
	if dir is None:
		dir = "/"
	file_details = []
	parent_dir = parent_directory + dir
	files_in_directory = os.listdir(parent_dir)

	for file_name in files_in_directory:
		dt = parse(str(time.ctime(os.path.getmtime(parent_dir + file_name))))
		parsed_date = dt.strftime('%Y-%m-%d %H:%M:%S')
		file_size = os.stat(parent_dir + file_name).st_size
		file_details.append([file_name, str(parsed_date), sizeof_fmt(file_size)])
	return render_template('index.html', content = file_details)

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
