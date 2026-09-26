"""
API de manutenção de Terrenos.

"Manutenção", aqui, significa as 4 operações clássicas sobre um cadastro:
  - Create  (criar)
  - Read    (listar / consultar um)
  - Update  (editar)
  - Delete  (excluir)

Conhecido pela sigla CRUD. Praticamente todo cadastro de sistema (Terrenos,
Casas, Pessoas, Contas a pagar...) segue exatamente esse mesmo padrão —
uma vez que você entender este arquivo, os próximos ficam muito mais rápidos
de construir, porque é a mesma receita repetida.
"""

from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Cria as tabelas no banco (se ainda não existirem) a partir dos modelos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Engeprestes - Terrenos")

# Libera o front-end (rodando no navegador) para chamar esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/terrenos", response_model=schemas.TerrenoOut)
def criar_terreno(terreno: schemas.TerrenoCreate, db: Session = Depends(get_db)):
    novo = models.Terreno(**terreno.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@app.get("/terrenos", response_model=List[schemas.TerrenoOut])
def listar_terrenos(db: Session = Depends(get_db)):
    return db.query(models.Terreno).order_by(models.Terreno.id.desc()).all()


@app.get("/terrenos/{terreno_id}", response_model=schemas.TerrenoOut)
def buscar_terreno(terreno_id: int, db: Session = Depends(get_db)):
    terreno = db.get(models.Terreno, terreno_id)
    if not terreno:
        raise HTTPException(status_code=404, detail="Terreno não encontrado")
    return terreno


@app.put("/terrenos/{terreno_id}", response_model=schemas.TerrenoOut)
def editar_terreno(terreno_id: int, dados: schemas.TerrenoUpdate, db: Session = Depends(get_db)):
    terreno = db.get(models.Terreno, terreno_id)
    if not terreno:
        raise HTTPException(status_code=404, detail="Terreno não encontrado")

    # Só atualiza os campos que vieram preenchidos na requisição
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(terreno, campo, valor)

    db.commit()
    db.refresh(terreno)
    return terreno


@app.delete("/terrenos/{terreno_id}")
def excluir_terreno(terreno_id: int, db: Session = Depends(get_db)):
    terreno = db.get(models.Terreno, terreno_id)
    if not terreno:
        raise HTTPException(status_code=404, detail="Terreno não encontrado")
    db.delete(terreno)
    db.commit()
    return {"ok": True}


# Serve a telinha de manutenção (static/index.html) em "/"
app.mount("/", StaticFiles(directory="static", html=True), name="static")
