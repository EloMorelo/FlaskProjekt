from flask import Flask, request, render_template, redirect, session
import sqlite3
import hashlib
import logging

DB_NAME = "users.db"

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # celowo słabe

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("/var/log/app/app.log"),
        logging.StreamHandler()
    ]
)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_db():
    return sqlite3.connect(DB_NAME)


@app.route("/", methods=["GET"])
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    password_hash = hash_password(password)

    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "unknown")

    query = (
        "SELECT id, username FROM users "
        f"WHERE username = '{username}' "
        f"AND password_hash = '{password_hash}'"
    )

    app.logger.warning(
        f"LOGIN_ATTEMPT ip={ip} ua='{ua}' "
        f"query=\"{query}\""
    )

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
    except Exception as e:
        app.logger.error(f"DB_ERROR ip={ip} error={e}")
        return "Internal error", 500

    if user:
        session["user"] = user[1]
        app.logger.warning(
            f"LOGIN_SUCCESS ip={ip} user={user[1]}"
        )
        return redirect("/dashboard")

    app.logger.warning(
        f"LOGIN_FAIL ip={ip} username={username}"
    )
    return render_template("login.html", error="Invalid credentials")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
