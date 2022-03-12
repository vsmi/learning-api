from .contest import test_user, client, session
from jose import jwt
from app.config import settings
from app import schemas
import pytest

def test_login_user(test_user, client):
    res = client.post("/login", data = {"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id") 

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",
[('usertest@gmail.com', 'password', 404),
('user@gmail.com', 'password123', 404),
('user@gmail.com', 'password', 404),
(None, 'password123', 422),
('usertest@gmail.com', None, 422)
])

def test_incorrect_login(test_user, client, email, password, status_code):

    res = client.post("/login", data = {"username": email, "password": password})
    assert res.status_code == status_code




