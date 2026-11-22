import csv
import json
import os
from datetime import date
from pathlib import Path

import psycopg

from etl.transformacao import (
    tratar_valor_monetario,
    transformar_clientes,
    transformar_pedidos,
)

RAIZ = Path(__file__).resolve().parent.parent

def ler_json(caminho):
    """Lê os dados brutos sem alterar o arquivo de origem."""
    with caminho.open(encoding='utf-8') as arquivo:
        return json.load(arquivo)


def ler_produtos(caminho):
    """Lê o CSV e converte os tipos necessários para o banco."""
    with caminho.open(encoding='utf-8-sig', newline='') as arquivo:
        produtos = list(csv.DictReader(arquivo))

    for produto in produtos:
        produto['produto_id'] = int(produto['produto_id'])
        produto['preco_base'] = tratar_valor_monetario(produto['preco_base'])
    return produtos


def preparar_dados():
    """Lê as fontes e aplica as transformações existentes."""
    produtos = ler_produtos(RAIZ / 'insumos' / 'dados' / 'produtos.csv')
    clientes_brutos = ler_json(RAIZ / 'brutos' / 'clientes.json')
    pedidos_brutos = ler_json(RAIZ / 'brutos' / 'pedidos.json')
    clientes, contadores_clientes = transformar_clientes(clientes_brutos)
    pedidos, contadores_pedidos = transformar_pedidos(pedidos_brutos)

    # Valida as datas de cadastro exigidas pelo contrato de dados.
    for cliente in clientes:
        cliente['cadastro_em'] = date.fromisoformat(cliente['cadastro_em'])

    return produtos, clientes, pedidos, contadores_clientes, contadores_pedidos


def conectar_banco(credenciais):
    """Conecta ao banco verdejar usando os parâmetros recebidos."""
    return psycopg.connect(dbname='verdejar', **credenciais)


def carregar_produtos(cursor, produtos):
    cursor.executemany(
        '''INSERT INTO produtos (produto_id, nome, categoria, preco_base)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (produto_id) DO NOTHING''',
        [(p['produto_id'], p['nome'], p['categoria'], p['preco_base']) for p in produtos],
    )


def carregar_clientes(cursor, clientes):
    cursor.executemany(
        '''INSERT INTO clientes (id, nome, email, cidade, estado, cadastro_em)
           VALUES (%s, %s, %s, %s, %s, %s)
           ON CONFLICT (id) DO NOTHING''',
        [(c['id'], c['nome'], c['email'], c['cidade'], c['estado'], c['cadastro_em'])
         for c in clientes],
    )


def carregar_pedidos(cursor, pedidos):
    cursor.executemany(
        '''INSERT INTO pedidos
           (id, cliente_id, data_pedido, status, valor_total, valor_itens, divergente)
           VALUES (%s, %s, %s, %s, %s, %s, %s)
           ON CONFLICT (id) DO NOTHING''',
        [(p['id'], p['cliente_id'], p['data_pedido'], p['status'], p['valor_total'],
          p['valor_itens'], p['divergente']) for p in pedidos],
    )


def carregar_itens(cursor, pedidos):
    # A posição na lista fornece uma linha única por pedido, começando em 1.
    itens = [
        (pedido['id'], linha, item['produto_id'], item['quantidade'], item['preco_unitario'])
        for pedido in pedidos
        for linha, item in enumerate(pedido['itens'], start=1)
    ]
    cursor.executemany(
        '''INSERT INTO itens_pedido (pedido_id, linha, produto_id, quantidade, preco_unitario)
           VALUES (%s, %s, %s, %s, %s)
           ON CONFLICT (pedido_id, linha) DO NOTHING''',
        itens,
    )


def mostrar_quantidades(cursor):
    """Mostra o total de registros armazenados em cada tabela."""
    for tabela, consulta in (
        ('produtos', 'SELECT COUNT(*) FROM produtos'),
        ('clientes', 'SELECT COUNT(*) FROM clientes'),
        ('pedidos', 'SELECT COUNT(*) FROM pedidos'),
        ('itens_pedido', 'SELECT COUNT(*) FROM itens_pedido'),
    ):
        cursor.execute(consulta)
        print(f'{tabela}: {cursor.fetchone()[0]}')


def carregar_dados(credenciais):
    """Carrega as quatro tabelas em uma transação."""
    produtos, clientes, pedidos, contadores_clientes, contadores_pedidos = preparar_dados()
    with conectar_banco(credenciais) as conexao:
        with conexao.cursor() as cursor:
            carregar_produtos(cursor, produtos)
            carregar_clientes(cursor, clientes)
            carregar_pedidos(cursor, pedidos)
            carregar_itens(cursor, pedidos)
            mostrar_quantidades(cursor)
    return contadores_clientes, contadores_pedidos


def ler_credenciais():
    """Lê as configurações do ambiente ou do arquivo .env na raiz."""
    nomes = {'PGHOST': 'host', 'PGPORT': 'port', 'PGUSER': 'user', 'PGPASSWORD': 'password'}
    valores_arquivo = {}
    caminho_env = RAIZ / '.env'

    # Aceita linhas simples NOME=valor, com aspas opcionais em volta do valor.
    if caminho_env.is_file():
        with caminho_env.open(encoding='utf-8-sig') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith('#') or '=' not in linha:
                    continue
                nome, valor = linha.split('=', 1)
                nome = nome.strip()
                valor = valor.strip()
                if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
                    valor = valor[1:-1]
                if nome in nomes:
                    valores_arquivo[nome] = valor

    # Variáveis já definidas no ambiente têm prioridade sobre o arquivo.
    valores = {nome: os.environ.get(nome, valores_arquivo.get(nome, '')) for nome in nomes}
    faltantes = [nome for nome, valor in valores.items() if not valor.strip()]
    if faltantes:
        raise ValueError('Variáveis de conexão ausentes ou vazias: ' + ', '.join(faltantes))

    return {parametro: valores[nome] for nome, parametro in nomes.items()}


def main():
    try:
        credenciais = ler_credenciais()
    except ValueError as erro:
        raise SystemExit(str(erro)) from erro
    carregar_dados(credenciais)


if __name__ == '__main__':
    main()
