import psycopg2
import os
import numpy as np

from flask import Flask, request, render_template

global user_name
global password

user_name = 'postgres'
password = "admin"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder='templates')
app.config['DEBUG'] = True


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
        cur.execute("\d security_agency")
        print(cur.fetchall())
        con.commit()
        con.close()
        return render_template('query.html', tables=tables)
    except Exception as e:
        return render_template('error.html')


@app.route('/dashboard', methods=['POST'])
def dashboard():
    global user_name
    global password
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    cur = con.cursor()
    cur.execute("Select * FROM security_agency LIMIT 0")
    tables_sa = [desc[0] for desc in cur.description]
    updated_sec_agency = request.form.getlist("rows_sec_agency")

    cur.execute("Select * FROM principle_employer LIMIT 0")
    tables_pe = [desc[0] for desc in cur.description]
    updated_pe = request.form.getlist("rows_pe")
    l1 = np.array(updated_sec_agency).reshape(
        len(updated_sec_agency) // len(tables_sa), len(tables_sa))
    l2 = np.array(updated_pe).reshape(
        len(updated_pe) // len(tables_pe), len(tables_pe))
    return render_template(
        "dashboard.html",
        colnames_sec_agency=tables_sa,
        rows_sec_agency=l1,
        colnames_pe=tables_pe,
        rows_pe=l2
    )


@app.route('/result', methods=['POST'])
def result():
    try:
        user = request.form['email']
        pswd = request.form['pass']
        if user == "admin" and pswd == "admin":
            con = psycopg2.connect(host="localhost",
                                   database="postgres",
                                   user=user_name,
                                   password=password)
            cur = con.cursor()
            cur.execute(
                """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
            )
            tables = cur.fetchall()
            cur.execute("Select * FROM security_agency LIMIT 0")
            colnames_sec_agency = [desc[0] for desc in cur.description]
            cur.execute("Select * FROM security_agency")
            rows_sec_agency = cur.fetchall()
            cur.execute("Select * FROM principle_employer LIMIT 0")
            colnames_pe = [desc[0] for desc in cur.description]
            cur.execute("Select * FROM principle_employer")
            rows_pe = cur.fetchall()
            con.commit()
            con.close()
            print(rows_sec_agency)
            return render_template('dashboard.html',
                                   colnames_sec_agency=colnames_sec_agency,
                                   rows_sec_agency=rows_sec_agency,
                                   colnames_pe=colnames_pe,
                                   rows_pe=rows_pe)
        else:
            return render_template('error.html')
            # return render_template('query.html', tables=tables)
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
                               user=user_name,
                               password=password)
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
        return render_template('queryResult.html',
                               rows=rows,
                               columns=column_names)
    except Exception as e:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
