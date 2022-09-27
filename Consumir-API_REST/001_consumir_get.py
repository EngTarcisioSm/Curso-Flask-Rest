# 1 bibliotecas necessárias para consumir api's
import json
# 2 trata de requisições 
import requests


# 3. Passado a url através de uma constante 
URL = 'http://127.0.1:5000'

# 4. efetuar o request sobre um metodo get em /hoteis. É solicitado o metodo, e a urla a ser feita a requisição
resposta_hoteis = requests.request('GET', URL + '/hoteis')
# print(resposta_hoteis.json())

# 5. é retornado uma lista de dicionários 
hoteis = resposta_hoteis.json()
for hotel in hoteis['hoteis']:
    print(hotel)

print()

# 6. o processo é identico para o consumo de qualquer API, mesmo aquelas hospedadas em sites. Ao exemplo abaixo temos o consumo da api do mercadolivre. O exemplo é um get sobre o recurso sites que retorna o id dos sites do mercado livre
ML_URL = 'http://api.mercadolibre.com'

# 7. efetuando a requisição. vale destacar que o objeto da requisição retorna com o valor de retorno da requisição html tamblem 
lista_sites = requests.request('GET', ML_URL+'/sites')
print(lista_sites) 
listaML = lista_sites.json()
# 8. iterando sobre a lista 
for lista in listaML:
    print(lista)

# 9. Achando dados do Brasil
for lista in listaML:
    if lista['name'] == 'Brasil':
        id_Brasil = lista['id']
        break
print(id_Brasil)
print()

# 10. buscar categorias do mercadolivre Brasil
lista_categorias = requests.request('Get', ML_URL + '/sites/' + id_Brasil + '/categories')
print(lista_categorias)

categorias = lista_categorias.json()

# 11. iterando
for cat in categorias:
    print(cat)