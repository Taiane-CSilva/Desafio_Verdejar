# Desafio Final — ETL Verdejar

## 1. Sobre o projeto

Projeto desenvolvido para o Desafio Final do Bootcamp AIR Fellowship — AI-Driven Data Engineering.

O objetivo é construir um processo ETL (Extração, Transformação e Carga) utilizando Python para extrair dados de uma API local e de um arquivo CSV, realizar os tratamentos necessários e armazenar os resultados no PostgreSQL.

A Verdejar é uma empresa fictícia de hortifrúti e os dados utilizados são sintéticos. O projeto prepara os dados para análises de vendas por mês, estado e categoria de produto.

## 2. Tecnologias e ambiente

- **Python 3.13:** desenvolvimento do ETL.
- **Requests:** consumo da API.
- **Pandas e módulo CSV:** leitura e processamento do catálogo de produtos.
- **PostgreSQL:** banco de dados utilizado (Caminho A, sem Docker).
- **Psycopg:** conexão entre Python e PostgreSQL.
- **pgAdmin 4:** consultas e validações SQL.
- **Pytest:** testes automatizados.
- **Git e GitHub:** versionamento.
- **VS Code:** ambiente de desenvolvimento.

## 3. Extração e transformação

Os dados foram extraídos das rotas `/clientes` e `/pedidos` da API e do arquivo `produtos.csv`.

Os arquivos JSON extraídos foram preservados na pasta `brutos/` para permitir o reprocessamento.

| Dados extraídos | Quantidade |
|---|---:|
| Clientes | 1.000 |
| Pedidos brutos | 5.100 |
| Produtos | 12 |

As transformações foram implementadas no arquivo `etl/transformacao.py`, seguindo as regras A1 a A6.

| Regra | Tratamento | Resultado |
|---|---|---:|
| A1 | E-mails nulos preservados | 81 |
| A2 | Estados corrigidos | 151 |
| A3 | Datas convertidas | 1.037 |
| A4 | Valores monetários convertidos | 1.255 |
| A5 | Pedidos duplicados descartados | 100 |
| A6 | Pedidos divergentes identificados | 238 |

Após a remoção das duplicidades, foram mantidos **5.000 pedidos únicos**.

O campo `valor_total` original foi preservado. O campo `valor_itens` foi calculado pela soma de `quantidade × preco_unitario` dos itens do pedido.

As regras e os tipos de dados estão documentados em `contrato_de_dados.md`.

## 4. Carga no PostgreSQL

A carga foi implementada no arquivo `etl/carga.py`, utilizando SQL parametrizado e a seguinte ordem de inserção:

1. `produtos`
2. `clientes`
3. `pedidos`
4. `itens_pedido`

Foi utilizada a estratégia `ON CONFLICT DO NOTHING` para evitar duplicações de registros com as mesmas chaves.

A carga foi executada duas vezes, mantendo os mesmos resultados:

| Tabela | Primeira execução | Segunda execução |
|---|---:|---:|
| Produtos | 12 | 12 |
| Clientes | 1.000 | 1.000 |
| Pedidos | 5.000 | 5.000 |
| Itens de pedido | 12.455 | 12.455 |

**Resultado:** idempotência confirmada nas duas execuções.

Também foram realizadas verificações de integridade no PostgreSQL:

- Pedidos sem cliente correspondente: 0.
- Pedidos cujo `valor_itens` armazenado não corresponde ao cálculo dos itens: 0.

## 5. Testes e reconciliação

Os testes automatizados estão disponíveis na pasta `tests/`.

| Arquivo | Testes |
|---|---:|
| `test_extracao_api.py` | 4 |
| `test_transformacao.py` | 14 |
| `test_carga.py` | 2 |
| `test_reconciliacao.py` | 1 |
| **Total** | **21** |

Comando utilizado:

```bash
python -m pytest tests -v
```

**Resultado:** 21 testes aprovados, sem falhas.

Foi apresentado um aviso de permissão relacionado ao cache do pytest no OneDrive, sem comprometer os resultados.

