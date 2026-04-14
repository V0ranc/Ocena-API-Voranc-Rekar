from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3
import bcrypt

app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = "6549321251"
DB_pot="db2.sqlite3"

#--- Baza ---
def baza():
    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute("create table if not exists user (id integer primary key autoincrement, username text, password text)")
    c.execute("create table if not exists post (id integer primary key autoincrement, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, context text, image text,  user_id integer)")
    c.execute("create table if not exists com (id integer primary key autoincrement, context text, user_id integer, note_id integer)")
    conn.commit()
    conn.close()
baza()


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

#--- Main Page---
@app.route("/mainPage")
def mainPage():
    if "user_id" not in session:
        return redirect("/loggin")

    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute(""" select post.id, post.context, post.image, post.created_at, user.username from post
            join user on post.user_id = user.id 
            order by post.created_at DESC """)
    post = c.fetchall()
    c.execute("""
        select com.context, com.note_id, user.username
        from com
        join user ON com.user_id = user.id
    """)
    comments = c.fetchall()
    conn.close()

    return render_template("main.html", post=post, comments=comments)

#--ADD POST--
@app.route("/addPost", methods=["GET", "POST"])
def addPost():
    if "user_id" not in session:
        return redirect("/loggin")
    
    if request.method == "POST":
        context = request.form["context"]
        image = request.form["image"]

        conn = sqlite3.connect(DB_pot)
        c = conn.cursor()
        c.execute("insert into post (context, image, user_id) values (?, ?, ?) "), (context, image, session["user_id"])
        conn.commit()
        conn.close()

        return redirect("/mainPage")
    return render_template("addPost.html")

@app.route("/com", method=["POST"])
def com():
    if "user_id" not in session:
        return redirect("/loggin")
    
    data = request.json
    context = data.get("context")
    post_id = data.get("post_id")
    
    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute("inser into com (context, user_id, note_id) VALUES (?, ?, ?)", (context, session["user_id"], post_id))
    conn.commit()
    conn.close()

    return jsonify({
        "username": session["user_id"],
        "context": context,
        "post_id": post_id
    })