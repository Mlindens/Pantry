from flask import Flask, render_template, request, flash, url_for
import os
import psycopg2
from dotenv import load_dotenv

# loads variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "mjuwamWAAW"

# gets variable from env
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.route("/")
def index():
    flash("Add a pantry item:")
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
def add():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = int(request.form['quantity'])
        size = request.form['size']
        exp_date = request.form['exp-date']

        with connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO pantry (name, quantity, size, exp_date)'
                               'VALUES (%s %s %s %s',
                               (product_name, quantity, size, exp_date))
        connection.commit()
        cursor.close()
        connection.close()

    return render_template()






