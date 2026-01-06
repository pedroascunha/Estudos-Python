# app/models.py
from sqlalchemy import Column, Integer, String
from app.database import Base


class Atleta(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True, nullable=False)
    cpf = Column(String(11), unique=True, index=True, nullable=False)
    centro_treinamento = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
