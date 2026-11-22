# Como usei a IA

## 0 - Preparação do projeto

Utilizei o ChatGPT como ferramenta de apoio durante a preparação do ambiente, principalmente para conferir as versões do Python e do PostgreSQL, verificar a conexão entre eles e esclarecer algumas dúvidas sobre Git.

### Sugestões aceitas

Durante a configuração do ambiente, utilizei a IA para me orientar na conexão entre Python e PostgreSQL. Após as configurações, realizei o teste pelo terminal do VS Code e confirmei que a conexão foi estabelecida sem apresentar erros.

Também utilizei a IA para revisar o funcionamento das branches e entender melhor a diferença entre a branch principal (`main`) e a branch de desenvolvimento. Com isso, consegui organizar o repositório e criar uma branch específica para o desafio.

### Sugestões rejeitadas

Ao configurar o arquivo `.gitignore`, tive dúvidas sobre quais arquivos deveriam ser ignorados. Inicialmente, a IA sugeriu as seguintes regras:

```gitignore
.venv/
__pycache__/
*.pyc
.env
.env.*
!.env.example
```

Como este é meu primeiro projeto utilizando Git de forma mais independente, preferi consultar novamente a documentação do desafio antes de aceitar todas as sugestões.

Optei por utilizar:

```gitignore
__pycache__/
.env
.venv/
brutos/
```

Mantive o `.env` para evitar o versionamento de senhas e a pasta `brutos/` conforme a orientação do PDF. Também incluí `__pycache__/`, por armazenar arquivos temporários gerados pelo Python, e `.venv/`, por conter o ambiente virtual do projeto.

Decidi não adicionar as demais regras neste momento, pois ainda não identifiquei a necessidade delas. Caso seja necessário, poderei atualizar o `.gitignore` durante o desenvolvimento.

### Falhas e retrabalho

Durante a organização inicial do projeto, precisei revisar alguns conceitos de Git antes de continuar, principalmente a diferença entre pastas e branches. Utilizei as explicações da IA para esclarecer essas dúvidas e conferir os comandos executados.

Também organizei as atividades do desafio em um Kanban no Trello, utilizando a documentação como referência. Depois, consultei a IA para conferir se as etapas estavam alinhadas com o que foi solicitado.

**Observação:** O registro de falhas em código sugerido pela IA será complementado durante o desenvolvimento do ETL.

---

## Parte 1 — Extração

### Sugestões aceitas

Durante a extração, voltei à seção 12 do curso da Udemy sobre consumo de APIs REST com Python, principalmente à parte de GET. Consegui escrever o início do código, mas tive dificuldades para desenvolver a função de paginação e o tratamento de erros.

Pedi ajuda ao ChatGPT para entender a lógica e desenvolver o restante do código. Utilizei as sugestões da IA, fiz ajustes e executei o programa para verificar os resultados.

Também utilizei o Codex no VS Code para implementar e executar testes automatizados com pytest. Foram realizados quatro testes, todos aprovados.

### Sugestões rejeitadas

Inicialmente, a IA sugeriu fazer testes manuais e depois apagar os códigos utilizados. Não concordei com essa abordagem, porque considero importante manter evidências que outras pessoas possam executar e conferir.

Pensei em deixar os testes comentados no código, mas a IA apresentou a alternativa de utilizar pytest. Achei mais adequada e decidi seguir com os testes automatizados.

Na leitura do arquivo `produtos.csv`, a IA sugeriu utilizar o módulo `csv`. Preferi utilizar pandas, com `pd.read_csv()`, porque já tinha aprendido esse método no curso e consegui desenvolver essa parte com mais autonomia.

### Falhas e retrabalho

Durante o desenvolvimento, tivemos problemas com a organização dos arquivos. O código de extração foi criado em uma pasta incorreta, dentro de `brutos`, e precisei recuperá-lo e reorganizá-lo na pasta `etl`.

Também tive dificuldades com a indentação e precisei corrigir trechos duplicados. Inicialmente, a IA sugeriu uma função utilizando `while`, mas pedi uma alternativa mais simples e seguimos com `for`, que eu já conhecia.

Na leitura do CSV, corrigi o delimitador e substituí o caminho absoluto do meu computador por um caminho relativo, pensando na execução do projeto por outras pessoas após a publicação no GitHub.

Por fim, questionei a falta de evidências dos testes manuais. Com apoio da IA e do Codex, passei a utilizar testes automatizados e organizei as evidências da extração em um PDF.


## Parte 2 — Transformação e Contrato de Dados

### Sugestões aceitas

Inicialmente, tive dificuldade para começar o Contrato de Dados, pois precisei revisar o conceito e entender sua finalidade. Para isso, pesquisei no Google e consultei um artigo da IBM sobre contratos de dados.

Depois de compreender melhor o assunto, solicitei ao ChatGPT que estruturasse um contrato para o projeto Verdejar, considerando o que eu havia pesquisado na IBM e as exigências do desafio.

Revisei o documento campo por campo, utilizando o `schema.sql` para conferir os tipos de dados, a obrigatoriedade e os relacionamentos entre as tabelas. Também conferi individualmente as regras das armadilhas A1 a A6 no enunciado, questionando algumas informações até entender sua origem.

Para implementar as transformações, utilizei o Codex, que me auxiliou na criação das funções Python no arquivo `transformacao.py`. Posteriormente, pedi ajuda ao ChatGPT para revisar o código, identificar as funções relacionadas a cada armadilha e compreender os resultados.

Também utilizei o Codex para criar os testes automatizados com pytest. Ao final, foram aprovados 18 testes, considerando os quatro testes de extração já existentes e os 14 testes de transformação.

