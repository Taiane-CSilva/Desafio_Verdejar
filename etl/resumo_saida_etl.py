from decimal import Decimal
from etl.carga import (
    RAIZ,
    ler_json,
    preparar_dados,
    ler_credenciais,
    conectar_banco
)

# Formatar valores em reais
def formatar_valor(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto

# Consultar as quantidades e os valores no PostgreSQL
def consultar_banco():
    credenciais = ler_credenciais()

    consultas = {
        "clientes": "SELECT COUNT(*) FROM clientes",
        "produtos": "SELECT COUNT(*) FROM produtos",
        "pedidos": "SELECT COUNT(*) FROM pedidos",
        "itens": "SELECT COUNT(*) FROM itens_pedido",
        "pedidos_unicos": "SELECT COUNT(DISTINCT id) FROM pedidos",
        "soma_itens": "SELECT SUM(valor_itens) FROM pedidos",
        "divergentes": "SELECT COUNT(*) FROM pedidos WHERE divergente = TRUE"
    }

    resultados = {}

    with conectar_banco(credenciais) as conexao:
        with conexao.cursor() as cursor:
            for nome, sql in consultas.items():
                cursor.execute(sql)
                resultados[nome] = cursor.fetchone()[0]

    return resultados

# Mostrar o resumo do ETL
def main():
    try:
        # Ler os arquivos brutos
        clientes_brutos = ler_json(RAIZ / "brutos" / "clientes.json")
        pedidos_brutos = ler_json(RAIZ / "brutos" / "pedidos.json")

        # Reutilizar as transformações do projeto
        produtos, clientes, pedidos, cont_clientes, cont_pedidos = preparar_dados()

        # Consultar os dados armazenados no banco
        banco = consultar_banco()

        # Calcular os valores da reconciliação
        soma_origem = sum(
            pedido["valor_itens"] for pedido in pedidos
        )

        soma_banco = banco["soma_itens"]
        diferenca = abs(soma_origem - soma_banco)

        # Extração
        print("Extração - páginas de clientes: não comprovável pelos arquivos preservados")
        print("Extração - páginas de pedidos: não comprovável pelos arquivos preservados")
        print("Extração - registros de clientes:", len(clientes_brutos))
        print("Extração - registros de pedidos:", len(pedidos_brutos))

        # Transformação
        print("Transformação - pedidos únicos:", len(pedidos))
        print("Transformação - pedidos duplicados descartados:",
              cont_pedidos["pedidos_duplicados_descartados"])
        print("Transformação - e-mails nulos:", cont_clientes["emails_nulos"])
        print("Transformação - estados corrigidos:", cont_clientes["estados_corrigidos"])
        print("Transformação - datas convertidas:", cont_pedidos["datas_convertidas"])
        print("Transformação - valores convertidos:", cont_pedidos["valores_convertidos"])

        # Carga
        print("Carga - clientes armazenados no PostgreSQL:", banco["clientes"])
        print("Carga - produtos armazenados no PostgreSQL:", banco["produtos"])
        print("Carga - pedidos armazenados no PostgreSQL:", banco["pedidos"])
        print("Carga - itens armazenados no PostgreSQL:", banco["itens"])

        # Reconciliação
        print(f"Reconciliação - pedidos únicos na origem: {len(pedidos)}; "
              f"no destino: {banco['pedidos_unicos']}")

        print(f"Reconciliação - soma de valor_itens na origem: {formatar_valor(soma_origem)}; "
              f"no destino: {formatar_valor(soma_banco)}; "
              f"diferença: {formatar_valor(diferenca)}")

        # Divergências
        print("Divergências - pedidos com diferença superior a R$ 0,01:",
              banco["divergentes"])

    except Exception as erro:
        print("Erro ao gerar o resumo:", erro)

if __name__ == "__main__":
    main()
