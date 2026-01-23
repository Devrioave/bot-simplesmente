# app/main.py
from fastapi import FastAPI, BackgroundTasks
from app.schemas import ChamadoInput
from app.services import buffer_manager # Importa o gestor de buffer configurado no services.py

# Inicialização da aplicação com o título da empresa
app = FastAPI(title="Bot Simplesmente")

@app.post("/webhook")
async def processar_mensagem(input_data: ChamadoInput, background_tasks: BackgroundTasks):
    """
    Endpoint principal que recebe as requisições do n8n.
    Agora utiliza um sistema de buffer (debounce) para evitar múltiplas respostas seguidas.
    """
    
    # Verificamos se a entrada é um formulário estruturado ou uma mensagem comum
    if input_data.is_formulario:
        # Para formulários (abertura de chamado), processamos via background task 
        # para garantir que o sistema Laravel responda sem travar o WhatsApp.
        background_tasks.add_task(buffer_manager.adicionar_e_processar, input_data)
    else:
        # Para mensagens de chat, enviamos para o buffer que aguardará 
        # 3 segundos de silêncio do utilizador antes de processar.
        await buffer_manager.adicionar_e_processar(input_data)
    
    # Retorna um status de sucesso imediato. 
    # A resposta real com o texto do bot será enviada depois via API externa.
    return {"status": "recebido", "modo": "buffer_ativado"}