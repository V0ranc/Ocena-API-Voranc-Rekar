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
        c.execute("SELECT * FROM user where username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
             session["user_id"] = user[0]
             session["username"] = user[1]
             return redirect("/main")
        return "Napačen login"
    return render_template("loggin.html")

# --- MAIN PAGE ---
@app.route("/main")
def main():
    if "user_id" not in session:
        return redirect("/loggin")
    
    filter_naslov = request.args.get("filter")

    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()

    if filter_naslov:
        c.execute('select * from notes where user_id=? and naslov like ?', (session["user_id"], f"%{filter_naslov}%"))
    
    else:
        c.execute("select * from notes where user_id=?", (session["user_id"],))

    notes = c.fetchall()
    conn.close()
    
    return render_template("main.html", notes=notes, filter_naslov=filter_naslov)

# ---vstvrjanje notesov ---
@app.route("/add_note", methods=["POST"])
def add_note():
    naslov = request.form["Naslov"]
    context = request.form["Polje"]

    user_id = session["user_id"]

    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute("insert into notes (naslov, context, user_id) values (?, ?, ?)", (naslov, context, user_id))
    conn.commit()
    note_id = c.lastrowid
    conn.close()

    return jsonify({
        "id": note_id,
        "naslov": naslov,
        "context": context
    })



@app.route("/delete_note", methods=["POST"])
def delete_note():
    note_id = request.form["id"]
    user_id = session["user_id"]

    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()

    c.execute("DELETE FROM notes WHERE id=? AND user_id=?", (note_id, user_id))
    conn.commit()
    conn.close()

    return redirect("/main") 


if __name__ == "__main__":
    app.run(debug=True, port=5000)
       
 
 

        