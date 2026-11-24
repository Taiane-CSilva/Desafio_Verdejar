# Desafio Final — ETL Verdejar

Projeto desenvolvido para o **Bootcamp AIR Fellowship — AI-Driven Data Engineering**, com o objetivo de construir um processo ETL (Extração, Transformação e Carga) utilizando Python e PostgreSQL.

A Verdejar é uma empresa fictícia de hortifrúti, com dados sintéticos disponibilizados por API e CSV. O projeto realiza a extração, aplica regras de qualidade e disponibiliza os dados tratados para análises de vendas.

O desenvolvimento foi realizado inicialmente com PostgreSQL local (**Caminho A**) e, posteriormente, ampliado com **Docker Compose (Caminho B)**, como atividade opcional (Stretch).

## Resumo dos resultados

| Indicador | Resultado |
|---|---:|
| Clientes extraídos | 1.000 |
| Pedidos extraídos | 5.100 |
| Produtos | 12 |
| Pedidos únicos após tratamento | 5.000 |
| Itens de pedido | 12.455 |
| Pedidos duplicados descartados | 100 |
| Pedidos divergentes identificados | 238 |
| Testes automatizados | 21 aprovados |
| Soma de `valor_itens` | R$ 311.228,75 |
| Diferença na reconciliação | **R$ 0,00** |

A carga foi executada duas vezes sem duplicações, tanto no ambiente local quanto no Docker.

## Índice

