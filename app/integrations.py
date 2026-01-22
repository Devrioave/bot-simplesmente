import os
import httpx
from dotenv import load_dotenv
from app.schemas import ChamadoInput

# Carrega as variáveis do .env
load_dotenv()

LARAVEL_API_URL = os.getenv("LARAVEL_API_URL")
LARAVEL_TOKEN = os.getenv("LARAVEL_API_TOKEN")

async def enviar_para_laravel(dados: ChamadoInput) -> bool:
    """Envia os dados do formulário validado para a API Laravel da Simplesmente."""
    if not LARAVEL_API_URL or not LARAVEL_TOKEN:
        print("⚠️ Erro: Credenciais do Laravel não configuradas no .env")
        return False

    # Mapeamento de campos: API Bot -> API Laravel
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
            # Retorna True se o Laravel responder com sucesso (200 ou 201)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Erro na integração com Laravel: {e}")
            return False