import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv  # <- ADICIONADO

# --- Configuração ---
load_dotenv()  # <- ADICIONADO: Carrega as variáveis do arquivo .env
app = Flask(__name__)
CORS(app)

# --- Conexão com o Banco de Dados ---
# Agora, ele lê a MONGO_URI diretamente do .env que acabou de ser carregado
mongo_uri = os.environ.get("MONGO_URI")
db_name = "global_solution_db"
collection_name = "cartoes_validos"

# Verifica se a MONGO_URI foi carregada
try:
    mongo_uri = os.environ.get("MONGO_URI") 
    
    if not mongo_uri:
        print("Erro: Variavel MONGO_URI nao encontrada. Verifique seu .env")
        collection = None
    else:
        client = MongoClient(mongo_uri)
        
        # ----- CORREÇÃO AQUI -----
        db = client['Users']         # O Banco de dados é 'Users'
        collection = db['Users']     # A Coleção é 'Users'
        # -------------------------

        client.admin.command('ping')
        print("Conectado ao MongoDB com sucesso!")

except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    collection = None

# --- Rotas da API ---


@app.route('/')
def index():
    """Rota inicial apenas para testar se a API está no ar."""
    return jsonify({"mensagem": "API do Totem Global Solution no ar!"})


@app.route('/api/validar', methods=['GET'])
def validar_uid():
    """
    Rota principal de validação para o totem.
    Recebe um UID via query param (ex: /api/validar?uid=E256A3B1)
    e o compara com a coleção no MongoDB.
    """

    # Se a conexão com o banco falhou na inicialização, retorna erro
    if collection is None:
        print("ERRO: Chamada de API falhou pois o banco nao esta conectado.")
        return jsonify({"erro": "Falha na conexao com o banco de dados"}), 500

    # Pega o UID enviado pelo ESP32 (ex: ?uid=E256A3B1)
    uid_recebido = request.args.get('uid')

    if not uid_recebido:
        print("Requisicao recebida sem o parametro 'uid'")
        return jsonify({"status": "negado", "erro": "Nenhum UID fornecido"}), 400

    print(f"\nRecebida consulta para UID: [{uid_recebido}]")

    try:
        # Busca o UID no banco de dados.
        # find_one() retorna o documento se achar, ou None se não achar.
        cartao = collection.find_one({"uid": uid_recebido})

        if cartao:
            # SUCESSO! Cartão encontrado.
            # Pega o nome, ou "Usuario" se não tiver
            proprietario = cartao.get("proprietario", "Usuario")
            proprietario = cartao.get("proprietario", "Usuario")
            print(
                f"Resultado: Cartao ENCONTRADO. Proprietario: {proprietario}")

            return jsonify({
                "status": "ok",
                "mensagem": "Acesso Liberado",
                "proprietario": proprietario
            }), 200  # HTTP 200 OK
        else:
            # FALHA! Cartão não encontrado no banco.
            print("Resultado: Cartao NAO ENCONTRADO.")
            return jsonify({
                "status": "negado",
                "mensagem": "Acesso Nao Autorizado"
            }), 404  # HTTP 404 Not Found (Não encontrado)

    except Exception as e:
        print(f"ERRO durante a busca no banco: {e}")
        return jsonify({"erro": "Erro interno do servidor ao consultar o banco"}), 500

# --- Inicialização ---


if __name__ == '__main__':
    # Roda o app na porta 5000, acessível por qualquer IP (host='0.0.0.0')
    # Isso é necessário para o Ngrok conseguir acessar sua API.
    print("Iniciando servidor Flask na porta 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
