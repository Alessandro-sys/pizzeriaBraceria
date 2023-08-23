import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
# librerie per il cambio email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
import random
import time


from helpers import apology, login_required


db = SQL("sqlite:///database.db")
dbUsers = SQL("sqlite:///users.db")

past_order = "all"
newPassword = None
emailToRecover = ""


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
        # if the user is not logged returns the home not logged template
        return render_template("home.html")
    
    elif len(session) != 0:
        if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:
            return render_template("homeAdmin.html")
        else:
            return render_template("homeLogged.html")


@app.route("/home")
def pages():
    # if the user gets in the www.divinapizzeria.com/home gets redirected in the / link
    return redirect("/")


@app.route("/menu")
def menu():

    categorie = db.execute("SELECT * FROM categorie")

    cibi = []

    for categoria in categorie:
        nomeCategoria = categoria["categoria"]
        cibiDatabase = db.execute("SELECT * FROM ?", categoria["categoria"])

        csx = []
        cdx = []

        cibiDatabaseSenzaNascosti = []

        for cibo in cibiDatabase:
            if cibo["status"] == "show":
                cibiDatabaseSenzaNascosti.append(cibo)
        
        for cibo in cibiDatabaseSenzaNascosti:
            if (cibo["id"] % 2) == 0:
                csx.append(cibo)
            else:
                cdx.append(cibo)

        doppioCibo = []

        doppioCibo.append(csx)
        doppioCibo.append(cdx)

        dizionario = {}
        dizionario["nome_categoria"] = nomeCategoria.upper()
        dizionario["contenuto_categoria"] = doppioCibo
        cibi.append(dizionario)


    
    if len(session) == 0:
        # if user is not logged, prints the menu in the not logged template
        return render_template("menu.html", cibi = cibi)
    
    elif len(session) != 0:
        # if user is logged, prints the menu in the logged template
        return render_template("menuLogged.html", cibi = cibi)


@app.route("/prenotazioni", methods=["GET", "POST"])
def prenotazioni():
    if request.method == "GET":
        # selects every time avaliable for booking
        orari = dbUsers.execute("SELECT * FROM orari_disponibili")

        orariEffettivi = []

        for orario in orari:
            if orario["status"] == "disp":
                    orariEffettivi.append(orario)

        
        orariOrdinati = sorted(orariEffettivi, key=lambda x: datetime.strptime(x["orario"], '%H:%M'))

        if len(session) == 0:
            # if user is not logged, prints the booking in the not logged template
            return render_template("prenota.html", orari = orariOrdinati)
        
        elif len(session) != 0:
            # if user is logged, prints the booking in the logged template
            return render_template("prenotaLogged.html", orari = orariOrdinati)


    elif request.method == "POST":
        # gets name from the form
        name = request.form.get("nome")

        # gets surname from the form
        surname = request.form.get("cognome")

        # gets password from the form
        telefono = request.form.get("phone")

        # gets date from the form
        data = request.form.get("date")

        # gets time from the form
        ora = request.form.get("orario")

        email = request.form.get("email")

        # gets how many people are coming
        posti = request.form.get("posti")
        
        # set the status of the order to default "incoming"
        status = ("pending")

        # checks if all data is correctly inserted
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
        
        if not email:
            return apology("assicurati di aver inserito l'email")
        
        if not posti:
            return apology("assicurati di aver inserito il numero di persone")

        dataConvertita = datetime.strptime(data, "%Y-%m-%d")

        data = dataConvertita.strftime("%d-%m-%Y")
        

        # inserts the booking into the database
        dbUsers.execute("INSERT INTO prenotazioni (nome, cognome, telefono, data, ora, status, posti, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", name, surname, telefono, data, ora, status, posti, email)

        idPrenotazione = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]
            

        dbUsers.execute("INSERT INTO gestione_prenotazioni (id_prenotazione, data, ora) VALUES (?, ?, ?)", idPrenotazione, data, ora)

        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.starttls()
        s.login("chiarulli14@gmail.com", "dajfosbvggcdemwu")

        newPasswordSend = Template('''

Gentile $nome,

La prenotazione richiesta per il $data alle $ora presso il nostro ristorante Divina è attualmente in attesa di conferma.

Dettagli della Prenotazione:
- Data: $data
- Ora: $ora
- Numero di Persone: $posti
- Nome del Cliente: $nome
- Numero di Contatto: $telefono

Stiamo lavorando per verificare la disponibilità e confermare la vostra prenotazione. 

Appena avremo ulteriori informazioni sulla conferma della vostra prenotazione, vi contatteremo immediatamente. 

Nel frattempo, vi invitiamo a rimanere in contatto con noi attraverso il numero 0805615713 per eventuali domande.

Cordiali saluti,
Divina Pizzeria Braceria

        ''')
        
        body = newPasswordSend.substitute(nome = name, data = data, ora = ora, posti = posti, telefono = telefono)

        senderEmail = "chiarulli14@gmail.com"


        msg = MIMEMultipart()
        msg['From'] = senderEmail
        msg['To'] = email
        msg['Subject'] = "Ricezione Prenotazione Divina"
        msg.attach(MIMEText(body, 'plain'))

        s.send_message(msg)
        s.quit()
        del msg


        # email al gestore
        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.starttls()
        s.login("chiarulli14@gmail.com", "dajfosbvggcdemwu")

        newPasswordSend = Template('''

Per favore verifica le disponibilità per la data richiesta e confermala/rifiutala

                                   
Dettagli della Prenotazione:
- Data: $data
- Ora: $ora
- Numero di Persone: $posti
- Nome del Cliente: $nome
- Numero di Contatto: $telefono
                                   
gestisci la prenotazione dal pannello di controllo


        ''')
        
        body = newPasswordSend.substitute(nome = name, data = data, ora = ora, posti = posti, telefono = telefono)

        senderEmail = "chiarulli14@gmail.com"


        msg = MIMEMultipart()
        msg['From'] = senderEmail
        
        utenti = dbUsers.execute("SELECT * FROM users")
        admin = []
        for utente in utenti:
            if utente["id"] == 1 or utente["id"] == 5:
                admin.append(utente["email"])

        emailAdminList = ', '.join(admin)
        
        msg['To'] = emailAdminList
        msg['Subject'] = "Nuova richiesta di prenotazione"
        msg.attach(MIMEText(body, 'plain'))

        s.send_message(msg)
        s.quit()

        del msg

        ## DA SISTEMARE DOPO. VA MODIFICATO LO STATUS SOLO ALLA DATA SELEZIONATA
        # db.execute("UPDATE orari_disponibili SET status = 'ndisp' WHERE orario = ?", ora)
        # user gets redirected to the homepage
        return redirect("/prenotazioneInviata")
    