### Sugestões rejeitadas ou modificadas

A IA sugeriu implementar as funções de transformação e realizar imediatamente os testes com pytest. Preferi separar essas atividades, pois queria primeiro revisar as funções e executá-las com os dados reais para entender os resultados.

Também considerei uma versão mais extensa e comentada do código sugerida pelo ChatGPT, mas preferi manter a versão mais enxuta do Codex, acrescentando apenas comentários para identificar as armadilhas A1 a A6.

Outra decisão minha foi realizar uma validação independente no Excel. Apesar de a IA já ter apresentado os contadores das transformações, preferi conferir os dados manualmente, utilizando filtros, fórmulas, Power Query e Tabelas Dinâmicas, pois tenho mais familiaridade com essas ferramentas.

### Falhas e retrabalho

A elaboração do Contrato de Dados levou mais tempo do que eu esperava, principalmente porque precisei estudar o conceito antes de conseguir validar o documento.

Durante a revisão, identifiquei informações que precisavam ser esclarecidas, como a diferença entre as regras definidas no `schema.sql` e as transformações exigidas pelas armadilhas. Também questionei a padronização da data de cadastro dos clientes, que não fazia parte da armadilha A3.

Na implementação das funções, os primeiros contadores de datas e valores consideravam todos os pedidos tratados. Solicitei ao Codex que ajustasse a lógica para diferenciar os registros processados daqueles que chegaram com formatos que precisavam de conversão.

A validação no Excel também exigiu retrabalho. Inicialmente, obtive contagens diferentes das apresentadas pelo Python porque estava considerando pedidos duplicados. Depois de identificar a diferença, ajustei os filtros e consegui confirmar os resultados das armadilhas A3, A4 e A5.

Na armadilha A6, precisei compreender melhor a relação entre pedidos e seus itens. Ao expandir os itens no Power Query, percebi que um pedido poderia aparecer em várias linhas. Também foi necessário remover os pedidos duplicados antes de calcular a soma dos itens, para evitar contagens incorretas.

Depois dessas correções, consegui confirmar no Excel os mesmos **238 pedidos divergentes** identificados pelo Python.

Por fim, executei os testes automatizados com pytest e procurei compreender o que estava sendo validado, principalmente a regra de que uma diferença de até R$ 0,01 não caracteriza divergência financeira.

### Aprendizados

Apesar de ter dedicado mais tempo à validação manual, considero que essa etapa foi importante para compreender melhor o funcionamento do ETL.

Aprendi a diferenciar as regras de transformação da estrutura do banco de dados, entendi a importância de remover duplicidades antes dos cálculos e compreendi melhor como os testes automatizados verificam o comportamento das funções.

A IA foi utilizada como apoio para pesquisa, documentação, implementação, revisão e testes. As decisões sobre o processo de trabalho e a conferência dos resultados foram realizadas por mim, com o objetivo de compreender e validar as entregas antes de avançar para a carga no PostgreSQL.

## Parte 3 — Carga no Banco de Dados

### Sugestões aceitas

Nesta etapa, utilizei o Codex para implementar o arquivo `etl/carga.py`, responsável por carregar os dados tratados nas quatro tabelas do PostgreSQL: produtos, clientes, pedidos e itens_pedido.

Solicitei ajuda ao ChatGPT para elaborar os prompts enviados ao Codex, definindo os requisitos da carga, a ordem das tabelas, o uso de consultas parametrizadas e a necessidade de evitar registros duplicados.

Após a implementação, executei o código e conferi as quantidades carregadas: 12 produtos, 1.000 clientes, 5.000 pedidos e 12.455 itens.

Executei a carga uma segunda vez para verificar a idempotência, confirmando que as quantidades permaneceram iguais.

Também solicitei ao Codex a criação de testes automatizados com pytest. A execução completa apresentou 20 testes aprovados, sendo dois específicos da etapa de carga.

Por fim, utilizei o ChatGPT para organizar as evidências em PDF, incluindo os resultados das duas execuções, dos testes automatizados e das consultas SQL realizadas no PostgreSQL.

### Sugestões rejeitadas ou modificadas

Preferi revisar a implementação antes de executar o código no banco de dados, em vez de permitir que a IA realizasse a carga automaticamente.

Também optei por executar pessoalmente a carga duas vezes no PostgreSQL, para verificar o comportamento com os dados reais, além dos testes automatizados criados pelo Codex.

### Dificuldades e pontos de atenção

Esta foi a etapa que concluí mais rapidamente, o que me gerou preocupação sobre a possibilidade de não ter conferido todos os detalhes necessários.

Uma dificuldade foi configurar a conexão com o PostgreSQL utilizando o arquivo `.env`. O Codex identificou a necessidade das variáveis de conexão, que configurei antes de executar a carga.

Para aumentar minha confiança no resultado, realizei consultas SQL diretamente no banco e confirmei as quantidades das quatro tabelas.

Também verifiquei se existiam pedidos sem clientes correspondentes e diferenças entre o valor dos itens armazenado e o total calculado a partir dos produtos de cada pedido. Ambas as consultas retornaram zero.

### Aprendizados

Compreendi melhor a diferença entre transformar os dados em Python e armazená-los efetivamente no PostgreSQL.

Também entendi o conceito de idempotência: executar novamente a carga com os mesmos dados não deve criar registros duplicados.

Aprendi que conferir apenas a quantidade de registros não é suficiente. Também é importante verificar a integridade dos relacionamentos e a consistência dos valores armazenados.

A IA foi utilizada principalmente para implementar o código e os testes, enquanto participei da definição dos requisitos, da execução, da conferência dos resultados e da documentação das evidências.