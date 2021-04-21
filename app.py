from flask import Flask, request, render_template, url_for
import os 
import sqlite3 as sql

app = Flask(__name__)
template_folder = os.path.join(os.path.dirname(__file__), "templates/")
app.static_folder = 'static'
app.static_url_path = '/static'

@app.route('/', methods=["GET"])
def index():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM list")
    names = cur.fetchall()
    conn.close()
    return render_template("index.html", names=names)

@app.route('/adduser' , methods=["GET"])
def goto():
    return render_template("register.html")

@app.route('/adduser', methods=["POST"])
def add():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")

    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO list (Firstname, Lastname, Email) VALUES (?,?,?)", (firstname,lastname,email))
    conn.commit()
    conn.close()

    return index()

@app.route('/edituser/<emp_id>', methods=["GET"])
def edituser(emp_id):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM list WHERE Emp_ID = ?", (emp_id))
    names = cur.fetchone()
    conn.close()
    return render_template("edituser.html", names=names)

@app.route('/editformuser', methods=["POST"])
def editformuser():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    empid = request.form.get("empid")
    
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE list SET Firstname=?,Lastname=?,Email=? WHERE Emp_ID=?", (firstname,lastname,email,empid))
    conn.commit()
    conn.close()

    return index()

@app.route('/deluser/<emp_id>', methods=["GET"])
def deluser(emp_id):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM list WHERE Emp_ID = ?", (emp_id))
    conn.commit()
    conn.close()
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)