@app.route("/logout")
def logout():
    # if the logout button is pressed the session resets
    session.clear()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # renders the template of the login page
        return render_template("login.html")
    
    elif request.method == "POST":
        
        # clears every past cookie from other sessions
        session.clear()

        # takes email from form
        email = request.form.get("email")
        
        # takes password from form
        password = request.form.get("password")

        # checks if email and password are correctly inserted
        if not email or not password:
            return apology("assicurati di aver inserito tutti i dati")
        
        # selects the user from the email from database
        rows = dbUsers.execute("SELECT * FROM users WHERE email = ?", email)

        # if len of array returned is not 1 or password is not the same as the return, returns error
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)
        
        # if everything is correct starts the session for the selected user
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    

@app.route("/register", methods=["GET", "POST"])
def register():

    # cleans session from past cookies
    session.clear()


    if request.method == "GET":
        # renders template for registration
        return render_template("register.html")
    
    
    elif request.method == "POST":
        # takes name from the form
        nome = request.form.get("name")
        
        # if no name is inserted returns error
        if not nome:
            return apology("Inserisci un nome")
        

        # takes surname from the form
        cognome = request.form.get("surname")
        
        # if no surname is inserted returns error
        if not cognome:
            return apology("Inserisci un cognome")
        

        # takes email from the form
        email = request.form.get("email")
        
        # if no email is inserted returns error
        if not email:
            return apology("Inserisci un'email")

        # takes password from the form
        password = request.form.get("password")
        
        # if no password is inserted returns error
        if not password:
            return apology("Inserisci una password")
        
        # selects every registered user from database
        registered = dbUsers.execute("SELECT email FROM users")
        
        # for each email in the database, if exists a mail same as the one inserted returns error
        for reemail in registered:
            if email == reemail["email"]:
                return apology("Email già in uso")
        
        # criptation of the password
        hash = generate_password_hash(password, method='pbkdf2', salt_length=16)

        # checks if the criptation is correct
        if not check_password_hash(hash, password):
            return apology("Internal server error, please try again in a few minutes")
        
        
        
        # inserts the new user's data into the database
        dbUsers.execute("INSERT INTO users (name, surname, email, hash) VALUES (?, ?, ?, ?)", nome, cognome, email, hash)

        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.starttls()
        s.login("chiarulli14@gmail.com", "dajfosbvggcdemwu")

        newPasswordSend = Template("Ciao $nome, benvenuto in Divina. L'account alla mail $mail è stato creato con successo!")
        
        body = newPasswordSend.substitute(nome = nome, mail = email)

        senderEmail = "chiarulli14@gmail.com"


        msg = MIMEMultipart()
        msg['From'] = senderEmail
        msg['To'] = email
        msg['Subject'] = "Conferma Registrazione"
        msg.attach(MIMEText(body, 'plain'))

        s.send_message(msg)
        s.quit()
        del msg

        return redirect("/registrazioneAvvenuta")
    

