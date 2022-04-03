from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  
import psycopg2
import pytest
from psycopg2.extras import RealDictCursor
import time
from app import models
from app.config import settings
from app.database import get_db, Base
from app.main import app
from app.oauth2 import create_access_token
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"email": "usertest@gmail.com", "password": "password123"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {"email": "usertest2@gmail.com", "password": "password123"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture()
def authorized_user(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_books(test_user, session, test_user2):
    books_data = [{
        "title": "Война и мир",
        "author": "Л Толстой",
        "rating": 5.0,
        "owner_id": test_user['id'],
        "read": True
    }, {
        "title": "Идиот",
        "author": "Ф М Достоевский",
        "rating": 5.0,
        "owner_id": test_user['id'],
        "read": True
    },
        {
       "title": "Война миров",
        "author": "Г Уэлс",
        "rating": 0.0,
        "owner_id": test_user['id'],
        "read": False
    }, {
        "title": "Ученица",
        "author": "Т Вестовер",
        "rating": 5.0,
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Жареные зеленые помидоры",
        "author": "Ф Флэгг",
        "rating": 5.0,
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Мертвые души",
        "author": "",
        "rating": 5.0,
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Капитанская дочка",
        "author": "Пушкин А С",
        "rating": 3.5,
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Мастер и маргарита",
        "author": "Булгаков",
        "rating": 4.5,
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Джейн Эйр",
        "author": "Бронте",
        "rating": 4.5,
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Гордость и предубеждение",
        "author": "Бронте",
        "rating": 3.5,
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Милый друг",
        "author": "ГиДе Мопассан",
        "rating": 4.5,
        "owner_id": test_user2['id'],
        "read": True
    },
    {
        "title": "Гордость и предубеждение",
        "author": "Остин",
        "rating": 4.5,
        "owner_id": test_user2['id'],
        "read": True
    },
    {
        "title": "Унесенные ветром",
        "author": "М Митччел",
        "owner_id": test_user['id'],
        "read": True
    },
    {
        "title": "Узорный покров",
        "author": "Моем",
        "rating": 0.0,
        "owner_id": test_user['id'],
        "read": False
    }]

    def create_book_model(book):
        return models.Book(**book)

    book_map = map(create_book_model, books_data)
    books = list(book_map)

    session.add_all(books)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    books = session.query(models.Book).all()
    return books


@pytest.fixture()
def test_voted_book(test_books, session, test_user):
    new_vote =  models.Vote(book_id=test_books[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
    

