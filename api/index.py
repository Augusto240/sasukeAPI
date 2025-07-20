from http.server import BaseHTTPRequestHandler
import json
import random
import re
from urllib.parse import parse_qs, urlparse

# Lista completa de citações do Sasuke com IDs
quotes = [
    {
        "id": 1,
        "quote": "Eu vou restaurar meu clã e destruir um certo alguém.",
        "context": "Ao se apresentar para o Time 7",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 2,
        "quote": "Meu nome é Sasuke Uchiha. Eu odeio muitas coisas, e não gosto de nada em particular.",
        "context": "Durante a apresentação do Time 7",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 3,
        "quote": "Eu tenho um irmão... que eu preciso matar!",
        "context": "Sobre sua ambição de vingança",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 4,
        "quote": "Eu há muito tempo fechei meus olhos... Meu único objetivo está na escuridão.",
        "context": "Ao deixar a Vila da Folha",
        "source": "Episódio 109 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 5,
        "quote": "Meu sonho não é apenas um sonho, mas uma realidade que eu farei acontecer.",
        "context": "Sobre sua vingança contra Itachi",
        "source": "Episódio 107 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 6,
        "quote": "Eu poupei sua vida por capricho, nada mais.",
        "context": "Para Naruto após sua primeira luta séria",
        "source": "Episódio 35 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 7,
        "quote": "Você ainda é muito fraco. Você não tem ódio suficiente.",
        "context": "Repetindo as palavras de Itachi",
        "source": "Episódio 131 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 8,
        "quote": "Eu cheguei a entender que a vingança é o caminho certo para mim.",
        "context": "Conversando com Kakashi",
        "source": "Episódio 108 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 9,
        "quote": "Poder não é vontade, é a capacidade de fazer as coisas acontecerem fisicamente.",
        "context": "Durante treinamento com Orochimaru",
        "source": "Episódio 34 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "id": 10,
        "quote": "Quando um homem aprende a amar, ele deve suportar o risco do ódio.",
        "context": "Reflexão após descobrir a verdade sobre Itachi",
        "source": "Episódio 142 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "id": 11,
        "quote": "Eu me recuso a seguir os passos de qualquer pessoa.",
        "context": "Ao formar o Time Hebi",
        "source": "Episódio 118 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "id": 12,
        "quote": "O que eu tenho não é um sonho, porque eu vou torná-lo realidade.",
        "context": "Declarando sua ambição",
        "source": "Episódio 3 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 13,
        "quote": "Se quiser me ridicularizar como um moleque influenciado por suas emoções, vá em frente.",
        "context": "Ao declarar guerra contra Konoha",
        "source": "Episódio 212 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "id": 14,
        "quote": "Eu não tenho sonhos para o futuro... apenas o passado. É tudo que existe dentro de mim.",
        "context": "Quando confrontado por Gaara",
        "source": "Episódio 83 (Naruto Clássico)",
        "category": "Genin"
    },
    {
        "id": 15,
        "quote": "Desculpe Sasuke... não haverá próxima vez.",
        "context": "Palavras de Itachi que atormentaram Sasuke",
        "source": "Episódio 84 (Naruto Clássico)",
        "category": "Flashback"
    },
    {
        "id": 16,
        "quote": "A única coisa que eu tenho certeza é que nada é certo.",
        "context": "Após descobrir a verdade sobre o massacre do clã",
        "source": "Episódio 143 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "id": 17,
        "quote": "O que eu vejo agora é apenas escuridão.",
        "context": "Após ser consumido pelo ódio",
        "source": "Episódio 216 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "id": 18,
        "quote": "Eu sou um vingador!",
        "context": "Sua frase mais emblemática",
        "source": "Vários episódios",
        "category": "Genin"
    },
    {
        "id": 19,
        "quote": "Esses olhos podem ver através da escuridão.",
        "context": "Sobre o poder do Sharingan",
        "source": "Episódio 129 (Naruto Shippuden)",
        "category": "Shippuden"
    },
    {
        "id": 20,
        "quote": "Eu vou acabar com essa maldição. Se alguém tiver que suportar o ódio dos Uchiha, eu prefiro que seja eu.",
        "context": "Sobre o legado dos Uchiha",
        "source": "Episódio 386 (Naruto Shippuden)",
        "category": "Shippuden"
    }
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_parts = urlparse(self.path)
        path = url_parts.path
        query_params = parse_qs(url_parts.query)
        
        # API Route: Random Quote
        if path == '/api/quote':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            quote = random.choice(quotes)
            self.wfile.write(json.dumps(quote).encode())
            return
        
        # API Route: All Quotes
        elif path == '/api/quotes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({"quotes": quotes}).encode())
            return
        
        # API Route: Quote by ID
        elif re.match(r'^/api/quote/(\d+)$', path):
            quote_id = int(re.match(r'^/api/quote/(\d+)$', path).group(1))
            quote = next((q for q in quotes if q["id"] == quote_id), None)
            
            self.send_response(200 if quote else 404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if quote:
                self.wfile.write(json.dumps(quote).encode())
            else:
                self.wfile.write(json.dumps({"message": "Citação não encontrada"}).encode())
            return
        
        # API Route: Search Quotes
        elif path == '/api/search':
            term = query_params.get('q', [''])[0].lower()
            
            if not term:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Termo de busca é obrigatório"}).encode())
                return
            
            results = [q for q in quotes if term in q["quote"].lower()]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"quotes": results}).encode())
            return
        
        # API Route: Quotes by Category
        elif re.match(r'^/api/quotes/category/([^/]+)$', path):
            category = re.match(r'^/api/quotes/category/([^/]+)$', path).group(1).lower()
            results = [q for q in quotes if q.get("category", "").lower() == category]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"quotes": results}).encode())
            return
        
        # API Route: All Categories
        elif path == '/api/categories':
            categories = list(set(q.get("category", "") for q in quotes if "category" in q))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"categories": categories}).encode())
            return
            
        # Home Page
        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API de Citações do Sasuke</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        :root {
            --primary-light: #3b55ce;
            --secondary-light: #4b6fe6;
            --background-light: #f7f9ff;
            --text-light: #333;
            --accent-light: #ff5757;
            --card-light: #fff;
            --border-light: #e1e5f2;
            
            --primary-dark: #161d3c;
            --secondary-dark: #252f69;
            --background-dark: #0a0e1f;
            --text-dark: #e1e5f2;
            --accent-dark: #ff304f;
            --card-dark: #1a2045;
            --border-dark: #252f69;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: background-color 0.3s, color 0.3s;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background-size: cover;
            background-attachment: fixed;
            position: relative;
        }

        body.light-mode {
            color: var(--text-light);
            background-color: var(--background-light);
            background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        body.dark-mode {
            color: var(--text-dark);
            background-color: var(--background-dark);
            background-image: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.5);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        header {
            text-align: center;
            padding: 30px 20px;
            margin-bottom: 30px;
        }

        .logo {
            max-width: 200px;
            margin: 0 auto 20px;
        }

        .logo img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .light-mode header h1 {
            color: var(--primary-light);
        }

        .dark-mode header h1 {
            color: var(--accent-dark);
        }

        header p {
            font-size: 1.2rem;
            opacity: 0.8;
        }

        .quote-section {
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .light-mode .quote-section {
            background-color: var(--card-light);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        .dark-mode .quote-section {
            background-color: var(--card-dark);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }

        .quote-container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }

        .sharingan-icon {
            margin-bottom: 15px;
        }

        .sharingan-icon img {
            width: 60px;
            height: 60px;
            transition: transform 0.3s ease;
        }

        .sharingan-icon img.spin {
            animation: spin 1s ease-in-out;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .quote-box {
            padding: 20px;
            border-radius: 8px;
            min-height: 120px;
            width: 100%;
            position: relative;
            transition: all 0.3s ease;
        }

        .light-mode .quote-box {
            background-color: #f7f9ff;
            border-left: 4px solid var(--primary-light);
        }

        .dark-mode .quote-box {
            background-color: #131936;
            border-left: 4px solid var(--accent-dark);
        }

        #quote-text {
            font-size: 1.5rem;
            font-style: italic;
            margin-bottom: 15px;
            transition: opacity 0.3s ease;
        }

        .quote-details {
            font-size: 0.9rem;
            opacity: 0.8;
            text-align: right;
            margin-top: 15px;
        }

        .quote-details p {
            margin: 5px 0;
        }

        .btn {
            border: none;
            padding: 12px 25px;
            font-size: 1rem;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin: 15px 0;
        }

        .light-mode .btn {
            background-color: var(--primary-light);
            color: white;
            box-shadow: 0 4px 15px rgba(59, 85, 206, 0.4);
        }

        .dark-mode .btn {
            background-color: var(--accent-dark);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 48, 79, 0.3);
        }

        .light-mode .btn:hover {
            background-color: #2a42b0;
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(59, 85, 206, 0.5);
        }

        .dark-mode .btn:hover {
            background-color: #e31b3a;
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(255, 48, 79, 0.4);
        }

        .btn i {
            margin-right: 8px;
        }

        .category-filters {
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid;
        }

        .light-mode .category-filters {
            border-color: var(--border-light);
        }

        .dark-mode .category-filters {
            border-color: var(--border-dark);
        }

        .category-filters h3 {
            margin-bottom: 15px;
            font-size: 1.1rem;
        }

        .filter-buttons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
        }

        .filter-btn {
            padding: 8px 16px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .light-mode .filter-btn {
            background-color: #e9ecf8;
            color: var(--text-light);
        }

        .dark-mode .filter-btn {
            background-color: #1e254e;
            color: var(--text-dark);
        }

        .light-mode .filter-btn:hover,
        .light-mode .filter-btn.active {
            background-color: var(--primary-light);
            color: white;
        }

        .dark-mode .filter-btn:hover,
        .dark-mode .filter-btn.active {
            background-color: var(--accent-dark);
            color: white;
        }

        .api-docs {
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 40px;
        }

        .light-mode .api-docs {
            background-color: var(--card-light);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        .dark-mode .api-docs {
            background-color: var(--card-dark);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }

        .api-docs h2 {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid;
        }

        .light-mode .api-docs h2 {
            color: var(--primary-light);
            border-color: var(--border-light);
        }

        .dark-mode .api-docs h2 {
            color: var(--accent-dark);
            border-color: var(--border-dark);
        }

        .endpoint {
            margin-bottom: 25px;
            padding: 15px;
            border-radius: 8px;
        }

        .light-mode .endpoint {
            background-color: #f7f9ff;
        }

        .dark-mode .endpoint {
            background-color: #131936;
        }

        .endpoint h3 {
            font-size: 1.2rem;
            margin-bottom: 8px;
        }

        .light-mode .endpoint h3 {
            color: var(--primary-light);
        }

        .dark-mode .endpoint h3 {
            color: var(--accent-dark);
        }

        .code-example {
            border-radius: 5px;
            padding: 15px;
            margin-top: 10px;
            overflow-x: auto;
        }

        .light-mode .code-example {
            background-color: #2d365d;
        }

        .dark-mode .code-example {
            background-color: #0c1025;
        }

        .code-example code {
            font-family: 'Courier New', Courier, monospace;
            color: #fff;
        }

        footer {
            text-align: center;
            padding: 20px;
            margin-top: 30px;
            border-top: 1px solid;
        }

        .light-mode footer {
            border-color: var(--border-light);
        }

        .dark-mode footer {
            border-color: var(--border-dark);
        }

        footer a {
            text-decoration: none;
            font-weight: bold;
        }

        .light-mode footer a {
            color: var(--primary-light);
        }

        .dark-mode footer a {
            color: var(--accent-dark);
        }

        footer a:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            header h1 {
                font-size: 2rem;
            }
            
            #quote-text {
                font-size: 1.2rem;
            }
            
            .code-example {
                padding: 10px;
            }
            
            .filter-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .filter-btn {
                width: 100%;
                max-width: 200px;
            }
        }
    </style>