@app.route("/admin")
@login_required
def admin():
    # checks if the user trying to access the admin page is user 1 or 2 (the only admins of the page)
    if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:
        return render_template("admin.html")
    
    else:
        return apology("Non sei autorizzato a visitare questa pagina.")


@app.route("/aggiungi", methods=["GET", "POST"])
@login_required
def aggiungi():
    if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:

        if request.method == "GET":
            # renders template for adding food to the menu
            categoria = request.args.get("categoria")
            return render_template("aggiungiCibo.html", categoria = categoria)
        
        elif request.method == "POST":

            categoria = request.form.get("categoria")

            # takes the name of the food from the form
            nome = request.form.get("nome")

            # takes the price of the food from the menu (format x,xx (2 decimals possibly))
            price = request.form.get("prezzo")

            # takes description of the food from the form
            description = request.form.get("description")

            # if name or price is not inserted returns error
            if (not nome) or (not price):
                return apology("chigghione inserisci tutti i dati")
            

            if description == None:
                # if there's no description adds a new food with no description
                db.execute("INSERT INTO ? (food_name, price) VALUES (?, ?)", categoria, nome, price)
            else:
                # if there's a description adds a new food with description
                db.execute("INSERT INTO ? (food_name, price, description) VALUES (?, ?, ?)", categoria, nome, price, description)

            return redirect(url_for("gestioneCiboCategoria", categoria=categoria))
    else:
        return apology("Non sei autorizzato")

@app.route("/rimuovi", methods=["GET", "POST"])
@login_required
def rimuovi():
    if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:
        
        if request.method == "POST":
            status = "hidden"
            categoria = request.form.get("nomeCategoria")
            item = request.form.get("nomeCibo")

            if not categoria or not item:
                return apology("Assicurati di aver riempito tutti i campi")
            
            
            db.execute("UPDATE ? SET status = ? WHERE food_name = ?", categoria, status, item)

            return redirect(url_for("gestioneCiboCategoria", categoria=categoria))

    else:
        return apology("Non sei autorizzato")
        



