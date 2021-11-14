import os

from flask import Flask, request, render_template
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['DEBUG'] = True

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@app.route('/', methods = ['POST','GET'])
def home():
    return render_template('temp.html',)

@app.route('/Login/login.html', methods = ['POST','GET'])
def home():
    return render_template('login.html',)

if __name__ == '__main__':
    app.run(debug=True)
