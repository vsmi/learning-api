import pytest
from app import schemas
from .contest import test_user, client, session
from app import schemas


def test_get_user(test_user, client):
    res = client.get(f"/users/{test_user['id']}")
    
    assert res.status_code == 200
    assert res.json().get("id") == test_user['id']
    assert res.json().get("email") == test_user['email']