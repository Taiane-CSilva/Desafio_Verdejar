import requests
import json

URL = 'http://127.0.0.1:8000'

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
            resposta = requests.get(URL + rota, params={'page': pagina, 'page_size': 50})

        except requests.exceptions.RequestException:
            print('Erro de conexão na página:', pagina)
            return registros

        if resposta.status_code != 200:
            print('Página inexistente ou erro HTTP:', pagina, resposta.status_code)
            return registros

        dados = resposta.json()
        registros.extend(dados['items'])

    return registros


clientes = extrair_dados('/clientes')
print('Total de clientes:', len(clientes))

pedidos = extrair_dados('/pedidos')
print('Total de pedidos:', len(pedidos))

if len(clientes) == 1000:
    arquivo = open('brutos/clientes.json', 'w', encoding='utf-8')
    json.dump(clientes, arquivo, indent=4, ensure_ascii=False)
    arquivo.close()
    print('Clientes salvos com sucesso!')
else:
    print('Clientes não foram salvos: extração incompleta.')

if len(pedidos) == 5100:
    arquivo = open('brutos/pedidos.json', 'w', encoding='utf-8')
    json.dump(pedidos, arquivo, indent=4, ensure_ascii=False)
    arquivo.close()
    print('Pedidos salvos com sucesso!')
else:
    print('Pedidos não foram salvos: extração incompleta.')

