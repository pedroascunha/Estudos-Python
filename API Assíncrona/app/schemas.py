from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime


class UsuarioCreate(BaseModel):
    username: str
    senha: str


class UsuarioOut(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}


class ContaCreate(BaseModel):
    numero: str


class ContaOut(BaseModel):
    id: int
    numero: str
    saldo: float

    model_config = {"from_attributes": True}


class TransacaoBase(BaseModel):
    valor: float

    @field_validator("valor")
    @classmethod
    def valor_positivo(cls, v: float):
        if v <= 0:
            raise ValueError("Valor deve ser positivo")
        return v


class DepositoCreate(TransacaoBase):
    pass


class SaqueCreate(TransacaoBase):
    pass


class TransacaoOut(BaseModel):
    id: int
    tipo: str
    valor: float
    criada_em: datetime

    model_config = {"from_attributes": True}


class ExtratoOut(BaseModel):
    conta: ContaOut
    transacoes: List[TransacaoOut]
