from cs50 import SQL


db = SQL("sqlite:///database.db")


categorie = db.execute("SELECT * FROM categorie")

cibi = []

for categoria in categorie:
    cibiDatabase = db.execute("SELECT * FROM ?", categoria["categoria"])

    csx = []
    cdx = []

    for cibo in cibiDatabase:
        if (cibo["id"] % 2) == 0:
            csx.append(cibo)
        else:
            cdx.append(cibo)

    doppioCibo = []

    doppioCibo.append(csx)
    doppioCibo.append(cdx)

    cibi.append(doppioCibo)


for categoria in cibi:
    print("CATEGORIA BREAK")
    for singolaCategoria in categoria:
        for cibo in singolaCategoria:
            print(cibo)