# API de Citações do Sasuke

Uma API RESTful para gerenciar e recuperar citações de Sasuke Uchiha, o melhor personagem do anime Naruto!

![Sasuke Uchiha](https://static.wikia.nocookie.net/narutofanon/images/e/e3/SasukeCl%C3%A1ssico832.gif/revision/latest?cb=20170412220258&path-prefix=pt-br)

## Funcionalidades

- 🔄 Obter citações aleatórias do Sasuke
- 📝 Visualizar todas as citações disponíveis
- 🔍 Pesquisar citações por palavra-chave
- 🏷️ Filtrar citações por categoria (Genin, Shippuden, etc.)
- 📚 Informações de contexto e fonte para cada citação
- ➕ Adicionar novas citações (com autenticação)
- 🗑️ Excluir citações (com autenticação)
- ⭐ Sistema de citações favoritas
- 🌙 Modo escuro/claro com tema Uchiha
- 🔒 Rotas protegidas com autenticação por token

## Instalação

### Usando Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/Augusto240/sasukeAPI.git
cd sasukeAPI

# Construa e inicie o contêiner
docker-compose up --build
```

### Instalação Manual

```bash
# Clone o repositório
git clone https://github.com/Augusto240/sasukeAPI.git
cd sasukeAPI

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

## Endpoints da API

| Método | Endpoint                      | Descrição                               | Autenticação |
|--------|-------------------------------|----------------------------------------|--------------|
| GET    | /sasuke/quote                 | Obter uma citação aleatória            | Não          |
| GET    | /sasuke/quotes                | Obter todas as citações                | Não          |
| GET    | /sasuke/quote/:id             | Obter uma citação específica por ID    | Não          |
| GET    | /sasuke/search?q=termo        | Pesquisar citações contendo o termo    | Não          |
| GET    | /sasuke/quotes/category/:cat  | Filtrar citações por categoria         | Não          |
| GET    | /sasuke/categories            | Listar todas as categorias disponíveis | Não          |
| GET    | /sasuke/favorites             | Listar todas as citações favoritas     | Não          |
| POST   | /sasuke/favorites/:id         | Adicionar uma citação aos favoritos    | Sim          |
| DELETE | /sasuke/favorites/:id         | Remover uma citação dos favoritos      | Sim          |
| POST   | /sasuke/quotes                | Adicionar uma nova citação             | Sim          |
| PUT    | /sasuke/quote/:id             | Atualizar uma citação existente        | Sim          |
| DELETE | /sasuke/quote/:id             | Excluir uma citação                    | Sim          |

## Exemplos de Uso

### Obter uma Citação Aleatória

```bash
curl -X GET http://localhost:5000/sasuke/quote
```

Resposta:
```json
{
  "id": 3,
  "quote": "Eu tenho um irmão... que eu preciso matar!",
  "context": "Sobre sua ambição de vingança",
  "source": "Episódio 3 (Naruto Clássico)",
  "category": "Genin"
}
```

### Obter Todas as Citações

```bash
curl -X GET http://localhost:5000/sasuke/quotes
```

### Pesquisar Citações

```bash
curl -X GET http://localhost:5000/sasuke/search?q=vingança
```

### Filtrar por Categoria

```bash
curl -X GET http://localhost:5000/sasuke/quotes/category/Shippuden
```

### Adicionar uma Nova Citação (Requer Autenticação)

```bash
curl -X POST http://localhost:5000/sasuke/quotes \
     -H "Authorization: Bearer sasuke_api_token" \
     -H "Content-Type: application/json" \
     -d '{
       "quote": "Sua nova citação do Sasuke", 
       "context": "Contexto da citação",
       "source": "Episódio X",
       "category": "Shippuden"
     }'
```

## Autenticação

Endpoints protegidos requerem um token Bearer no cabeçalho Authorization:

```
Authorization: Bearer sasuke_api_token
```

O token da API pode ser definido usando a variável de ambiente `API_TOKEN`.

## Interface Web

A API inclui uma interface web simples e elegante que permite:

- Visualizar citações aleatórias do Sasuke
- Filtrar citações por categoria
- Alternar entre modo claro e escuro
- Ver a documentação da API

Acesse a interface web navegando para `http://localhost:5000/` após iniciar o servidor.

## Configuração

A configuração é gerenciada por variáveis de ambiente:

| Variável            | Descrição                      | Padrão                     |
|---------------------|----------------------------------|-----------------------------|
| DEBUG               | Ativar modo de depuração         | True                        |
| SECRET_KEY          | Chave secreta do Flask           | sasuke_uchiha_secret        |
| API_TOKEN           | Token para endpoints protegidos  | sasuke_api_token            |
| PORT                | Porta em que o servidor executa  | 5000                        |

## Contribuindo

1. Faça um fork do repositório
2. Crie um branch para sua funcionalidade: `git checkout -b minha-funcionalidade`
3. Faça commit das suas alterações: `git commit -m 'Adiciona nova funcionalidade'`
4. Envie para o branch: `git push origin minha-funcionalidade`
5. Abra um Pull Request
