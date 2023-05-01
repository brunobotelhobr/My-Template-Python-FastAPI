from ast import List
import json
from unittest import TestCase

from fastapi.testclient import TestClient
from pydantic import Json

from api.settings.router import settings
from api.main import app
from api.users.schema import UserIn, UserOut
from api.utils import generator

client = TestClient(app)


# Lists
user_out_list = []
user_in_list = []
for _ in range(10):
    user_in_list.append(UserIn(name=generator.name(), email=generator.email(), password=generator.password()))  # type: ignore


def test_create_user():
    """Test User Creation."""
    for user_in in user_in_list:
        response = client.post("/admin/users/", content=user_in.json())
        assert response.status_code == 201
        user_out = UserOut.parse_raw(response.content)
        for field in user_in.dict():
            if field != "password":
                assert getattr(user_out, field) == getattr(user_in, field)
        user_out_list.append(user_out)
    # Test same email creation
    user_in = {'name': generator.name(), 'email': user_out_list[0].email, 'password': generator.password()}
    response = client.post("/admin/users/", content=json.dumps(user_in))
    assert response.status_code == 404
    # Test invalid email
    user_in = {'name': generator.name(), 'email': 'invalid_email', 'password': generator.password()}
    response = client.post("/admin/users/", content=json.dumps(user_in))
    assert response.status_code == 422
    # Test invalid password
    user_in = {'name': generator.name(), 'email': generator.email(), 'password': ''}
    response = client.post("/admin/users/", content=json.dumps(user_in))
    assert response.status_code == 422
    # Test invalid name
    user_in = {'name': '', 'email': generator.email(), 'password': generator.password()}
    response = client.post("/admin/users/", content=json.dumps(user_in))
    assert response.status_code == 422


def test_user_get():
    """Test User Get."""
    for user_out in user_out_list:
        response = client.get(f"/admin/users/{user_out.key}")
        assert response.status_code == 200
        for field in user_out.dict():
            if field != "password_setting_date":
                assert response.json()[field] == getattr(user_out, field)
    # Test invalid key
    response = client.get("/admin/users/invalid_key")
    assert response.status_code == 404


def test_user_list():
    """Test User List."""
    response = client.get("/admin/users/")
    assert response.status_code == 200
    cache = []
    for i in json.loads(response.content):
        cache.append(UserOut.parse_raw(i))
        print(UserOut.parse_raw(i))
    # for u in user_out_list:
    #     assert u.name in cache
    # # Test pagination
    # response = client.get("/admin/users/?skip=5&limit=5")
    # assert response.status_code == 200
    # cache = []
    # for i in response.json():
    #     cache.append(UserOut.parse_obj(i))
    # for u in user_out_list[5:]:
    #     assert u.name in cache
    # # Test invalid pagination
    # response = client.get("/admin/users/?skip=invalid&limit=invalid")
    # assert response.status_code == 422