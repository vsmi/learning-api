import pytest

def test_vote_dir_1(authorized_user, test_books):
    data = {
        "book_id": test_books[0].id,
        "dir": 1
    }
    res = authorized_user.post("/votes/", json = data)
    assert res.status_code == 201

def test_vote_dir_0(authorized_user, test_books, test_voted_book):
    data = {
        "book_id": test_books[3].id,
        "dir": 0
    }
    res = authorized_user.post("/votes/", json = data)
    assert res.status_code == 201

def test_double_vote(authorized_user, test_books, test_voted_book):
    data = {
        "book_id": test_books[3].id,
        "dir": 1
    }
    res = authorized_user.post("/votes/", json = data)
    assert res.status_code == 409

def test_vote_for_book_not_exist(authorized_user, test_books):
    data = {
        "book_id": 8888,
        "dir": 1
    }
    res = authorized_user.post("/votes/", json = data)
    assert res.status_code == 404

def test_delete_vote_not_exist(authorized_user, test_books, test_voted_book):
    data = {
        "book_id": test_books[0].id,
        "dir": 0
    }
    res = authorized_user.post("/votes/", json = data)
    assert res.status_code == 404

def test_vote_user_not_auth(client, test_books):
    data = {
        "book_id": test_books[0].id,
        "dir": 1
    }
    res = client.post("/votes/", json = data)
    assert res.status_code == 401