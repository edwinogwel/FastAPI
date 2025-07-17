from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

get_db = database.get_db


@router.post("/", response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/", response_model=List[schemas.ShowUser])
def all(db: Session = Depends(get_db)):
    return user.all(db)


@router.get("/{id}", response_model=schemas.ShowUser)
def show(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)
