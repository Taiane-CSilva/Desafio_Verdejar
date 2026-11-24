# Como usei a IA

Durante o desenvolvimento do desafio Verdejar, utilizei o ChatGPT para esclarecer dúvidas, elaborar prompts e revisar soluções. Também utilizei o Codex no VS Code para implementar funções e testes dentro dos escopos solicitados.

Os pedidos descritos abaixo são resumos do que solicitei à IA, e não transcrições literais dos prompts.

## Parte 0 — Preparação do projeto

### Sugestões aceitas

Utilizei o ChatGPT para esclarecer dúvidas sobre a configuração do Python, PostgreSQL e Git. Segui as orientações necessárias e validei o ambiente executando os comandos no VS Code.

### Sugestões rejeitadas ou modificadas

**Pedido à IA:** orientação para configurar o `.gitignore`.

O ChatGPT sugeriu ignorar `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `.env.*` e criar uma exceção para `.env.example`.

Após consultar o desafio, preferi utilizar:

```gitignore
__pycache__/
.env
.venv/
brutos/
```

**Justificativa:** manter as credenciais, o ambiente virtual e os dados brutos fora do versionamento.

**Validação:** conferi as orientações do desafio e a organização dos arquivos.

## Parte 1 — Extração

### Sugestões aceitas

**Pedido à IA:** orientação para criar testes que comprovassem o funcionamento da extração.

Após executar o código, questionei a falta de evidências reproduzíveis. O ChatGPT sugeriu utilizar pytest. Aceitei a proposta, solicitei ajuda para elaborar o prompt e utilizei o Codex para gerar os testes.

**Validação:** executei os quatro testes automatizados, todos aprovados.

### Sugestões rejeitadas ou modificadas

A IA sugeriu utilizar o módulo `csv` para ler `produtos.csv`. Preferi utilizar pandas, com `pd.read_csv()`, por ser um método que eu já conhecia.

Também solicitei uma alternativa com `for` para a paginação da API, em vez de `while`, por ser uma estrutura que eu compreendia melhor.

**Validação:** executei a leitura dos arquivos e conferi os registros retornados.

### Falhas e retrabalho

Inicialmente, o código de extração foi criado na pasta `brutos/`. Precisei reorganizá-lo em `etl/` e corrigir problemas de indentação e trechos duplicados.

Também ajustei o delimitador do CSV e substituí o caminho absoluto por um caminho relativo.

## Parte 2 — Transformação e contrato de dados

### Sugestões aceitas

**Pedido à IA:** estruturar o contrato de dados considerando as regras do desafio, o `schema.sql` e uma referência sobre contratos de dados consultada no site da IBM.

Aceitei a estrutura proposta pelo ChatGPT após revisar os campos, tipos, obrigatoriedade e regras de transformação.

**Validação:** comparei as informações com o esquema SQL e as regras A1 a A6.

Também utilizei o Codex para implementar as funções de transformação e gerar testes automatizados. Ao final dessa etapa, executei 18 testes com sucesso.

### Sugestões rejeitadas ou modificadas

A IA sugeriu implementar as transformações e executar imediatamente os testes com pytest. Preferi revisar primeiro as funções e conferir os resultados antes de avançar.

Também decidi validar os contadores de forma independente no Excel, ferramenta com a qual tenho mais familiaridade, para não depender apenas dos resultados apresentados pelo Python.

### Falhas e retrabalho

Na implementação inicial, os contadores de datas e valores não diferenciavam corretamente os registros que precisavam de conversão.

**Correção:** solicitei ao Codex o ajuste da lógica dos contadores.

**Validação:** executei novamente as transformações e conferi os resultados com os dados de origem, incluindo os 238 pedidos divergentes da regra A6.

## Parte 3 — Carga no PostgreSQL

### Sugestões aceitas

**Pedido à IA:** implementar a carga dos dados tratados no PostgreSQL, respeitando a ordem das tabelas, utilizando SQL parametrizado e evitando duplicações.

Utilizei o ChatGPT para preparar os prompts e o Codex para implementar `etl/carga.py`.

**Validação:** executei a carga duas vezes e confirmei que as quantidades permaneceram iguais: 12 produtos, 1.000 clientes, 5.000 pedidos e 12.455 itens de pedido.

Também solicitei ao Codex testes específicos da carga, totalizando 20 testes aprovados até essa etapa.

### Sugestões rejeitadas ou modificadas

Preferi revisar o código e executar pessoalmente a carga no PostgreSQL, em vez de permitir a execução automática pela IA.

**Validação:** conferi as quantidades no pgAdmin e realizei consultas de integridade dos dados.

## Parte 4 — Testes e reconciliação

### Sugestões aceitas

**Pedido à IA:** criar um teste de reconciliação que comparasse a quantidade de pedidos únicos e a soma de `valor_itens` entre a origem tratada e o PostgreSQL.

Utilizei o ChatGPT para elaborar o prompt e o Codex para gerar o teste em pytest.

**Validação:** confirmei 5.000 pedidos na origem e no destino, soma de R$ 311.228,75 em ambos e diferença de R$ 0,00.

Ao final, executei a suíte completa com **21 testes aprovados**.

### Sugestões rejeitadas ou modificadas

O ChatGPT sugeriu uma consulta SQL com subconsultas. Como tive dificuldade para compreender sua estrutura inicialmente, preferi começar com consultas mais simples e depois retomar a sugestão.

**Validação:** executei as consultas no pgAdmin e confirmei que a soma dos valores mensais correspondia à soma geral da tabela.

Também utilizei o ChatGPT para esclarecer dúvidas sobre `DATE_TRUNC`, `valor_total` e `valor_itens`, além de organizar o README e as evidências.

## Etapa extra — Implementação do Docker

### Sugestões aceitas

Decidi implementar o Docker como atividade opcional, utilizando o ChatGPT para me orientar, pois ainda estava aprendendo a ferramenta. A IA sugeriu criar o `Dockerfile`, o `.dockerignore` e o arquivo de orquestração.

Durante a configuração, explicou como utilizar um PostgreSQL separado do banco local, ajustar a API para aceitar conexões entre contêineres e configurar o endereço por variável de ambiente.

Fiz questão de reforçar a importância da **idempotência**, para evitar duplicações. Executei o ETL duas vezes no Docker e confirmei as mesmas quantidades, com 5.000 pedidos, 12.455 itens e diferença financeira de R$ 0,00.

### Sugestões rejeitadas ou modificadas

Questionei se colocar `evidencias/` e `kanban/` no `.dockerignore` impediria o recrutador de visualizar essas pastas no GitHub. Após entender que os arquivos continuariam versionados, aceitei a sugestão.

Também preferi utilizar `docker-compose.yml`, conforme o desafio, em vez de `compose.yaml`, inicialmente sugerido pela IA.

### Falhas, correções e validações

Na primeira tentativa, o ETL apresentou erro pela ausência de `import os`, necessário para utilizar a variável de ambiente da API. Corrigi a importação e consegui executar o processo.

Ao executar os testes no Docker, 20 passaram e um falhou porque os arquivos JSON não estavam disponíveis no novo contêiner. Com a orientação da IA, executei a extração antes dos testes e consegui aprovar os 21 testes.

Para realizar uma revisão adicional, solicitei ao ChatGPT um prompt para o Codex analisar a implementação sem alterar arquivos. O Codex identificou um risco de reutilização de dados antigos caso a extração falhasse. Aceitei a correção proposta, que passou a interromper o processo quando as quantidades extraídas fossem incompletas.

Também ajustei o tratamento de erros do script de resumo, para que uma exceção fosse sinalizada ao Docker.

**Validação:** simulei uma API indisponível e confirmei que a carga foi cancelada. Depois, executei novamente o ETL, obtendo diferença financeira de R$ 0,00, e confirmei os **21 testes aprovados após as correções**.

Na revisão final, o Codex apontou como melhorias opcionais a definição de versões das dependências e o uso de credenciais configuráveis. Mantive essas sugestões registradas, priorizando a validação e a documentação necessárias à entrega.

## Considerações finais

Utilizei a IA como ferramenta de apoio durante todas as etapas, principalmente para implementação, testes, documentação e esclarecimento de dúvidas.

Procurei revisar as sugestões, compreender o código gerado e validar os resultados por conta própria, utilizando Python, PostgreSQL, Excel e Docker. Também rejeitei ou adaptei orientações quando encontrei alternativas que compreendia melhor.

A experiência mostrou pontos em que ainda preciso desenvolver mais autonomia, principalmente em Python e testes automatizados, mas também me ajudou a compreender melhor o funcionamento de um processo ETL completo.