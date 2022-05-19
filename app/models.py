from http.client import HTTPException
from sqlite3 import Timestamp
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship, validates
from pydantic import BaseModel, constr, validator
from fastapi import HTTPException, status



class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    read = Column(Boolean, server_default='TRUE', nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    description = Column(String, nullable=True)

# sqlalchemy validator
    # @validates("description")
    # def max_length_description(self, key, value):
    #     column_type = getattr(type(self), key).expression.type
    #     print("column_type", column_type)
    #     max_length = column_type.length

    #     if len(value) > max_length:
    #         raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY, 
    #         detail=f"Value '{value}' for column '{key}' "
    #             f"exceed maximum length of '{max_length}'"
    #         )
    #     return value





# pydantic validator - не работает
# class Book_model(BaseModel):    
#     title: str
#     author: str
#     rating: float
#     read: bool
#     owner_id: int
#     description: constr(max_length=10)

#     @validator('description')
#     def max_length_description(cls, v, values, **kwargs):
#         if len(v) > 10:
#             raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail="description must be less 10")
#         return v





class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "vote"

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) 


