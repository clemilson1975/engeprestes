"""
Modelos do banco de dados (cada classe = uma tabela).

Começamos só com Terrenos. Reparem que os campos aqui batem com as colunas
que já existiam na sua planilha — a diferença é que agora "custo_total" é
calculado pelo próprio banco (não dá pra ele ficar errado ou desatualizado).
"""

from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from database import Base


class Terreno(Base):
    __tablename__ = "terrenos"

    id = Column(Integer, primary_key=True, index=True)
    local = Column(String(200), nullable=False)
    proprietario = Column(String(200))  # texto por enquanto; vira FK quando criarmos a tabela Pessoas
    mt2 = Column(Float)
    data_aquisicao = Column(Date)
    custo_compra = Column(Float, default=0)
    outros_gastos = Column(Float, default=0)
    status = Column(String(50), default="Pagando")  # Pagando, Liquidado...
    vendido = Column(Boolean, default=False)

    @property
    def custo_total(self):
        return (self.custo_compra or 0) + (self.outros_gastos or 0)
