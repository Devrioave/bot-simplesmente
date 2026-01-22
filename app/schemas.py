from pydantic import BaseModel
from typing import Optional

class ChamadoInput(BaseModel):
    # Este campo é essencial para processar o "Oi" ou saudações
    mensagem: Optional[str] = None  
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    motivo: Optional[str] = None
    descricao: Optional[str] = None
    is_formulario: bool = False