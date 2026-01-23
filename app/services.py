import asyncio
import random
from typing import Dict, List
from app.schemas import ChamadoInput
from app.integrations import enviar_para_laravel, enviar_mensagem_whatsapp

# --- Dicionário de Mensagens ---
TEXTOS = {
    "saudacoes": [
        "Olá! 👋 Seja bem-vindo ao atendimento da *Simplesmente*. Como posso ajudar?",
        "Oi! Tudo bem? 😊 Sou o assistente da *Simplesmente*. No que posso ser útil hoje?",
        "Bem-vindo! 🚀 Você está no canal de suporte e serviços da *Simplesmente*."
    ],
    "menu_principal": (
        "Escolha uma das opções abaixo:\n\n"
        "1️⃣ *Abrir Chamado Técnico* (Suporte)\n"
        "2️⃣ *Conhecer Nossos Serviços* (Portfólio)\n"
        "3️⃣ *Falar com um Consultor*"
    ),
    "modelo_chamado": (
        "🛠️ *Abertura de Chamado*\n\n"
        "Para que nossa equipe técnica possa te ajudar, copie, preencha e envie a mensagem abaixo:\n\n"
        "----------------------------\n"
        "*NOME:* \n"
        "*TELEFONE:* \n"
        "*E-MAIL:* \n"
        "*MOTIVO:* (Suporte técnico / Dúvida / Instalação)\n"
        "*DESCRIÇÃO:* \n"
        "----------------------------"
    ),
    "servicos_detalhados": (
        "💡 *Nossas Soluções na Simplesmente:*\n\n"
        "💻 *Infraestrutura de TI:* Gestão de servidores, backup em nuvem e suporte remoto.\n\n"
        "🛡️ *Segurança Eletrônica:* Instalação de câmeras (CFTV), alarmes e controle de acesso.\n\n"
        "🌐 *Redes & Conectividade:* Configuração de Wi-Fi corporativo, cabeamento estruturado e fibra óptica.\n\n"
        "Caso queira um orçamento específico, escolha a opção *1* para detalhar sua necessidade no formulário."
    )
}

class MessageBufferManager:
    """Gerencia o agrupamento de mensagens (Debounce)."""
    def __init__(self):
        self.buffers: Dict[str, List[str]] = {}
        self.tasks: Dict[str, asyncio.Task] = {}

    async def adicionar_e_processar(self, dados: ChamadoInput):
        telefone = dados.telefone
        if not telefone: return

        # Acumula a mensagem no buffer do usuário
        if telefone not in self.buffers:
            self.buffers[telefone] = []
        if dados.mensagem:
            self.buffers[telefone].append(dados.mensagem)

        # Se já existir uma tarefa de espera, cancela para reiniciar o tempo
        if telefone in self.tasks:
            self.tasks[telefone].cancel()

        # Cria uma nova tarefa que aguarda 3 segundos de silêncio
        self.tasks[telefone] = asyncio.create_task(self._executar_apos_espera(telefone, dados))

    async def _executar_apos_espera(self, telefone: str, dados_originais: ChamadoInput):
        try:
            await asyncio.sleep(3.0) # Tempo de espera por novas mensagens
            
            # Une as mensagens acumuladas e limpa o buffer
            conversa_completa = " ".join(self.buffers.get(telefone, []))
            self.buffers.pop(telefone, None)
            self.tasks.pop(telefone, None)

            # Atualiza os dados para o processamento final
            dados_originais.mensagem = conversa_completa
            
            # Gera a resposta com base na sua lógica de diálogos
            resposta_texto = await obter_resposta_suporte(dados_originais)
            
            # Envia via API (Evolution) de forma assíncrona
            await enviar_mensagem_whatsapp(telefone, resposta_texto)
            
        except asyncio.CancelledError:
            pass # Ignora cancelamentos por novas mensagens

# Instância global para ser usada no main.py
buffer_manager = MessageBufferManager()

async def obter_resposta_suporte(dados: ChamadoInput) -> str:
    """Orquestra os diálogos do bot Simplesmente."""
    
    if dados.is_formulario:
        sucesso = await enviar_para_laravel(dados)
        if sucesso:
            return (
                f"✅ *Chamado Registrado!* \n\n"
                f"Obrigado, {dados.nome}. Seus dados foram enviados para o nosso sistema.\n"
                "🚀 Em breve, um técnico entrará em contato pelo seu telefone ou e-mail."
            )
        else:
            return "⚠️ *Erro de Conexão:* Não consegui salvar seu chamado no sistema."

    mensagem = (dados.mensagem or "").lower().strip()

    if any(s in mensagem for s in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "inicio", "voltar"]):
        saudacao = random.choice(TEXTOS["saudacoes"])
        return f"{saudacao}\n\n{TEXTOS['menu_principal']}"

    if any(s in mensagem for s in ["1", "suporte", "chamado", "tecnico", "técnico"]):
        return TEXTOS["modelo_chamado"]

    if any(s in mensagem for s in ["2", "serviço", "serviços", "portfolio", "portfólio"]):
        return f"{TEXTOS['servicos_detalhados']}\n\nPara voltar ao menu, digite *Início*."

    if any(s in mensagem for s in ["3", "consultor", "humano", "falar", "atendente"]):
        return "Entendido! 👨‍💻 Vou te transferir para um de nossos consultores."

    return "Ainda não entendi muito bem... 🤔\n\nEscolha uma das opções: 1️⃣ Suporte, 2️⃣ Serviços ou 3️⃣ Consultor."