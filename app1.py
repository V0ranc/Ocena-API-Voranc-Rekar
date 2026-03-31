from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3

app = Flask(__name__, template_folder="templates1", ststic_folder="static1")
app.secret_key = "skrivnost123"

DB_pot="db1.sqlite3"
#--- Baza ---
def baza():
    conn = sqlite3.connect('db1.sqlite3')
    c = conn.cursor()
    c.execute('create table if not exists user (id intiger primary key autoincrement, username text, password text)')
    c.execute('create table if not exists notes (id intiger primary key autoincrement, context text, user_id integer)')
    c.commit()
    c.close()

    init_db()


#--- registracija ---
@app.route("/reg", methods = ["GET", "POST"])
def reg():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]