import psycopg2
import os

from flask import Flask, request, render_template

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder='templates')
app.config['DEBUG'] = True

user_name=''
password=""
@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('temp.html', )


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html', )


@app.route('/query', methods=['POST', 'GET'])
def query():
    try:
        global user_name
        global password
        con = psycopg2.connect(host="localhost",
                            database="postgres",
                            user=user_name,
                            password=password)
        cur = con.cursor()
        cur.execute(
            """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
        )
        tables = cur.fetchall()
        con.commit()
        con.close()
        return render_template('query.html', tables=tables)
    except Exception as e:
        return render_template('error.html')


@app.route('/result', methods=['POST'])
def result():
    try:
        con = psycopg2.connect(host="localhost",
                            database="postgres",
                            user=request.form['email'],
                            password=request.form['pass'])
        cur = con.cursor()
        cur.execute(
            """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
        )
        global user_name
        user_name=request.form['email']
        global password
        password=request.form['pass']
        tables = cur.fetchall()
        con.commit()
        con.close()
        return render_template('query.html', tables=tables)
    except Exception as e:
        print(e)
        return render_template('error.html')


@app.route('/queryResult', methods=['POST', 'GET'])
def queryResult():

    command = request.form["command"]
    table = request.form["table"][2:-3]
    values = request.form["values"]

    if command == "complex":
        query = request.form["complex"]

    elif "select" in command:
        query = command + " * from " + table + ';'

    elif command == "insert into":
        query = command + " " + table + " values(" + values + ");"

    elif command == "alter table":
        action = request.form["action"]
        query = command + " " + table + " " + action + ';'

    elif command == "update":
        col = request.form["set"]
        where = request.form["where"]
        query = command + " " + table + " set " + col + " where " + where + ';'
        print(query)
    try:
        con = psycopg2.connect(host="localhost",
                            database="postgres",
                            user="postgres",
                            password="admin")
        cur = con.cursor()
        cur.execute(query)
        if "select" in query:
            rows = cur.fetchall()
        else:
            query = "select" + " * from " + table + ';'
            cur.execute(query)
            rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        con.commit()
        con.close()
        return render_template('queryResult.html', rows=rows, columns=column_names)
    except Exception as e:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
