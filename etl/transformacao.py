from datetime import datetime
from decimal import Decimal

# A1 - Preservar clientes com e-mail nulo
def tratar_email(cliente):
    return cliente.copy()

# A2 - Converter a sigla do estado para maiúsculas
def tratar_estado(cliente):
    cliente_tratado = cliente.copy()
    cliente_tratado['estado'] = cliente_tratado['estado'].upper()
    return cliente_tratado

# A1 e A2 - Tratar clientes e contar e-mails nulos e estados corrigidos
def transformar_clientes(clientes):
    clientes_tratados = []
    contadores = {'emails_nulos': 0, 'estados_corrigidos': 0}

    for cliente in clientes:
        tratado = tratar_estado(tratar_email(cliente))
        contadores['emails_nulos'] += tratado['email'] is None
        contadores['estados_corrigidos'] += tratado['estado'] != cliente['estado']
        clientes_tratados.append(tratado)

    return clientes_tratados, contadores

# A3 - Converter os dois formatos de data dos pedidos
def tratar_data_pedido(data_pedido):
    formato = '%d/%m/%Y' if '/' in data_pedido else '%Y-%m-%d'
    return datetime.strptime(data_pedido, formato).date()

# A4 - Converter valores monetários para Decimal com duas casas
def tratar_valor_monetario(valor):
    return Decimal(str(valor).replace(',', '.')).quantize(Decimal('0.01'))

# A5 - Remover pedidos duplicados, mantendo o primeiro ID encontrado
def remover_pedidos_duplicados(pedidos):
    ids_vistos = set()
    pedidos_unicos = []
    descartados = 0

    for pedido in pedidos:
        if pedido['id'] in ids_vistos:
            descartados += 1
        else:
            ids_vistos.add(pedido['id'])
            pedidos_unicos.append(pedido)

    return pedidos_unicos, descartados

# A3, A4 e A6 - Tratar um pedido e calcular possíveis divergências
def tratar_pedido(pedido):
    tratado = pedido.copy()

    # A3 - Converter a data
    tratado['data_pedido'] = tratar_data_pedido(pedido['data_pedido'])

    # A4 - Converter o valor total
    tratado['valor_total'] = tratar_valor_monetario(pedido['valor_total'])
    tratado['itens'] = []

    # A6 - Tratar os preços dos itens antes de calcular a soma
    for item in pedido['itens']:
        item_tratado = item.copy()
        item_tratado['preco_unitario'] = tratar_valor_monetario(item['preco_unitario'])
        tratado['itens'].append(item_tratado)

    # A6 - Somar quantidade x preço unitário
    tratado['valor_itens'] = sum(
        (item['quantidade'] * item['preco_unitario'] for item in tratado['itens']),
        Decimal('0.00'),
    )

    # A6 - Marcar divergência quando a diferença superar R$ 0,01
    tratado['divergente'] = abs(tratado['valor_total'] - tratado['valor_itens']) > Decimal('0.01')

    return tratado

# A3, A4, A5 e A6 - Tratar todos os pedidos e contabilizar as ocorrências
def transformar_pedidos(pedidos):

    # A5 - Remover duplicados
    pedidos_unicos, descartados = remover_pedidos_duplicados(pedidos)

    # A3, A4 e A6 - Aplicar as transformações
    pedidos_tratados = [tratar_pedido(pedido) for pedido in pedidos_unicos]

    contadores = {
        # A3 - Datas que chegaram com barras
        'datas_convertidas': sum('/' in pedido['data_pedido'] for pedido in pedidos_unicos),

        # A4 - Valores totais que chegaram como texto com vírgula
        'valores_convertidos': sum(
            isinstance(pedido['valor_total'], str) and ',' in pedido['valor_total']
            for pedido in pedidos_unicos
        ),

        # A5 - Pedidos repetidos descartados
        'pedidos_duplicados_descartados': descartados,

        # A6 - Pedidos com divergência financeira
        'pedidos_divergentes': sum(pedido['divergente'] for pedido in pedidos_tratados),
    }

    return pedidos_tratados, contadores