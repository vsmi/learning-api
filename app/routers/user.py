import email
from .. import models, schemas, utils
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix= "/users",
    tags= ['Users']
)

# Users
# Создаем пользователя
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict()) # упаковка аргументов
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not check_user:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"User with this email {user.email} is already registered")


#Выбрать пользователя по id
@router.get("/{id}", response_model=schemas.UserOut)
def get_User(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id {id} was not found")
    return user