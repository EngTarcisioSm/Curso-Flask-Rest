# utilizando put limitando as casas decimais 
# os metodos post e put utilizam dados semelhantes
import json 
import requests
import random
from time import sleep, time

init = time()
# login
URL = 'http://brynden2022.pythonanywhere.com/'

endpoint_login = URL + '/login'
# print(endpoint_login)

body_login = {
    'login': 'bryan2',
    'senha': '123456'
}

header_login = {
    'Content-Type': 'application/json'
}

resposta_login = requests.request('POST', endpoint_login, json=body_login, headers=header_login)
# print(resposta_login.status_code)

print("Resposta Login: ", resposta_login.json())

token = resposta_login.json()['acess_token']
# print(token)

header_include_hotel = header_login
header_include_hotel['Authorization'] = 'Bearer ' + token

LISTA_CIDADES = [
    'São Paulo',
    'Rio de Janeiro',
    'Brasília',
    'Salvador',
    'Fortaleza',
    'Belo Horizonte',
    'Manaus',
    'Curitiba',
    'Recife',
    'Goiânia',
    'Belém',
    'Porto Alegre',
    'Guarulhos',
    'Campinas',
    'São Luís',
    'São Gonçalo',
    'Maceió'
]

endpoint_cadastro = URL + '/hoteis/'



# body_include_hotel = {
#     "nome": "Hotel " + str(1),
#     "estrelas": round(random.uniform(1.0, 5.0), 1),
#     "diaria": round(random.uniform(100.00, 10000.00),2),
#     "cidade": LISTA_CIDADES[random.randint(0,len(LISTA_CIDADES)-1)],
#     "site_id": random.randint(1,3)
# }
# resposta_cadastro_hotel = requests.request('PUT', endpoint_cadastro + "Hotel " + str(1), json=body_include_hotel, headers=header_include_hotel)

# print(resposta_cadastro_hotel.status_code)

for x in range(3001, 13001):
    body_include_hotel = {
        "nome": "Hotel " + str(x),
        "estrelas": round(random.uniform(1.0, 5.0), 1),
        "diaria": round(random.uniform(100.00, 10000.00),2),
        "cidade": LISTA_CIDADES[random.randint(0,len(LISTA_CIDADES)-1)],
        "site_id": random.randint(1,3)
    }
    resposta_cadastro_hotel = requests.request('PUT', endpoint_cadastro + "Hotel " + str(x), json=body_include_hotel, headers=header_include_hotel)

    print(resposta_cadastro_hotel.status_code)
    # sleep(0.01)
finish = time()
print("Tempo: ", finish-init)