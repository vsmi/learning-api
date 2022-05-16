from urllib import response
import pytest
from app import schemas


def test_get_books_unauthorized(client, test_books):
    res = client.get("/books/")
    assert res.status_code == 200

def test_get_books_default_param(authorized_user, test_books):
    res = authorized_user.get("/books/")

    def validate(post):
        return schemas.CurrentBook(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == 10
    assert res.status_code == 200

def test_get_books_limit_5(authorized_user, test_books):
    res = authorized_user.get("/books?limit=5")
    assert len(res.json()) == 5
    assert res.status_code == 200

def test_get_books_rating_5(authorized_user, test_books):
    res = authorized_user.get("/books?rating=5")
    assert len(res.json()) == 5
    assert res.status_code == 200

def test_get_books_limit_rating(authorized_user, test_books):
    res = authorized_user.get("/books?rating=5&limit=2")
    assert len(res.json()) == 2
    assert res.status_code == 200

def test_get_books_limit_rating_string(authorized_user, test_books):
    res = authorized_user.get("/books?rating='5'&limit='2'")
    assert res.status_code == 422
################################################################################

def test_get_one_book_unauthorized(client, test_books):
    res = client.get(f"/books/{test_books[0].id}")
    assert res.status_code == 200

def test_get_one_book_by_other_user(authorized_user, test_books):
    res = authorized_user.get(f"/books/{test_books[11].id}")
    assert res.status_code == 200

def test_get_one_book(authorized_user, test_books):
    res = authorized_user.get(f"/books/{test_books[0].id}")
    #print(res.json())
    book = schemas.CurrentBook(**res.json())
    assert book.id == test_books[0].id
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

###############################################################################

def test_update_book(authorized_user, test_books):
    res = authorized_user.put(f"/books/{test_books[0].id}", json = {"title": "Анна Каренина", "rating" : 4.0, "read": True})
    book = schemas.CurrentBook(**res.json())
    assert res.status_code == 200
    assert book.title == "Анна Каренина"
    assert book.rating == 4.0

def test_update_book_not_exist(authorized_user, test_books):
    res = authorized_user.put("/books/88888", json = {"title": "Анна Каренина", "rating" : 4.0, "read": True})
    #book = schemas.CurrentBook(**res.json())
    assert res.status_code == 404

def test_update_book_not_auth(client, test_books):
    res = client.put(f"/books/{test_books[0].id}", json = {"title": "Анна Каренина", "rating" : 4.0, "read": True})
    #book = schemas.CurrentBook(**res.json())
    assert res.status_code == 401

def test_update_book_not_credentials(authorized_user, test_user, test_user2, test_books):
    data = {
        "title": "Анна Каренина", 
        "rating" : 4.0, 
        "read": True,
        "id": test_books[11].id
        }
    res = authorized_user.put(f"/books/{test_books[11].id}", json = data)
    assert res.status_code == 403

################################################################################

def test_delete_book(authorized_user, test_books):
    res = authorized_user.delete(f"/books/{test_books[0].id}")
    assert res.status_code == 204


def test_delete_book_non_exist(authorized_user, test_books):
    res = authorized_user.delete("/books/88888")
    assert res.status_code == 404

def test_delete_book_not_auth(client, test_books):
    res = client.delete(f"/books/{test_books[0].id}")
    assert res.status_code == 401

def test_delete_book_not_credentials(authorized_user, test_user, test_user2, test_books):
    res = authorized_user.delete(f"/books/{test_books[11].id}")
    assert res.status_code == 403

##############################################################################

def test_get_books_by_author_unauthorized(client, test_books):
    res = client.get(f"/books/by-author/{test_books[9].author}")
    def validate(post):
        return schemas.CurrentBook(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == 2
    assert res.status_code == 200


def test_get_books_by_author(authorized_user, test_books):
    res = authorized_user.get(f"/books/by-author/{test_books[9].author}?rating=4")

    def validate(post):
        return schemas.CurrentBook(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == 1
    assert res.status_code == 200

def test_get_books_not_found(authorized_user, test_books):
    res = authorized_user.get("/books/by-author/НетТакогоАвтораВБазе")

    def validate(post):
        return schemas.CurrentBook(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == 0
    assert res.status_code == 200

def test_get_books_invalid_param_author(authorized_user, test_books):
    res = authorized_user.get("/books/by-author/")

    assert res.status_code == 422

def test_get_books_invalid_param_rating(authorized_user, test_books):
    res = authorized_user.get(f"/books/by-author/{test_books[9].author}?rating='d'")

    assert res.status_code == 422

# Дописать fixture и тесты на limit