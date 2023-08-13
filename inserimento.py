from cs50 import SQL

db = SQL("sqlite:///database.db")

while True:
    item = input("Nome ")
    price = input("Prezzo ")
    description = input("Descrizione ")


    db.execute("INSERT INTO vini (food_name, price, description) VALUES (?, ?, ?)", item, price, description)