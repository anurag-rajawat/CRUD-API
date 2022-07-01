import pytest
from fastapi.testclient import TestClient

from finalversion import models
from finalversion.main import app
from finalversion.oauth2 import create_access_token
from finalversion.tests.db_utils import engine, TestingSession
from finalversion.utils import get_db


@pytest.fixture
def dummy_db_session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def dummy_client(dummy_db_session):
    def override_get_db2():
        try:
            yield dummy_db_session
        finally:
            dummy_db_session.close()

    app.dependency_overrides[get_db] = override_get_db2
    yield TestClient(app)


@pytest.fixture
def first_dummy_user(dummy_client):
    user_data = {"email": "anurag@gmail.com",
                 "password": "password123"}
    response = dummy_client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def second_dummy_user(dummy_client):
    user_data = {"email": "dummyuser@gmail.com",
                 "password": "password123"}
    response = dummy_client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def dummy_token(first_dummy_user):
    return create_access_token({"user_id": first_dummy_user["id"]})


@pytest.fixture
def dummy_authorized_client(dummy_client, dummy_token):
    dummy_client.headers = {
        **dummy_client.headers,
        "Authorization": f"Bearer {dummy_token}"
    }
    return dummy_client


@pytest.fixture
def dummy_courses(first_dummy_user, second_dummy_user, dummy_db_session):
    courses_data = [
        {
            "name": "Introduction to Database",
            "description": "This course is designed by keeping beginners in mind",
            "user_id": first_dummy_user["id"]},
        {
            "name": "Introduction to DB-Design",
            "description": "This is an intermediate course for this you've a good understanding of databases",
            "user_id": first_dummy_user["id"]},
        {
            "name": "Introduction to Flask",
            "description": "Introductory Flask course",
            "user_id": first_dummy_user["id"]},
        {
            "name": "Personal Growth courses",
            "description": "If you want to become something then start working on yourself.",
            "user_id": second_dummy_user["id"]
        }
    ]

    courses = list(map(lambda course: models.Course(**course), courses_data))
    dummy_db_session.add_all(courses)
    dummy_db_session.commit()
    courses = dummy_db_session.query(models.Course).all()
    return courses