@app.route("/utentiPrenotati", methods=["GET", "POST"])
@login_required
def utentiPrenotati():
    if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:
        if request.method == "GET":
            # access the global variable past_order, it containst the last order of the bookings selected
            global past_order

            # gets current date
            data_odierna = datetime.now().date()
            
            # selected every booked user from the database
            prenotati = dbUsers.execute("SELECT * FROM prenotazioni")
            
            # sorts the lists of the booked users from time
            lista_dizionari_ordinata = sorted(prenotati, key=lambda x: (datetime.strptime(x["data"], "%d-%m-%Y"), datetime.strptime(x["ora"], "%H:%M")) , reverse=True)

            # initialise three lists, one containing today orders, one containing future orders and one containing past orders
            today = []
            past = []
            incoming = []

            # adds in every list the correct booking
            for dizionario in lista_dizionari_ordinata:
                data_dizionario = datetime.strptime(dizionario["data"], "%d-%m-%Y").date()

                if data_dizionario == data_odierna:
                    today.append(dizionario)
                elif data_dizionario < data_odierna:
                    past.append(dizionario)
                else:
                    incoming.append(dizionario)
            
            # gets the selected order from the form
            ordine = request.args.get("sort")
            
            # # if no order is inserted it can be either the first time on the page or a booking status has been changed
            # if not ordine:
            #     # takes the last selected order
            #     ordine = past_order
            
            # # renders the layout of the booking based on the order selected 
            # if ordine == "all":
            #     past_order = ordine
            #     return render_template("utentiPrenotati.html", prenotati = lista_dizionari_ordinata)
            # if ordine == "today":
            #     past_order = ordine
            #     return render_template("utentiPrenotati.html", prenotati = today)
            # elif ordine == "past":
            #     past_order = ordine
            #     return render_template("utentiPrenotati.html", prenotati = past)
            # elif ordine == "incoming":
            #     past_order = ordine
            #     return render_template("utentiPrenotati.html", prenotati = incoming)

            return render_template("utentiPrenotati.html", prenotati = lista_dizionari_ordinata, passati = past, arrivo = incoming, oggi = today)


        elif request.method == "POST":
            # gets the new order status from the form
            nuovoStatus = request.form.get("cambioStatus")

            # gets the booking id from the form
            idPrenotazione = request.form.get("idPrenotazione")
        
            # checks if the id is selected
            if not idPrenotazione:
                return apology("Errore interno del server, riprova più tardi")

            # checks if the status is selected
            if not nuovoStatus:
                return apology("Nuovo status non inserito correttamente")
        
            userInfo = dbUsers.execute("SELECT * FROM prenotazioni WHERE id = ?", idPrenotazione)
            nome = userInfo[0]["nome"]
            data = userInfo[0]["data"]
            ora = userInfo[0]["ora"]
            email = userInfo[0]["email"]
            numero = userInfo[0]["telefono"]
            posti = userInfo[0]["posti"]

            if nuovoStatus == "incoming":
                s = smtplib.SMTP(host="smtp.gmail.com", port=587)
                s.starttls()
                s.login("chiarulli14@gmail.com", "dajfosbvggcdemwu")

                newPasswordSend = Template('''


Gentile $nome,

Siamo lieti di confermare la vostra prenotazione per il $data alle $ora.

Dettagli della Prenotazione:
- Data: $data
- Ora: $ora
- Numero di Persone: $posti
- Nome del Cliente: $nome
- Numero di Contatto: $numero

In caso di qualsiasi modifica o cancellazione della prenotazione, vi preghiamo di contattarci al numero 0805615713

Se avete ulteriori richieste speciali o esigenze alimentari, vi preghiamo di comunicarcele in anticipo in modo da poterle soddisfare al meglio.

Cordiali saluti,  
Divina Pizzeria Braceria



                ''')
                
                body = newPasswordSend.substitute(nome = nome, data = data, ora = ora, numero = numero, posti = posti)

                senderEmail = "chiarulli14@gmail.com"


                msg = MIMEMultipart()
                msg['From'] = senderEmail
                msg['To'] = email
                msg['Subject'] = "Conferma Prenotazione Divina"
                msg.attach(MIMEText(body, 'plain'))

                s.send_message(msg)
                s.quit()
                del msg

            elif nuovoStatus == "past":
                s = smtplib.SMTP(host="smtp.gmail.com", port=587)
                s.starttls()
                s.login("chiarulli14@gmail.com", "dajfosbvggcdemwu")

                newPasswordSend = Template('''

Gentile $nome,

Siamo spiacenti di informarvi che la prenotazione richiesta per il $data alle $ora presso il nostro ristorante Divina non è stata confermata.

Ci scusiamo sinceramente per l'inconveniente

Vi invitiamo a contattarci al numero 0805615713 per ulteriori informazioni o per discutere di alternative disponibili per una nuova prenotazione.

Ci auguriamo di avere l'opportunità di accogliervi nel nostro ristorante in futuro e vi ringraziamo per la vostra comprensione.

Cordiali saluti,
Divina Pizzeria Braceria


''')
                
                body = newPasswordSend.substitute(nome = nome, data = data, ora = ora)

                senderEmail = "chiarulli14@gmail.com"


                msg = MIMEMultipart()
                msg['From'] = senderEmail
                msg['To'] = email
                msg['Subject'] = "Prenotazione rifiutata"
                msg.attach(MIMEText(body, 'plain'))

                s.send_message(msg)
                s.quit()
                del msg

            # updates the status in the database
            dbUsers.execute("UPDATE prenotazioni SET status = ? WHERE id = ?", nuovoStatus, idPrenotazione)

            return redirect("/utentiPrenotati")
    else:
        return apology("Non sei autorizzato")
    

@app.route("/forgottenEmail", methods=["GET", "POST"])
def forgottenEmail():
    global emailToRecover
    if request.method == "GET":
        return render_template("recuperoEmail.html")
    elif request.method == "POST":
        email = request.form.get("email")
        if not email:
            return apology("Please insert a valid email")
        
        user = dbUsers.execute("SELECT * FROM users WHERE email = ?", email)
        if len(user) != 1:
            return apology("No user found")
        else:
            emailToRecover = email
            return redirect("/forgotten")



