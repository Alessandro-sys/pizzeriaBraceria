from datetime import datetime

lista_dizionari = [
    {"nome": "Mario", "cognome": "Rossi", "data": "2023/08/05", "ora": "14:30"},
    {"nome": "Luca", "cognome": "Bianchi", "data": "2023/08/05", "ora": "12:45"},
    {"nome": "Anna", "cognome": "Verdi", "data": "2023/08/04", "ora": "09:15"},
]

lista_dizionari_ordinata = sorted(lista_dizionari, key=lambda x: (datetime.strptime(x["data"], "%Y/%m/%d"), datetime.strptime(x["ora"], "%H:%M")) , reverse=True)

print(lista_dizionari_ordinata)
