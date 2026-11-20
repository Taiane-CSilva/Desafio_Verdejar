## Como usei a IA — Preparação do projeto

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