from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3
import bcrypt

app = Flask(__name__, template_folder="templates1", static_folder="static1")

DB_pot="db1.sqlite3"
#--- Baza ---
def baza():
    conn = sqlite3.connect('db1.sqlite3')
    c = conn.cursor()
    c.execute('create table if not exists user (id integer primary key autoincrement, username text, password text)')
    c.execute('create table if not exists notes (id integer primary key autoincrement, context text, user_id integer)')
    conn.commit()
    conn.close()

# homepage
@app.route("/")
def home():
    if "user" in session:
        return redirect("/main")
    return redirect("/loggin")

#--- registracija ---
@app.route("/reg", methods = ["GET", "POST"])
def reg():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')
        haspass = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

@app.route("/loggin", methods = ["GET", "POST"])
def loggin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')

        conn = sqlite3.connect('db1.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM user where usename=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
             session["user"] = user[0]
             return redirect("/main")
        return "Napačen login"
    return render_template("loggin.html")

app.run(debug=True)
       
 
 

        