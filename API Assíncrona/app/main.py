from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas
from .security import (
    hash_senha,
    login,
    get_current_user,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Bancária Assíncrona com FastAPI")


# ---------- AUTENTICAÇÃO (JWT) ----------

@app.post("/auth/signup", response_model=schemas.UsuarioOut)
async def criar_usuario(
    usuario_in: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
):
    if db.query(models.Usuario).filter(
        models.Usuario.username == usuario_in.username
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe",
        )

    user = models.Usuario(
        username=usuario_in.username,
        senha_hash=hash_senha(usuario_in.senha),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/token")
async def obter_token(token_data=Depends(login)):
    return token_data


# ---------- CONTAS ----------

@app.post("/contas/", response_model=schemas.ContaOut)
async def criar_conta(
    conta_in: schemas.ContaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    if db.query(models.Conta).filter(
        models.Conta.numero == conta_in.numero
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conta já existe",
        )

    conta = models.Conta(
        numero=conta_in.numero,
        usuario_id=usuario.id,
        saldo=0.0,
    )
    db.add(conta)
    db.commit()
    db.refresh(conta)
    return conta


def _get_conta_or_404(
    numero: str, usuario_id: int, db: Session
) -> models.Conta:
    conta = (
        db.query(models.Conta)
        .filter(models.Conta.numero == numero, models.Conta.usuario_id == usuario_id)
        .first()
    )
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada",
        )
    return conta


# ---------- TRANSAÇÕES (DEPÓSITO/SAQUE) ----------

@app.post("/contas/{numero}/deposito", response_model=schemas.TransacaoOut)
async def depositar(
    numero: str,
    deposito: schemas.DepositoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    conta = _get_conta_or_404(numero, usuario.id, db)

    conta.saldo += deposito.valor
    transacao = models.Transacao(
        tipo="deposito", valor=deposito.valor, conta_id=conta.id
    )

    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao


@app.post("/contas/{numero}/saque", response_model=schemas.TransacaoOut)
async def sacar(
    numero: str,
    saque: schemas.SaqueCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    conta = _get_conta_or_404(numero, usuario.id, db)

    if saque.valor > conta.saldo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente",
        )

    conta.saldo -= saque.valor
    transacao = models.Transacao(
        tipo="saque", valor=saque.valor, conta_id=conta.id
    )

    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao


# ---------- EXTRATO ----------

@app.get("/contas/{numero}/extrato", response_model=schemas.ExtratoOut)
async def extrato(
    numero: str,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    conta = _get_conta_or_404(numero, usuario.id, db)
    transacoes = (
        db.query(models.Transacao)
        .filter(models.Transacao.conta_id == conta.id)
        .order_by(models.Transacao.criada_em.desc())
        .all()
    )

    return schemas.ExtratoOut(
        conta=conta,
        transacoes=transacoes,
    )
