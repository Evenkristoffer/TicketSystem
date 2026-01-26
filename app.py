"""
Copyright (c) TechSupport AS -  No rights deserved.
"""

import os

import pymysql
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")


def get_db():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "ticketsystem"),
        port=int(os.environ.get("DB_PORT", "3306")),
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def init_db():
    # Lager tabeller hvis de mangler og sørger for en standard admin-bruker.
    with get_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    brukernavn VARCHAR(50) UNIQUE NOT NULL,
                    passord_hash VARCHAR(255) NOT NULL,
                    rolle ENUM('admin','support','ansatt') NOT NULL DEFAULT 'ansatt'
                ) CHARACTER SET utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tickets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    bruker_id INT NOT NULL,
                    tittel VARCHAR(100) NOT NULL,
                    beskrivelse TEXT NOT NULL,
                    status ENUM('apen','under arbeid','lukket') DEFAULT 'apen',
                    FOREIGN KEY (bruker_id) REFERENCES users(id)
                ) CHARACTER SET utf8mb4
                """
            )
            cursor.execute(
                """
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'rolle'
                """,
                (os.environ.get("DB_NAME", "ticketsystem"),),
            )
            if not cursor.fetchone():
                cursor.execute(
                    "ALTER TABLE users ADD COLUMN rolle ENUM('admin','support','ansatt') NOT NULL DEFAULT 'ansatt' AFTER passord_hash"
                )
            cursor.execute("SELECT id FROM users WHERE brukernavn = %s", ("admin",))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (brukernavn, passord_hash, rolle) VALUES (%s, %s, %s)",
                    ("admin", generate_password_hash("1234"), "admin"),
                )


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    # Hvis innlogget, hopp til dashboard
    if session.get("user"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with get_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, brukernavn, passord_hash, rolle FROM users WHERE brukernavn = %s",
                    (username,),
                )
                user = cursor.fetchone()

        if user and check_password_hash(user["passord_hash"], password):
            session["user_id"] = user["id"]
            session["user"] = user["brukernavn"]
            session["rolle"] = user["rolle"]
            return redirect(url_for("dashboard"))
        else:
            error = "Feil brukernavn eller passord."

    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    message = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if title and description:
            with get_db() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO tickets (bruker_id, tittel, beskrivelse, status)
                        VALUES (%s, %s, %s, 'apen')
                        """,
                        (session["user_id"], title, description),
                    )
            message = "Ticket lagret."
        else:
            message = "Skriv inn tittel og beskrivelse."

    with get_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT t.id, t.tittel, t.beskrivelse, t.status, u.brukernavn AS eier
                FROM tickets t
                JOIN users u ON t.bruker_id = u.id
                ORDER BY t.id DESC
                """
            )
            tickets = cursor.fetchall()

    return render_template(
        "dashboard.html",
        user=session["user"],
        rolle=session.get("rolle"),
        tickets=tickets,
        message=message,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    message = None
    roles = ["admin", "support", "ansatt"]

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role")

        if not username or not password or role not in roles:
            message = "Fyll ut alle felter og velg rolle."
            return render_template("register.html", message=message, roles=roles)
        
        with get_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM users WHERE brukernavn = %s", (username,)
                )
                if cursor.fetchone():
                    message = "Brukernavnet finnes allerede."
                    return render_template("register.html", message=message, roles=roles)

                cursor.execute(
                    "INSERT INTO users (brukernavn, passord_hash, rolle) VALUES (%s, %s, %s)",
                    (username, generate_password_hash(password), role),
                )
        return redirect(url_for("login"))

    return render_template("register.html", message=message, roles=roles)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=33096)
