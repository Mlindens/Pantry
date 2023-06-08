from flask import Flask, render_template, request, url_for, redirect
import os
import psycopg2
from dotenv import load_dotenv

# loads variables from .env file
load_dotenv()

# initialize flask
app = Flask(__name__)
app.secret_key = "mjuwamWAAW"

# gets variable from env
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.route("/")
def index():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM pantry''')
            data = cursor.fetchall()
    return render_template("index.html", data=data)


@app.route("/add/", methods=["POST", "GET"])
def add():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        size = request.form['size']
        exp_date = request.form['exp_date']

        with connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO pantry (product_name, quantity, size, exp_date)
                    VALUES (%s, %s, %s, %s)
                ''', (product_name, quantity, size, exp_date))

        connection.commit()
        return redirect(url_for('index'))

    return render_template("add.html")


@app.route("/update", methods=["POST"])
def update():
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    size = request.form['size']
    exp_date = request.form['exp_date']
    id = request.form['id']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''UPDATE pantry SET product_name=%s, quantity=%s, size=%s, 
                           exp_date=%s WHERE id=%s''', (product_name, quantity, size, exp_date, id))
    connection.commit()
    return redirect(url_for('index'))


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form['id']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM pantry WHERE id=%s''', id)

    connection.commit()
    return redirect(url_for('index'))
