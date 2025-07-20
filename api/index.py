from flask import Flask, request, jsonify, Response
from http.server import BaseHTTPRequestHandler
import json
import random
import os

quotes = [
    {
        "quote": "Eu vou restaurar meu clã e destruir um certo alguém.",
        "context": "Ao se apresentar para o Time 7",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Meu nome é Sasuke Uchiha. Eu odeio muitas coisas, e não gosto de nada em particular.",
        "context": "Durante a apresentação do Time 7",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Eu tenho um irmão... que eu preciso matar!",
        "context": "Sobre sua ambição de vingança",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Eu há muito tempo fechei meus olhos... Meu único objetivo está na escuridão.",
        "context": "Ao deixar a Vila da Folha",
        "source": "Episódio 109 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Meu sonho não é apenas um sonho, mas uma realidade que eu farei acontecer.",
        "context": "Sobre sua vingança contra Itachi",
        "source": "Episódio 107 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Eu poupei sua vida por capricho, nada mais.",
        "context": "Para Naruto após sua primeira luta séria",
        "source": "Episódio 35 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Você ainda é muito fraco. Você não tem ódio suficiente.",
        "context": "Repetindo as palavras de Itachi",
        "source": "Episódio 131 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Eu cheguei a entender que a vingança é o caminho certo para mim.",
        "context": "Conversando com Kakashi",
        "source": "Episódio 108 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Poder não é vontade, é a capacidade de fazer as coisas acontecerem fisicamente.",
        "context": "Durante treinamento com Orochimaru",
        "source": "Episódio 34 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "quote": "Quando um homem aprende a amar, ele deve suportar o risco do ódio.",
        "context": "Reflexão após descobrir a verdade sobre Itachi",
        "source": "Episódio 142 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "quote": "Eu me recuso a seguir os passos de qualquer pessoa.",
        "context": "Ao formar o Time Hebi",
        "source": "Episódio 118 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "quote": "O que eu tenho não é um sonho, porque eu vou torná-lo realidade.",
        "context": "Declarando sua ambição",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Se quiser me ridicularizar como um moleque influenciado por suas emoções, vá em frente.",
        "context": "Ao declarar guerra contra Konoha",
        "source": "Episódio 212 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "quote": "Eu não tenho sonhos para o futuro... apenas o passado. É tudo que existe dentro de mim.",
        "context": "Quando confrontado por Gaara",
        "source": "Episódio 83 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "quote": "Desculpe Sasuke... não haverá próxima vez.",
        "context": "Palavras de Itachi que atormentaram Sasuke",
        "source": "Episódio 84 (Naruto Clássico)",
        "category": "Flashback"
    },
    {
        "quote": "A única coisa que eu tenho certeza é que nada é certo.",
        "context": "Após descobrir a verdade sobre o massacre do clã",
        "source": "Episódio 143 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "quote": "O que eu vejo agora é apenas escuridão.",
        "context": "Após ser consumido pelo ódio",
        "source": "Episódio 216 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "quote": "Eu sou um vingador!",
        "context": "Sua frase mais emblemática",
        "source": "Vários episódios",
        "category": "Genin"
    },
    {
        "quote": "Esses olhos podem ver através da escuridão.",
        "context": "Sobre o poder do Sharingan",
        "source": "Episódio 129 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "quote": "Eu vou acabar com essa maldição. Se alguém tiver que suportar o ódio dos Uchiha, eu prefiro que seja eu.",
        "context": "Sobre o legado dos Uchiha",
        "source": "Episódio 386 (Naruto Shippuden)",
        "category": "Shippuden"
    }
]

app = Flask(__name__)

@app.route('/api/quote', methods=['GET'])
def get_random_quote():
    quote = random.choice(quotes)
    return jsonify(quote)

@app.route('/api/quotes', methods=['GET'])
def get_all_quotes():
    return jsonify({"quotes": quotes})

@app.route('/api/quote/<int:id>', methods=['GET'])
def get_quote_by_id(id):
    for quote in quotes:
        if quote.get("id") == id:
            return jsonify(quote)
    return jsonify({"message": "Citação não encontrada"}), 404

@app.route('/api/search', methods=['GET'])
def search_quotes():
    term = request.args.get('q', '')
    if not term:
        return jsonify({"message": "Termo de busca é obrigatório"}), 400
    
    results = [q for q in quotes if term.lower() in q.get("quote", "").lower()]
    return jsonify({"quotes": results})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = set(q.get("category", "") for q in quotes if "category" in q)
    return jsonify({"categories": list(categories)})

@app.route('/api/quotes/category/<category>', methods=['GET'])
def get_quotes_by_category(category):
    results = [q for q in quotes if q.get("category", "").lower() == category.lower()]
    return jsonify({"quotes": results})

@app.route('/', methods=['GET'])
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API de Citações do Sasuke</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            h1 { color: #2c3e50; text-align: center; }
            .quote-box { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; }
            button { background: #3498db; color: white; border: none; padding: 10px 20px; cursor: pointer; display: block; margin: 20px auto; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>API de Citações do Sasuke</h1>
        
        <div class="quote-box" id="quote-display">
            Clique no botão para ver uma citação aleatória do Sasuke.
        </div>
        
        <button id="get-quote">Ver Citação</button>
        
        <h2>Endpoints da API:</h2>
        <div class="endpoint">
            <h3>GET /api/quote</h3>
            <p>Obter uma citação aleatória</p>
        </div>
        <div class="endpoint">
            <h3>GET /api/quotes</h3>
            <p>Obter todas as citações</p>
        </div>
        <div class="endpoint">
            <h3>GET /api/quote/:id</h3>
            <p>Obter uma citação específica por ID</p>
        </div>
        <div class="endpoint">
            <h3>GET /api/search?q=termo</h3>
            <p>Pesquisar citações contendo o termo</p>
        </div>
        <div class="endpoint">
            <h3>GET /api/quotes/category/:categoria</h3>
            <p>Filtrar citações por categoria</p>
        </div>
        
        <script>
            document.getElementById('get-quote').addEventListener('click', async () => {
                const response = await fetch('/api/quote');
                const data = await response.json();
                document.getElementById('quote-display').textContent = data.quote;
            });
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

def handler(event, context):
    return app

if __name__ == "__main__":
    app.run(debug=True)