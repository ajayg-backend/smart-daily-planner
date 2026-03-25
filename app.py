import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = []

@app.route("/planner", methods=["GET", "POST"])
def planner():

    if request.method == "POST":


        time = request.form.get("time")
        task = request.form.get("task")
        day = request.form.get("day")

        tasks.append({
            "day": day,
            "time": time,

            "task": task
        })

    return render_template("planner.html", tasks=tasks)

@app.route("/delete/<int:index>")
def delete(index):
    if index < len(tasks):
        tasks.pop(index)
    return redirect("/planner")

@app.route("/")
def home():
    return render_template("planner.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("lifeos.db")
        c = conn.cursor()

        c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))

        conn.commit()
        conn.close()

        return redirect("/login")
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("lifeos.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
                  
        user = c.fetchone()

        conn.close()

        if user:
            return redirect("/")
        else:
            return "Login Failed"
        
    return render_template("login.html")

    
def create_db():
    conn = sqlite3.connect("lifeos.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()
    
create_db()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5001))
    )

