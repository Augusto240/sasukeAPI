from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
import random
from pathlib import Path
from datetime import datetime

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sasuke_uchiha_secret')
app.config['API_TOKEN'] = os.environ.get('API_TOKEN', 'sasuke_api_token')

data_dir = Path('data')
data_dir.mkdir(exist_ok=True)
quotes_file = data_dir / 'quotes.json'
favorites_file = data_dir / 'favorites.json'

default_quotes = [
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

def initialize_quotes():
    try:
        if not quotes_file.exists() or quotes_file.stat().st_size == 0:
            quotes = [{"id": i+1, **quote} for i, quote in enumerate(default_quotes)]
            with open(quotes_file, 'w', encoding='utf-8') as f:
                json.dump({"quotes": quotes}, f, indent=2, ensure_ascii=False)
                
        if not favorites_file.exists():
            with open(favorites_file, 'w', encoding='utf-8') as f:
                json.dump({"favorites": []}, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao inicializar arquivos: {e}")

def get_quotes():
    try:
        if quotes_file.exists():
            with open(quotes_file, 'r', encoding='utf-8') as f:
                return json.load(f).get("quotes", [])
        else:
            initialize_quotes()
            with open(quotes_file, 'r', encoding='utf-8') as f:
                return json.load(f).get("quotes", [])
    except Exception as e:
        print(f"Erro ao obter citações: {e}")
        return []

def save_quotes(quotes):
    try:
        with open(quotes_file, 'w', encoding='utf-8') as f:
            json.dump({"quotes": quotes}, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar citações: {e}")

def get_favorites():
    try:
        if favorites_file.exists():
            with open(favorites_file, 'r', encoding='utf-8') as f:
                return json.load(f).get("favorites", [])
        else:
            with open(favorites_file, 'w', encoding='utf-8') as f:
                json.dump({"favorites": []}, f, indent=2, ensure_ascii=False)
            return []
    except Exception as e:
        print(f"Erro ao obter favoritos: {e}")
        return []

def save_favorites(favorites):
    try:
        with open(favorites_file, 'w', encoding='utf-8') as f:
            json.dump({"favorites": favorites}, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar favoritos: {e}")

def is_authorized():
    auth_header = request.headers.get('Authorization')
    expected_token = app.config.get('API_TOKEN')
    
    if not auth_header or not auth_header.startswith('Bearer ') or auth_header[7:] != expected_token:
        return False
    return True

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('../static', filename)

@app.route('/')
def home():
    return render_template('index.html', year=datetime.now().year)

@app.route('/sasuke/quote', methods=['GET'])
def get_random_quote():
    initialize_quotes()
    quotes = get_quotes()
    if not quotes:
        return jsonify({"message": "Nenhuma citação encontrada"}), 404
    
    quote = random.choice(quotes)
    return jsonify(quote)

@app.route('/sasuke/quotes', methods=['GET'])
def get_all_quotes():
    initialize_quotes()
    quotes = get_quotes()
    return jsonify({"quotes": quotes})

@app.route('/sasuke/quote/<int:id>', methods=['GET'])
def get_quote_by_id(id):
    initialize_quotes()
    quotes = get_quotes()
    for quote in quotes:
        if quote.get("id") == id:
            return jsonify(quote)
    return jsonify({"message": "Citação não encontrada"}), 404

@app.route('/sasuke/search', methods=['GET'])
def search_quotes():
    initialize_quotes()
    term = request.args.get('q', '')
    if not term:
        return jsonify({"message": "Termo de busca é obrigatório"}), 400
    
    quotes = get_quotes()
    results = [q for q in quotes if term.lower() in q.get("quote", "").lower()]
    return jsonify({"quotes": results})

@app.route('/sasuke/quotes/category/<category>', methods=['GET'])
def get_quotes_by_category(category):
    initialize_quotes()
    quotes = get_quotes()
    results = [q for q in quotes if q.get("category", "").lower() == category.lower()]
    return jsonify({"quotes": results})

@app.route('/sasuke/categories', methods=['GET'])
def get_categories():
    initialize_quotes()
    quotes = get_quotes()
    categories = set(q.get("category", "") for q in quotes if "category" in q)
    return jsonify({"categories": list(categories)})

@app.route('/sasuke/favorites', methods=['GET'])
def get_all_favorites():
    favorites = get_favorites()
    return jsonify({"favorites": favorites})

@app.route('/sasuke/favorites/<int:id>', methods=['POST'])
def add_favorite(id):
    if not is_authorized():
        return jsonify({"message": "Não autorizado"}), 401
        
    quotes = get_quotes()
    favorites = get_favorites()
        
    quote = next((q for q in quotes if q.get("id") == id), None)
    if not quote:
        return jsonify({"message": "Citação não encontrada"}), 404
        
    if id in [f.get("id") for f in favorites]:
        return jsonify({"message": "Citação já está nos favoritos"}), 400
        
    favorites.append(quote)
    save_favorites(favorites)
    
    return jsonify({"message": "Citação adicionada aos favoritos", "quote": quote}), 201

@app.route('/sasuke/favorites/<int:id>', methods=['DELETE'])
def remove_favorite(id):
    if not is_authorized():
        return jsonify({"message": "Não autorizado"}), 401
        
    favorites = get_favorites()
    filtered_favorites = [f for f in favorites if f.get("id") != id]
    
    if len(filtered_favorites) < len(favorites):
        save_favorites(filtered_favorites)
        return "", 204
    
    return jsonify({"message": "Citação não encontrada nos favoritos"}), 404

@app.route('/sasuke/quotes', methods=['POST'])
def add_quote():
    initialize_quotes()    
    if not is_authorized():
        return jsonify({"message": "Não autorizado"}), 401
        
    data = request.get_json()
    if not data or not data.get('quote'):
        return jsonify({"message": "Texto da citação é obrigatório"}), 400
    
    quote_text = data.get('quote')
    if len(quote_text) > 500:
        return jsonify({"message": "Citação não pode exceder 500 caracteres"}), 400
        
    context = data.get('context', 'Desconhecido')
    source = data.get('source', 'Desconhecido')
    category = data.get('category', 'Outros')
        
    quotes = get_quotes()
    ids = [q.get("id", 0) for q in quotes]
    new_id = max(ids) + 1 if ids else 1
    
    new_quote = {
        "id": new_id, 
        "quote": quote_text,
        "context": context,
        "source": source,
        "category": category
    }
    
    quotes.append(new_quote)
    save_quotes(quotes)
    
    return jsonify(new_quote), 201

@app.route('/sasuke/quote/<int:id>', methods=['DELETE'])
def delete_quote(id):
    initialize_quotes()    
    if not is_authorized():
        return jsonify({"message": "Não autorizado"}), 401
    
    quotes = get_quotes()
    filtered_quotes = [q for q in quotes if q.get("id") != id]
    
    if len(filtered_quotes) < len(quotes):
        save_quotes(filtered_quotes)
        return "", 204
    
    return jsonify({"message": "Citação não encontrada"}), 404

@app.route('/sasuke/quote/<int:id>', methods=['PUT'])
def update_quote(id):
    initialize_quotes()    
    if not is_authorized():
        return jsonify({"message": "Não autorizado"}), 401
        
    data = request.get_json()
    if not data or not data.get('quote'):
        return jsonify({"message": "Texto da citação é obrigatório"}), 400
    
    quote_text = data.get('quote')
    if len(quote_text) > 500:
        return jsonify({"message": "Citação não pode exceder 500 caracteres"}), 400
    
    quotes = get_quotes()
    for quote in quotes:
        if quote.get("id") == id:
            quote["quote"] = quote_text
            quote["context"] = data.get('context', quote.get('context', 'Desconhecido'))
            quote["source"] = data.get('source', quote.get('source', 'Desconhecido'))
            quote["category"] = data.get('category', quote.get('category', 'Outros'))
            
            save_quotes(quotes)
            return jsonify(quote)
    
    return jsonify({"message": "Citação não encontrada"}), 404

app.debug = False

from flask import request

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    return jsonify({"error": "Rota não encontrada"}), 404

from http.server import HTTPServer, BaseHTTPRequestHandler
from werkzeug.serving import make_server
import sys

app.initialize = initialize_quotes

def handler(event, context):
    return app(event, context)