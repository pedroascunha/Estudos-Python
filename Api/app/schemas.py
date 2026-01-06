# app/schemas.py
from pydantic import BaseModel


class AtletaBase(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str


class AtletaCreate(AtletaBase):
    pass


# resposta customizada do GET ALL (sem cpf, apenas o que o desafio pede)
class AtletaOut(BaseModel):
    id: int
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True
