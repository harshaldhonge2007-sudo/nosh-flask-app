from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


# -------------------------
# APP SETUP
# -------------------------
app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY", "dev-key")

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "nosh.db")



# -------------------------
# DATABASE HELPERS
# -------------------------
def get_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Dashboard table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dashboard_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        calories INTEGER DEFAULT 0,
        water INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# AUTH ROUTES
# -------------------------
@app.route("/")
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()

    if user:
        session["user_id"] = user[0]
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        init_db()   # <-- IMPORTANT

        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password)
            )
            user_id = cur.lastrowid

            cur.execute(
                "INSERT INTO dashboard_data (user_id) VALUES (?)",
                (user_id,)
            )

            conn.commit()
            print("SIGNUP SUCCESS:", email)


        except sqlite3.IntegrityError:
            conn.close()
            return redirect(url_for("login"))

        conn.close()
        return redirect(url_for("login"))

    return render_template("signup.html")


# -------------------------
# DASHBOARD (PROTECTED)
# -------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

# -------------------------
# MODULE PAGES (PROTECTED)
# -------------------------
@app.route("/workout")
def workout():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("workout.html")


@app.route("/diet")
def diet():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("diet.html")


@app.route("/mentalhealth")
def mentalhealth():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("mentalhealth.html")


@app.route("/custom_diet_plan")
def custom_diet_plan():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("custom_diet_plan.html")


# -------------------------
# WORKOUT DETAIL ROUTES (FIX FOR WERKZEUG ERROR)
# -------------------------
@app.route("/fullbody")
def fullbody():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("fullbody.html")


@app.route("/upper-lower")
def upperlowerworkout():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("upperlowerworkout.html")


@app.route("/powerlift")
def powerliftworkout():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("powerliftworkout.html")


@app.route("/push-pull")
def pushpull():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("pushpull.html")


@app.route("/bro-split")
def brosplit():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("brosplit.html")


@app.route("/arnold")
def arnold():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("arnold.html")


@app.route("/german-volume")
def germanworkout():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("germanworkout.html")


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------------
# APP START (RENDER READY)
# -------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
