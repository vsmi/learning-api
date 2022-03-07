from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from pydantic.types import conint

class UserOut(BaseModel):
    id: int
    email: EmailStr
    
    
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: Optional[str]
    rating: Optional[float] = None
    read: bool

class BookCreate(BookBase):
     pass 

class BookUpdate(BookBase):
    pass  

class CurrentBook(BookBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
   email: EmailStr
   password: str 

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    book_id: int
    dir: conint(le=1)
