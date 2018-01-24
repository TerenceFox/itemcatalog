from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index_loggedin.html')


@app.route('/category/<string:id>')
def showCategory(id):
    return render_template('category.html', id=id)
