from pydantic import BaseModel
from typing import Optional

class MensagemInput(BaseModel):
    mensagem: str  # Texto que vem do cliente

class ChamadoInput(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    motivo: Optional[str] = None
    descricao: Optional[str] = None # No JS está como 'descricao' sem o 'ã'
    is_formulario: bool = False