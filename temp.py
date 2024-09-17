import os

from flask import Flask, request, render_template
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,static_folder='templates')
app.config['DEBUG'] = True

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


import psycopg2

@app.route('/', methods = ['POST','GET'])
def home():
    return render_template('temp.html',)

@app.route('/login', methods = ['POST','GET'])
def login():
    return render_template('login.html',)

@app.route('/query', methods = ['POST','GET'])
def query():
    con=psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="2511"
    )
    cur=con.cursor()
    cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
    tables=cur.fetchall()
    con.commit()
    con.close()
    return render_template('query.html',tables=tables)

@app.route('/queryResult', methods = ['POST','GET'])
def queryResult():
    
    command=request.form["command"]
    table=request.form["table"]
    if command=="select *":
        query=command+" from "+table+';'
    elif command=="insert into":
        query=command+" from "+table+';'
    
    elif command=="alter table":
        action=request.form["action"]
        query=command+" "+table+" "+action+';'
    
    elif command=="update":
        query=command+" from "+table+';'
    
    con=psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="2511"
    )
    cur=con.cursor()
    cur.execute(query)
    rows=cur.fetchall()
    con.commit()
    con.close()
    return render_template('index.html',rows=rows)

if __name__ == '__main__':
    app.run(debug=True)

