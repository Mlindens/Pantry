from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "mjuwamWAAW"


@app.route("/")
def index():
    flash("Add a pantry item:")
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
def add():
    flash(f"Hi, {str(request.form['name_input'])}")
    return render_template("index.html")




