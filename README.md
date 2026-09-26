# Engeprestes — Terrenos (primeira fatia do sistema)

Uma tabela, uma API de manutenção (CRUD) e uma tela para usar isso. Depois de
entender este exemplo, os próximos módulos (Casas, Pessoas, Contas a pagar...)
seguem exatamente a mesma receita.

## Como rodar agora (sem precisar de internet nem de conta em lugar nenhum)

```bash
# 1. Entre na pasta do projeto
cd engeprestes

# 2. Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o servidor
uvicorn main:app --reload
```

Abra **http://127.0.0.1:8000** no navegador — essa é a telinha de manutenção
de terrenos, já funcionando. Você pode cadastrar, editar e excluir terrenos,
e tudo fica salvo no arquivo `engeprestes.db` (criado automaticamente na
primeira execução).

Quer ver a API "por dentro"? Acesse **http://127.0.0.1:8000/docs** — o FastAPI
gera automaticamente uma documentação interativa onde dá pra testar cada
operação (criar, listar, editar, excluir) sem nem abrir a telinha.

## Estrutura dos arquivos — o que cada um faz

| Arquivo | Papel |
|---|---|
| `database.py` | Onde e como conectar ao banco (hoje: SQLite; depois: Postgres) |
| `models.py` | A tabela `Terreno`, em formato Python (SQLAlchemy) |
| `schemas.py` | O que a API aceita/devolve, com validação automática (Pydantic) |
| `main.py` | As 4 operações de manutenção (criar, listar, editar, excluir) |
| `static/index.html` | A telinha — HTML + JavaScript puro, sem framework |

## Quando quiser migrar para o Postgres (Supabase)

1. Crie uma conta gratuita em supabase.com e um novo projeto.
2. Na aba "Connect" do projeto, copie a "Connection string" (modo `URI`).
3. Copie `.env.example` para `.env` e cole a connection string na variável
   `DATABASE_URL`.
4. Rode `uvicorn main:app --reload` de novo — pronto, os mesmos dados agora
   vivem no Postgres na nuvem, e nenhuma linha do `main.py`, `models.py` ou
   `schemas.py` precisou mudar.

## O padrão que se repete (para os próximos módulos)

Para cada novo cadastro (Casas, Pessoas, Contas a pagar...), o caminho é:
1. Uma classe nova em `models.py` (a tabela)
2. Um esquema novo em `schemas.py` (validação)
3. As 4 rotas de manutenção em `main.py` (ou um arquivo separado, quando o
   projeto crescer)
4. Uma tela nova (ou uma aba na mesma tela)

Quando estiver confortável com Terrenos, é só avisar que seguimos para o
próximo módulo.
