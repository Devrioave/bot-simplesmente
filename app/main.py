from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Evolution API Handler")

# Definindo o esquema do que a Evolution API costuma enviar
# Você pode expandir isso conforme a documentação da Evolution
class EvolutionWebhook(BaseModel):
    event: str
    instance: str
    data: dict  # Aqui virão os detalhes da mensagem

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API está rodando!"}

@app.post("/webhook")
async def receive_webhook(payload: EvolutionWebhook):
    # Por enquanto, apenas printamos para validar o recebimento
    print(f"Evento recebido: {payload.event}")
    print(f"Dados da mensagem: {payload.data}")
    
    # Aqui retornaremos a resposta que o n8n vai processar
    return {
        "status": "success",
        "message": "Webhook processado pelo FastAPI",
        "original_event": payload.event
    }