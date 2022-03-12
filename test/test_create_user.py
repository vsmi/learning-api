from app import schemas
from .contest import test_user, client, session
from app import schemas
import pytest



def test_create_new_user(client):
    res = client.post("/users/", json = {"email": "testuser@gmail.ru", "password": "test123"})
    new_user = schemas.UserOut(**res.json())

    assert res.status_code == 201
    assert new_user.email == "testuser@gmail.ru"



def test_create_user_already_created(test_user, client):
    res = client.post("/users/", json = {"email": test_user['email'], "password": test_user['password']})
    
    assert res.status_code == 409
    assert res.json().get("detail") == f"User with this email {test_user['email']} is already registered"


@pytest.mark.parametrize("email, password, status_code",
[('usertest@', 'password', 422),
('user@gmail', 'password123', 422),
('user@gmail.', 'password', 422),
(None, 'password123', 422),
('usertest@gmail.com', None, 422)
])
def test_incorrect_user_data(client, email, password, status_code):
    res = client.post("/users/", json = {"email": email, "password": password})
    
    assert res.status_code == status_code
