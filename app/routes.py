from flask import Flask,render_template,Blueprint, flash, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User,db

main = Blueprint("main",__name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@main.route("/")
def home():
    return render_template("base.html")

@main.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        print("already logged in")
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user == None:
            return redirect(url_for("main.login"))
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            print("user login successful")
            return redirect(url_for("main.home"))
        else:
            print("wrong password")
    return render_template("login.html",form=form)

@main.route("/signup", methods=["POST","GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form=RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            print("already exists")
            return redirect(url_for("main.login"))
        new_user = User(username=form.username.data,password=generate_password_hash(form.password.data,method="pbkdf2:sha256",salt_length=8))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.login"))
    else:
        print(form.errors)
    return render_template("signup.html",form=form)

@main.route("/logout", methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))
