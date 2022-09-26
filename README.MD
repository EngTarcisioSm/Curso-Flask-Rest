# 037 Transformando relacionamento de agregação em composição

- Observação
    - Ao criar um hotel com site "site_id" que não existe, o sistema cria esse erro deve ser corrigido 
    - Ao apagar um site, efetuando busca por hoteis no recurso hoteis o mesmo continua aparecendo sendo que o mais logico seria nenhum hotel associado aquele site aparecer 
        - A situação atual seria uma situação de agregação onde mesmo o site sendo excluido, os hoteis associados a ele permaneceria, ao "corrigir" essa situação a relação passa a de fato ser de composição 
- Att
    - models/siteModel.py (1,2)
    - resources/hotel.py (3,4)
    - models/siteModel.py (5)