# app/main.py
from fastapi import FastAPI
from app.schemas import ChamadoInput # Importa o contrato de dados estruturado
from app.services import obter_resposta_suporte # Importa a lógica de diálogos

# Inicialização da aplicação com o título da empresa
app = FastAPI(title="Bot Simplesmente")

@app.post("/webhook")
async def processar_mensagem(input_data: ChamadoInput):
    """
    Endpoint principal que recebe as requisições do n8n.
    Processa saudações, triagem de serviços e abertura de chamados.
    """
    
    # É fundamental usar o 'await' aqui, pois o serviço agora realiza 
    # uma chamada externa para a API do Laravel.
    resposta_texto = await obter_resposta_suporte(input_data)
    
    # Retorna o JSON que será lido pela Evolution API através do n8n
    return {"resposta": resposta_texto}