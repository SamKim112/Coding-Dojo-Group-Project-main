from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.event import Event

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login_reg_page():
    return render_template ("home_page.html")

@app.route('/dashboard')
def dashboard_page():
    if "user_id" not in session :
        return redirect ("/")
    data = {
        "id" : session['user_id']
    }
    logged_in_user = User.get_one_by_id(data)

    return render_template ("dashboard.html", this_user = logged_in_user, events=Event.get_all())

#hidden routes
@app.route('/register', methods=["POST"])
def register_user():
    print(request.form)
    if not User.validate_registration(request.form):
        return redirect ('/')
    else: 
        hashed_password = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name" : request.form ['first_name'],
            "last_name" : request.form ['last_name'],
            "email" : request.form ['email'],
            "password" : hashed_password
        }
        session["user_id"] = User.register_user(data)
        return redirect ("/dashboard")


@app.route('/login', methods=["POST"])
def login_user():
    if not User.validate_login(request.form):
        return redirect ('/')
    else: 
        data= {
        "email" : request.form ['email']
        }
        found_user = User.get_one_by_email(data)
        session["user_id"] = found_user.id
        return redirect ("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
