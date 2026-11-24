# CONTRATO DE DADOS — VERDEJAR

**Projeto:** Desafio Final do Bootcamp — ETL Verdejar  
**Versão:** 1.0 — Em validação  
**Banco de destino:** PostgreSQL  
**Referências:** `schema.sql`, Desafio Final v3 (18/11/2026) e artigo *O que é um contrato de dados?*, da IBM.

## 1. Objetivo

Este contrato define a estrutura, os tipos de dados, a obrigatoriedade dos campos e as regras de transformação utilizadas no projeto Verdejar.

O objetivo é garantir que os dados extraídos da API e do arquivo CSV sejam tratados e carregados corretamente no PostgreSQL, mantendo sua integridade e qualidade.

O documento também servirá como referência para o desenvolvimento das transformações e dos testes de validação.

## 2. Origem e destino dos dados

A Verdejar é uma empresa fictícia de comércio eletrônico de hortifrúti. O projeto consiste em extrair os dados de clientes, pedidos e produtos, realizar as transformações necessárias e armazená-los no banco de dados.

| Origem | Dados fornecidos | Destino |
|---|---|---|
| API `/clientes` | Cadastro de clientes | `clientes` |
| API `/pedidos` | Pedidos e seus itens | `pedidos` e `itens_pedido` |
| `dados/produtos.csv` | Catálogo de produtos | `produtos` |

O banco PostgreSQL possui quatro tabelas de destino, cuja estrutura está definida no arquivo `schema.sql`.

## 3. Esquema e regras de transformação

### 3.1. Tabela clientes

**Origem:** API `/clientes`  
**Destino:** `clientes`

| Campo | Tipo | Aceita nulo? | Regra de transformação |
|---|---|---|---|
| `id` | INTEGER | Não | Manter como número inteiro e identificador único do cliente. |
| `nome` | TEXT | Não | Manter como texto obrigatório. |
| `email` | TEXT | Sim | Preservar o e-mail informado. Quando ausente, armazenar `NULL`, sem excluir o cliente. |
| `cidade` | TEXT | Não | Manter como texto obrigatório. |
| `estado` | CHAR(2) | Não | Padronizar a sigla do estado para maiúsculas. Exemplo: `pr` → `PR`. |
| `cadastro_em` | DATE | Não | Validar a data de cadastro e garantir sua compatibilidade com o tipo DATE do PostgreSQL, mantendo a padronização utilizada no banco. |

**Regras de qualidade:**

- **A1 — E-mails ausentes:** manter os clientes mesmo quando não possuem e-mail, armazenando `NULL` e contabilizando os registros afetados.
- **A2 — Padronização dos estados:** converter as siglas para maiúsculas antes da carga e contabilizar as correções.

**Decisão adicional de qualidade:** validar também a data de cadastro, para garantir sua compatibilidade com o banco. Essa decisão não faz parte da armadilha A3, que trata especificamente das datas dos pedidos.

### 3.2. Tabela produtos

**Origem:** `dados/produtos.csv`  
**Destino:** `produtos`

| Campo | Tipo | Aceita nulo? | Regra de transformação |
|---|---|---|---|
| `produto_id` | INTEGER | Não | Manter como número inteiro e identificador único do produto. |
| `nome` | TEXT | Não | Manter como texto obrigatório. |
| `categoria` | TEXT | Não | Manter como texto obrigatório. |
| `preco_base` | NUMERIC(10,2) | Não | Armazenar como número decimal com duas casas. |

**Regra de qualidade:**

Os dados dos produtos devem respeitar os tipos, a obrigatoriedade e a unicidade definidos no `schema.sql`.

Não há uma armadilha A1–A6 específica para esta tabela.

### 3.3. Tabela pedidos

**Origem:** API `/pedidos`  
**Destino:** `pedidos`

| Campo | Tipo | Aceita nulo? | Regra de transformação |
|---|---|---|---|
| `id` | INTEGER | Não | Manter como número inteiro e identificador único. Remover pedidos repetidos pelo ID, preservando a primeira ocorrência. |
| `cliente_id` | INTEGER | Não | Manter como número inteiro, relacionado a um cliente existente. |
| `data_pedido` | DATE | Não | Converter datas nos formatos `YYYY-MM-DD` e `DD/MM/YYYY` para uma data válida no PostgreSQL. |
| `status` | TEXT | Não | Manter como texto obrigatório. |
| `valor_total` | NUMERIC(12,2) | Não | Converter valores numéricos e textos com vírgula decimal para números com duas casas decimais. |
| `valor_itens` | NUMERIC(12,2) | Não | Calcular a soma de `quantidade × preco_unitario` dos itens de cada pedido. |
| `divergente` | BOOLEAN | Não | Definir como `TRUE` quando a diferença absoluta entre `valor_total` e `valor_itens` for maior que R$ 0,01. Caso contrário, `FALSE`. |

**Regras de qualidade:**

