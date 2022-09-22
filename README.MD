# 023: Logout

- Lembrando que para deslogar é necessário estar logado

- Criar o recurso de logout
- Att
    - resources/usuario.py (1,2,3,4,5,6,7)
    - blacklist.py (8)
    - resources/usuario.py (9)
    - no arquivo app.py (10,11,12,13,14,15,16)







- OBSERVACAO 2
- Atualização
~~~
IMPORTANTE! Atualização do flask_jwt_extended
Houve uma atualização da biblioteca flask_jwt_extended, e uma série de coisas foram renomeadas. Para acompanhar a aula com a biblioteca atualizada você precisará fazer as seguintes adaptações:

- Substitua @jwt_required por ===> @jwt_required()

- Renomeie @jwt.token_in_blacklist_loader para ===>  @jwt.token_in_blocklist_loader

- Substitua get_raw_jwt por ===> get_jwt

- Na função def verifica_blacklist(token): acrescente um self na frente do token: ===> def verifica_blacklist(self,token):

Pode ser que funcione com apenas essas adaptações. Teste, e se ainda assim obtiver algum erro, adicione duas variáveis (jwt_header, jwt_payload) na função token_de_acesso_invalidado:

Antes def token_de_acesso_invalidado():   ===> Depois def token_de_acesso_invalidado(jwt_header, jwt_payload):

Com essas alterações, você conseguirá acompanhar o curso.

Documentação completa das alterações: https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/
~~