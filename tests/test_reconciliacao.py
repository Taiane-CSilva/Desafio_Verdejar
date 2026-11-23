from decimal import Decimal

from etl.carga import RAIZ, conectar_banco, ler_credenciais, ler_json
from etl.transformacao import transformar_pedidos


def test_reconciliacao_de_pedidos():
    # A transformação remove IDs repetidos e calcula o valor dos itens.
    pedidos_brutos = ler_json(RAIZ / 'brutos' / 'pedidos.json')
    pedidos, _ = transformar_pedidos(pedidos_brutos)
    quantidade_origem = len(pedidos)
    soma_origem = sum((pedido['valor_itens'] for pedido in pedidos), Decimal('0.00'))

    # A conexão usa a configuração existente e a transação é somente de leitura.
    with conectar_banco(ler_credenciais()) as conexao:
        conexao.read_only = True
        with conexao.cursor() as cursor:
            cursor.execute('SELECT COUNT(*), COALESCE(SUM(valor_itens), 0) FROM pedidos')
            quantidade_banco, soma_banco = cursor.fetchone()

    diferenca = abs(soma_origem - soma_banco)
    print(f'Pedidos únicos: origem={quantidade_origem}, PostgreSQL={quantidade_banco}')
    print(f'Soma de valor_itens: origem=R$ {soma_origem}, PostgreSQL=R$ {soma_banco}')
    print(f'Diferença absoluta: R$ {diferenca} (máximo permitido: R$ 0.01)')

    assert quantidade_origem == quantidade_banco, 'Quantidade de pedidos diferente'
    assert diferenca <= Decimal('0.01'), 'Diferença financeira superior a R$ 0,01'
