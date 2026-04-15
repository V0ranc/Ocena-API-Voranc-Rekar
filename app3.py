from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3
import bcrypt
import requests

app = Flask(__name__, template_folder="templates3", static_folder="static3")
app.secret_key = "jwidcnwe734749ez6zgg54567433dbbtjdfsf112"
DB_pot="db3.sqlite3"

#--- Baza ---

@app.route("/")
def mainPage():

#--- registracija ---
@app.route("/reg", methods = ["GET", "POST"])
def reg():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')

        conn = sqlite3.connect(DB_pot)
        c = conn.cursor()
        c.execute('select * from user where username=?', (username,))
        if c.fetchone():
            conn.close()
            return "Uporabnik že obstaja"
        
        haspass = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        
        c.execute("insert into user(username, password) VALUES (?, ?)", (username, haspass))
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
        c.execute("SELECT * FROM user where username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
             session["user_id"] = user[0]
             session["username"] = user[1]
             return redirect("/mainPage")
        return "Napačen login"
    return render_template("loggin.html")


