from app import oauth2
from .. import models, schemas, utils, oauth2
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix= "/votes",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    book = db.query(models.Book).filter(models.Book.id == vote.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {vote.book_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.book_id == vote.book_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has alredy voted on book {vote.book_id}")

        new_vote = models.Vote(book_id=vote.book_id, user_id=current_user.id) # упаковка аргументов
        db.add(new_vote)
        db.commit()
        return {"msg": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg": "successfully deleted vote"}



