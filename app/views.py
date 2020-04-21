from app import app

from os.path import expanduser #remove

from app.forms import LoginForm, RegisterForm
from app import models, login_manager, db
from flask import g, render_template, redirect 
from app.file_utils import FileUtils

from flask_login import current_user, login_user, logout_user, login_required
from dateutil.parser import parse

import time, datetime as dt
import os, shutil, stat #to remove

import hashlib

file_utils = FileUtils()



@app.route('/download/<filename>')
@login_required
def download_file(filename):
	return file_utils.download_file(filename)
	
@app.route('/delete_item/<filename>')
@login_required
def delete_item(filename):
	file_utils.delete_item(filename)
	return redirect("/")

@app.route('/')
@app.route('/dir/<dir>')
@app.route('/<dir>')
@login_required
def index(dir = None):
	if dir is None:
		files_in_directory = os.listdir(file_utils.app_directory)
		browse_dir = file_utils.resource_directory()
	else:
		browse_dir = [file_utils.app_directory]
		browse_dir.append(dir + "/")
		dir_to_browse = ""
		for list_item in browse_dir:
			if len(browse_dir) > 1:
				dir_to_browse += list_item
		browse_dir =  dir_to_browse
	
	file_utils.app_directory = browse_dir
	file_details = []


	files_in_directory = os.listdir(browse_dir)
	for file_name in files_in_directory:
		full_path = browse_dir

		dt = parse(str(time.ctime(os.path.getmtime(full_path))))
		parsed_date = dt.strftime('%Y-%m-%d %H:%M:%S')
		file_size = os.stat(full_path).st_size
		file_details.append([file_name, str(parsed_date),file_utils.sizeof_fmt(file_size)])
		print("Tutaj 1 {} ".format(file_utils.app_directory))
		print("Tutaj 2 {} ".format(browse_dir))
		if file_utils.app_directory != browse_dir:
			file_details.append(["../", str(parsed_date),file_utils.sizeof_fmt(file_size)])
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
