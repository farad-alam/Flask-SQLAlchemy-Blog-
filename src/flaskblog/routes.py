from flaskblog import app
from flask import render_template, url_for, redirect


@app.route('/')
def home():
    return render_template('home.html', title="Flask Blog - Home")