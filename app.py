from flask import Flask, request, render_template, url_for, redirect
import pymysql
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pharmacy'

conn = pymysql.connect(host = app.config['MYSQL_HOST'], user = app.config['MYSQL_USER'], password= app.config['MYSQL_PASSWORD'], db = app.config['MYSQL_DB'])

cur = conn.cursor()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    uname = request.form["uname"]
    passw = request.form["pass"]
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (uname, passw))
    user = cur.fetchone()
    while True:
        if user and user[3] == 'inventory':

            return redirect(url_for('inventory'))
        
        elif user and user[3] == 'cashier':

            return redirect(url_for('cashier'))
        
        else:
            msg = 'invalid account'
            return render_template("index.html", msg = msg)

@app.route("/inventory")
def inventory():
    cur.execute ("SELECT * FROM import_view")
    row = cur.fetchall()
    current_date = datetime.datetime.now().date()
    return render_template("inventory.html", storage=row, date=current_date)

@app.route("/cashier")
def cashier():
    return render_template("cashier.html")


@app.route('/import', methods=['POST'])
def impo():
    mname = request.form["medname"]
    truck = request.form["truck"]
    area = request.form["area"]
    emp = request.form["empname"]
    import_date = request.form["imprtdate"]
    expiration_date = request.form["exprdate"]
    quantity = request.form["tproducts"]

 
    cur.execute("""
        INSERT INTO import (medicine_id, truck_id, storage_area, employee_id, import_date, expiration_date, total_products)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (mname, truck, area, emp, import_date, expiration_date, quantity))
  
    conn.commit()
    
    return render_template("receipt.html", mname=mname, truck=truck, area=area, emp=emp, import_date=import_date, expiration_date=expiration_date, quantity=quantity)

@app.route('/delete', methods=['POST'])
def delete():
    id_s = request.form['id']
    print(id_s)
    cur.execute("DELETE FROM import WHERE import_id = %s", (id_s))
    conn.commit()
    return redirect(url_for('inventory'))

@app.route('/edit', methods=['POST'])
def edit():
    id_s = request.form['id']
    cur.execute("""SELECT * FROM import_view WHERE import_id = %s""", (id_s,))
    row = cur.fetchone()
    
    cur.execute("""SELECT * FROM import WHERE import_id = %s""", (id_s,))
    real = cur.fetchone()
    
    return render_template("edit_det.html", row=row, real=real)

@app.route('/update', methods=['POST'])
def update():
    id_s = request.form['id']
    mname = request.form['med']
    truck = request.form['truck']
    area = request.form['area']
    emp = request.form['empname']
    import_date = request.form['imprtdate']
    expiration_date = request.form['exprdate']
    quantity = request.form['tproducts']

    cur.execute("""UPDATE import SET medicine_id = %s, truck_id = %s, storage_area = %s, employee_id = %s, import_date = %s, expiration_date = %s, total_products = %s WHERE import_id = %s""", (mname, truck, area, emp, import_date, expiration_date, quantity, (id_s,),))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory'))


    
    # if user and user[3] == 'inventory':
        
    #     query = "SELECT * FROM import_view"
    #     row = execute_query(query)
        
    #     current_date = datetime.datetime.now().date()
    #     print(current_date)
            
    #     return render_template("inventory.html", storage=row, date=current_date)
    
    # elif user and user[3] == 'cashier':
    #     return render_template("cashier.html")
    
    # else:
    #     msg = "I can't let you, your account is unknown!"
    #     return render_template("index.html", msg=msg)


# @app.route('/import', methods=['POST'])
# def import_med():
#     mname = request.form["medname"]
#     truck = request.form["truck"]
#     area = request.form["area"]
#     emp = request.form["empname"]
#     import_date = request.form["imprtdate"]
#     expiration_date = request.form["exprdate"]
#     quantity = request.form["tproducts"]

#     query = """INSERT INTO import (medicine_id, truck_id, storage_area, employee_id, import_date, expiration_date, total_products)
#                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    
#     execute_query(query, (mname, truck, area, emp, import_date, expiration_date, quantity))

    
#     return render_template("receipt.html",mname = mname, truck = truck, area = area, emp = emp, import_date = import_date, expiration_date = expiration_date, quantity = quantity)


    
if __name__ == '__main__':
    app.run(debug=True)


#----------------------------------------------------
#select one data
    # c.execute("SELECT * FROM admin where admin_id = 1")
    # row = c.fetchone()
#----------------------------------------------------    
#insert data to a table
    # c.execute("""
    # INSERT INTO admin (username, password, fullname)
    # VALUES
    # ('jhoren', 'jhoren123', 'Jhogoregen')
    # """)
    # conn.commit()
    # conn.close()

    # uname = "maria"
    # passw = "maria123"
    # fname = "Maria Teresa Presillas"
    # c.execute('''INSERT INTO admin (username, password, fullname) VALUES (%s, %s, %s)''', (uname, passw, fname))

    # conn.commit()
    # conn.close()
#----------------------------------------------------
#delete data in the table
    # username_to_delete = 'example_username'
    
    #c.execute("""DELETE FROM admin WHERE username = %s""",(username_to_update))
    #conn.commit()
    #conn.close()
#----------------------------------------------------
    #c.execute("""UPDATE admin SET password = %s WHERE username = %s""",(pass,user))
    #conn.commit()
    #conn.close()
#----------------------------------------------------
#loop data in html
# <table border="1">
#         <tr>
#             <th>Username</th>
#             <th>Password</th>
#             <th>Fullname</th>
#         </tr>
#         {% for row in data %}
#         <tr>
#             <td>{{ row[0] }}</td>
#             <td>{{ row[1] }}</td>
#             <td>{{ row[2] }}</td>
#         </tr>
#         {% endfor %}
#     </table>