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