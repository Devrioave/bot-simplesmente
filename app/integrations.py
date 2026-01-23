import os
import httpx
from dotenv import load_dotenv
from app.schemas import ChamadoInput

# Carrega as variáveis do .env
load_dotenv()

# Credenciais para a API Laravel (Cadastro de Chamados)
LARAVEL_API_URL = os.getenv("LARAVEL_API_URL")
LARAVEL_TOKEN = os.getenv("LARAVEL_API_TOKEN")

# Credenciais para a Evolution API (Envio de Respostas)
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")

async def enviar_para_laravel(dados: ChamadoInput) -> bool:
    """Envia os dados do formulário validado para a API Laravel da Simplesmente."""
    if not LARAVEL_API_URL or not LARAVEL_TOKEN:
        print("⚠️ Erro: Credenciais do Laravel não configuradas no .env")
        return False

    payload = {
        "solicitante_nome": dados.nome,
        "solicitante_telefone": dados.telefone,
        "solicitante_email": dados.email,
        "categoria": dados.motivo,
        "descricao": dados.descricao,
        "origem": "WhatsApp Bot"
    }
    
    headers = {
        "Authorization": f"Bearer {LARAVEL_TOKEN}",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LARAVEL_API_URL, json=payload, headers=headers)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Erro na integração com Laravel: {e}")
            return False

async def enviar_mensagem_whatsapp(telefone: str, texto: str) -> bool:
    """Envia a resposta final processada de volta para o WhatsApp."""
    if not EVOLUTION_API_URL or not EVOLUTION_API_KEY:
        print("⚠️ Erro: Credenciais da Evolution API não configuradas.")
        return False

    payload = {
        "number": telefone,
        "options": {"delay": 1200, "presence": "composing"},
        "textMessage": {"text": texto}
    }
    
    headers = {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        try:
            # Certifique-se que a URL termina em /message/sendText/NOME_DA_INSTANCIA
            response = await client.post(EVOLUTION_API_URL, json=payload, headers=headers)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Erro ao enviar para WhatsApp: {e}")
            return False