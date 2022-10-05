from flask import request, url_for
from sql_alchemy import banco
# 9. importar o post do flask
from requests import post

# 10. definindo as constantes necessárias 
MAILGUN_DOMAIN = 'sandboxb1d539110ee8458db1357011202af8dd.mailgun.org'
MAILGUN_API_KEY = '3962fcd2efbcdbc171e795b8612bef71-4534758e-ded3acc0'
FROM_TITLE = 'CONFIRMAÇÃO DE CADASTRO'
FROM_EMAIL = 'no-reply@gmail.com'

class UserModel(banco.Model):

    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    # 3. inserindo o atributo que obriga o campo a não ser nulo e ser ao mesmo
    # tempo único
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    # 2. inserido o atributo que obriga o campo a não ser nulo
    senha = banco.Column(banco.String(40), nullable=False)
    # 1. Adicionando um campo de email ao cadastro, não permitindo que ele
    # seja vazio e obrigatoriamente ele deve ser unico
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    # 4. inserido o campo email para o objeto
    def __init__(self, login, senha, ativado, email) -> None:
        self.login = login
        self.senha = senha
        self.ativado = ativado
        self.email = email

    # 5. inserido o email no json
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'ativado': self.ativado,
            'email': self.email
        }

    # 6. metodo para o envio de email de confirmação
    def send_confirmation_email(self):
        # http://127.0.0.1:5000/confirmacao/{usuario_id}

        # 7. formando a url que será enviada, é utilizado o slicing "[:-1]"
        # pois o endereço ao final vem com duas barras, dessa forma elimina-se
        # uma delas
        link = request.url_root[:-1] + url_for('userconfirm',
                                               user_id=self.user_id)
        # 8. Deve ser efetuado um post para ser enviado o email, o flask
        # possui em seu modulo um meio de efetuar posts atraves de requests. O
        # Campo data refere-se a requisitos que a api de envio de emais
        # necessita, uma observação são os campos text e html, caso o email
        # não suporte html será enviado o text do contrario é enviado o html
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                          'to': self.email,
                          'subject': 'Confirmação de Cadastro',
                          'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                          'html': '<html><p>Confirme seu cadastro clicando no link a seguir: <a href="{}">CONFIRMAR EMAIL</a></p></html>'.format(link)
                          }
                    )

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    # 14. criação do metodo de busca  de usuario por email  
    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
