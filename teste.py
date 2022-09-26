import sqlite3

print("oi")
connection = sqlite3.connect('Autenticacao_Usuario/banco.db')
cursor = connection.cursor()

consulta = "SELECT * FROM hoteis WHERE (estrelas > ? and estrelas < ?) and (diaria > ? and diaria < ?) and cidade = ? LIMIT ? OFFSET ?"

resultado = cursor.execute(consulta, tuple([-1, 10, 0, 1000000000, "Rio Claro", 100, 0]))

for x in resultado:
    print(x)