from app.schemas import ChamadoInput

def obter_resposta_suporte(dados: ChamadoInput) -> str:
    # 1. Definição do Formulário Padrão (Baseado na interface da Simplesmente)
    formulario_template = (
        "Para abrir o seu chamado, copie e preencha os dados abaixo:\n\n"
        "*NOME:* \n"
        "*TELEFONE:* \n"
        "*E-MAIL:* \n"
        "*MOTIVO:* (Suporte técnico / Dúvida / Solicitação / Outro)\n"
        "*DESCRIÇÃO:* "
    )

    # 2. Lógica: O n8n identificou que é um formulário preenchido?
    # Usamos o booleano que vem do seu nó de JavaScript no n8n
    if dados.is_formulario:
        return (
            f"✅ *Chamado Registrado!*\n\n"
            f"Olá {dados.nome}, recebemos a sua solicitação sobre '{dados.motivo}'. "
            "Os nossos consultores da Simplesmente irão analisar os dados e "
            "entraremos em contato em breve pelo e-mail ou telefone fornecido."
        )

    # 3. Lógica para saudações ou mensagens iniciais
    # Para isto funcionar, adicione a chave 'mensagem' no seu nó JavaScript do n8n
    texto_usuario = (dados.mensagem or "").lower()
    
    if any(saudacao in texto_usuario for saudacao in ["oi", "olá", "bom dia", "ajuda", "chamado"]):
        return (
            "Olá! Bem-vindo ao suporte da Simplesmente. 🛠️\n\n"
            f"{formulario_template}"
        )
    
    # 4. Caso o bot receba algo que não seja o formulário nem uma saudação
    return (
        "Não consegui identificar a sua solicitação. 🤔\n"
        "Se deseja abrir um chamado, por favor utilize o formato abaixo:\n\n"
        f"{formulario_template}"
    )