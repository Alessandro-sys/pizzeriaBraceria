from cs50 import SQL

db = SQL("sqlite:///database.db")

while True:
    item = input("Orario ")
    db.execute("INSERT INTO orari_disponibili (orario) VALUES (?)", item)