import re
from unittest import TestCase

from fastapi.testclient import TestClient

from api.settings.router import settings
from api.users.router import router
from api.users.schema import UserIn, UserOut
from api.utils import generator

client = TestClient(router)


#Listas
user_in_list = []
user_out_list = []

# Fill UserIn
for _ in range(10):
    user_in_list.append(UserIn(name=generator.name(), email=generator.email(), password=generator.password()))  # type: ignore


def test_create_user():
    """Test User Creation."""
    for user_in in user_in_list:
        response = client.post("/users", json=user_in.json())
        assert response.status_code == 200
        user_out_list.append(UserOut(**response.json(), key=response.json()["key"]))
        assert response.json() == UserOut(**response.json()).dict()

# def test_list():
#     """Test User List."""
#     response = c.get("/users")
#     assert response.status_code == 200
    #assert len(response.json()) == 10
    
# def test_user_get():
#     """Test User Get."""
#     for user_out in user_out_list:
#         response = c.get(f"/users/{user_out.key}")
#         assert response.status_code == 200
#         assert response.json() == user_out.dict()



