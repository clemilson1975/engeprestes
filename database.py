"""
Configuração da conexão com o banco de dados.

Por padrão usa SQLite (arquivo local "engeprestes.db"), então você roda o
projeto agora, sem precisar de internet nem de criar conta em lugar nenhum.

Quando quiser migrar para o Postgres (Supabase/Neon), basta criar um arquivo
".env" com a linha:

    DATABASE_URL=postgresql://usuario:senha@host:5432/nome_do_banco

Nenhuma outra linha do projeto precisa mudar — é essa a vantagem de usar o
SQLAlchemy como camada intermediária entre o código Python e o banco.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # lê o arquivo .env, se existir

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./engeprestes.db")

# Normaliza a URL do Postgres para usar o driver "psycopg" (v3) explicitamente.
# Isso evita depender de qual prefixo cada provedor (Supabase, Heroku, etc.)
# entrega por padrão — "postgres://" e "postgresql://" viram a mesma coisa.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# connect_args só é necessário para SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Abre uma sessão de banco por requisição e garante que ela é fechada depois."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
