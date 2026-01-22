from app.schemas import ChamadoInput

def obter_resposta_suporte(dados: ChamadoInput) -> str:
    # 1. Template do Formulário da Simplesmente
    formulario_template = (
        "*NOME:* \n"
        "*TELEFONE:* \n"
        "*E-MAIL:* \n"
        "*MOTIVO:* (Suporte técnico / Serviços / Outros)\n"
        "*DESCRIÇÃO:* "
    )

    # 2. Template de Catálogo de Serviços (Resumido)
    servicos_template = (
        "💻 *Computação:* TI Gerenciada, Nuvem, Cibersegurança, Software e Backup.\n"
        "🛡️ *CFTV & Segurança:* Instalação, Alarmes, Controlo de Acesso e Monitorização.\n"
        "🌐 *Redes:* Conectividade, Wi-Fi Corporativo e Infraestrutura."
    )

    # 3. Se o formulário já foi preenchido e identificado pelo n8n
    if dados.is_formulario:
        return (
            f"✅ *Solicitação Recebida com Sucesso!*\n\n"
            f"Obrigado, {dados.nome}. Registamos o seu chamado sobre '{dados.motivo}'.\n\n"
            "🚀 *Próximo passo:* A nossa equipa na *Simplesmente* fará a triagem e "
            "receberá um retorno em breve por este canal."
        )

    # 4. Lógica de Diálogos e Instruções
    texto_usuario = (dados.mensagem or "").lower().strip()

    # Fluxo: Saudação Inicial
    if any(s in texto_usuario for s in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]):
        return (
            "Olá! 👋 Seja bem-vindo ao atendimento da *Simplesmente*.\n\n"
            "Como posso ajudar hoje?\n"
            "1️⃣ *Suporte técnico*\n"
            "2️⃣ *Serviços*\n"
            "3️⃣ *Outros*\n\n"
            "Digite o número ou o nome da opção desejada."
        )

    # Fluxo 1: Suporte técnico
    if any(s in texto_usuario for s in ["1", "suporte", "técnico", "tecnico"]):
        return (
            "Entendido! Para suporte técnico na *Simplesmente*, "
            "precisamos de alguns detalhes. 🛠️\n\n"
            "Copie a mensagem abaixo, preencha e envie de volta:\n\n"
            f"{formulario_template}"
        )

    # Fluxo 2: Serviços (Catálogo + Formulário)
    if any(s in texto_usuario for s in ["2", "serviço", "serviços"]):
        return (
            "Ficamos felizes pelo interesse nos nossos serviços! 💡\n\n"
            f"{servicos_template}\n\n"
        )

    # Fluxo 3: Outros
    if any(s in texto_usuario for s in ["3", "outros", "outro", "consultor", "falar"]):
        return (
            "Para outros assuntos ou falar com um consultor da *Simplesmente*, "
            "precisamos identificar a sua necessidade. 👨‍💻\n\n"
            "Por favor, use o modelo abaixo para detalhar a sua solicitação:\n\n"
            f"{formulario_template}"
        )

    # Fluxo: Agradecimentos
    if any(s in texto_usuario for s in ["obrigado", "valeu", "obrigada"]):
        return "A *Simplesmente* agradece o seu contato! Tenha um ótimo dia! 😊"

    # Resposta Padrão (Fallback)
    return (
        "Ainda não entendi muito bem... 🤔\n\n"
        "Se precisa de ajuda na *Simplesmente*, escolha uma das opções:\n"
        "1️⃣ Suporte técnico\n"
        "2️⃣ Serviços\n"
        "3️⃣ Outros"
    )