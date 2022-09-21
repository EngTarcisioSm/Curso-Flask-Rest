# 021_Criando_login

- Criação do recurso de efetuar login com o usuario
- Att
    - resources/usuario.py (1,2,3,4,5,6,7,8,9,10,11)
    - app.py (12,13,14,15)

- Observações 
    - É instalado a biblioteca Flask-JWT, responsavel por efetuar login e logout 
        - pip install Flask-JWT-Extended
    - ) Werkzeug==2.2.2 não possui mais a função de comparação segura de string sendo necessário um downgrade para a versiona 2.0.0 que possui a função 
        - pip install Werkzeug==2.0.0
    - A partir da implementação do JWT torna-se possivel exigir que o usuario possua um token de acesso para poder consumir a aplicação 