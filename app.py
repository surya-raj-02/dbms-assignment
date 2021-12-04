import psycopg2
import os
import numpy as np

from flask import Flask, request, render_template

global user_name
global password


user_name = 'postgres'
password = "2511"
sa = {'25262': "password",
      '25261': "password",
      '25263': "password",
      '25264': "password",
      '25265': "password",
      '25266': "password",
      '25267': "password",
      '25268': "password",
      }

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder='templates')
app.config['DEBUG'] = True


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('temp.html', )


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html', )


# @app.route('/query', methods=['POST', 'GET'])
# def query():
#     try:
#         global user_name
#         global password
#         con = psycopg2.connect(host="localhost",
#                                database="postgres",
#                                user=user_name,
#                                password=password)
#         cur = con.cursor()
#         cur.execute(
#             """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
#         )
#         tables = cur.fetchall()
#         cur.execute("\d security_agency")
#         print(cur.fetchall())
#         con.commit()
#         con.close()
#         return render_template('query.html', tables=tables)
#     except Exception as e:
#         return render_template('error.html')


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


@app.route('/guardInfo', methods=['POST'])
def guardInfo():

    uid = request.form["uid"]
    user = request.form["user"]
    pswd = request.form["password"]
    print("___________________________")
    print(user)
    print(pswd)
    print("___________________________")
    print(uid)
    print("___________________________")
    if user in list(sa.keys()) and (pswd == sa[user] or pswd=="adminSA"):
        con = psycopg2.connect(host="localhost",
                               database="postgres",
                               user=user_name,
                               password=password)

        cur = con.cursor()
        query1 = "select agency_name from security_agency where agency_id="+user+";"
        cur.execute(query1)

        agency_name = cur.fetchall()[0][0]
        query = "select * from guards where uid="+uid+';'
        cur.execute(query)

        guardColnames = [desc[0] for desc in cur.description]
        guardlen = len(guardColnames)
        guardRows = cur.fetchall()[0]

        query = "select * from dependents where uan="+uid+';'
        cur.execute(query)
        depColnames = [desc[0] for desc in cur.description]
        depRows = cur.fetchall()

        query = "select * from salary where e_no="+uid+';'
        cur.execute(query)
        salColnames = [desc[0] for desc in cur.description]
        sallen = len(salColnames)
        salaryRows = cur.fetchall()[0]

        query = "select * from extras where e_no="+uid+';'
        cur.execute(query)
        extrasColnames = [desc[0] for desc in cur.description]
        exlen = len(extrasColnames)
        extrasRows = cur.fetchall()[0]

        # print("renedering template")
        return render_template('GuardDashboard.html',
                               guardlen=guardlen,
                               securityagency=agency_name,
                               guardcolnames=guardColnames,
                               depcolnames=depColnames,
                               salcolnames=salColnames,
                               exlen=exlen,
                               sallen=sallen,
                               extrascolnames=extrasColnames,
                               guardrows=guardRows,
                               deprows=depRows,
                               salrows=salaryRows,
                               extrasrows=extrasRows,
                               agency_id=user,
                               user=user,
                               password=pswd,
                               uid=uid)


