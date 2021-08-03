import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

#----- Home Page -----
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get_shows")
def get_shows():
    shows = mongo.db.shows.find()
    return render_template("shows.html", shows=shows)


#----- Registration Page -----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #----- Check if username already exists -----
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "genre": request.form.get("favourite_genre").lower()
        }
        mongo.db.user.insert_one(register)

        #----- Put User in session cookie -----
        session["user"] = request.form.get("username").lower()
        flash("Welcome! You are now registered!")
    return render_template("registration.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
