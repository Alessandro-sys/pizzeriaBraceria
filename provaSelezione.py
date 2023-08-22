from cs50 import SQL


db = SQL("sqlite:///database.db")


categorie = db.execute("SELECT * FROM categorie")

cibi = []

for categoria in categorie:
    cibiDatabase = db.execute("SELECT * FROM ?", categoria["categoria"])
    cibi.append(cibiDatabase)


for categoria in cibi:
    print("CATEGORIA BREAK")
    for cibo in categoria:
        print(cibo)