- **A3 — Datas:** converter os formatos `YYYY-MM-DD` e `DD/MM/YYYY` para o tipo DATE do PostgreSQL.
- **A4 — Valores monetários:** converter valores numéricos e textos com vírgula decimal para números com duas casas decimais.
- **A5 — Pedidos duplicados:** manter apenas a primeira ocorrência de cada ID, descartando os registros repetidos.
- **A6 — Divergência financeira:** calcular a soma dos itens, comparar com o valor total informado e marcar como divergente quando a diferença for maior que R$ 0,01.

**Observação:** o tratamento da A6 não deve substituir o valor total informado. Os campos `valor_total` e `valor_itens` devem ser preservados separadamente para permitir a identificação da divergência.

### 3.4. Tabela itens_pedido

**Origem:** itens contidos nos pedidos recebidos da API `/pedidos`  
**Destino:** `itens_pedido`

| Campo | Tipo | Aceita nulo? | Regra de transformação |
|---|---|---|---|
| `pedido_id` | INTEGER | Não | Associar o item ao identificador do pedido correspondente. |
| `linha` | INTEGER | Não | Identificar a posição do item dentro do pedido, mantendo a combinação `pedido_id` e `linha` única. |
| `produto_id` | INTEGER | Não | Manter como número inteiro, relacionado a um produto existente. |
| `quantidade` | INTEGER | Não | Manter ou converter para número inteiro. |
| `preco_unitario` | NUMERIC(10,2) | Não | Armazenar como número decimal com duas casas. |

**Regras de qualidade:**

- **A5 — Pedidos duplicados:** os itens de um pedido repetido também não devem ser carregados novamente. Somente os itens dos pedidos mantidos após a remoção das duplicidades serão considerados na carga.
- **A6 — Divergência financeira:** utilizar os campos `quantidade` e `preco_unitario` para calcular o valor dos itens de cada pedido. Esse resultado será comparado com o `valor_total` informado na tabela `pedidos`.

Além disso, cada item deve estar associado a um pedido e a um produto existentes no banco.

**Observação sobre `linha`:** a numeração deve identificar cada item de um mesmo pedido sem repetição. A forma de obter ou atribuir essa numeração será confirmada durante a implementação, conforme a estrutura dos dados extraídos.

## 4. Regras gerais de qualidade dos dados

As seis armadilhas declaradas no desafio deverão ser tratadas antes da carga.

| Código | Problema | Tratamento esperado |
|---|---|---|
| A1 | E-mails ausentes | Manter os clientes e armazenar `NULL`. |
| A2 | Siglas de estado em minúsculas | Converter para maiúsculas. |
| A3 | Datas de pedidos em formatos diferentes | Converter para o tipo DATE. |
| A4 | Valores totais com vírgula decimal | Converter para número com duas casas. |
| A5 | Pedidos repetidos | Manter a primeira ocorrência de cada ID e evitar duplicação dos itens. |
| A6 | Divergência entre o total informado e a soma dos itens | Calcular, comparar e marcar a divergência quando superar R$ 0,01. |

O processo de transformação deverá apresentar contadores de e-mails nulos, estados corrigidos, datas convertidas, valores convertidos, pedidos repetidos descartados e pedidos divergentes.

## 5. Integridade e validação

Os dados deverão respeitar as restrições definidas no PostgreSQL:

- **Chaves primárias:** garantir identificadores únicos e não nulos.
- **Chaves estrangeiras:** garantir o relacionamento correto entre clientes, pedidos, produtos e itens.
- **Campos obrigatórios:** não permitir valores nulos em colunas definidas como `NOT NULL`.
- **Tipos de dados:** garantir compatibilidade com os tipos especificados no `schema.sql`.
- **Idempotência:** executar novamente o ETL com a mesma entrada não deve gerar registros duplicados.

As transformações serão verificadas por testes automatizados, consultas SQL de validação e reconciliação entre a origem e o destino.

## 6. Disponibilidade e responsabilidades

Os dados são disponibilizados por uma API local e um arquivo CSV.

O ETL será responsável por extrair, tratar e carregar esses dados no PostgreSQL, conforme as regras documentadas neste contrato.

O desafio não estabelece um SLA de disponibilidade ou atualização dos dados. Por isso, não serão definidos prazos ou percentuais de disponibilidade sem uma exigência específica.

O contrato será mantido no repositório Git para permitir o acompanhamento de alterações durante o desenvolvimento.

## 7. Referências

**Documentação do projeto**

- *Desafio Final do Bootcamp — ETL da Verdejar*, versão v3 consolidada de 18/11/2026.
- `schema.sql` — estrutura das tabelas de destino.
- `README_insumos.md` — orientações dos arquivos de origem.

**Referência conceitual**

- GOMSTYN, Alice; JONKER, Alexandra. *O que é um contrato de dados?* IBM Think. Disponível em: https://www.ibm.com/br-pt/think/topics/data-contract

O conteúdo da IBM foi utilizado como referência para organizar as seções de objetivo, esquema, qualidade, responsabilidades e disponibilidade. As regras específicas de transformação foram baseadas nas exigências do desafio Verdejar.