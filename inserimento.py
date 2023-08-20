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

antipasti = db.execute("SELECT * FROM antipasti")

for element in antipasti:
    if element["description"] == None:
        db.execute("UPDATE antipasti SET description = '' WHERE food_name = ?", element["food_name"])
