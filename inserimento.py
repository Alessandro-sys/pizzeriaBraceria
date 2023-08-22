# from cs50 import SQL

# db = SQL("sqlite:///database.db")
# while True:
#     nome = input("Nome: ")
#     prezzo = input("Prezzo: ")
#     descrizione = input("Descrizione: ")

#     if not descrizione:
#         db.execute("INSERT INTO antipasti (food_name, price) VALUES (?, ?)", nome, prezzo)
#     else:
#         db.execute("INSERT INTO antipasti (food_name, price, description) VALUES (?, ?, ?)", nome, prezzo, descrizione)


from cs50 import SQL

db = SQL("sqlite:///database.db")
dbUsers = SQL("sqlite:///users.db")


orari = db.execute("SELECT * FROM orari_disponibili")

for orario in orari:
    orarioDaInserire = orario["orario"]
    dbUsers.execute("INSERT INTO orari_disponibili (orario) VALUES (?)", str(orarioDaInserire))