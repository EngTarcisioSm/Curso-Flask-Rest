# Passos

## Cadastro
- Acessar
  - https://www.pythonanywhere.com/
- Clicar em:
  - Start running Python online in less than a minute!
- Na página aberta clicar em 
  - Create a Begin account
- Registrar
- Proximo passo é confirmar o email do cadastro 

## Ajustes 
- Efetuar uma cópia do projeto 
- remover arquivos desnecessários como cashes arquivos git e etc 
- o py anywher utiliza mysql logo é necessário migrar o banco de dados 
 
  - Na área de Dashboard clicar no canto superior a direita em Databases e definir uma senha para o banco de dados (brynden123456)
  - Uma nova página aparecerá com informações a serem inseridas no projeto 
    ~~~
    Database host address:brynden2022.mysql.pythonanywhere-services.com
    Username:brynden2022
    Start a console on:brynden2022$default
    ~~~
- no arquivo app.py na constante (app.config['SQLALCHEMY_DATABASE_URI'] )
  - inserir na mesma linha o prefixo "mysql:" seguido do nome do usuario seguido da senha seguido de "@" por fim o endereço do banco de dados   por fim o nome do banco de dados, ficando da seguinte forma 
    ~~~
        mysql://brynden2022:brynden123456@brynden2022.mysql.pythonanywhere-services.com/brynden2022$default
    ~~~
    - É Recomendavel em projetos reais não armazenar esses dados em código, mais sim em um arquivo a parte 

## Criando e configurando ambiente virtual 
- Na página do dashboard clicar em console 
- Clicar em bash e será aberto um console 
- Digitar o comando para criar um ambiente virtual dentro do bash aberto 
~~~
mkvirtualenv --python=/usr/bin/python3.9 venv
~~~
- Instalar as bibliotecas 
~~~
pip install flask flask-restful flask-jwt-extended flask-sqlalchemy requests mysql-connector-python Werkzeug==2.0.0
~~~

## Correções 
- Em resources/hotel.py é o unico local em que esta se manipulando diretamente o banco de dados via comandos sql com o banco sqlite3, isso deve ser corrigido 
- Para corrigir isso ao inves de importar o  "sqlite3" será importado o mysql.connector 
  - Ao utilizar esse outro modulo ele apresenta algumas sintexes diferentes 
    - Alterações em resources/hoteis.py (1,2,3,4) 
  - Algumas outras alterações devem ser efetuadas é com relação a forma a qual as pesquisas são efetuadas. Nas strings de pesquisa deve ser substituidos o "?" por "%s", essas alterações são feitas no arquivo filtros.py em resources

## Uploads dos arquivos 
- No dashboard clicando em Files é possivel ver que os arquivos do projeto
- Deve ser recriada toda a estrutura de diretorios e importando cada arquivo 
- Diretorios são criados no canto esquerdo acima colocando um nome no campo e clicando em "New directory"
- Os arquivos app.py, createDb.py e sql_alchemy.py devem ser copiados para o diretório raiz, ou seja /home/{user}

## Configurações finais 
- No dashboard clicar em web 
- Clicar em "Add a new web app"
- Clciar em next, escolher "Manual configuration", escolher a versão do python, clicar em next
- Na sessão Virtualenv clicar em "Enter path to a virtualenv, if desired" para especificar o caminho do ambiente virtual, bastando apenas inserir o nome do ambiente virtual colocado e clicar no simbolo de certo
- Em Code, "WSGI configuration file" clicar no link, será aberto uma página com a aplicação default. Na linha onde esta a função def application() esta a aplicação que esta sendo executada (uma aplicação default) deve ser deletada toda a função 
- Existem vários comentários indicando frameworks, sa sessão de flask, descomentar: 
  - import sys
  - path e as linhas de if abaixo dele e o from 
- Em path informar o caminho que aplicação esta, deixando apenas '/home/<user>' 
- Em from modifica-lo para 
  ~~~
    from app import app as application  # noqa
  ~~~
- Clicar em "SAVE"
- No dashboard em Reload clicar no botão 

- no arquivo app.py o import do banco deve ser movido para junto dos outros imports no inicio do arquivo, a inicialização do banco dada por "banco.init_app(app)" deve ser movido para baixo da linha "app = Flask(__name__) e o if ao final do arquivo deve ser totalmente removido 
- criar um recurso em app indicando que a aplicação esta funcional diretamente pelo seu link raiz, abaixo de "jwt = JWTManager(app)" 
~~~
@app.route('/')
def index():
    return '<h1>Operante!</h1>'
~~~

- Observações 
  - Ao usar mysql todas strings devem ter seu tamanho definido 
  - deve-se instalar no ambiente virtual o modulo mysqlclient