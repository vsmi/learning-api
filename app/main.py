from fastapi import FastAPI
from . import models
from .database import engine
from .routers import book, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8000",
]

#models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#Корневой вызов
@app.get("/")
def root():
    return {"Welcome": "Have a nice day!"}
        


