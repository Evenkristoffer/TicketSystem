from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # endre denne

# Ekstremt enkel bruker-liste (ingen database)
USER = {"username": "admin", "password": "1234"}
TICKETS = []  # lagres i minnet
NEXT_ID = 1


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


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("user"):
        return redirect(url_for("login"))

    global NEXT_ID
    message = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if title and description:
            TICKETS.append(
                {
                    "id": NEXT_ID,
                    "title": title,
                    "description": description,
                    "status": "apen",
                    "owner": session["user"],
                }
            )
            NEXT_ID += 1
            message = "Ticket lagt til."
        else:
            message = "Skriv inn tittel og beskrivelse."

    return render_template(
        "dashboard.html", user=session["user"], tickets=TICKETS, message=message
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
