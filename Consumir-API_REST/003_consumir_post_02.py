# 1. consumir um Post ('Login') da aplicação criada 
import json 
import requests

URL = 'http://127.0.1:5000'

endpoint_login = URL + '/login'
print(endpoint_login)

body_login = {
    'login': 'bryan',
    'senha': 'nov2015'
}

header_login = {
    'Content-Type': 'application/json'
}

resposta_login = requests.request('POST', endpoint_login, json=body_login, headers=header_login)
print(resposta_login.status_code)

print("Resposta Login: ", resposta_login.json())