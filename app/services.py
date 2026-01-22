import random
from app.schemas import ChamadoInput
from app.integrations import enviar_para_laravel

# --- Dicionário de Mensagens (Facilita a manutenção) ---
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

async def obter_resposta_suporte(dados: ChamadoInput) -> str:
    """
    Orquestra os diálogos do bot Simplesmente.
    """
    
    # 1. Fluxo de Envio para o Laravel (Formulário preenchido)
    if dados.is_formulario:
        sucesso = await enviar_para_laravel(dados)
        if sucesso:
            return (
                f"✅ *Chamado Registrado!* \n\n"
                f"Obrigado, {dados.nome}. Seus dados foram enviados para o nosso sistema.\n"
                "🚀 Em breve, um técnico entrará em contato pelo seu telefone ou e-mail."
            )
        else:
            return "⚠️ *Erro de Conexão:* Não consegui salvar seu chamado no sistema. Por favor, tente novamente em instantes."

    # 2. Processamento da Mensagem do Usuário
    mensagem = (dados.mensagem or "").lower().strip()

    # --- Fluxo 1: Saudação e Menu Principal ---
    if any(s in mensagem for s in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "inicio", "voltar"]):
        saudacao = random.choice(TEXTOS["saudacoes"])
        return f"{saudacao}\n\n{TEXTOS['menu_principal']}"

    # --- Fluxo 2: Suporte Técnico (Opção 1) ---
    if any(s in mensagem for s in ["1", "suporte", "chamado", "tecnico", "técnico"]):
        return TEXTOS["modelo_chamado"]

    # --- Fluxo 3: Serviços (Opção 2) ---
    if any(s in mensagem for s in ["2", "serviço", "serviços", "portfolio", "portfólio"]):
        return f"{TEXTOS['servicos_detalhados']}\n\nPara voltar ao menu, digite *Início*."

    # --- Fluxo 4: Falar com Humano (Opção 3) ---
    if any(s in mensagem for s in ["3", "consultor", "humano", "falar", "atendente"]):
        return (
            "Entendido! 👨‍💻 Vou te transferir para um de nossos consultores.\n\n"
            "Por favor, aguarde um momento que já vamos te atender."
        )

    # --- Resposta Padrão (Fallback) ---
    return (
        "Ainda não entendi muito bem... 🤔\n\n"
        "Para que eu possa te ajudar, escolha uma das opções:\n"
        "1️⃣ Suporte\n"
        "2️⃣ Serviços\n"
        "3️⃣ Consultor"
    )