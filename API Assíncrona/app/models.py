from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)

    contas = relationship("Conta", back_populates="usuario")


class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(20), unique=True, index=True, nullable=False)
    saldo = Column(Float, default=0.0)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="contas")
    transacoes = relationship("Transacao", back_populates="conta")


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(10), nullable=False)  # "deposito" ou "saque"
    valor = Column(Float, nullable=False)
    criada_em = Column(DateTime, default=datetime.utcnow)
    conta_id = Column(Integer, ForeignKey("contas.id"))

    conta = relationship("Conta", back_populates="transacoes")
