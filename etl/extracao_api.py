
import requests
import json
import os

URL = os.getenv('API_URL', 'http://127.0.0.1:8000')


def extrair_dados(rota):
    registros = []

    try:
        resposta = requests.get(URL + rota, params={'page': 1, 'page_size': 50})

    except requests.exceptions.RequestException:
        print('Erro na primeira requisição')
        return registros

    if resposta.status_code != 200:
        print('Erro na primeira página:', resposta.status_code)
        return registros

    dados = resposta.json()
    total_paginas = dados['total_pages']
    print(f'Total de páginas da rota {rota}: {total_paginas}')

    for pagina in range(1, total_paginas + 1):
        try:
            resposta = requests.get(
                URL + rota,
                params={'page': pagina, 'page_size': 50}
            )

        except requests.exceptions.RequestException:
            print('Erro de conexão na página:', pagina)
            return registros

        if resposta.status_code != 200:
            print('Página inexistente ou erro HTTP:', pagina, resposta.status_code)
            return registros

        dados = resposta.json()
        registros.extend(dados['items'])

    return registros


if __name__ == '__main__':
    clientes = extrair_dados('/clientes')
    print('Total de clientes:', len(clientes))

    pedidos = extrair_dados('/pedidos')
    print('Total de pedidos:', len(pedidos))

    if len(clientes) != 1000 or len(pedidos) != 5100:
        raise SystemExit(
            'Extração incompleta: esperados 1000 clientes e 5100 pedidos. '
            'Carga cancelada.'
        )

    with open('brutos/clientes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(clientes, arquivo, indent=4, ensure_ascii=False)
    print('Clientes salvos com sucesso!')

    with open('brutos/pedidos.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pedidos, arquivo, indent=4, ensure_ascii=False)
    print('Pedidos salvos com sucesso!')
