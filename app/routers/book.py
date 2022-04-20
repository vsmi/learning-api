from asyncio.windows_events import NULL
from app import oauth2
from .. import models, schemas, utils, oauth2
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix= "/books",
    tags=['Books']
)

# Вызовет список всех книг и инф по ним
@router.get("/", response_model=List[schemas.CurrentBook])
async def get_books(db: Session = Depends(get_db), limit: int = 10, rating: Optional[float] = None):
    # cursor.execute("""SELECT * FROM books """) 
    # books = cursor.fetchall()
    if rating:
        books = db.query(models.Book).filter(models.Book.rating >= rating).limit(limit).all()
    else:
        books = db.query(models.Book).limit(limit).all()
    return books


# создаст запись в базе
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.CurrentBook)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO books (title, author, rating, read) VALUES (%s, %s, %s, %s) RETURNING * """, 
    # (book.title, book.author, book.rating, book.read))
    # new_book = cursor.fetchone()
    # conn.commit()
    new_book = models.Book(owner_id=current_user.id, **book.dict()) # упаковка аргументов
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# вернет инф по определенной книге через id
@router.get("/{id}", response_model=schemas.CurrentBook)
def get_book(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM books WHERE id = %s""", [str(id)])  # (str(id),) принимает либо словарь, либо кортеж
    # print ("id=",id, "type=",type(id))
    # book = cursor.fetchone()
    book_query = db.query(models.Book).filter(models.Book.id == id)   
    book = book_query.first()   
    if not book:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"book with id {id} was not found")

    # if book.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"book with id {id} was not found"}
    return book


# удалит запись с указанным индексом
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM books WHERE id = %s RETURNING *""", (str(id),))
    # deleted_book = cursor.fetchone()
    # conn.commit()
    deleted_book_query = db.query(models.Book).filter(models.Book.id == id)
    deleted_book = deleted_book_query.first()

    if not deleted_book:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"book with id {id} was not found")   
    
    if deleted_book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    deleted_book_query.delete(synchronize_session=False) 
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

# изменит запись с указанным индексом
@router.put("/{id}", response_model=schemas.CurrentBook)
def update_book(id: int, book: schemas.BookUpdate, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE books SET title = %s, author = %s, rating = %s, read = %s WHERE id = %s 
    # RETURNING * """, (book.title, book.author, book.rating, book.read, str(id)))
    # updated_book = cursor.fetchone()
    # conn.commit()
    updated_book_query = db.query(models.Book).filter(models.Book.id == id)
    updated_book = updated_book_query.first()
    if not updated_book:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"book with id {id} was not found")  

    if updated_book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    updated_book_query.update(book.dict(), synchronize_session=False)
    db.commit()
    return updated_book_query.first()