### Reconciliação

O teste `tests/test_reconciliacao.py` compara a quantidade de pedidos únicos e a soma de `valor_itens` entre a origem tratada e o PostgreSQL.

| Verificação | Origem | PostgreSQL |
|---|---:|---:|
| Pedidos únicos | 5.000 | 5.000 |
| Soma de `valor_itens` | R$ 311.228,75 | R$ 311.228,75 |

- Diferença financeira: R$ 0,00.
- Tolerância permitida: R$ 0,01.
- Resultado: reconciliação aprovada (`1 passed`).

## 6. Consultas SQL de validação e análises de vendas

As consultas obrigatórias estão disponíveis no arquivo `consultas_validacao.sql` e foram executadas no PostgreSQL por meio do pgAdmin 4.

### A — Total de vendas por mês

Foi utilizado `DATE_TRUNC` para agrupar os pedidos por mês e `SUM(valor_itens)` para calcular os totais.

| Mês de 2026 | Total de `valor_itens` |
|---|---:|
| Janeiro | R$ 30.355,02 |
| Fevereiro | R$ 33.855,86 |
| Março | R$ 30.617,70 |
| Abril | R$ 31.170,96 |
| Maio | R$ 30.777,02 |
| Junho | R$ 31.557,73 |
| Julho | R$ 32.685,17 |
| Agosto | R$ 29.260,04 |
| Setembro | R$ 29.909,71 |
| Outubro | R$ 31.039,54 |
| **Total geral** | **R$ 311.228,75** |

**Teste da consulta A:**

- Soma dos meses: R$ 311.228,75.
- Soma geral da tabela: R$ 311.228,75.
- Diferença: R$ 0,00.

### B — Quantidade de pedidos por estado

Consulta realizada com `INNER JOIN` entre `pedidos` e `clientes`.

| Estado | Pedidos |
|---|---:|
| RS | 1.543 |
| SC | 1.127 |
| PR | 974 |
| SP | 880 |
| MG | 476 |
| **Total** | **5.000** |

### C — Pedidos divergentes

A consulta seleciona os registros com `divergente = TRUE`, exibindo os valores originais, calculados e a diferença financeira.

**Resultado:** 238 pedidos divergentes.

### Análises complementares — Objetivo da Verdejar

Além das três consultas obrigatórias de validação, foram realizadas análises para atender ao objetivo do projeto de disponibilizar informações de vendas por mês, estado e categoria de produto.

A análise mensal está apresentada na consulta A. As análises complementares por estado e categoria foram executadas no pgAdmin e conferidas com o total geral de `valor_itens`.

#### D — Valor de vendas por estado

Consulta realizada com `INNER JOIN` entre `pedidos` e `clientes`, agrupando os valores por estado e utilizando `SUM(p.valor_itens)`.

| Estado | Total de `valor_itens` |
|---|---:|
| RS | R$ 96.280,95 |
| SC | R$ 71.238,58 |
| PR | R$ 59.426,74 |
| SP | R$ 54.306,80 |
| MG | R$ 29.975,68 |
| **Total geral** | **R$ 311.228,75** |

**Validação:** a soma dos cinco estados corresponde ao total geral armazenado no PostgreSQL.

#### E — Valor de vendas por categoria de produto

Consulta realizada com `INNER JOIN` entre `itens_pedido` e `produtos`, agrupando os valores por categoria e calculando a soma de `quantidade × preco_unitario`.

| Categoria | Total |
|---|---:|
| Frutas | R$ 175.161,36 |
| Legumes | R$ 93.908,07 |
| Folhas | R$ 42.159,32 |
| **Total geral** | **R$ 311.228,75** |

**Validação:** a soma das três categorias corresponde ao total geral de `valor_itens`.

### Considerações sobre os resultados

As análises por mês, estado e categoria apresentaram o mesmo total geral de **R$ 311.228,75**, em concordância com a reconciliação da origem e do destino.

