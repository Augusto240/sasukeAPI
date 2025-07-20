from http.server import BaseHTTPRequestHandler
import json
import random

# Adicione IDs aos quotes se ainda não tiver
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
    # ... outros quotes ...
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/quote':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            quote = random.choice(quotes)
            self.wfile.write(json.dumps(quote).encode())
            return
            
        elif self.path == '/api/quotes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({"quotes": quotes}).encode())
            return
            
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API de Citações do Sasuke</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f8f9fa;
        }
        h1 { 
            color: #2c3e50; 
            text-align: center;
            margin-bottom: 30px;
        }
        .quote-box { 
            background: #fff; 
            border-left: 4px solid #3498db; 
            padding: 20px; 
            margin: 20px 0; 
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-style: italic;
            font-size: 1.2rem;
        }
        button { 
            background: #3498db; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            cursor: pointer; 
            display: block; 
            margin: 20px auto;
            border-radius: 4px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        .endpoint { 
            background: #fff; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .endpoint h3 {
            margin-top: 0;
            color: #3498db;
        }
        footer {
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-size: 0.9rem;
        }
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
        <p>Obter uma citação aleatória do Sasuke</p>
    </div>
    <div class="endpoint">
        <h3>GET /api/quotes</h3>
        <p>Obter todas as citações disponíveis</p>
    </div>
    
    <footer>
        API de Citações do Sasuke &copy; 2025 | Criado por <a href="https://github.com/Augusto240">Augusto240</a>
    </footer>
    
    <script>
        document.getElementById('get-quote').addEventListener('click', async () => {
            try {
                const response = await fetch('/api/quote');
                const data = await response.json();
                document.getElementById('quote-display').textContent = data.quote;
            } catch (error) {
                console.error('Erro:', error);
                document.getElementById('quote-display').textContent = 'Erro ao buscar citação. Tente novamente.';
            }
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