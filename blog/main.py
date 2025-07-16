from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas, models
from .database import engine, SessionLocal
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", response_model=schemas.ShowBlog, tags=["blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(
        models.Blog.id == id).update(dict(request))

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    db.commit()

    return "updated"


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==
                                        id).delete(synchronize_session=False)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    db.commit()

    return "deleted"


@app.get("/blogs", response_model=List[schemas.ShowBlog], tags=["blogs"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.get("/blog/{id}", response_model=schemas.ShowBlog, tags=["blogs"])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found")

    return blog


@app.post("/user", response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users", response_model=List[schemas.ShowUser], tags=["users"])
def all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["users"])
def show(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    return user
