import os

from flask import Flask, request, render_template
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/r', methods = ['POST','GET'])
def home():
    
    return render_template('temp.html',)


if __name__ == '__main__':
    app.run(debug=True)
