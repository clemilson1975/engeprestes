"""
Esquemas Pydantic: definem o formato de dados que a API aceita (entrada) e
devolve (saída). Isso é o que dá validação automática de graça — se alguém
mandar "mt2": "abc" em vez de um número, a API já recusa antes de chegar
no banco.
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TerrenoBase(BaseModel):
    local: str
    proprietario: Optional[str] = None
    mt2: Optional[float] = None
    data_aquisicao: Optional[date] = None
    custo_compra: Optional[float] = 0
    outros_gastos: Optional[float] = 0
    status: Optional[str] = "Pagando"
    vendido: Optional[bool] = False


class TerrenoCreate(TerrenoBase):
    pass


class TerrenoUpdate(TerrenoBase):
    local: Optional[str] = None  # no update, nada é obrigatório


class TerrenoOut(TerrenoBase):
    id: int
    custo_total: float

    model_config = ConfigDict(from_attributes=True)
