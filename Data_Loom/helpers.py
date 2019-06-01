import csv
import os
import urllib.request
import numpy as np
import pandas as pd
import sqlite3

from flask import redirect, render_template, request, session
from functools import wraps

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components




#import csv to the database
def import_csv_to_database(database, csv, table_name):
    con = sqlite3.connect(database)
    if not con:
        print('Could not connect to the database')

    df = pd.read_csv(csv)

    df.to_sql(con=con, name=table_name, if_exists='replace', flavor='sqlite')

    print('{}'.format(df))



def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# get a random int between 1 and 100
def pick_random():
    """Pick a random int"""
    return np.random.randint(1, 100)

# Create a sample set whenthe user registers
def create_example_dataset(user_db):
    """Create example tables and insert data into the tables"""
    user_db.execute("CREATE TABLE 'example_1' ('num1' INTEGER, 'num2' INTEGER, 'num3' INTEGER)")
    for i in range(10):
        num1 = pick_random()
        num2 = pick_random()
        num3 = pick_random()

        user_db.execute("INSERT INTO example_1 (num1, num2, num3) VALUES (:num1, :num2, :num3)",
                num1 = num1,
                num2 = num2,
                num3 = num2,
                )

    user_db.execute("CREATE TABLE 'example_2' ('num1' INTEGER, 'num2' INTEGER, 'num3' INTEGER)")

    for i in range(10):
        num1 = pick_random()
        num2 = pick_random()
        num3 = pick_random()

        user_db.execute("INSERT INTO example_1 (num1, num2, num3) VALUES (:num1, :num2, :num3)",
                num1 = num1,
                num2 = num2,
                num3 = num2,
                )

# format the plot.html
def format_plot(div, script):
    dataset_dropdown = '{% block dataset %}\n' + '{% for data in dataset %}\n' + '<option value = "{{ data }}">{{ data }}</option>\n' +'{% endfor %}\n' + '{% endblock %}'
    dataset2_dropdown = '{% block dataset2 %}\n' + '{% for data in dataset2 %}\n' + '<option value = "{{ data }}">{{ data }}</option>\n' + '{% endfor %}\n' + '{% endblock %}'

    formatted = '{% extends "layout.html" %} \n' + dataset_dropdown + dataset2_dropdown + '{% block main %}' + script + div + '\n{% endblock %}'
    return formatted

def lines(a, b):
    """Return lines in both a and b"""
    return list(set(a.split("\n")).intersection(b.split("\n")))

def plot_plot():
    """ Create the Plot"""
    # create plots with random datasets because I cant get the plotting to work with the data from the database
    #configure plot size
    width = 800
    height = 600
    plot = figure(plot_width=width, plot_height=height)

    # Create random list for x and y for testing
    x = []
    y = []

    for i in range(10):
            num1 = np.random.randint(1, 100)
            num2 = np.random.randint(1, 100)
            x.append(num1)
            y.append(num2)


    glyph_size = int(request.form.get("gylph_size"))
    glyph_shape = request.form.get("glyph_shape")
    glyph_color = request.form.get("glyph_color")
    glyph_alpha = float(request.form.get("alpha"))
    print(glyph_size)
    print(glyph_shape)
    print(glyph_color)
    print(glyph_alpha)

    if glyph_shape == 'circle':
        plot.circle(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)
    elif glyph_shape == 'square':
        plot.square(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)
    elif glyph_shape == 'triangle':
        plot.triangle(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)
    elif glyph_shape == 'diamond':
        plot.diamond(x, y, size=glyph_size, color=glyph_color, alpha=glyph_alpha)

    script, div = components(plot)

    # formatting the inserted plot.html
    dataset_dropdown = '{% block dataset %}\n' + '{% for data in dataset %}\n' + '<option value = "{{ data }}">{{ data }}</option>\n' +'{% endfor %}\n' + '{% endblock %}'
    dataset2_dropdown = '{% block dataset2 %}\n' + '{% for data in dataset2 %}\n' + '<option value = "{{ data }}">{{ data }}</option>\n' + '{% endfor %}\n' + '{% endblock %}'

    file = open("templates/plot.html", "w")
    total = '{% extends "layout.html" %} \n' + dataset_dropdown + dataset2_dropdown + '{% block main %}' + script + div + '\n{% endblock %}'
    file.write(total)
    file.close()
