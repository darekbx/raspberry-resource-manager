from app import app
from flask import render_template, redirect

from app.forms import LoginForm
from app import models
from app import login_manager
from flask_login import login_user, logout_user, login_required

@app.route('/')
@login_required
def index():
	
	users = models.User.query.all()

	return render_template('index.html', name="{0}".format(len(users)))

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route('/login', methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = models.User.query.filter_by(name=form.name.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect("/")

	return render_template('login.html', form=form)
