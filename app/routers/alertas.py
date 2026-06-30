from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(
    prefix="/alertas",
    tags=["Alertas"]
)

@router.get("/", response_model=List[schemas.Alerta])
def read_alertas(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Alerta).all()

@router.post("/", response_model=schemas.Alerta, status_code=status.HTTP_201_CREATED)
def create_alerta(
    alerta: schemas.AlertaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_alerta = models.Alerta(**alerta.model_dump())
    db.add(db_alerta)
    db.commit()
    db.refresh(db_alerta)
    return db_alerta

@router.delete("/{alerta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alerta(
    alerta_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_alerta = db.query(models.Alerta).filter(models.Alerta.id == alerta_id).first()
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    db.delete(db_alerta)
    db.commit()
    return None
