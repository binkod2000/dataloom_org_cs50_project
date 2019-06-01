import os
import re
import sys
import argparse
import pandas as pd
import numpy as np
import sqlite3
import cs50

from html import escape
from cs50 import SQL
from flask import Flask, flash, abort, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components

from helpers import apology, plot_plot, login_required, pick_random, create_example_dataset, format_plot , import_csv_to_database, lines


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///databases/dataloom.db")

user_database = ''
set_data_dropdown = ''
user_database_location = ''

@app.route("/")
@login_required
def index():

    return render_template("plot.html", dataset = set_data_dropdown, dataset2 = set_data_dropdown)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Get user name for db name
        user_database = request.form.get("username") + '_datasets.db'
        user_database_location = "databases/user_databases/" + user_database

        # Connect to user dataset database
        user_db = sqlite3.connect(user_database_location)
        if user_db == None:
            print('no file found')
            return apology("Database Not Found", 403)

        # Get just the numbers from the database query
        user_db.row_factory = lambda cursor, row: row[0]
        c = user_db.cursor()
        set_data_dropdown = c.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'").fetchall()

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("plot.html", dataset = set_data_dropdown, dataset2 = set_data_dropdown)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/plot", methods=["GET", "POST"])
@login_required
def plot():
    """Create plot from data"""
    # # Connect to user dataset database
    # user_db = sqlite3.connect(user_database_location)
    # if user_db == None:
    #     print('no file found')
    #     return apology("Database Not Found", 403)
    # else:
    #     print('db connected {}'.format(user_database))

    # #configure plot size
    # width = 800
    # height = 600
    # plot = figure(plot_width=width, plot_height=height)

    # # Grab the dataset to use and what column for x, and y
    # dataset = request.form.get("dataset")
    # dataset2 = request.form.get("dataset2")
    # x_axis = request.form.get("x_axis")
    # y_axis = request.form.get("y_axis")

    # # gets the x and y list but for some reason bokeh plots print with no glyphs
    # # Get just the numbers from the database query
    # user_db.row_factory = lambda cursor, row: row[0]
    # c = user_db.cursor()
    # xtemp = "SELECT " + x_axis + " FROM " + dataset
    # ytemp = "SELECT " + y_axis + " FROM " + dataset2
    # print(xtemp)
    # print(ytemp)

    # x = c.execute(xtemp).fetchall()
    # print(x)
    # if x == None:
    #     return apology("Dataset not found", 400)

    # y = c.execute(ytemp).fetchall()
    # print(y)
    # if y == None:
    #     return apology("Dataset not found", 400)


    # if len(x) != len(y):
    #     return apology("Length Must match", 400)

    # # variables to controll the glyphs size, color and transparency
    # glyph_size = int(request.form.get("gylph_size"))
    # glyph_shape = request.form.get("glyph_shape")
    # glyph_color = request.form.get("color")
    # glyph_alpha = float(request.form.get("alpha"))


    # if not glyph_shape or not gylph_size or not gylph_color or not gylph_aplha:
    #     return render_template("failure.html")

    # if glyph_shape == 'circle':
    #     plot.circle(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)
    # elif glyph_shape == 'square':
    #     plot.square(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)
    # elif glyph_shape == 'triangle':
    #     plot.triangle(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)
    # elif glyph_shape == 'diamond':
    #     plot.diamond(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)

    # script, div = components(plot)

    # file = open("templates/plot.html", "w")
    # total = format_plot(div, script)
    # file.write(total)
    # file.close()
    plot_plot()

    return render_template("plot.html", dataset = set_data_dropdown, dataset2 = set_data_dropdown)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("Must Confirm password", 400)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        else:

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

            # check to see if user name has been taken
            if rows:
                return apology("Username taken.", 400)
            else:

                # insert user data into table users on database dataloom
                db.execute("INSERT INTO users (first_name, last_name, username, email_address, password) VALUES (:first_name, :last_name, :username, :email_address, :password)",
                            first_name = request.form.get("first_name"),
                            last_name = request.form.get("last_name"),
                            username = request.form.get("username"),
                            email_address = request.form.get("email_address"),
                            password = generate_password_hash(request.form.get("password")))

                # Create a database for each user to store the user datasets
                # Create Database Name
                database_name = request.form.get("username") + '_datasets.db'
                data_name_loc = 'databases/user_databases/'+ database_name

                # Write a file named after the user to be used as the user database
                db_file = open(data_name_loc,"w")
                if db_file == None:
                    print('no file found')
                db_file.close()


                # Connect to user database
                user_db = SQL("sqlite:///" + data_name_loc)
                if user_db == None:
                    print('no file found')
                    return apology("User Database Not Found", 403)

                # create a example table and insert some random data in the table
                create_example_dataset(user_db)



                # Redirect user to home page
                return render_template("reg_log.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    """Handle requests for /compare via POST"""
    # # csv = request.form("upload_file")

    # table_name = request.form.get("dataset_name")
    # if not table_name:
    #     abort(400, "Missing dataset name")

    # print(type(csv))
    # print(table_name)
    # print(user_database_location)

    # # import_csv_to_database(user_database_location, csv, table_name)

    return render_template("plot.html")


# @app.route("/data_viz", methods=["GET", "POST"])
# @login_required
# def data_viz():
#     #TODO
#     return render_template("plot.html")

@app.route("/import_file", methods=["GET", "POST"])
@login_required
def import_file():
    #TODO
    return render_template("import.html")

# @app.route("/change_password", methods=["GET", "POST"])
# @login_required
# def change():
#     """Change user password"""
#     return render_template("change_password.html")
