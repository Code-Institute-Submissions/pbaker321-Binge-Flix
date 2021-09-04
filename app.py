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


# Home Page
@app.route("/")
def home():
    return render_template("home.html")


# Trending Shows
@app.route("/get_shows")
def get_shows():
    shows = mongo.db.shows.find()
    return render_template("shows.html", shows=shows)


# Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.user.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.user.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("registration.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.user.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Profile Page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.user.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        shows = list(mongo.db.shows.find().sort("_id", -1))
        return render_template("profile.html", username=username, shows=shows)

    return redirect(url_for("login"))


# User Logout
@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("You are now logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add a Show
@app.route("/add_shows", methods=["GET", "POST"])
def add_shows():
    if request.method == "POST":
        show = {
            "show_name": request.form.get("show_name"),
            "genre_name": request.form.get("genre_name"),
            "seasons": request.form.get("seasons"),
            "platform": request.form.get("platform"),
            "starring": request.form.get("starring"),
            "review": request.form.get("review"),
            "posted_by": session["user"]
        }
        mongo.db.shows.insert_one(show)
        flash("You added a show!")
        return redirect(url_for("get_shows"))

    genre_catergory = mongo.db.genre_catergory.find().sort("genre_name", 1)
    platform_catergory = mongo.db.platform_catergory.find().sort(
        "platform_name", 1)
    return render_template(
        "add_shows.html", genre_catergory=genre_catergory, platform_catergory=platform_catergory)


# Edit Show
@app.route("/edit-show/<show_id>", methods=["GET", "POST"])
def edit_show(show_id):
    if request.method == "POST":
        submit = {
            "show_name": request.form.get("show_name"),
            "genre_name": request.form.get("genre_name"),
            "seasons": request.form.get("seasons"),
            "platform": request.form.get("platform"),
            "starring": request.form.get("starring"),
            "review": request.form.get("review"),
            "posted_by": session["user"]
        }
        mongo.db.shows.update({"_id": ObjectId(show_id)}, submit)
        flash("You edited a show!")

    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    genre_catergory = mongo.db.genre_catergory.find().sort(
        "genre_name", 1)
    platform_catergory = mongo.db.platform_catergory.find().sort(
        "platform_name", 1)
    return render_template("edit_show.html", show=show, genre_catergory=genre_catergory, platform_catergory=platform_catergory)


# Delete Shows from DB
@app.route("/delete_show/<show_id>")
def delete_show(show_id):
    mongo.db.shows.remove({"_id": ObjectId(show_id)})
    flash("Show Has Been Deleted!")
    return redirect(url_for("get_shows"))


# Like a Show
@app.route("/like/<show_id>", methods=["GET", "POST"])
def like(show_id):
    if request.method == "POST":
        likes = {
            "show_likes": request.form.update("show_likes"+1),
        }
        mongo.db.shows.update({"_id": ObjectId(show_id)}, likes=likes)
        flash("You edited a show!")

    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    return render_template("shows.html", show=show)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