</head>
<body class="light-mode">
    <div class="theme-toggle">
        <i class="fas fa-moon" id="theme-toggle-icon"></i>
    </div>
    
    <div class="container">
        <header>
            <div class="logo">
                <img src="./static/images/sasuke.png" alt="Sasuke Uchiha">
            </div>
            <h1>API de Citações do Sasuke</h1>
            <p>Explore a sabedoria e a determinação de Sasuke Uchiha</p>
        </header>
        
        <section class="quote-section">
            <div class="quote-container">
                <div class="sharingan-icon">
                    <img src="./static/images/sharingan.png" alt="Sharingan" class="spin-on-click" id="sharingan-img">
                </div>
                <div class="quote-box">
                    <p id="quote-text">Clique no botão para ver uma citação do Sasuke</p>
                    <div class="quote-details">
                        <p id="quote-context"></p>
                        <p id="quote-source"></p>
                        <p id="quote-category"></p>
                    </div>
                </div>
            </div>
            <button id="get-quote" class="btn">
                <i class="fas fa-bolt"></i> Ver Citação Aleatória
            </button>
            <div class="category-filters">
                <h3>Filtrar por época:</h3>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-category="all">Todas</button>
                    <button class="filter-btn" data-category="Genin">Genin</button>
                    <button class="filter-btn" data-category="Shippuden">Shippuden</button>
                    <button class="filter-btn" data-category="Flashback">Flashbacks</button>
                </div>
            </div>
        </section>
        
        <section class="api-docs">
            <h2>Uso da API</h2>
            <div class="endpoint">
                <h3>GET /api/quote</h3>
                <p>Obter uma citação aleatória do Sasuke</p>
                <div class="code-example">
                    <code>curl -X GET https://sasuke-api.vercel.app/api/quote</code>
                </div>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/quotes</h3>
                <p>Obter todas as citações do Sasuke</p>
                <div class="code-example">
                    <code>curl -X GET https://sasuke-api.vercel.app/api/quotes</code>
                </div>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/quote/:id</h3>
                <p>Obter uma citação específica pelo ID</p>
                <div class="code-example">
                    <code>curl -X GET https://sasuke-api.vercel.app/api/quote/1</code>
                </div>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/search?q=termo</h3>
                <p>Pesquisar citações contendo o termo</p>
                <div class="code-example">
                    <code>curl -X GET https://sasuke-api.vercel.app/api/search?q=vingança</code>
                </div>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/quotes/category/:categoria</h3>
                <p>Filtrar citações por categoria</p>
                <div class="code-example">
                    <code>curl -X GET https://sasuke-api.vercel.app/api/quotes/category/Shippuden</code>
                </div>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/categories</h3>
                <p>Listar todas as categorias disponíveis</p>
                <div class="code-example">
                    <code>curl -X GET https://sasuke-api.vercel.app/api/categories</code>
                </div>
            </div>
        </section>
        
        <footer>
            <p>API de Citações do Sasuke &copy; 2025 | Criado por <a href="https://github.com/Augusto240">Augusto240</a> | <a href="https://github.com/Augusto240/sasukeAPI">Ver no GitHub</a></p>
        </footer>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const quoteText = document.getElementById('quote-text');
            const quoteContext = document.getElementById('quote-context');
            const quoteSource = document.getElementById('quote-source');
            const quoteCategory = document.getElementById('quote-category');
            const getQuoteBtn = document.getElementById('get-quote');
            const themeToggle = document.querySelector('.theme-toggle');
            const themeIcon = document.getElementById('theme-toggle-icon');
            const sharinganImg = document.getElementById('sharingan-img');
            const filterButtons = document.querySelectorAll('.filter-btn');
            
            let currentCategory = 'all';
            let currentQuoteId = null;

            // Theme toggle
            if (localStorage.getItem('theme') === 'dark') {
                document.body.classList.replace('light-mode', 'dark-mode');
                themeIcon.classList.replace('fa-moon', 'fa-sun');
            }

            themeToggle.addEventListener('click', () => {
                if (document.body.classList.contains('light-mode')) {
                    document.body.classList.replace('light-mode', 'dark-mode');
                    themeIcon.classList.replace('fa-moon', 'fa-sun');
                    localStorage.setItem('theme', 'dark');
                } else {
                    document.body.classList.replace('dark-mode', 'light-mode');
                    themeIcon.classList.replace('fa-sun', 'fa-moon');
                    localStorage.setItem('theme', 'light');
                }
            });

            async function fetchQuote(category = 'all') {
                try {
                    let url = '/api/quote';
                    
                    if (category !== 'all') {
                        const categoryResponse = await fetch(`/api/quotes/category/${category}`);
                        if (!categoryResponse.ok) {
                            throw new Error('Falha ao buscar citações da categoria');
                        }
                        
                        const categoryData = await categoryResponse.json();
                        if (!categoryData.quotes || categoryData.quotes.length === 0) {
                            return {
                                quote: "Não há citações nesta categoria.",
                                context: "",
                                source: "",
                                category: ""
                            };
                        }
                        const randomIndex = Math.floor(Math.random() * categoryData.quotes.length);
                        return categoryData.quotes[randomIndex];
                    } else {
                        const response = await fetch(url);
                        if (!response.ok) {
                            throw new Error('Falha ao buscar citação');
                        }
                        
                        return await response.json();
                    }
                } catch (error) {
                    console.error('Erro ao buscar citação:', error);
                    return {
                        quote: "Erro ao buscar citação. Por favor, tente novamente.",
                        context: "",
                        source: "",
                        category: ""
                    };
                }
            }

            async function updateQuote() {
                quoteText.style.opacity = '0.5';
                quoteContext.textContent = '';
                quoteSource.textContent = '';
                quoteCategory.textContent = '';

                sharinganImg.classList.add('spin');

                setTimeout(async () => {
                    const quoteData = await fetchQuote(currentCategory);

                    setTimeout(() => {
                        quoteText.textContent = quoteData.quote;
                        currentQuoteId = quoteData.id;
                        
                        if (quoteData.context) {
                            quoteContext.textContent = `Contexto: ${quoteData.context}`;
                        }
                        
                        if (quoteData.source) {
                            quoteSource.textContent = `Fonte: ${quoteData.source}`;
                        }
                        
                        if (quoteData.category) {
                            quoteCategory.textContent = `Categoria: ${quoteData.category}`;
                        }
                        
                        quoteText.style.opacity = '1';
                        sharinganImg.classList.remove('spin');
                    }, 300);
                }, 700);
            }

            function setActiveCategory(category) {
                filterButtons.forEach(btn => {
                    if (btn.dataset.category === category) {
                        btn.classList.add('active');
                    } else {
                        btn.classList.remove('active');
                    }
                });
            }

            getQuoteBtn.addEventListener('click', updateQuote);

            filterButtons.forEach(btn => {
                btn.addEventListener('click', () => {
                    currentCategory = btn.dataset.category;
                    setActiveCategory(currentCategory);
                    updateQuote();
                });
            });

            // Initial quote
            updateQuote();
        });
    </script>
</body>
</html>'''
            
            self.wfile.write(html.encode('utf-8'))
            return
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint não encontrado"}).encode())
            return