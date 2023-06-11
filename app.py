from flask import Flask, render_template, request, url_for, redirect, flash
import os
import psycopg2
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Initialize flask
app = Flask(__name__)
app.secret_key = "mjuwamWAAW"

# Get database connection URL from environment variables
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.route("/")
def index():
    """
    Route to home page. It retrieves and displays all records from the pantry table in the database.
    """
    # Execute a SQL query to fetch all records from the pantry table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM pantry ORDER BY id ASC''')
            data = cursor.fetchall()
    # Render the index.html template and pass the fetched data
    return render_template("index.html", data=data)


@app.route("/add/", methods=["POST", "GET"])
def add():
    """
    Route to add a new record to the pantry table. It handles both GET (display the form)
    and POST (submit the form) methods.
    """
    if request.method == 'POST':
        # Fetch form data
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        size = request.form['size']
        exp_date = request.form['exp_date']

        # Insert new record into pantry table
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO pantry (product_name, quantity, size, exp_date)
                    VALUES (%s, %s, %s, %s)
                    ''', (product_name, quantity, size, exp_date))

        # Commit the transaction
        connection.commit()
        # Redirect to the home page after successful addition
        return redirect(url_for('index'))

    # Render the add.html form in case of GET request
    return render_template("add.html")


@app.route("/update/", methods=["POST"])
def update():
    """
    Route to update an existing record in the pantry table. It handles POST method only.
    """
    if request.method == "POST":
        # Fetch form data
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        size = request.form['size']
        exp_date = request.form['exp_date']
        id = request.form['id']

        # Update the record in pantry table
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('''UPDATE pantry SET product_name=%s, quantity=%s, size=%s, 
                               exp_date=%s WHERE id=%s''', (product_name, quantity, size, exp_date, id))
        # Commit the transaction
        connection.commit()

        # Redirect to the home page after successful update
        return redirect(url_for('index'))


@app.route("/delete/<id>", methods=["POST", "GET"])
def delete(id):
    """
    Route to delete an existing record from the pantry table. It handles both GET (confirmation)
    and POST (actual deletion) methods.
    """
    # Delete the record from pantry table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM pantry WHERE id=%s''', (id,))
    # Commit the transaction
    connection.commit()
    # Redirect to the home page after successful deletion
    return redirect(url_for('index'))