1. [Tecnologias utilizadas](#1-tecnologias-utilizadas)
2. [Extração e transformação](#2-extração-e-transformação)
3. [Carga e idempotência](#3-carga-e-idempotência)
4. [Testes e reconciliação](#4-testes-e-reconciliação)
5. [Consultas SQL e análises](#5-consultas-sql-e-análises)
6. [Execução local — Caminho A](#6-execução-local--caminho-a)
7. [Execução com Docker Compose](#7-execução-com-docker-compose)
8. [Evidências e documentação](#8-evidências-e-documentação)
9. [Uso de IA e versionamento](#9-uso-de-ia-e-versionamento)

---

## 1. Tecnologias utilizadas

- **Python 3.13:** desenvolvimento do ETL.
- **Requests:** consumo da API.
- **Pandas e CSV:** leitura e processamento de dados.
- **PostgreSQL:** armazenamento dos dados tratados.
- **Psycopg:** conexão com o PostgreSQL.
- **pgAdmin 4:** consultas e validações SQL.
- **Pytest:** testes automatizados.
- **Docker e Docker Compose:** execução e orquestração dos serviços.
- **Git e GitHub:** versionamento.
- **VS Code:** ambiente de desenvolvimento.

## 2. Extração e transformação

A extração foi implementada em `etl/extracao_api.py` e `etl/extracao_csv.py`, utilizando as rotas `/clientes` e `/pedidos` da API e o arquivo `produtos.csv`.

Os arquivos JSON extraídos são armazenados em `brutos/` antes da transformação, permitindo reprocessar os dados sem consultar novamente a API. A pasta não é versionada.

A extração percorre as páginas das rotas, verifica as respostas HTTP e trata falhas de conexão e páginas inexistentes.

| Rota | Páginas | Registros extraídos |
|---|---:|---:|
| `/clientes` | 20 | 1.000 |
| `/pedidos` | 102 | 5.100 |

As transformações foram implementadas em `etl/transformacao.py`, seguindo as regras A1 a A6 do desafio.

| Regra | Tratamento realizado | Resultado |
|---|---|---:|
| A1 | E-mails nulos preservados | 81 |
| A2 | Estados padronizados | 151 |
| A3 | Datas convertidas | 1.037 |
| A4 | Valores monetários convertidos | 1.255 |
| A5 | Pedidos duplicados descartados | 100 |
| A6 | Divergências financeiras identificadas | 238 |

Após o tratamento, foram mantidos **5.000 pedidos únicos**.

O valor informado em `valor_total` foi preservado após a padronização monetária, enquanto `valor_itens` foi calculado pela soma de `quantidade × preco_unitario`. O campo `divergente` identifica pedidos cuja diferença absoluta entre esses valores é superior a R$ 0,01.

As definições dos campos, tipos e regras estão documentadas em `contrato_de_dados.md`.

## 3. Carga e idempotência

A carga foi implementada em `etl/carga.py`, utilizando SQL parametrizado e respeitando a seguinte ordem de inserção:

1. `produtos`
2. `clientes`
3. `pedidos`
4. `itens_pedido`

Para evitar duplicações, foram utilizadas as chaves primárias das tabelas e a estratégia `ON CONFLICT DO NOTHING`.

### Validação da idempotência

A carga foi executada duas vezes no mesmo banco, mantendo as quantidades:

| Tabela | 1ª execução | 2ª execução |
|---|---:|---:|
| Produtos | 12 | 12 |
| Clientes | 1.000 | 1.000 |
| Pedidos | 5.000 | 5.000 |
| Itens de pedido | 12.455 | 12.455 |

**Resultado:** idempotência confirmada para os mesmos dados de origem.

Também foram realizadas verificações de integridade no PostgreSQL local:

- Pedidos sem cliente correspondente: **0**.
- Pedidos com `valor_itens` armazenado diferente da soma calculada dos itens: **0**.

## 4. Testes e reconciliação

Os testes automatizados estão disponíveis na pasta `tests/`.

| Arquivo | Quantidade de testes |
|---|---:|
| `test_extracao_api.py` | 4 |
| `test_transformacao.py` | 14 |
| `test_carga.py` | 2 |
| `test_reconciliacao.py` | 1 |
| **Total** | **21** |

Para executar os testes no ambiente local, após preparar o banco, iniciar a API e gerar os arquivos brutos conforme a seção 6:

```bash
python -m pytest tests -v
```

**Resultado obtido:** 21 testes aprovados.

Na execução local, ocorreu um aviso de permissão relacionado ao cache do pytest no OneDrive, sem comprometer os resultados.

### Reconciliação

O teste `tests/test_reconciliacao.py` compara a quantidade de pedidos únicos e a soma de `valor_itens` entre a origem tratada e o PostgreSQL.

| Verificação | Origem | PostgreSQL |
|---|---:|---:|
| Pedidos únicos | 5.000 | 5.000 |
| Soma de `valor_itens` | R$ 311.228,75 | R$ 311.228,75 |
| Diferença financeira | | **R$ 0,00** |

A tolerância definida para a diferença financeira é de R$ 0,01.

A reconciliação também foi confirmada durante a execução com Docker Compose.

## 5. Consultas SQL e análises

As três consultas obrigatórias estão disponíveis em `consultas_validacao.sql` e foram executadas no pgAdmin 4.

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

A soma dos meses corresponde ao total geral da tabela. O teste de consulta apresentou os seguintes resultados:

| Verificação | Resultado |
|---|---:|
| Soma dos totais mensais | R$ 311.228,75 |
| Soma geral de `valor_itens` | R$ 311.228,75 |
| Diferença | **R$ 0,00** |

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

A consulta identifica registros com `divergente = TRUE`, exibindo os valores originais, calculados e a diferença financeira.

**Resultado:** 238 pedidos divergentes.

### Análises complementares

Além das consultas obrigatórias, foram realizadas análises por estado e categoria de produto, conforme o objetivo do projeto.

**D — Valor de vendas por estado**

| Estado | Total de `valor_itens` |
|---|---:|
| RS | R$ 96.280,95 |
| SC | R$ 71.238,58 |
| PR | R$ 59.426,74 |
| SP | R$ 54.306,80 |
| MG | R$ 29.975,68 |
| **Total geral** | **R$ 311.228,75** |

A análise foi realizada com `INNER JOIN` entre pedidos e clientes, agrupando os valores por estado.

**E — Valor de vendas por categoria**

| Categoria | Total |
|---|---:|
| Frutas | R$ 175.161,36 |
| Legumes | R$ 93.908,07 |
| Folhas | R$ 42.159,32 |
| **Total geral** | **R$ 311.228,75** |

A análise considera a soma de `quantidade × preco_unitario` dos itens, agrupada por categoria.

### Considerações sobre os resultados

As análises por mês, estado e categoria apresentaram o mesmo total de **R$ 311.228,75**, confirmando a consistência dos cálculos.

As consultas consideram todos os status dos pedidos, inclusive cancelados e em transporte. Portanto, os valores representam o total dos itens registrados, não exclusivamente o faturamento dos pedidos entregues.

Como o desafio não estabelece uma regra específica para excluir esses status, os dados foram preservados nas análises.

## 6. Execução local — Caminho A

### Pré-requisitos

Ter Python 3 e PostgreSQL instalados, além de um ambiente virtual Python com as dependências do projeto.

### Instalar dependências

Com o ambiente virtual ativo:

```bash
python -m pip install requests pandas "psycopg[binary]" pytest
```

### Configurar o PostgreSQL

Criar o banco `verdejar` e executar `insumos/schema.sql` para criar as tabelas.

Na raiz do projeto, criar um arquivo `.env`:

```env
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=sua_senha_local
```

O arquivo é lido automaticamente por `etl/carga.py` e não deve ser enviado ao GitHub.

### Iniciar a API

Na pasta `insumos`, executar:

```bash
python api_verdejar.py
```

A API ficará disponível em `http://127.0.0.1:8000`.

### Executar o ETL

Em outro terminal, na raiz do projeto, criar a pasta de dados brutos, caso ainda não exista:

```bash
mkdir brutos
```

Executar a extração:

```bash
python -m etl.extracao_api
```

Depois, realizar a carga:

```bash
python -m etl.carga
```

A extração valida a quantidade esperada de **1.000 clientes e 5.100 pedidos**. Se estiver incompleta, o processo retorna erro e não deve prosseguir para a carga.

### Visualizar o resumo

```bash
python -m etl.resumo_saida_etl
```

O resumo apresenta os registros extraídos, tratamentos realizados, quantidades armazenadas, divergências e reconciliação financeira.

Esse comando consulta os dados sem executar novamente a extração ou a carga.

Para executar somente o teste de reconciliação:

```bash
python -m pytest tests/test_reconciliacao.py -v -s
```

As consultas de `consultas_validacao.sql` também podem ser executadas no pgAdmin, conectado ao banco `verdejar`.

## 7. Execução com Docker Compose

Como atividade opcional, implementei a orquestração com Docker Compose, permitindo iniciar a API, o PostgreSQL e executar o ETL com um único comando.

Os arquivos utilizados são:

- `Dockerfile`: prepara o ambiente Python e instala as dependências.
- `.dockerignore`: evita copiar arquivos locais e sensíveis para a imagem.
- `docker-compose.yml`: configura os três serviços.

O PostgreSQL utiliza um volume Docker separado do banco local. O arquivo `insumos/schema.sql` cria as tabelas automaticamente na primeira inicialização de um volume vazio.

### Pré-requisito

Ter Docker com suporte ao Docker Compose instalado e funcionando. A execução deve ser feita a partir da versão do projeto que contém o `Dockerfile` e o `docker-compose.yml` (branch `teste-docker` durante o desenvolvimento).

### Executar o projeto

Na raiz do repositório:

```bash
docker compose up --build
```

Esse comando inicia o PostgreSQL e a API, aguarda os healthchecks dos serviços e executa a extração, transformação, carga e resumo do ETL.

O terminal pode continuar mostrando mensagens porque a API e o PostgreSQL permanecem ativos após o término do ETL.

Para verificar a situação dos contêineres, utilizar outro terminal:

```bash
docker compose ps -a
```

**Resultado validado:** o serviço `etl` apresentou `Exited (0)`, indicando que terminou normalmente.

### Conferir os dados carregados

```bash
docker compose exec db psql -U verdejar -d verdejar -c "SELECT COUNT(*) FROM pedidos;"
```

Resultado esperado: **5.000 pedidos**.

### Validar a idempotência

Executar novamente o ETL no mesmo banco Docker:

```bash
docker compose run --rm etl
```

A segunda execução manteve as quantidades de 12 produtos, 1.000 clientes, 5.000 pedidos e 12.455 itens, sem duplicações.

O contêiner temporário é removido após a execução, mas os dados do PostgreSQL permanecem armazenados no volume.

### Executar os testes no Docker

Como os arquivos extraídos são temporários no contêiner do ETL, a extração precisa acontecer antes dos testes:

```bash
docker compose run --rm etl sh -c "mkdir -p brutos && python -m etl.extracao_api && python -m pytest tests -v"
```

**Resultado obtido: 21 testes aprovados.**

Esse comando não executa novamente a carga.

### Teste de falha da API

Para validar o tratamento de erros, foi simulada uma API indisponível usando:

```bash
docker compose run --rm --no-deps -e API_URL=http://127.0.0.1:9999 etl
```

A extração identificou a falha, apresentou a mensagem de extração incompleta e interrompeu o processo antes da carga.

O script `etl/resumo_saida_etl.py` também foi ajustado para retornar código de erro quando ocorre uma exceção durante a geração do resumo.

### Resultados no Docker

| Verificação | Resultado |
|---|---:|
| Clientes | 1.000 |
| Produtos | 12 |
| Pedidos únicos | 5.000 |
| Itens de pedido | 12.455 |
| Pedidos duplicados descartados | 100 |
| Pedidos divergentes | 238 |
| Reconciliação financeira | **R$ 0,00 de diferença** |
| Testes automatizados | **21 aprovados** |

### Validação em ambiente independente — Debian

Para validar a portabilidade do projeto, realizei uma execução adicional em uma máquina virtual Debian, utilizando o Oracle VirtualBox, simulando a experiência de um recrutador. Baixei o ZIP da branch `teste-docker` diretamente do repositório público no GitHub, sem utilizar os arquivos do ambiente Windows de desenvolvimento.

**Ambiente utilizado:**

| Componente | Versão |
|---|---|
| Sistema operacional | Debian 13 |
| Virtualização | Oracle VirtualBox |
| Docker | 26.1.5 |
| Docker Compose | 2.26.1-4 |

Após instalar o Docker e o Docker Compose, executei o projeto sem alterações no código e sem instalar manualmente Python, PostgreSQL ou as dependências do ETL na máquina virtual.

**Resultados obtidos:**

| Validação | Resultado |
|---|---|
| API | Up (healthy) |
| PostgreSQL | Up (healthy) |
| ETL | Exited (0) |
| Clientes | 1.000 |
| Produtos | 12 |
| Pedidos confirmados por consulta SQL | 5.000 |
| Itens de pedido | 12.455 |
| Duplicidades descartadas | 100 |
| Pedidos divergentes | 238 |
| Soma de `valor_itens` na origem e no destino | R$ 311.228,75 |
| Diferença na reconciliação | R$ 0,00 |
| Testes automatizados | 21 aprovados |

A saída final do pytest, obtida após executar a extração no contêiner temporário, foi:

```text
21 passed in 0.30s
```

A validação confirmou que o projeto pode ser baixado do GitHub e executado em outro sistema operacional com Docker e Docker Compose, sem depender das configurações do ambiente original. As evidências foram registradas na pasta `evidencias/`.

### Encerrar a execução

Em outro terminal, na raiz do projeto, execute:

```bash
docker compose down
```

O comando remove os contêineres e a rede do projeto, preservando o volume de dados do PostgreSQL.

### Observações

- O banco Docker é independente do PostgreSQL instalado no computador.
- O volume preserva os dados entre as execuções.
- O esquema SQL é aplicado automaticamente apenas na inicialização de um volume vazio.
- O comando principal executa o ETL; os testes são executados separadamente.
- A senha definida no Compose é fictícia e destinada exclusivamente ao ambiente local de demonstração.
- As dependências Python não estão fixadas em versões específicas.
- As pastas `evidencias/` e `kanban/` não são copiadas para a imagem Docker, mas continuam disponíveis no repositório GitHub.
- A proteção contra extração incompleta vale para a execução encadeada. A carga executada isoladamente ainda pode utilizar arquivos brutos já existentes.

## 8. Evidências e documentação

As evidências estão organizadas em:

- `evidencias/evidencias.pdf`: documento consolidado com evidências da extração, transformação, carga, testes, reconciliação e consultas SQL.
- `evidencias/`: registros complementares da validação em máquina virtual Debian.
- `kanban/`: capturas do quadro Kanban utilizado para organizar e acompanhar as atividades.

Documentação complementar:

- `contrato_de_dados.md`: regras e estrutura dos dados.
- `consultas_validacao.sql`: consultas SQL de validação e análise.
- `como_usei_ia.md`: registro das sugestões, decisões, correções e validações envolvendo inteligência artificial.

A execução com Docker Compose também foi validada por meio dos resultados no terminal, dos testes de idempotência, da simulação de falha e dos 21 testes automatizados.

## 9. Uso de IA e versionamento

O ChatGPT e o Codex foram utilizados como ferramentas de apoio para compreensão dos requisitos, elaboração de prompts, implementação, testes e documentação.

As sugestões aceitas, rejeitadas ou modificadas, além das dificuldades e validações realizadas, estão registradas em `como_usei_ia.md`.

O projeto foi desenvolvido com commits organizados por etapa. A implementação opcional do Docker foi realizada em uma branch separada, preservando a versão anterior do projeto.

A integração com a branch principal será apresentada por meio de Pull Request após a revisão final.
