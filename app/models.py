from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal

class EstadoBase(BaseModel):
    """Modelo base para dados da Bancada Camila."""
    info_valor: Literal['informacao', 'dado'] = Field(..., description="Tipo da informação (dado ou informacao)")
    variavel: str = Field(..., max_length=100, description="Nome da variável (ex: 'Temperatura', 'Nível_Estoque')")
    valor: str = Field(..., max_length=45, description="Valor da variável (pode ser texto ou número)")

class Estado(EstadoBase):
    """Modelo completo com ID e Data, usado para resposta da API."""
    idestado: int = Field(..., description="ID único do registro no banco de dados.")
    data: datetime = Field(..., description="Timestamp da inserção do dado.")

    class Config:
        orm_mode = True 
        schema_extra = {
            "example": {
                "idestado": 123,
                "info_valor": "dado",
                "variavel": "Temperatura",
                "valor": "25.5",
                "data": "2025-09-30T15:00:00"
            }
        }

class StatusResponse(BaseModel):
    """Modelo para respostas de status da API."""
    status: str = Field(..., description="Status da operação")
    message: str = Field(..., description="Mensagem detalhada do status")