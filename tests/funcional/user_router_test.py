import json

from fastapi.testclient import TestClient

from api.main import app
from api.settings.router import settings
from api.users.schema import UserIn, UserOut
from api.utils import generator

client = TestClient(app)


# Initialize variables
users = []


def test_create_user():
    """Test User Creation."""
    # Test valid creation
    for _ in range(10):
        u = UserIn(name=generator.name(), email=generator.email(), password=generator.password())  # type: ignore
        response = client.post("/admin/users/", content=u.json())
        assert response.status_code == 201
        out = UserOut.parse_raw(response.content)
        print(out)
        for field in u.dict():
            if field != "password":
                assert getattr(u, field) == getattr(out, field)
        users.append(out)
    # Test same email creation
    test = {"name": generator.name(), "email": users[0].email, "password": generator.password()}  # type: ignore
    response = client.post("/admin/users/", content=json.dumps(test))
    assert response.status_code == 404
    # Test invalid email
    test = {"name": generator.name(), "email": "invalid_email", "password": generator.password()}  # type: ignore
    response = client.post("/admin/users/", content=json.dumps(test))
    assert response.status_code == 422
    # Test invalid password
    test = {"name": generator.name(), "email": generator.email(), "password": ""}  # type: ignore
    response = client.post("/admin/users/", content=json.dumps(test))
    assert response.status_code == 422
    # Test invalid name
    test = {"name": "", "email": generator.email(), "password": generator.password()}  # type: ignore
    response = client.post("/admin/users/", content=json.dumps(test))
    assert response.status_code == 422


def test_user_get():
    """Test User Get."""
    for u in users:
        response = client.get(f"/admin/users/{u.key}")
        assert response.status_code == 200
        for field in u.dict():
            if field != "password_setting_date":
                assert response.json()[field] == getattr(u, field)
            else:
                assert response.json()[field] == getattr(u, field).isoformat()
    # Test invalid key
    response = client.get("/admin/users/invalid_key")
    assert response.status_code == 404


def test_user_list():
    """Test User List."""
    response = client.get("/admin/users/")
    assert response.status_code == 200
    # Check if each of the users in the list is in the response.
    for u in users:
        # Format Time
        u = u.dict()
        u["password_setting_date"] = u["password_setting_date"].isoformat()
        assert u in response.json()
    # Test pagination
    response = client.get("/admin/users/?skip=5&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5
    # Test invalid pagination
    response = client.get("/admin/users/?skip=invalid&limit=invalid")
    assert response.status_code == 422


def test_user_update():
    """Test User Update."""
    for u in users:
        print(u)
        u.name = generator.name()
        u.email = generator.email()
        print(u)
        print(users[0])
        response = client.patch(f"/admin/users/{u.key}", content=u.json())
        assert response.status_code == 200
        for field in u.dict():
            if field != "password_setting_date":
                assert response.json()[field] == getattr(u, field)
            else:
                assert response.json()[field] == getattr(u, field).isoformat()
    # Test invalid key
    test = {"name": generator.name(), "email": generator.email()}
    response = client.patch("/admin/users/invalid_key", content=json.dumps(test))
    assert response.status_code == 404
    # Test invalid email
    user_in = {"name": generator.name(), "email": "invalid_email"}
    response = client.patch(f"/admin/users/{users[0].key}", content=json.dumps(user_in))
    assert response.status_code == 422
    # Test invalid name
    user_in = {"name": "", "email": generator.email()}
    response = client.patch(f"/admin/users/{users[0].key}", content=json.dumps(user_in))
    assert response.status_code == 422


def test_user_delete():
    """Test User Delete."""
    # Test delete disabled
    settings.users.allow_delete = False
    for u in users:
        response = client.delete(f"/admin/users/{u.key}")
        assert response.status_code == 404
    # Test delete enabled
    settings.users.allow_delete = True
    u = users[0]
    response = client.delete(f"/admin/users/{u.key}")
    assert response.status_code == 200
    assert UserOut.parse_raw(response.content)
    # Test invalid key
    response = client.delete("/admin/users/invalid_key")
    assert response.status_code == 404
