import sqlite3
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from etl import carga


@pytest.fixture
def banco_simulado(monkeypatch):
    # O SQLite em memória simula as chaves do esquema sem acessar o PostgreSQL.
    banco = sqlite3.connect(':memory:')
    banco.execute('PRAGMA foreign_keys = ON')
    banco.executescript('''
        CREATE TABLE produtos (produto_id INTEGER PRIMARY KEY, nome TEXT, categoria TEXT, preco_base NUMERIC);
        CREATE TABLE clientes (id INTEGER PRIMARY KEY, nome TEXT, email TEXT, cidade TEXT, estado TEXT, cadastro_em TEXT);
        CREATE TABLE pedidos (id INTEGER PRIMARY KEY, cliente_id INTEGER REFERENCES clientes(id),
            data_pedido TEXT, status TEXT, valor_total NUMERIC, valor_itens NUMERIC, divergente BOOLEAN);
        CREATE TABLE itens_pedido (pedido_id INTEGER REFERENCES pedidos(id), linha INTEGER,
            produto_id INTEGER REFERENCES produtos(produto_id), quantidade INTEGER, preco_unitario NUMERIC,
            PRIMARY KEY (pedido_id, linha));
    ''')
    chamadas = []

    class CursorSimulado:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def executemany(self, sql, parametros):
            chamadas.append((sql, parametros))
            # Adapta apenas os marcadores e os tipos Python para o SQLite.
            linhas = [tuple(str(valor) if isinstance(valor, (Decimal, date)) else valor
                            for valor in linha) for linha in parametros]
            banco.executemany(sql.replace('%s', '?'), linhas)

        def execute(self, sql):
            self.resultado = banco.execute(sql)

        def fetchone(self):
            return self.resultado.fetchone()

    conexao = MagicMock()
    conexao.__enter__.return_value = conexao
    conexao.cursor.return_value = CursorSimulado()
    monkeypatch.setattr(carga, 'conectar_banco', lambda credenciais: conexao)

    produtos = [{'produto_id': 1, 'nome': 'Alface', 'categoria': 'folhas',
                 'preco_base': Decimal('5.00')}]
    clientes = [{'id': 1, 'nome': 'Ana', 'email': None, 'cidade': 'Curitiba',
                 'estado': 'PR', 'cadastro_em': date(2026, 1, 1)}]
    pedidos = [{'id': 1, 'cliente_id': 1, 'data_pedido': date(2026, 2, 1),
                'status': 'entregue', 'valor_total': Decimal('10.00'),
                'valor_itens': Decimal('10.00'), 'divergente': False,
                'itens': [{'produto_id': 1, 'quantidade': 1, 'preco_unitario': Decimal('5.00')},
                          {'produto_id': 1, 'quantidade': 1, 'preco_unitario': Decimal('5.00')}]}]
    monkeypatch.setattr(carga, 'preparar_dados', lambda: (produtos, clientes, pedidos, {}, {}))

    yield banco, chamadas
    banco.close()


def test_carga_repetida_mantem_contagens(banco_simulado):
    banco, _ = banco_simulado

    def contagens():
        return tuple(banco.execute('SELECT COUNT(*) FROM ' + tabela).fetchone()[0]
                     for tabela in ('produtos', 'clientes', 'pedidos', 'itens_pedido'))

    # A mesma entrada é carregada duas vezes no mesmo banco em memória.
    carga.carregar_dados({})
    primeira = contagens()
    carga.carregar_dados({})

    assert primeira == (1, 1, 1, 2)
    assert contagens() == primeira


def test_ordem_e_parametros_das_insercoes(banco_simulado):
    _, chamadas = banco_simulado
    carga.carregar_dados({})

    # As consultas permanecem separadas dos valores enviados ao cursor.
    tabelas = [sql.split()[2] for sql, _ in chamadas]
    assert tabelas == ['produtos', 'clientes', 'pedidos', 'itens_pedido']
    for sql, linhas in chamadas:
        assert linhas
        assert all(sql.count('%s') == len(linha) for linha in linhas)
    assert [linha[:2] for linha in chamadas[3][1]] == [(1, 1), (1, 2)]
