from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Bot Simplesmente")

# 1. Definição do contrato de entrada (JSON recebido do n8n)
class MensagemInput(BaseModel):
    mensagem: str  # Chave que contém o texto do cliente

@app.post("/webhook")
async def processar_mensagem(input_data: MensagemInput):
    # O FastAPI valida automaticamente se a chave "mensagem" existe
    texto_cliente = input_data.mensagem
    
    # 2. Definição da lógica de resposta de suporte
    resposta_suporte = (
        "Olá! Bem-vindo ao suporte da Simplesmente. 🛠️\n\n"
        "Para abrir seu chamado, por favor preencha os dados abaixo:\n\n"
        "*Nome:* \n"
        "*E-mail:* \n"
        "*Motivo:* (Suporte / Dúvida / Solicitação)\n"
        "*Descrição:* "
    )
    
    # 3. Retorno do JSON com a chave "resposta" conforme solicitado
    return {"resposta": resposta_suporte}