# 034_RelacionamentosTabelas_Criando_Classe_Site

- Observações
    - A única alteração a ser feita na classe models/Hotel, será a inclusão da chave estrangeira de site
    - Será necessário criar o models/site, com uma primary_key "site_id e uma url do tipo string
    - Por fim é necessário efetuar a representação das duas classes em "um site para muitos "HOTEL""

- Att
    - model/siteModel.py (1,2,3,4,5)
    - model/hotelModel (6,7,8,9)
    - - model/siteModel.py (10,11,12,13)
    - - model/hotelModel (14)