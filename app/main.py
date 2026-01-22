# app/main.py
from fastapi import FastAPI
from app.schemas import ChamadoInput # Importa o novo esquema
from app.services import obter_resposta_suporte # Ou a função que criou

app = FastAPI(title="Bot Simplesmente")

@app.post("/webhook")
async def processar_mensagem(input_data: ChamadoInput):
    # Agora o 'input_data' tem todos os campos (nome, email, etc.)
    # Pode passar o objeto inteiro para o serviço processar
    resposta = obter_resposta_suporte(input_data)
    return {"resposta": resposta}