import sqlite3
from flask import Flask, render_template, request, redirect


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
con = sqlite3.connect("drama.db", check_same_thread=False)
db = con.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        rating = request.form.get("rating")
        db.execute("INSERT INTO dramas (name, rating) VALUES (?, ?)", (title, rating))
        con.commit()
        return redirect("/")

    else:
        dramas = db.execute("SELECT * FROM dramas").fetchall()
        return render_template("index.html", dramas=dramas)
