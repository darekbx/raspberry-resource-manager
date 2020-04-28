from app import app
from app.forms import LoginForm, RegisterForm
from app import models, login_manager, db
from flask import g, render_template, redirect , request, flash
from flask import send_file
from flask_login import current_user, login_user, logout_user, login_required
from dateutil.parser import parse
from werkzeug.utils import secure_filename


import time, datetime as dt
import os, shutil, stat
from os.path import expanduser
import hashlib

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

@app.route('/download/<path:dir>')
def download(dir):
	absolute_dir = expanduser("~") + app.config['RESOURCES-DIRECTORY']
	return send_file(os.path.join(absolute_dir, dir) , as_attachment=True)


@app.route('/delete_item/<filename>')
@login_required
def delete_item(filename):
	parent_directory = expanduser("~") + app.config['RESOURCES-DIRECTORY']
	file_to_remove = os.path.join(parent_directory, filename)


	
	is_file = os.path.isfile(file_to_remove)
	if is_file:
		
		os.chmod(file_to_remove, stat.S_IWRITE)
		os.remove(file_to_remove)
	else:
		dir_to_remove = file_to_remove
		files_in_directory_to_remove = os.listdir(dir_to_remove)

		for file_chmod in files_in_directory_to_remove:
			os.chmod(dir_to_remove + "/" + file_chmod, stat.S_IWRITE)
		
		shutil.rmtree(dir_to_remove, ignore_errors=True)
	

	if "\\" in filename:
		dir_to_display = "/dir/" + filename.rsplit("\\", 1)[0]
	else:
		dir_to_display = "/"

	flash('File has been removed!', 'success')
	return redirect(dir_to_display)

@app.route('/')
@app.route('/dir/')
@app.route('/dir/<path:dir>')
@login_required
def index(dir = ""):
	absolute_dir = expanduser("~") + app.config['RESOURCES-DIRECTORY'] + "/" + dir
	
	file_details = []
	files_in_directory = os.listdir(absolute_dir)

	if dir != "": 
		head, tail = os.path.split(dir)
		file_details.append({
			"name": "..", 
			"date": "", 
			"size": "",
			"is_dir": True,
			"path": head
		})

	for file_name in files_in_directory:
		path = os.path.join(absolute_dir, file_name)
		dt = parse(str(time.ctime(os.path.getmtime(path))))
		parsed_date = dt.strftime('%Y-%m-%d %H:%M:%S')
		file_size = os.stat(path).st_size
		file_details.append({
			"name": file_name, 
			"date": str(parsed_date), 
			"size": sizeof_fmt(file_size),
			"is_dir": os.path.isdir(path),
			"path": os.path.join(dir, file_name)
		})

	file_details.sort(key=lambda item: item['is_dir'], reverse=True)
	return render_template('index.html', content = file_details, current_dir = dir)

def allowed_file(filename):
	 return '.' in filename and \
		 filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@login_required
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
	
	if request.method == 'POST':
		dir_to_display = 'dir/' + request.form['dir_to_upload']

		if 'file' not in request.files:
			flash('Incorrect file part', 'warning')
			return redirect(dir_to_display)

		file = request.files['file']

		if file.filename == '':
			flash('Please choose a file to upload', 'warning')
			return redirect(dir_to_display)

		dir_to_save = expanduser("~") + app.config['RESOURCES-DIRECTORY'] #+ "/"
		if request.form['dir_to_upload'] != "":
			dir_to_save += request.form['dir_to_upload']

		if file and allowed_file(file.filename):

			if os.path.exists(dir_to_save + file.filename):	
				print(dir_to_save + file.filename)											
				ts = time.gmtime()
				timestamp = time.strftime("%H%M%S", ts)

				name, extension = os.path.splitext(file.filename)
				file.filename = name + "_" + timestamp + "." + extension
				flash("File has been saved successfuly as: {} ".format(file.filename), 'success')
			else:
				flash('File has been saved successfuly!', 'success')

			try:
				file.save(os.path.join(dir_to_save, secure_filename(file.filename)))
			except:
				flash('An exception occured!', 'warning')

			
		else:
			filename_split = file.filename.rsplit(".", 1)[1]
			flash('File extenstion ".{}" is not allowed!'.format(filename_split), 'warning')
			return redirect(dir_to_display)


	return redirect(dir_to_display)

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