@app.route("/forgotten", methods=["GET","POST"])
def forgotten():
    global emailToRecover
    global newPassword
    if newPassword == None:
        newPassword = str(random.randint(1000, 9999))
    else:
        newPassword = newPassword

    if request.method == "GET":
        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.starttls()
        s.login("chiarulli14@gmail.com", "dajfosbvggcdemwu")

        newPasswordSend = Template("Nuova password: $password")
        password_value = newPassword
        body = newPasswordSend.substitute(password=password_value)

        print(password_value)
        email = "chiarulli14@gmail.com"


        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = emailToRecover
        msg['Subject'] = "Recupero Password Divina"
        msg.attach(MIMEText(body, 'plain'))

        s.send_message(msg)
        s.quit()
        del msg

        return render_template("recupero.html")
    elif request.method == "POST":
        inserted = request.form.get("password")

        print(newPassword)

        if inserted == newPassword:
            rows = dbUsers.execute("SELECT * FROM users WHERE email = ?", emailToRecover)
            session["user_id"] = rows[0]["id"]
            newPassword = None
            return redirect("/newPassword")
        

@app.route("/newPassword", methods=["GET", "POST"])
def newPasswordFun():
    if request.method == "GET":
        return render_template("newPassword.html")
    elif request.method == "POST":
        password = request.form.get("password")
        if not password:
            return apology("Assicurati di aver inserito la password corretta")
        
        currUser = session["user_id"]
        hash = generate_password_hash(password, method='pbkdf2', salt_length=16)
        dbUsers.execute("UPDATE users SET hash = ? WHERE id = ?", hash, currUser)

        return redirect("/")
    

@app.route("/ripristinaElementi", methods=["GET", "POST"])
@login_required
def ripristinaElementi():
    if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:
        
        if request.method == "POST":
            status = "show"
            categoria = request.form.get("nomeCategoria")
            item = request.form.get("nomeCibo")

            if not categoria or not item:
                return apology("Assicurati di aver riempito tutti i campi")
            
            
            db.execute("UPDATE ? SET status = ? WHERE food_name = ?", categoria, status, item)

            return redirect(url_for("gestioneCiboCategoria", categoria=categoria))
    else:
        return apology("Non sei autorizzato")



@app.route("/orari", methods=["GET","POST"])
@login_required
def orari():
    if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:
        if request.method == "GET":
            data = request.args.get("data")

            if not data:
                # Ottieni la data odierna
                data_odierna = datetime.now()

                # Formatta la data nel formato "dd-mm-yyyy"
                data = data_odierna.strftime("%d-%m-%Y")
            else:
                dataConvertita = datetime.strptime(data, "%Y-%m-%d")

                data = dataConvertita.strftime("%d-%m-%Y")

            orariGiàSelezionatiData = dbUsers.execute("SELECT * FROM gestione_prenotazioni WHERE data = ?", data)

            orariSelezionati = []

            for prenotazione in orariGiàSelezionatiData:
                orariSelezionati.append(prenotazione["ora"])

            orari = dbUsers.execute("SELECT * FROM orari_disponibili")

            orariModificati = []

            print(orariSelezionati)

            for orario in orari:
                if orario["orario"] in orariSelezionati:
                    orario["status"] = "prenotato"
                    orariModificati.append(orario)
                else:
                    orariModificati.append(orario)

            print(orariModificati)

            orariOrdinati = sorted(orariModificati, key=lambda x: datetime.strptime(x["orario"], '%H:%M'))

            return render_template("orari.html", orari = orariOrdinati)
        
        elif request.method == "POST":
            idOrario = request.form.get("idOrario")
            nuovoStatus = request.form.get("cambioStatus")

            if not idOrario:
                return apology("Errore interno del server", 104)
            if not nuovoStatus:
                return apology("Assdicurati di aver completato tutti i campi")
            
            dbUsers.execute("UPDATE orari_disponibili SET status = ? WHERE id = ?", nuovoStatus, idOrario)

            return redirect("/orari")

    else:
        return apology("Non sei autorizzato")
    

