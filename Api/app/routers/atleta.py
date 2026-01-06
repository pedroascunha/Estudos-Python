# app/routers/atleta.py
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/atletas", tags=["Atletas"])


# POST - cria atleta (tratando cpf duplicado)
@router.post(
    "/",
    response_model=schemas.AtletaOut,
    status_code=status.HTTP_201_CREATED,
)
async def criar_atleta(
    atleta_in: schemas.AtletaCreate,
    db: Session = Depends(get_db),
):
    atleta = models.Atleta(**atleta_in.dict())

    try:
        db.add(atleta)
        db.commit()
        db.refresh(atleta)
    except IntegrityError:
        db.rollback()
        # mensagem e status code conforme instrução do desafio
        raise HTTPException(
            status_code=303,
            detail=f"Ja existe um atleta cadastrado com o cpf: {atleta_in.cpf}",
        )

    return atleta


# GET ALL - com filtros por query param + paginação + response customizado
@router.get(
    "/",
    response_model=Page[schemas.AtletaOut],
    status_code=status.HTTP_200_OK,
)
async def listar_atletas(
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Atleta)

    # filtros (query parameters)
    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)

    atletas = query.order_by(models.Atleta.id).all()

    # fastapi-pagination cuida de limit / offset na resposta
    return paginate(atletas)


# GET by id (exemplo extra, sem mudanças de desafio)
@router.get(
    "/{atleta_id}",
    response_model=schemas.AtletaOut,
    status_code=status.HTTP_200_OK,
)
async def obter_atleta(
    atleta_id: int,
    db: Session = Depends(get_db),
):
    atleta = db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta nao encontrado",
        )

    return atleta
