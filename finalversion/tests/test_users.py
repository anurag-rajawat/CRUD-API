import pytest
from jose import jwt

from finalversion import schemas
from ..oauth2 import SECRET_KEY, ALGORITHM


def test_create_user(client):
    response = client.post("/users/", json={"email": "test@gmail.com",
                                            "password": "password123"})
    new_user = schemas.CreateUserResponse(**response.json())
    assert new_user.email == "test@gmail.com"
    assert response.status_code == 201


def test_login_user(client, create_dummy_user):
    response = client.post("/login", data={"username": create_dummy_user["email"],
                                           "password": create_dummy_user["password"]})
    login_result = schemas.Token(**response.json())
    payload = jwt.decode(login_result.access_token, SECRET_KEY, ALGORITHM)
    id = payload.get("user_id")
    assert id == create_dummy_user["id"]
    assert login_result.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "wrongpassword", 403),
    ("anurag@gmail.com", "wrongpassword", 403),
    ("anurag@gmail.com", 2121, 403),
    ("anurag", 2121, 403),
    (None, "password123", 422),
    ("anurag@gmail", None, 422),
    (None, None, 422),
])
def test_login_with_incorrect_credentials(client, create_dummy_user, email, password, status_code):
    response = client.post("/login", data={"username": email,
                                           "password": password})
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid Credentials!"
