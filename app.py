from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import requests
import time
import threading

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)  # Enable CORS for frontend communication

# Database of authorized IDs
ids_autorizados = {
    "12345": {"nome": "João Silva", "departamento": "TI"},
    "67890": {"nome": "Maria Santos", "departamento": "RH"},
    "11111": {"nome": "Pedro Costa", "departamento": "Financeiro"},
    "22222": {"nome": "Ana Oliveira", "departamento": "Marketing"},
    "99999": {"nome": "Admin", "departamento": "Administração"}
}

# Access history
historico_acessos = []

# Last access (for interface display)
ultimo_acesso = {
    "id": "",
    "status": "",
    "nome": "",
    "departamento": "",
    "timestamp": ""
}

# FIWARE Configuration
FIWARE_URL = "http://130.131.19.158:1026/v2/entities/TesteESP32"
ultimo_id_verificado = None
monitoramento_ativo = True

def monitorar_fiware():
    """Monitor FIWARE constantly for new IDs"""
    global ultimo_id_verificado, ultimo_acesso
    
    print("\n🔍 Monitoramento do FIWARE iniciado...")
    
    while monitoramento_ativo:
        try:
            response = requests.get(FIWARE_URL, timeout=5)
            
            if response.status_code == 200:
                dados = response.json()
                
                if 'idRecebido' in dados:
                    id_recebido = dados['idRecebido']['value']
                    
                    if id_recebido and id_recebido != ultimo_id_verificado:
                        ultimo_id_verificado = id_recebido
                        processar_id(id_recebido)
                        
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erro ao conectar com FIWARE: {e}")
        except Exception as e:
            print(f"❌ Erro no monitoramento: {e}")
        
        time.sleep(2)

def processar_id(id_recebido):
    """Process ID received from FIWARE"""
    global ultimo_acesso
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if id_recebido in ids_autorizados:
        usuario = ids_autorizados[id_recebido]
        
        print(f"\n{'='*50}")
        print(f"✅ ACESSO LIBERADO - {timestamp}")
        print(f"ID: {id_recebido}")
        print(f"Nome: {usuario['nome']}")
        print(f"Departamento: {usuario['departamento']}")
        print(f"{'='*50}\n")
        
        historico_acessos.append({
            "timestamp": timestamp,
            "id": id_recebido,
            "nome": usuario['nome'],
            "status": "LIBERADO"
        })
        
        ultimo_acesso = {
            "id": id_recebido,
            "status": "LIBERADO",
            "nome": usuario['nome'],
            "departamento": usuario['departamento'],
            "timestamp": timestamp
        }
        
        atualizar_fiware_resposta("LIBERADO", usuario['nome'], usuario['departamento'])
        
    else:
        print(f"\n{'='*50}")
        print(f"❌ ACESSO NEGADO - {timestamp}")
        print(f"ID: {id_recebido}")
        print(f"Motivo: ID não autorizado")
        print(f"{'='*50}\n")
        
        historico_acessos.append({
            "timestamp": timestamp,
            "id": id_recebido,
            "nome": "Desconhecido",
            "status": "NEGADO"
        })
        
        ultimo_acesso = {
            "id": id_recebido,
            "status": "NEGADO",
            "nome": "Desconhecido",
            "departamento": "N/A",
            "timestamp": timestamp
        }
        
        atualizar_fiware_resposta("NEGADO", "Desconhecido", "N/A")

def atualizar_fiware_resposta(status, nome, departamento):
    """Send response back to FIWARE"""
    try:
        url = f"{FIWARE_URL}/attrs"
        
        payload = {
            "statusAcesso": {"type": "Text", "value": status},
            "nomeUsuario": {"type": "Text", "value": nome},
            "departamento": {"type": "Text", "value": departamento}
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.patch(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code in [200, 204]:
            print(f"✅ Resposta enviada ao FIWARE: {status}")
            
    except Exception as e:
        print(f"❌ Erro ao enviar resposta ao FIWARE: {e}")

# API Routes
@app.route('/')
def home():
    """Serve the main HTML page"""
    return send_from_directory('public', 'index.html')

@app.route('/api/ultimo_acesso')
def api_ultimo_acesso():
    """Get last access information"""
    return jsonify(ultimo_acesso)

@app.route('/api/historico_recente')
def api_historico_recente():
    """Get recent access history"""
    return jsonify({
        "historico": list(reversed(historico_acessos[-10:]))
    })

@app.route('/api/estatisticas')
def api_estatisticas():
    """Get access statistics"""
    liberados = sum(1 for h in historico_acessos if h['status'] == 'LIBERADO')
    negados = sum(1 for h in historico_acessos if h['status'] == 'NEGADO')
    
    return jsonify({
        "total": len(historico_acessos),
        "liberados": liberados,
        "negados": negados
    })

@app.route('/listar_autorizados', methods=['GET'])
def listar_autorizados():
    """List all authorized IDs"""
    return jsonify({
        "total": len(ids_autorizados),
        "ids_autorizados": ids_autorizados
    }), 200

@app.route('/historico', methods=['GET'])
def historico():
    """Get complete access history"""
    return jsonify({
        "total_tentativas": len(historico_acessos),
        "historico": historico_acessos
    }), 200

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 INSIGHT JOBS - API DE CONTROLE DE ACESSO")
    print("="*60)
    print(f"\n📡 Monitorando FIWARE em: {FIWARE_URL}")
    print(f"🌐 Interface web em: http://localhost:5000")
    print(f"\n📋 IDs Autorizados no sistema: {len(ids_autorizados)}")
    for id_key, usuario in ids_autorizados.items():
        print(f"   • ID {id_key}: {usuario['nome']} ({usuario['departamento']})")
    print("\n" + "="*60 + "\n")
    
    # Start FIWARE monitoring thread
    thread_monitor = threading.Thread(target=monitorar_fiware, daemon=True)
    thread_monitor.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)
