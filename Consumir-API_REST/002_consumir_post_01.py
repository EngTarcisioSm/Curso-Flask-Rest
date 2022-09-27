# 1. consumir um Post ('Cadastro') da aplicação criada 
import json 
import requests

URL = 'http://127.0.1:5000'

endpoint_cadastro = URL + '/cadastro'
print('Impressao do Endpoint: ', endpoint_cadastro)


# 2. criação do body da requisição
body_cadastro = {
    'login': 'bryan',
    'senha': 'nov2015'
}

# 3. criando o header 
headers_cadastro = {
    'Content-Type': 'application/json'
}

# 4. montagem da requisição, o terceiro parametro refere-se ao body da requisição html e o quarto parametro refere-se ao header 
resposta_cadastro = requests.request('POST', endpoint_cadastro, json=body_cadastro, headers=headers_cadastro)

# 5. verificando o status da requisição
print(resposta_cadastro.status_code)

# 6. verificando a resposta da requisição
print(resposta_cadastro.json())