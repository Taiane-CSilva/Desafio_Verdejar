-- VALIDAÇÃO DA CARGA - QUANTIDADE DE REGISTROS

-- Totais armazenados nas tabela, esperado: 12 produtos, 1.000 clientes, 5.000 pedidos e 12.455 itens de pedido.
SELECT COUNT(*) AS total_produtos FROM produtos;
SELECT COUNT(*) AS total_clientes FROM clientes;
SELECT COUNT(*) AS total_pedidos FROM pedidos;
SELECT COUNT(*) AS total_itens FROM itens_pedido;

-- PEDIDOS SEM CLIENTE CORRESPONDENTE
-- Verifica se existe pedido associado a um cliente ausente, resultado esperado: zero.
SELECT COUNT(*) AS pedidos_sem_cliente
FROM pedidos p
LEFT JOIN clientes c
    ON p.cliente_id = c.id
WHERE c.id IS NULL;

-- CONFERÊNCIA DO VALOR DOS ITENS
-- Confere se o valor_itens armazenado corresponde à soma dos itens de cada pedido, resultado esperado: zero.
SELECT COUNT(*) AS pedidos_com_diferenca
FROM pedidos p
INNER JOIN (
    SELECT
        pedido_id,
        SUM(quantidade * preco_unitario) AS total_calculado
    FROM itens_pedido
    GROUP BY pedido_id
) i
    ON p.id = i.pedido_id
WHERE ABS(p.valor_itens - i.total_calculado) > 0.01;



-- Consulta A: Total de vendas por mês
SELECT
    DATE_TRUNC('month', data_pedido)::DATE AS mes,
    SUM(valor_itens) AS total_vendas
FROM pedidos
GROUP BY mes
ORDER BY mes;

-- Consulta B: Quantidade de pedidos por estado
SELECT
    c.estado,
    COUNT(*) AS quantidade_pedidos
FROM pedidos p
INNER JOIN clientes c
    ON p.cliente_id = c.id
GROUP BY c.estado
ORDER BY quantidade_pedidos DESC;

-- Consulta C: Pedidos divergentes
SELECT
    id,
    cliente_id,
    data_pedido,
    valor_total,
    valor_itens,
    valor_total - valor_itens AS diferenca
FROM pedidos
WHERE divergente = TRUE
ORDER BY id;


-- Teste da Consulta A:  A soma dos meses deve bater com a soma geral da tabela
SELECT
    (SELECT SUM(valor_itens) FROM pedidos) AS valor_itens_total,
    SUM(total_mensal) AS soma_dos_meses
FROM (
    SELECT SUM(valor_itens) AS total_mensal
    FROM pedidos
    GROUP BY DATE_TRUNC('month', data_pedido)
)AS meses;


--SOLICITAÇÕES DO CLIENTE:

-- Vendas por mês
SELECT
    DATE_TRUNC('month', data_pedido)::DATE AS mes,
    SUM(valor_itens) AS total_vendas
FROM pedidos
GROUP BY mes
ORDER BY mes;

-- Vendas por estado
SELECT
    c.estado,
    SUM(p.valor_itens) AS total_vendas
FROM pedidos p
INNER JOIN clientes c
    ON p.cliente_id = c.id
GROUP BY c.estado
ORDER BY total_vendas DESC;


-- Vendas por categoria de produto
SELECT
    pr.categoria,
    SUM(i.quantidade * i.preco_unitario) AS total_vendas
FROM itens_pedido i
INNER JOIN produtos pr
    ON i.produto_id = pr.produto_id
GROUP BY pr.categoria
ORDER BY total_vendas DESC;