from sql_alchemy import banco


class UserModel(banco.Model):
    # 1. Inserção do nome da tabela e as colunas para que o SQL_Alchemy consiga gerar a tabela 
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Interger, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    # 2. Parametros de inicialização do objeto
    def __init__(self, login, senha) -> None:
        self.login = login
        self.senha = senha
        # 3. o proprio SQL_Alchemy incrementará automaticamente o user_id

    # 4. O json utilizado é apenas do id e login
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    # 5. Será necessário a localização de usuarios efetuada pelo ID
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    # 6. Atualiza a tabela quando inseridos novos usuarios 
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
    
    # 7. Não existirá update de usuarios 
    # def update_hotel(self, nome, estrelas, diaria, cidade):
    #     self.nome = nome
    #     self.estrelas = estrelas
    #     self.diaria = diaria
    #     self.cidade = cidade
    
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()