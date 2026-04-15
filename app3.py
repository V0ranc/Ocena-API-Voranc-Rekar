from flask import Flask, render_template, request, session, redirect, jsonify
import sqlite3
import bcrypt
import requests

app = Flask(__name__, template_folder="templates3", static_folder="static3")
app.secret_key = "jwidcnwe734749ez6zgg54567433dbbtjdfsf112"
DB_pot="db3.sqlite3"

#--- Baza ---
def baza_db():
    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS user 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT, 
                  security_answer TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS assets 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  coin_id TEXT, 
                  amount REAL, 
                  user_id INTEGER)""")
    conn.commit()
    conn.close()

baza_db()

@app.route("/")
def main():
    return render_template("loggin.html")

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

@app.route("/mainPage")
def mainPage():
    if "user_id" not in session:
        return redirect("/loggin")
    
    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute("SELECT id, coin_id, amount FROM assets WHERE user_id = ?", (session["user_id"],))
    coins = c.fetchall()
    conn.close()
    
    return render_template("mainPage.html", username=session["username"], coins=coins)

@app.route("/add_coin", methods=["POST"])
def add_coin():
    if "user_id" not in session:
        return redirect("/loggin")
    
    coin_id = request.form["coin_id"].lower().strip()
    amount = request.form["amount"]
    
    conn = sqlite3.connect(DB_pot)
    c = conn.cursor()
    c.execute("INSERT INTO assets (coin_id, amount, user_id) VALUES (?, ?, ?)", 
              (coin_id, amount, session["user_id"]))
    conn.commit()
    conn.close()
    
    return redirect("/mainPage")

@app.route("/get_price/<coin>")
def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=eur"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if coin in data:
            return jsonify({"success": True, "price": data[coin]['eur']})
    except:
        pass
    return jsonify({"success": False})



if __name__ == "__main__":
    app.run(debug=True, port=5001)