@app.route("/aggiungiOrario", methods=["GET","POST"])
@login_required
def aggiungiOrario():
    if session["user_id"] == 1 or session["user_id"] == 5 or session["user_id"] == 8:
        if request.method == "GET":
            return redirect("/orari")
        elif request.method == "POST":
            nuovoOrario = request.form.get("nuovoOrario")

            if not nuovoOrario:
                return apology("Assicurati di aver riempito tutti i campi")
            

            def verifica_formato_ore(input_string):
                try:
                    datetime.strptime(input_string, '%H:%M')
                    return True
                except ValueError:
                    return False

            
            if verifica_formato_ore(nuovoOrario):
                dbUsers.execute("INSERT INTO orari_disponibili (orario) VALUES (?)", nuovoOrario)
                return redirect("orari")
            else:
                return apology("Assicurati di aver inserito l'orario nel formato coretto, hh:mm")

        

@app.route("/termini")
def termini():
    return render_template("termini.html")

@app.route("/cookie")
def cookie():
    return render_template("cookie.html")



@app.route("/registrazioneAvvenuta")
def registrazioneAvvenuta():
    return render_template("registrazioneAvvenuta.html")

@app.route("/prenotazioneInviata")
def prenotazioneInviata():
    return render_template("prenotazioneInviata.html")



@app.route("/gestioneCategorie", methods=["GET", "POST"])
@login_required
def gestioneCategorie():
    if request.method == "GET":

        categorie = db.execute("SELECT * FROM categorie")

        cibi = []

        for categoria in categorie:
            nomeCategoria = categoria["categoria"]
            cibiDatabase = db.execute("SELECT * FROM ?", categoria["categoria"])



            dizionario = {}
            dizionario["nome_categoria"] = nomeCategoria
            dizionario["contenuto_categoria"] = cibiDatabase
            cibi.append(dizionario)


        return render_template("gestioneCategoria.html", cibi = cibi)
    
    elif request.method == "POST":
        categoria_selezionata = request.form.get("nomeCategoria")

        if not categoria_selezionata:
            return apology("assicurati di aver selezionato una categoria")
        
        return redirect(url_for("gestioneCiboCategoria", categoria=categoria_selezionata))
    


@app.route("/gestioneCiboCategoria/<categoria>", methods=["GET","POST"])
@login_required
def gestioneCiboCategoria(categoria):
    if request.method == "GET":

        cibi = db.execute("SELECT * FROM ?", categoria)

        return render_template("cibi.html", cibi = cibi, categoria = categoria)
    


@app.route("/modifica", methods=["GET","POST"])
@login_required
def modifica():
    if request.method == "GET":
        categoria = request.args.get("nomeCategoria")
        ciboSelezionato = request.args.get("nomeCibo")

        dettagliCibo = db.execute("SELECT * FROM ? WHERE food_name = ?", categoria, ciboSelezionato)
        
        food_name = dettagliCibo[0]["food_name"]
        price = dettagliCibo[0]["price"]
        description = dettagliCibo[0]["description"]

        return render_template("modificaCibo.html", categoria = categoria, nome = food_name, prezzo = price, descrizione = description)
    
    elif request.method == "POST":
        oldNome = request.form.get("oldName")
        categoria = request.form.get("categoria")
        nome = request.form.get("nome")
        prezzo = request.form.get("prezzo")
        description = request.form.get("description")
        if not description:
            description = ""
        if not nome or not prezzo:
            return apology("Assicurati di aver riempito i campi di nome e prezzo")
        if not oldNome:
            return apology("Errore del server")


        db.execute("UPDATE ? SET food_name = ? WHERE food_name = ?", categoria, nome, oldNome)
        db.execute("UPDATE ? SET price = ? WHERE food_name = ?", categoria, prezzo, nome)
        db.execute("UPDATE ? SET description = ? WHERE food_name = ?", categoria, description, nome)

        return redirect(url_for("gestioneCiboCategoria", categoria=categoria))
    


@app.route("/aggiungiCategoria", methods=["GET","POST"])
@login_required
def aggiungiCategoria():
    if request.method == "GET":
        return render_template("aggiungiCategoria.html")
    
    elif request.method == "POST":
        nomeCategoria = request.form.get("nome")

        if not nomeCategoria:
            return apology("Assicurati di aver inserito il nome della categoria")
        
        db.execute("INSERT INTO categorie (categoria) VALUES (?)", nomeCategoria)
        db.execute("CREATE TABLE ?(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, food_name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'show', price TEXT NOT NULL, description TEXT NOT NULL DEFAULT '')", nomeCategoria)

        return redirect("gestioneCategorie")