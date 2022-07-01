import pytest
from fastapi.testclient import TestClient

from finalversion import models
from finalversion.main import app
from finalversion.oauth2 import create_access_token
from finalversion.tests.db_utils import engine, TestingSession
from finalversion.utils import get_db


@pytest.fixture
def db_session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db2():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db2
    yield TestClient(app)


@pytest.fixture
def create_dummy_user(client):
    user_data = {"email": "anurag@gmail.com",
                 "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def create_second_dummy_user(client):
    user_data = {"email": "dummyuser@gmail.com",
                 "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(create_dummy_user):
    return create_access_token({"user_id": create_dummy_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def create_dummy_courses(create_dummy_user, create_second_dummy_user, db_session):
    courses_data = [
        {
            "name": "Introduction to Database",
            "description": "This course is designed by keeping beginners in mind",
            "user_id": create_dummy_user["id"]},
        {
            "name": "Introduction to DB-Design",
            "description": "This is an intermediate course for this you've a good understanding of databases",
            "user_id": create_dummy_user["id"]},
        {
            "name": "Introduction to Flask",
            "description": "Introductory Flask course",
            "user_id": create_dummy_user["id"]},
        {
            "name": "Personal Growth courses",
            "description": "If you want to become something then start working on yourself.",
            "user_id": create_second_dummy_user["id"]
        }
    ]

    courses = list(map(lambda course: models.Course(**course), courses_data))
    db_session.add_all(courses)
    db_session.commit()
    courses = db_session.query(models.Course).all()
    return courses
