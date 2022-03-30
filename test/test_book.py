from urllib import response
import pytest
from app import schemas
from .contest import authorized_user, client, session, token, test_user, test_books, test_user2

def test_get_books(authorized_user, test_books):
    res = authorized_user.get("/books/")
    assert len(res.json()) == len(test_books)
    assert res.status_code == 200

################################################################################

@pytest.mark.parametrize("title, author, rating, read, status_code", [
    ("Три товарища", "Э М Ремарк", 4.8, True, 201),
    ("Триумфальная арка", "Э М Ремарк", 4.0, False, 201)
]) 
def test_create_book(authorized_user, test_user, test_books, title, author, rating, read, status_code):
    res = authorized_user.post("/books/", json = {"title": title, "author": author, "rating": rating, "read": read})
    assert res.status_code == status_code 

def test_create_book_without_title(authorized_user):
    res = authorized_user.post("/books/", json = {"author": "Тара Ветовер", "rating": 5.0, "read": True})
    assert res.status_code == 422

def test_create_book_without_read(authorized_user):
    res = authorized_user.post("/books/", json = {"title": "Ученица", "author": "Тара Ветовер", "rating": 5.0})
    assert res.status_code == 422

def test_create_book_without_optional_fields(authorized_user):
    res = authorized_user.post("/books/", json = {"title": "Ученица", "read": True})
    assert res.status_code == 201

@pytest.mark.parametrize("title, author, rating, read, status_code", [
    (123, "Э М Ремарк", 4.8, True, 201), # Конвертирует int в str
    ("", "Э М Ремарк", 4.0, False, 201), # Принимает пустое
    (" ", "Э М Ремарк", 4.8, True, 201), # Принимает пробелы
    ("Война и мир", 123, 4.8, True, 201), # Конвертирует int в str
    ("Война и мир", "", 4.8, True, 201), # Принимает пустое
    ("Война и мир", " ", 4.8, True, 201), # Принимает пробелы
    ("Война и мир", "Толстой", "", True, 422),
    ("Война и мир", "Толстой", "rating", True, 422),
    ("Война и мир", "Толстой", 5.0, 1, 201), # Конвертирует 1 в true
    ("Война и мир", "Толстой", 5.0, 15, 422),
    ("Война и мир", "Толстой", 5.0, "1", 201) # Конвертирует "1" в true
]) 
def test_create_book_invalid_values(authorized_user, test_user, test_books, title, author, rating, read, status_code):
    res = authorized_user.post("/books/", json = {"title": title, "author": author, "rating": rating, "read": read})
    assert res.status_code == status_code 