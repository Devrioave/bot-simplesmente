import os
import httpx
import re # Adicionado para limpeza de string
from dotenv import load_dotenv
from app.schemas import ChamadoInput

load_dotenv()

# Credenciais do Laravel
LARAVEL_API_URL = os.getenv("LARAVEL_API_URL")
LARAVEL_TOKEN = os.getenv("LARAVEL_API_TOKEN")

# Credenciais da Evolution API
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")

async def enviar_para_laravel(dados: ChamadoInput) -> bool:
    """Envia apenas os dígitos do telefone para o Laravel para evitar erro de tamanho (max string)."""
    if not LARAVEL_API_URL or not LARAVEL_TOKEN:
        print("⚠️ [ERRO] Credenciais do Laravel não configuradas no .env")
        return False

    # CORREÇÃO: Remove o '@s.whatsapp.net' e mantém apenas os números para o Laravel
    telefone_apenas_numeros = "".join(filter(str.isdigit, str(dados.telefone)))

    payload = {
        "solicitante_nome": dados.nome,
        "solicitante_telefone": telefone_apenas_numeros, # Envia ex: 558184724599
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
            print(f"📡 [LARAVEL] Enviando telefone limpo: {telefone_apenas_numeros}")
            response = await client.post(LARAVEL_API_URL, json=payload, headers=headers)
            
            if response.status_code not in [200, 201]:
                # Log detalhado do erro de validação do Laravel
                print(f"❌ [LARAVEL] Erro {response.status_code}: {response.text}")
                return False
            
            print("✅ [LARAVEL] Chamado registado com sucesso!")
            return True
        except Exception as e:
            print(f"💥 [LARAVEL] Falha crítica: {e}")
            return False

async def enviar_mensagem_whatsapp(telefone: str, texto: str) -> bool:
    """Envia a resposta usando o JID completo para o WhatsApp."""
    if not EVOLUTION_API_URL or not EVOLUTION_API_KEY:
        print("⚠️ [ERRO] Credenciais da Evolution API ausentes.")
        return False

    target = str(telefone).strip()
    
    # Se o JID não estiver completo, formata (caso venha do buffer comum)
    if "@" not in target:
        target = "".join(filter(str.isdigit, target))
        if not target.startswith("55"): target = "55" + target
        target = f"{target}@s.whatsapp.net"

    payload = {
        "number": target,
        "text": texto,
        "options": {"delay": 1200, "presence": "composing"}
    }
    
    headers = {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(EVOLUTION_API_URL, json=payload, headers=headers)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"💥 [WHATSAPP] Erro: {e}")
            return False