from app import schemas
import pytest
from jose import jwt
from app.config import settings


# def test_root(client):
#     res=client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'sososososo'
#     assert res.status_code == 200

def test_create_user(client):
    res=client.post("/users/", json={"email": "soso@gmail.com", "password":"123"})


    new_user=schemas.UserOut(**res.json())#do we have an id, email and the created at?
    assert new_user.email == "soso@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):    
    res=client.post("/login", data={"username": test_user['email'], "password":test_user['password']})
    login_res=schemas.Token(**res.json())
    payload=jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])#payload data
    #to extract payload data
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('eueueu@gmail.com', '7364', 403),
    ('soso@gmail.com', '777', 403),
    ('eueueu@gmail.com', '777', 403),
    (None, '7364', 422),
    ('soso@gmail.com', None, 422) 
])
def test_incorrect_login(test_user, client, email, password,status_code ):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid credentials'
    