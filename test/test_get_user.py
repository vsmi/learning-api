import pytest
from app import schemas
from app import schemas


def test_get_user(test_user, client):
    res = client.get(f"/users/{test_user['id']}")
    
    assert res.status_code == 200
    assert res.json().get("id") == test_user['id']
    assert res.json().get("email") == test_user['email']



def test_id_doesnot_exist(client):
    res = client.get("/users/-1")
    
    assert res.status_code == 404

def test_invalid_id_string(client):
    res = client.get("/users/id")

    assert res.status_code == 422

def test_invalid_id_empty(client):
    res = client.get("/users/")

    assert res.status_code == 405