@app.route('/Loginresult2', methods=['POST'])
def Loginresult2():
    try:
        temp = request.form["xyz"].split(',')
        user = temp[0][2:-1]
        pswd = temp[1][2:-2]
        
        print(user)
        print(pswd)
        if user in list(sa.keys()) and (pswd == sa[user] or pswd=="adminSA"):
            con = psycopg2.connect(host="localhost",
                                   database="postgres",
                                   user=user_name,
                                   password=password)
            cur = con.cursor()
            
            query1 = "select agency_name from security_agency where agency_id="+user+";"
            cur.execute(query1)
            agency_name = cur.fetchall()[0][0]

            query2 = "select count(*) from principle_employer where agency_id="+user+";"
            cur.execute(query2)
            noOfPE = cur.fetchall()[0][0]

            query3 = "select count(*) from guards where agency_id ="+user+";"
            cur.execute(query3)
            noOfGuards = cur.fetchall()[0][0]

            query4 = "select avg(basic_vda+hra) from salary where agency_id="+user+";"
            cur.execute(query4)
            avgSalGuards = int(cur.fetchall()[0][0])

            query5 = "select sum(pf+eldi+uniform_cost) from contributions where c_id="+user+";"
            cur.execute(query5)
            TotCon = cur.fetchall()[0][0]

            query6 = "select count(*) from manager where agency_id="+user+";"
            cur.execute(query6)
            NoOfMan = cur.fetchall()[0][0]
            try:
                updated_sec_agency = request.form.getlist("rows_sec_agency")
                print(updated_sec_agency)
                cur.execute("Select * FROM dependents LIMIT 0")
                tables_sa = [desc[0] for desc in cur.description]
                l1 = np.array(updated_sec_agency).reshape(
                    len(updated_sec_agency) // len(tables_sa), len(tables_sa))
                db_sec_agency = [i.tolist() for i in l1]
                cur.execute("Select * FROM dependents where uan="+l1[0][4]+";")
                for i in cur.fetchall():
                    for j in db_sec_agency:
                        if str(i[3])==str(j[3]):

                            l = ""
                            print("ell")
                            for p in range(len(tables_sa)-1):
                                if p>1:
                                    l = l+str(tables_sa[p])+"="+""+str(j[p])+","
                                else:
                                    l = l+str(tables_sa[p])+"="+"'"+str(j[p])+"',"
                            l = l + tables_sa[-1]+"="+str(i[-1])
                            print("UPDATE dependents SET "+l + "WHERE "+ str(tables_sa[3]) + "=" + str(i[3]) + ";")
                            cur.execute("UPDATE dependents SET "+l + " WHERE "+ str(tables_sa[3]) + "=" + str(i[3]) + ";")
                con.commit()
            except Exception as e:
                pass

            if pswd=="adminSA":
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
            return render_template('SecurityDashboard.html',
                                   securityagency=agency_name,
                                   noOfPE=noOfPE,
                                   noOfGuards=noOfGuards,
                                   AvgSalaryOfGuards=avgSalGuards,
                                   TotalContribution=TotCon,
                                   noOfManagers=NoOfMan,
                                   agency_id=user,
                                   password=pswd)
            

        else:
            return render_template('error.html')

    except Exception as e:
        print(e)
        return render_template('error.html')


@app.route('/Loginresult', methods=['POST'])
def Loginresult():
    try:
        user = request.form['email']

        print("________________________________________________________________________")
        print(user)
        print("________________________________________________________________________")
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
        # print(type(sa))
        # print(type(user))
        # print(sa[user])
        elif user in list(sa.keys()) and (pswd == sa[user] or pswd=="adminSA"):
            con = psycopg2.connect(host="localhost",
                                   database="postgres",
                                   user=user_name,
                                   password=password)
            cur = con.cursor()

            query1 = "select agency_name from security_agency where agency_id="+user+";"
            cur.execute(query1)
            agency_name = cur.fetchall()[0][0]

            query2 = "select count(*) from principle_employer where agency_id="+user+";"
            cur.execute(query2)
            noOfPE = cur.fetchall()[0][0]

            query3 = "select count(*) from guards where agency_id ="+user+";"
            cur.execute(query3)
            noOfGuards = cur.fetchall()[0][0]

            query4 = "select avg(basic_vda+hra) from salary where agency_id="+user+";"
            cur.execute(query4)
            avgSalGuards = int(cur.fetchall()[0][0])

            query5 = "select sum(pf+eldi+uniform_cost) from contributions where c_id="+user+";"
            cur.execute(query5)
            TotCon = cur.fetchall()[0][0]

            query6 = "select count(*) from manager where agency_id="+user+";"
            cur.execute(query6)
            NoOfMan = cur.fetchall()[0][0]

            return render_template('SecurityDashboard.html',
                                   securityagency=agency_name,
                                   noOfPE=noOfPE,
                                   noOfGuards=noOfGuards,
                                   AvgSalaryOfGuards=avgSalGuards,
                                   TotalContribution=TotCon,
                                   noOfManagers=NoOfMan,
                                   agency_id=user,
                                   password=pswd)

        else:
            return render_template('error.html')

    except Exception as e:
        print(e)
        return render_template('error.html')


# @app.route('/queryResult', methods=['POST', 'GET'])
# def queryResult():

#     command = request.form["command"]
#     table = request.form["table"][2:-3]
#     values = request.form["values"]

#     if command == "complex":
#         query = request.form["complex"]

#     elif "select" in command:
#         query = command + " * from " + table + ';'

#     elif command == "insert into":
#         query = command + " " + table + " values(" + values + ");"

#     elif command == "alter table":
#         action = request.form["action"]
#         query = command + " " + table + " " + action + ';'

#     elif command == "update":
#         col = request.form["set"]
#         where = request.form["where"]
#         query = command + " " + table + " set " + col + " where " + where + ';'
#         print(query)
#     try:
#         con = psycopg2.connect(host="localhost",
#                                database="postgres",
#                                user=user_name,
#                                password=password)
#         cur = con.cursor()
#         cur.execute(query)
#         if "select" in query:
#             rows = cur.fetchall()
#         else:
#             query = "select" + " * from " + table + ';'
#             cur.execute(query)
#             rows = cur.fetchall()
#         column_names = [desc[0] for desc in cur.description]
#         con.commit()
#         con.close()
#         return render_template('queryResult.html',
#                                rows=rows,
#                                columns=column_names)
#     except Exception as e:
#         return render_template('error.html')


@app.route('/securityDashboardResult_managers', methods=['POST', 'GET'])
def securityDashboardResult_managers():
    temp = request.form["managers"].split(',')
    i = temp[0][2:-1]
    pwdx = temp[1][2:-2]
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    cur = con.cursor()
    query = "select * from manager where agency_id="+i+';'
    print(query)
    cur.execute(query)
    rows = cur.fetchall()
    print(rows)
    column_names = [desc[0] for desc in cur.description]
    con.commit()
    con.close()
    return render_template('queryResult.html',
                           rows=rows,
                           columns=column_names,
                           user=i,
                           password=pwdx)


@app.route('/securityDashboardResult_contributions', methods=['POST', 'GET'])
def securityDashboardResult_contributions():
    temp = request.form["contributions"].split(',')
    i = temp[0][2:-1]
    pwdx = temp[1][2:-2]
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    cur = con.cursor()
    query = "select * from contributions where c_id="+i+';'
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    con.commit()
    con.close()
    return render_template('queryResult.html',
                           rows=rows,
                           columns=column_names,
                           user=i,
                           password=pwdx)


@app.route('/securityDashboardResult_guards', methods=['POST', 'GET'])
def securityDashboardResult_guards():
    temp = request.form["guards"].split(',')
    i = temp[0][2:-1]
    pwdx = temp[1][2:-2]
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    cur = con.cursor()
    query = "select * from guards where agency_id="+i+';'
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    con.commit()
    con.close()
    return render_template('queryResultManager.html',
                           rows=rows,
                           columns=column_names,
                           user=i,
                           password=pwdx)


@app.route('/securityDashboardResult_PE', methods=['POST', 'GET'])
def securityDashboardResult_PE():
    temp = request.form["PE"].split(',')
    i = temp[0][2:-1]
    pwdx = temp[1][2:-2]
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    cur = con.cursor()
    query = "select * from principle_employer where agency_id="+i+';'
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    con.commit()
    con.close()
    return render_template('queryResult.html',
                           rows=rows,
                           columns=column_names,
                           user=i,
                           password=pwdx)

@app.route('/dashboardEdit', methods=['POST', 'GET'])
def dashboardEdit():
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    cur = con.cursor()
    
    cur.execute("Select * FROM security_agency LIMIT 0")
    colnames_sec_agency = [desc[0] for desc in cur.description]
    collen=len(colnames_sec_agency)
    cur.execute("Select * FROM security_agency")
    rows_sec_agency = cur.fetchall()
    cur.execute("Select * FROM principle_employer LIMIT 0")
    colnames_pe = [desc[0] for desc in cur.description]
    cur.execute("Select * FROM principle_employer")
    rows_pe = cur.fetchall()
    con.commit()
    con.close()
    print(rows_sec_agency)
    return render_template('dashboardEdit.html',
                           colnames_sec_agency=colnames_sec_agency,
                           collen=collen,
                           rows_sec_agency=rows_sec_agency,
                           colnames_pe=colnames_pe,
                           rows_pe=rows_pe)

@app.route('/guardsEdit', methods=['POST', 'GET'])
def guardsEdit():
    temp = request.form["guards"].split(',')
    i = temp[0][2:-1]
    pwdx = temp[1][2:-2]
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    cur = con.cursor()
    query = "select * from guards where agency_id="+i+';'
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    con.commit()
    con.close()
    return render_template('queryResultManagerEdit.html',
                           rows=rows,
                           columns=column_names,
                           user=i,
                           password=pwdx)


@app.route('/guardUpdate', methods=['POST', 'GET'])
def guardUpdate():
    temp = request.form["guards"].split(',')
    i = temp[0][2:-1]
    pwdx = temp[1][2:-2]
    uid=request.form["uid"]
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    
    cur = con.cursor()

    cur.execute("select * from guards where agency_id="+i+';')
    colnames_guards = [desc[0] for desc in cur.description]
    for x in [0,1,2,3,4,5,6,7]:
        value=request.form[str(x)]
        query="UPDATE guards SET "+colnames_guards[x]+"=\'"+value+"\' WHERE agency_id="+str(i)+"and uid="+str(uid)+";"
        print(query)
        cur.execute(query)
    
    con.commit()


    query = "select * from guards where agency_id="+i+';'
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    con.commit()
    con.close()
    return render_template('queryResultManagerEdit.html',
                           rows=rows,
                           columns=column_names,
                           user=i,
                           password=pwdx)


@app.route('/SAUpdate', methods=['POST', 'GET'])
def SAUpdate():
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    
    cur = con.cursor()
    uid = request.form["uid"]
    user = request.form["uid"]
    pswd = request.form["password"]  

    cur.execute("Select * FROM security_agency;")
    colnames_sec_agency = [desc[0] for desc in cur.description]
    collen=len(colnames_sec_agency)
    for i in [0,2]:
        value=request.form[str(i)]
        query="UPDATE security_agency SET "+colnames_sec_agency[i]+"=\'"+value+"\' WHERE agency_id="+uid+";"
        print(query)
        cur.execute(query)
    
    con.commit()
    
    
    cur.execute("Select * FROM security_agency")
    rows_sec_agency = cur.fetchall()
    cur.execute("Select * FROM principle_employer LIMIT 0")
    colnames_pe = [desc[0] for desc in cur.description]
    cur.execute("Select * FROM principle_employer")
    rows_pe = cur.fetchall()
    con.commit()
    con.close()
    print(rows_sec_agency)
    return render_template('dashboardEdit.html',
                           colnames_sec_agency=colnames_sec_agency,
                           collen=collen,
                           rows_sec_agency=rows_sec_agency,
                           colnames_pe=colnames_pe,
                           rows_pe=rows_pe)

@app.route('/guardUpdateAdd', methods=['POST', 'GET'])
def guardUpdateAdd():
    temp = request.form["guards"].split(',')
    i = temp[0][2:-1]
    pwdx = temp[1][2:-2]
    
    con = psycopg2.connect(host="localhost",
                           database="postgres",
                           user=user_name,
                           password=password)
    
    cur = con.cursor()

    cur.execute("select * from guards where agency_id="+i+';')
    colnames_guards = [desc[0] for desc in cur.description]

    query= "INSERT INTO extras values(0,0,"+request.form[str(1)]+",0,0,0,0);"
    print(query)
    cur.execute(query)

    query= "INSERT INTO salary values("+request.form[str(5)]+",0,0,"+request.form[str(6)]+","+request.form[str(1)] +");"
    print(query)
    cur.execute(query)

    query= "INSERT INTO guards (" +colnames_guards[0]+","+colnames_guards[1]+","+colnames_guards[2]+","+colnames_guards[3]+","+colnames_guards[4]+","+colnames_guards[5]+","+colnames_guards[6]+","+colnames_guards[7]+") VALUES("+request.form[str(0)]+","+request.form[str(1)]+",'"+request.form[str(2)]+"',"+request.form[str(3)]+",'"+request.form[str(4)]+"',"+request.form[str(5)]+","+request.form[str(6)]+","+request.form[str(7)]+");"
    print(query)
    cur.execute(query)
    
    con.commit()


    query = "select * from guards where agency_id="+i+';'
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    con.commit()
    con.close()
    return render_template('queryResultManagerEdit.html',
                           rows=rows,
                           columns=column_names,
                           user=i,
                           password=pwdx)


if __name__ == '__main__':
    app.run(debug=True)
