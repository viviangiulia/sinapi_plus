# scripts/create_database.py
from infrastructure.database.engine import engine
from infrastructure.database.orm import Base


Base.metadata.create_all(engine)

print("Banco de dados e tabelas criados com sucesso.")