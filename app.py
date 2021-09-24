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
    shows = list(mongo.db.shows.find().sort("likes", -1))
    return render_template("shows.html", shows=shows)


# Show Details
@app.route("/show_details/<show_id>")
def show_details(show_id):
    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    return render_template("show_details.html", show=show)


# Search bar function
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    shows = list(mongo.db.shows.find({"$text": {"$search": query}}))
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
        flash("Registration Successful! Now add a Show")
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

    # Finds session users shows in DB
    if session["user"]:
        shows = list(mongo.db.shows.find().sort("_id", -1))
        users = mongo.db.user.find()
        return render_template(
            "profile.html", username=username, shows=shows, users=users)

    return redirect(url_for("login"))


# User Logout
@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("You are now logged out")
    session.pop("user")
    return redirect(url_for("home"))


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
            "show_image": request.form.get("show_image"),
            "posted_by": session["user"]
        }
        mongo.db.shows.insert_one(show)
        flash("You added a show!")
        return redirect(url_for("get_shows"))

    # For the dropdown menus
    genres = mongo.db.genres.find().sort("genre", 1)
    platforms = mongo.db.platforms.find().sort("platform", 1)
    return render_template(
        "add_shows.html", genres=genres, platforms=platforms)


# Edit Show
@app.route("/edit-show/<show_id>", methods=["GET", "POST"])
def edit_show(show_id):
    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    if session["user"].lower() == show["posted_by"].lower():

        if request.method == "POST":
            show_db = mongo.db.shows
            show_db.update_one({
                "_id": ObjectId(show_id),
            }, {
                "$set": {
                    "show_name": request.form.get("show_name"),
                    "genre_name": request.form.get("genre_name"),
                    "seasons": request.form.get("seasons"),
                    "platform": request.form.get("platform"),
                    "starring": request.form.get("starring"),
                    "review": request.form.get("review"),
                    "show_image": request.form.get("show_image"),
                    "posted_by": session["user"],
                }
            })
            flash("You edited a show!")
            return redirect(url_for("get_shows"))
        show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
        genres = mongo.db.genres.find().sort("genre", 1)
        platforms = mongo.db.platforms.find().sort("platform", 1)
        return render_template(
            "edit_show.html", show=show, genres=genres, platforms=platforms)


# Delete Shows from DB
@app.route("/delete_show/<show_id>")
def delete_show(show_id):
    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    if session["user"].lower() == show["posted_by"].lower():

        mongo.db.shows.remove({"_id": ObjectId(show_id)})
        flash("Successfully Deleted")
        return redirect(url_for("get_shows"))


# Like a Show
@app.route('/like/<show_id>')
def like(show_id):
    # Finds the show and adds 1
    mongo.db.shows.find_one_and_update(
        {'_id': ObjectId(show_id)},
        {'$inc': {'likes': 1}}
    )
    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    return render_template("show_details.html", show=show)


# Disike a Show
@app.route('/dislike/<show_id>')
def dislike(show_id):
    # Finds the show and minus 1
    mongo.db.shows.find_one_and_update(
        {'_id': ObjectId(show_id)},
        {'$inc': {'likes': -1}}
    )
    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    return render_template("show_details.html", show=show)


# Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('error/500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
