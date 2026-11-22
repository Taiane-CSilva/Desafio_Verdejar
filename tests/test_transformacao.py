from copy import deepcopy
from datetime import date
from decimal import Decimal

import pytest

from etl.transformacao import (
    remover_pedidos_duplicados,
    tratar_data_pedido,
    tratar_email,
    tratar_estado,
    tratar_pedido,
    tratar_valor_monetario,
    transformar_clientes,
    transformar_pedidos,
)


# A1 - O cliente e o e-mail nulo são preservados.
def test_email_nulo_mantem_cliente_sem_alterar_original():
    cliente = {'id': 1, 'email': None, 'estado': 'pr'}
    original = deepcopy(cliente)

    resultado = tratar_email(cliente)
    clientes, contadores = transformar_clientes([cliente])

    assert resultado == original
    assert resultado is not cliente
    assert len(clientes) == 1
    assert clientes[0]['email'] is None
    assert contadores['emails_nulos'] == 1
    assert cliente == original


# A2 - A sigla é padronizada e a correção é contada.
def test_estado_minusculo_e_convertido_sem_alterar_original():
    cliente = {'id': 1, 'email': 'a@exemplo.com', 'estado': 'pr'}
    original = deepcopy(cliente)

    resultado = tratar_estado(cliente)
    clientes, contadores = transformar_clientes([cliente])

    assert resultado['estado'] == 'PR'
    assert clientes[0]['estado'] == 'PR'
    assert contadores['estados_corrigidos'] == 1
    assert cliente == original


# A3 - Os dois formatos representam a mesma data.
@pytest.mark.parametrize('entrada', ['2026-03-15', '15/03/2026'])
def test_data_pedido_nos_dois_formatos(entrada):
    assert tratar_data_pedido(entrada) == date(2026, 3, 15)


# A4 - Valores textuais e numéricos tornam-se decimais com duas casas.
@pytest.mark.parametrize('entrada', ['125,84', 125.84, 125])
def test_valor_monetario_e_decimal(entrada):
    esperado = Decimal('125.00') if entrada == 125 else Decimal('125.84')
    resultado = tratar_valor_monetario(entrada)

    assert resultado == esperado
    assert resultado.as_tuple().exponent == -2


# A5 - A primeira ocorrência de cada ID é mantida.
def test_pedidos_duplicados_mantem_primeiro_e_contam_descartes():
    pedidos = [
        {'id': 1, 'cliente_id': 10, 'valor_total': 20},
        {'id': 1, 'cliente_id': 10, 'valor_total': 20},
        {'id': 2, 'cliente_id': 10, 'valor_total': 20},
        {'id': 1, 'cliente_id': 10, 'valor_total': 20},
    ]
    original = deepcopy(pedidos)

    resultado, descartados = remover_pedidos_duplicados(pedidos)

    assert resultado == [pedidos[0], pedidos[2]]
    assert resultado[0] is pedidos[0]
    assert descartados == 2
    assert pedidos == original


# A6 - A diferença absoluta deve superar um centavo.
@pytest.mark.parametrize(
    ('total', 'divergente'),
    [('25,00', False), ('25,01', False), ('24,99', False),
     ('25,02', True), ('24,98', True)],
)
def test_divergencia_e_soma_dos_itens(total, divergente):
    pedido = {
        'id': 1,
        'data_pedido': '2026-03-15',
        'valor_total': total,
        'itens': [
            {'produto_id': 1, 'quantidade': 2, 'preco_unitario': 10.00},
            {'produto_id': 2, 'quantidade': 1, 'preco_unitario': 5.00},
        ],
    }
    original = deepcopy(pedido)

    resultado = tratar_pedido(pedido)

    assert resultado['valor_itens'] == Decimal('25.00')
    assert resultado['valor_total'] == Decimal(total.replace(',', '.'))
    assert resultado['divergente'] is divergente
    assert pedido == original


# A3 a A6 - Contadores consideram somente pedidos mantidos após a deduplicação.
def test_contadores_dos_pedidos_e_preservacao_dos_originais():
    pedidos = [
        {'id': 1, 'data_pedido': '15/03/2026', 'valor_total': '10,02',
         'itens': [{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 10}]},
        {'id': 1, 'data_pedido': '15/03/2026', 'valor_total': '10,02',
         'itens': [{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 10}]},
        {'id': 2, 'data_pedido': '2026-03-15', 'valor_total': 10,
         'itens': [{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 10}]},
    ]
    original = deepcopy(pedidos)

    resultado, contadores = transformar_pedidos(pedidos)

    assert [pedido['id'] for pedido in resultado] == [1, 2]
    assert contadores == {
        'datas_convertidas': 1,
        'valores_convertidos': 1,
        'pedidos_duplicados_descartados': 1,
        'pedidos_divergentes': 1,
    }
    assert pedidos == original
