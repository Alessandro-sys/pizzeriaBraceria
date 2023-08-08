import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

db = SQL("sqlite:///database.db")
dbUsers = SQL("sqlite:///users.db")

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if len(session) == 0:
        return render_template("home.html")
    elif len(session) != 0:
        return render_template("homeLogged.html")

@app.route("/home")
def pages():
    return redirect("/")

@app.route("/menu")
def menu():
    bevande = db.execute("SELECT * FROM bevande")
    sx = []
    dx = []
    for bevanda in bevande:
        id = int(bevanda["id"])
        
        if (id % 2) == 0:
            dx.append(bevanda)
        else:
            sx.append(bevanda)

    if len(session) == 0:
        return render_template("menu.html", sx = sx, dx = dx)
    elif len(session) != 0:
        return render_template("menuLogged.html", sx = sx, dx = dx)

@app.route("/prenotazioni", methods=["GET", "POST"])
def prenotazioni():
    if request.method == "GET":
        orari = db.execute("SELECT * FROM orari_disponibili")
        if len(session) == 0:
            return render_template("prenota.html", orari = orari)
        elif len(session) != 0:
            return render_template("prenotaLogged.html", orari = orari)
    elif request.method == "POST":
        name = request.form.get("nome")
        surname = request.form.get("cognome")
        telefono = request.form.get("phone")
        data = request.form.get("date")
        ora = request.form.get("orario")
        status = ("incoming")

        if not name:
            return apology("assicurati di aver inserito il tuo nome")
        
        if not surname:
            return apology("assicurati di aver inserito il tuo cognome")
        
        if not telefono:
            return apology("assicurati di aver inserito il tuo telefono")
        
        if not data:
            return apology("assicurati di aver inserito la data")
        
        if not ora:
            return apology("assicurati di aver inserito l'ora")
        
        dbUsers.execute("INSERT INTO prenotazioni (nome, cognome, telefono, data, ora, status) VALUES (?, ?, ?, ?, ?, ?)", name, surname, telefono, data, ora, status)

        return redirect("/")
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":

        session.clear()

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return apology("assicurati di aver inserito tutti i dati")
        

        rows = dbUsers.execute("SELECT * FROM users WHERE email = ?", email)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)
        
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    

@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        nome = request.form.get("name")
        if not nome:
            return apology("Inserisci un nome")
        
        cognome = request.form.get("surname")
        if not cognome:
            return apology("Inserisci un cognome")
        
        email = request.form.get("email")
        if not email:
            return apology("Inserisci un'email")

        password = request.form.get("password")
        if not password:
            return apology("Inserisci una password")
        
        registered = dbUsers.execute("SELECT email FROM users")
        for reemail in registered:
            if email in reemail["email"]:
                return apology("Email già in uso")
        
        hash = generate_password_hash(password, method='pbkdf2', salt_length=16)

        if not check_password_hash(hash, password):
            return apology("Internal server error, please try again in a few minutes")
        
        dbUsers.execute("INSERT INTO users (name, surname, email, hash) VALUES (?, ?, ?, ?)", nome, cognome, email, hash)

        return redirect("/")
    
@app.route("/admin")
@login_required
def admin():
    
    if session["user_id"] == 1 or session["user_id"] == 2:
        return render_template("admin.html")
    
    else:
        return apology("Non sei autorizzato a visitare questa pagina.")


@app.route("/aggiungi", methods=["GET", "POST"])
@login_required
def aggiungi():
    if request.method == "GET":
        return render_template("aggiungi.html")
    elif request.method == "POST":
        nome = request.form.get("food_name")
        price = request.form.get("price")
        description = request.form.get("descrizione")

        if (not nome) or (not price):
            return apology("chigghione inserisci tutti i dati")
        
        if description == None:
            db.execute("INSERT INTO bevande (food_name, price) VALUES (?, ?)", nome, price)
        else:
            db.execute("INSERT INTO bevande (food_name, price, description) VALUES (?, ?, ?)", nome, price, description)

        return redirect("/aggiungi")

@app.route("/rimuovi", methods=["GET", "POST"])
@login_required
def rimuovi():
    if request.method == "GET":
        menu = db.execute("SELECT * FROM bevande")
        return render_template("rimuovi.html", menu = menu)
    
    if request.method == "POST":
        item = request.form.get("item")
        db.execute("DELETE FROM bevande WHERE food_name = ?", item)
        return redirect("/rimuovi")

@app.route("/utentiPrenotati", methods=["GET", "POST"])
@login_required
def utentiPrenotati():
    if request.method == "GET":
        prenotati = dbUsers.execute("SELECT * FROM prenotazioni")

        lista_dizionari_ordinata = sorted(prenotati, key=lambda x: (datetime.strptime(x["data"], "%Y-%m-%d"), datetime.strptime(x["ora"], "%H:%M")) , reverse=True)


        return render_template("utentiPrenotati.html", prenotati = lista_dizionari_ordinata)

    elif request.method == "POST":
        nuovoStatus = request.form.get("cambioStatus")
        idPrenotazione = request.form.get("idPrenotazione")
        
        if not idPrenotazione:
            return apology("Errore interno del server, riprova più tardi")

        if not nuovoStatus:
            return apology("Nuovo status non inserito correttamente")
        
        dbUsers.execute("UPDATE prenotazioni SET status = ? WHERE id = ?", nuovoStatus, idPrenotazione)

        return redirect("/utentiPrenotati")
    

@app.route("/rimuoviBook", methods=["GET", "POST"])
@login_required
def rimuoviBook():
    if request.method == "GET":
        return redirect("/utentiPrenotati")