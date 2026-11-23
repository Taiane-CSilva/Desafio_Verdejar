# Como usei a IA

Durante o desenvolvimento do desafio Verdejar, utilizei o ChatGPT para esclarecer dúvidas, elaborar prompts e revisar as soluções. Também utilizei o Codex no VS Code para implementar funções e testes dentro dos escopos solicitados.

Os pedidos descritos abaixo são resumos do que solicitei à IA, e não transcrições literais dos prompts.

## Parte 0 — Preparação do projeto

### Sugestões aceitas

Utilizei o ChatGPT para esclarecer dúvidas sobre a configuração do Python, do PostgreSQL e do Git. Segui as orientações necessárias e validei a configuração executando os comandos no VS Code.

### Sugestões rejeitadas ou modificadas

**Pedido à IA:** orientação para configurar o `.gitignore`.

O ChatGPT sugeriu ignorar `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `.env.*` e criar uma exceção para `.env.example`.

Após consultar a documentação do desafio, preferi utilizar:

```gitignore
__pycache__/
.env
.venv/
brutos/
```

**Justificativa:** manter o arquivo de credenciais, o ambiente virtual e os dados brutos fora do versionamento, conforme as necessidades do projeto.

**Validação:** conferi as orientações do desafio e a organização dos arquivos.

## Parte 1 — Extração

### Sugestões aceitas

**Pedido à IA:** orientação para criar testes que comprovassem o funcionamento da extração.

Após executar o código de extração, questionei a falta de evidências reproduzíveis. O ChatGPT sugeriu utilizar pytest, e aceitei a proposta. Solicitei ajuda para elaborar o prompt e utilizei o Codex para gerar os testes.

**Validação:** executei os quatro testes automatizados, todos aprovados.

### Sugestões rejeitadas ou modificadas

A IA sugeriu utilizar o módulo `csv` para ler `produtos.csv`. Preferi utilizar pandas, com `pd.read_csv()`, porque já conhecia esse método.

**Validação:** executei a leitura e conferi os registros retornados.

Também solicitei uma alternativa com `for` para a paginação da API, em vez da estrutura com `while` sugerida inicialmente, por ser uma construção que eu compreendia melhor.

### Falhas e retrabalho

O código de extração foi criado inicialmente na pasta `brutos/`. Precisei reorganizá-lo em `etl/` e corrigir problemas de indentação e trechos duplicados.

Também ajustei o delimitador do CSV e substituí o caminho absoluto por um caminho relativo.

## Parte 2 — Transformação e contrato de dados

### Sugestões aceitas

**Pedido à IA:** estruturar o contrato de dados do Verdejar considerando as regras do desafio, o `schema.sql` e uma referência sobre contratos de dados que consultei no site da IBM.

Aceitei a estrutura proposta pelo ChatGPT após revisar os campos, tipos, obrigatoriedade e regras de transformação.

**Validação:** comparei as informações individualmente com o esquema SQL e as regras A1 a A6.

Também utilizei o Codex para implementar as funções de transformação e gerar testes automatizados. Ao final dessa etapa, executei 18 testes com sucesso.

### Sugestões rejeitadas ou modificadas

A IA sugeriu implementar as transformações e realizar imediatamente os testes com pytest. Preferi revisar primeiro as funções e conferir os resultados antes de avançar.

Também optei por validar os contadores de forma independente no Excel, para não depender apenas dos resultados apresentados pelo Python.

### Falhas e retrabalho

Na implementação inicial, os contadores de datas e valores não diferenciavam corretamente os registros que realmente precisavam de conversão.

**Correção:** solicitei ao Codex que ajustasse a lógica dos contadores.

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

**Validação:** executei o teste e confirmei 5.000 pedidos na origem e no destino, soma de R$ 311.228,75 em ambos e diferença de R$ 0,00.

Ao final, executei a suíte completa com **21 testes aprovados**.

### Sugestões rejeitadas ou modificadas

O ChatGPT sugeriu uma consulta SQL com subconsultas. Como tive dificuldade para entender sua estrutura inicialmente, preferi começar com consultas mais simples e depois retomar a sugestão.

**Validação:** executei as consultas no pgAdmin e confirmei que a soma dos valores mensais correspondia à soma geral da tabela.

Também utilizei o ChatGPT para esclarecer dúvidas sobre `DATE_TRUNC`, `valor_total` e `valor_itens`, além de organizar o README e as evidências.

## Considerações finais

Utilizei a IA como ferramenta de apoio durante todas as etapas, principalmente para implementação, testes e esclarecimento de dúvidas.

Procurei revisar as sugestões, compreender o código gerado e validar os resultados antes de concluir cada etapa.