As consultas consideram todos os status dos pedidos, inclusive cancelados e em transporte. Portanto, os valores representam o total dos itens registrados e não exclusivamente o faturamento dos pedidos entregues.

Como o desafio não estabelece uma regra de negócio específica para excluir esses status, os dados foram preservados nas análises.

## 7. Como executar

### Pré-requisitos

Python 3, PostgreSQL local, ambiente virtual Python e dependências instaladas.

### Instalar dependências

Com o ambiente virtual ativo:

```bash
python -m pip install requests pandas "psycopg[binary]" pytest
```

### Configurar o banco

Criar o banco `verdejar` no PostgreSQL e executar o arquivo `insumos/schema.sql` para criar as tabelas.

Configurar na raiz do projeto um arquivo `.env`:

```text
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=sua_senha_local
```

O arquivo `.env` é lido automaticamente pelo `etl/carga.py`, por meio da função `ler_credenciais()`. Não é necessário carregar as variáveis manualmente no terminal.

O arquivo `.env` está no `.gitignore` e não deve ser enviado ao GitHub.

### Iniciar a API

Na pasta `insumos`:

```bash
python api_verdejar.py
```

A API ficará disponível em `http://127.0.0.1:8000`.

### Extrair e carregar os dados

Com a API em execução, abrir outro terminal na raiz do projeto e executar:

```bash
python -m etl.extracao_api
```

Esse comando extrai os dados das rotas `/clientes` e `/pedidos` e salva os arquivos em `brutos/`.

**Importante:** a pasta `brutos/` precisa existir antes da extração.

Depois, executar a carga no PostgreSQL:

```bash
python -m etl.carga
```

### Visualizar o resumo do ETL

Para consultar os resultados de extração, transformação, carga e reconciliação, executar na raiz do projeto:

```bash
python -m etl.resumo_saida_etl
```

O script `etl/resumo_saida_etl.py` apresenta no terminal:

- Quantidade de registros extraídos de clientes e pedidos.
- Pedidos únicos e duplicados descartados.
- Contadores das armadilhas A1 a A6.
- Quantidades armazenadas nas quatro tabelas do PostgreSQL.
- Comparação dos pedidos únicos e da soma de `valor_itens` entre origem e destino.
- Diferença financeira da reconciliação.

O comando reutiliza os arquivos preservados em `brutos/`, aplica as funções de transformação e consulta o PostgreSQL apenas para leitura, **sem executar novamente a extração ou a carga**.

A quantidade original de páginas consumidas pela API não pode ser comprovada apenas pelos arquivos JSON preservados. Por isso, o script informa essa limitação em vez de apresentar um número não verificado.

### Executar os testes

```bash
python -m pytest tests -v
```

Para visualizar os resultados da reconciliação:

```bash
python -m pytest tests/test_reconciliacao.py -v -s
```

As consultas do arquivo `consultas_validacao.sql` podem ser executadas no pgAdmin, conectado ao banco `verdejar`.

## 8. Evidências e documentação

As evidências do projeto estão organizadas nas seguintes pastas:

- `evidencias/evidencias.pdf`: documento consolidado com as evidências de extração, transformação, carga, testes, reconciliação e consultas SQL.
- `kanban/`: capturas do quadro Kanban utilizado para organizar e acompanhar as etapas do desafio.

Documentação complementar:

- `contrato_de_dados.md`: regras e estrutura dos dados.
- `consultas_validacao.sql`: consultas de validação e análises SQL.
- `como_usei_ia.md`: registro do uso de inteligência artificial.

## 9. Uso de IA e versionamento

O ChatGPT e o Codex foram utilizados como ferramentas de apoio para compreensão dos requisitos, desenvolvimento, testes e documentação.

As decisões, sugestões aceitas ou modificadas, dificuldades e validações realizadas estão registradas no arquivo `como_usei_ia.md`.

O projeto foi desenvolvido em uma branch específica, com commits organizados por etapa. A integração com a branch principal será realizada por meio de Pull Request após a revisão final.