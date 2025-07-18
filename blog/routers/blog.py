from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database
from ..repository import blog
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.create(request, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.update(id, request, db)


@router.get("/all", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.get_all(db)


@router.get("/{id}", response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.show(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.destroy(id, db)
