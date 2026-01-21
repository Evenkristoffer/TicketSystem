from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # endre denne

# Ekstremt enkel bruker-liste (ingen database)
USER = {"username": "admin", "password": "1234"}


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    # Hvis allerede innlogget, hopp til dashboard
    if session.get("user"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Feil brukernavn eller passord."

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
