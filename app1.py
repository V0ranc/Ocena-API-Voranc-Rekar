from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3
import bcrypt

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = "6549321251"
DB_pot="db1.sqlite3"

#--- Baza ---
def baza():
    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute('create table if not exists user (id integer primary key autoincrement, username text, password text)')
    c.execute('create table if not exists notes (id integer primary key autoincrement, naslov text, context text, user_id integer)')
    conn.commit()
    conn.close()
baza()

# --- homepage ---
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

        conn = sqlite3.connect(DB_pot)
        c = conn.cursor()
        c.execute('select * from user where usernamw=?', (username))
        if c.fetchone():
            conn.close()
            return "Uporabnik že obstaja"
        
        haspass = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        
        c.execute('insert into user(username, password) VALUES (?, ?)', (username, haspass))
        conn.commit()
        conn.close()

        return redirect("/loggin")

    return render_template("reg.html")

#--- login ---
@app.route("/loggin", methods = ["GET", "POST"])
def loggin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')

        conn = sqlite3.connect(DB_pot)
        c = conn.cursor()
        c.execute("SELECT * FROM user where usename=?", (username))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
             session["user"] = user[0]
             return redirect("/main")
        return "Napačen login"
    return render_template("loggin.html")

# --- MAIN PAGE ---
@app.route("/main")
def main():
    if "user" not in session:
        return redirect("/loggin")
    
    filter = request.args.get("filter")

    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()

    if filter:
        c.execute('select * from notes where naslov=?', (f"%{filter}%"))
    
    else:
        c.execute("select * from notes")

    notes = c.fetchall()
    conn.close()
    return render_template("main.html", user=session["user"])






app.run(debug=True)
       
 
 

        