# 1. Biblioteca necessária para manipulação do banco SQLigth
import sqlite3

# 2. Efetua conexão com o banco, caso ele não exista o mesmo é criado
connection = sqlite3.connect('banco.db')

# 3. Cria o cursos de manipulação do banco de dados
cursor = connection.cursor()

# 4. String para criação da tabela
create_table = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, \
    nome text, estrelas real, diaria real, cidade text)"

# 6. String para inserir um hotel no banco de dados
insert_hotel = " INSERT INTO hoteis VALUES('alpha', 'Alpha Hotel', 4.3, 345.30, \
    'Rio de Janeiro')"

# 7. Insere o hotel no banco de dados
cursor.execute(insert_hotel)

# 5. Cria a tabela caso a mesma já não exista
cursor.execute(create_table)
connection.commit()
connection.close()
