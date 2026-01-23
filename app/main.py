# app/main.py
from fastapi import FastAPI, BackgroundTasks, Request
from app.schemas import ChamadoInput
from app.services import buffer_manager

app = FastAPI(title="Bot Simplesmente")

@app.post("/webhook")
async def processar_mensagem(request: Request, background_tasks: BackgroundTasks):
    # Log agressivo para ver o que chega no terminal
    body = await request.json()
    print(f"\n--- 📥 DADOS RECEBIDOS DO N8N ---")
    print(body)
    print(f"--------------------------------\n")
    
    # Converte o JSON para o nosso formato estruturado
    try:
        input_data = ChamadoInput(**body)
    except Exception as e:
        print(f"❌ Erro na validação dos dados: {e}")
        return {"status": "erro", "detalhe": str(e)}

    if input_data.is_formulario:
        background_tasks.add_task(buffer_manager.adicionar_e_processar, input_data)
    else:
        await buffer_manager.adicionar_e_processar(input_data)
    
    return {"status": "recebido", "modo": "buffer_ativado"}