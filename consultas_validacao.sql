-- Consulta A: Total de vendas por mês
SELECT
    DATE_TRUNC('month', data_pedido)::DATE AS mes,
    SUM(valor_itens) AS total_itens_mensal
FROM pedidos
GROUP BY DATE_TRUNC('month', data_pedido)::DATE
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
