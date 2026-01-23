import asyncio
import random
from typing import Dict, List
from app.schemas import ChamadoInput
from app.integrations import enviar_para_laravel, enviar_mensagem_whatsapp


# =========================
# TEXTOS DO BOT
# =========================
TEXTOS = {
    "saudacoes": [
        "Olá! 👋 Seja bem-vindo ao atendimento da *Simplesmente*. Como posso ajudar?",
        "Oi! Tudo bem? 😊 Sou o assistente da *Simplesmente*. No que posso ser útil hoje?",
        "Bem-vindo! 🚀 Você está no canal de suporte e serviços da *Simplesmente*."
    ],

    "agradecimentos": [
        "Nós que agradecemos! 😊 Se precisar de algo mais, é só me chamar.",
        "Disponha! 🙌 Estou aqui sempre que precisar.",
        "Fico feliz em ajudar! 💙 Quer voltar ao menu ou falar com um consultor?",
        "Por nada! 🚀 Se quiser, posso te ajudar com mais alguma coisa."
    ],

    "despedidas": [
        "Até mais! 👋 Obrigado por entrar em contato com a *Simplesmente*.",
        "Foi um prazer te atender 😊 Qualquer coisa, é só chamar.",
        "Encerrando por aqui. Desejamos um ótimo dia! 🌟"
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


# =========================
# PALAVRAS-CHAVE (INTENTS)
# =========================
PALAVRAS_SAUDACAO = [
    "oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "inicio", "voltar"
]

PALAVRAS_AGRADECIMENTO = [
    "obrigado", "obrigada", "valeu", "obg", "obgd", "agradeço", "agradecido"
]

PALAVRAS_DESPEDIDA = [
    "tchau", "até mais", "ate mais", "até logo", "encerrar", "finalizar"
]

PALAVRAS_SUPORTE = [
    "1", "suporte", "chamado", "tecnico", "técnico"
]

PALAVRAS_SERVICOS = [
    "2", "serviço", "serviços", "portfolio", "portfólio"
]

PALAVRAS_CONSULTOR = [
    "3", "consultor", "humano", "atendente", "falar"
]


# =========================
# GERENCIADOR DE BUFFER
# =========================
class MessageBufferManager:
    """Gerencia o agrupamento de mensagens (debounce)."""

    def __init__(self):
        self.buffers: Dict[str, List[str]] = {}
        self.tasks: Dict[str, asyncio.Task] = {}

    async def adicionar_e_processar(self, dados: ChamadoInput):
        telefone = dados.telefone
        if not telefone:
            return

        if telefone not in self.buffers:
            self.buffers[telefone] = []

        if dados.mensagem:
            self.buffers[telefone].append(dados.mensagem)

        if telefone in self.tasks:
            self.tasks[telefone].cancel()

        self.tasks[telefone] = asyncio.create_task(
            self._executar_apos_espera(telefone, dados)
        )

    async def _executar_apos_espera(self, telefone: str, dados_originais: ChamadoInput):
        try:
            await asyncio.sleep(3.0)

            conversa_completa = " ".join(self.buffers.get(telefone, []))
            self.buffers.pop(telefone, None)
            self.tasks.pop(telefone, None)

            dados_originais.mensagem = conversa_completa

            resposta_texto = await obter_resposta_suporte(dados_originais)
            await enviar_mensagem_whatsapp(telefone, resposta_texto)

        except asyncio.CancelledError:
            pass


buffer_manager = MessageBufferManager()


# =========================
# ORQUESTRADOR DO BOT
# =========================
async def obter_resposta_suporte(dados: ChamadoInput) -> str:
    """Controla os diálogos do bot Simplesmente."""

    # --- FORMULÁRIO ---
    if dados.is_formulario:
        sucesso = await enviar_para_laravel(dados)
        if sucesso:
            return (
                f"✅ *Chamado Registrado!*\n\n"
                f"Obrigado, {dados.nome}. Seus dados foram enviados com sucesso.\n"
                "🚀 Em breve, um técnico entrará em contato."
            )
        return "⚠️ *Erro:* Não consegui registrar seu chamado agora. Tente novamente."

    mensagem = (dados.mensagem or "").lower().strip()

    # --- SAUDAÇÃO ---
    if any(p in mensagem for p in PALAVRAS_SAUDACAO):
        return f"{random.choice(TEXTOS['saudacoes'])}\n\n{TEXTOS['menu_principal']}"

    # --- AGRADECIMENTO ---
    if any(p in mensagem for p in PALAVRAS_AGRADECIMENTO):
        return f"{random.choice(TEXTOS['agradecimentos'])}\n\n{TEXTOS['menu_principal']}"

    # --- DESPEDIDA ---
    if any(p in mensagem for p in PALAVRAS_DESPEDIDA):
        return random.choice(TEXTOS["despedidas"])

    # --- SUPORTE ---
    if any(p in mensagem for p in PALAVRAS_SUPORTE):
        return TEXTOS["modelo_chamado"]

    # --- SERVIÇOS ---
    if any(p in mensagem for p in PALAVRAS_SERVICOS):
        return f"{TEXTOS['servicos_detalhados']}\n\nPara voltar ao menu, digite *Início*."

    # --- CONSULTOR ---
    if any(p in mensagem for p in PALAVRAS_CONSULTOR):
        return "Perfeito! 👨‍💻 Vou te transferir para um de nossos consultores agora."

    # --- FALLBACK ---
    return (
        "Não consegui entender muito bem 🤔\n\n"
        "Escolha uma opção:\n"
        "1️⃣ Suporte\n"
        "2️⃣ Serviços\n"
        "3️⃣ Consultor"
    )
