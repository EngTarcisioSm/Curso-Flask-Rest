from sql_alchemy import banco


class UserModel(banco.Model):

    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    # 1. incluso o campo para verificação se o usuário ja foi ativado, será do 
    # tipo boolean e por default será dado como false, desta forma mesmo que o 
    # usuário não preencha esse campo terá um valor inicial de "False" 
    ativado = banco.Column(banco.Boolean, default=False)

    # 2. Adicionar o seu recebimento dentro do inicializador 
    def __init__(self, login, senha, ativado) -> None:
        self.login = login
        self.senha = senha
        self.ativado = ativado 

    # 3. acrescentado no JSON
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'ativado': self.ativado
        }

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

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()