import os

from flask import Flask, request, render_template
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,static_folder='templates')
app.config['DEBUG'] = True


@app.route('/', methods = ['POST','GET'])
def home():
    return render_template('temp.html',)

@app.route('/login', methods = ['POST','GET'])
def login():
    return render_template('login.html',)

if __name__ == '__main__':
    app.run(debug=True)
