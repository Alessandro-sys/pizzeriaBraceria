from cs50 import SQL


db = SQL("sqlite:///database.db")


categorie = db.execute("SELECT * FROM categorie")

cibi = {}

for categoria in categorie:
    nomeCategoria = categoria["categoria"]
    cibiDatabase = db.execute("SELECT * FROM ?", nomeCategoria)

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

    cibi[nomeCategoria] = doppioCibo

    

print(cibi)
