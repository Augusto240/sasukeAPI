from http.server import BaseHTTPRequestHandler
import json
import random

# Citações com IDs adicionados
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
    # Continuar com todas as citações...
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/api/quote':
            quote = random.choice(quotes)
            self.wfile.write(json.dumps(quote).encode())
        elif self.path == '/api/quotes':
            self.wfile.write(json.dumps({"quotes": quotes}).encode())
        elif self.path == '/':
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
                
                <script>
                    document.getElementById('get-quote').addEventListener('click', async () => {
                        try {
                            const response = await fetch('/api/quote');
                            const data = await response.json();
                            document.getElementById('quote-display').textContent = data.quote;
                        } catch (error) {
                            console.error('Erro:', error);
                            document.getElementById('quote-display').textContent = 'Erro ao buscar citação.';
                        }
                    });
                </script>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
            return
        else:
            self.wfile.write(json.dumps({"error": "Endpoint não encontrado"}).encode())