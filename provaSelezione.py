from cs50 import SQL


db = SQL("sqlite:///database.db")


categoria  = "Pasta Cazz e Maccarun"

db.execute("DELETE FROM categorie WHERE categoria = ?", categoria)
