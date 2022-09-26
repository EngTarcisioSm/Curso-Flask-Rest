
CONSULTA_COM_CIDADE = "SELECT * FROM hoteis \
                WHERE cidade = ? \
                and (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                LIMIT ? OFFSET ?"

CONSULTA_SEM_CIDADE = "SELECT * FROM hoteis WHERE \
                (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                LIMIT ? OFFSET ?"

def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=10,
                          diaria_min=0,
                          diaria_max=99999999999,
                          limit=50,
                          offset=0,
                          **dados):

    if cidade:
        return {
            'cidade': cidade,
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }
