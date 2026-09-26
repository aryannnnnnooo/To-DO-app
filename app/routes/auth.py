from flask import session, render_template, redirect, url_for, flash, Blueprint
from app import form
from app.models import User, db
from app.form import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST", "GET"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists. Please choose a different username.", "danger")
            return render_template("register.html", form=form)

        user = User(
            username=username,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash("You have successfully registered!", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["POST", "GET"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:

            session["user"] = username
            session["user_id"] = user.id

            flash("You have successfully logged in!", "success")

            return redirect(url_for("tasks.view_tasks"))
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out" , "info")
    return redirect(url_for("auth.login"))