import pytest

from finalversion import models


@pytest.fixture
def dummy_like(dummy_db_session, dummy_courses, first_dummy_user):
    new_like = models.Rating(course_id=dummy_courses[1].id, user_id=first_dummy_user["id"])
    dummy_db_session.add(new_like)
    dummy_db_session.commit()


def test_like_course(dummy_authorized_client, dummy_courses):
    response = dummy_authorized_client.post("/ratings/", json={
        "course_id": dummy_courses[1].id,
        "choice": 1
    })
    assert response.status_code == 201
    assert response.json() == "Successfully rated the course!"


def test_like_course_twice_should_fail(dummy_authorized_client, dummy_courses, dummy_like):
    response = dummy_authorized_client.post("/ratings/", json={
        "course_id": dummy_courses[1].id,
        "choice": 1
    })
    assert response.status_code == 409


def test_unlike_like_course_should_pass(dummy_authorized_client, dummy_courses, dummy_like):
    response = dummy_authorized_client.post("/ratings/", json={
        "course_id": dummy_courses[1].id,
        "choice": 0
    })
    assert response.status_code == 201
    assert response.json() == "Successfully removed the rating"


def test_unlike_doesnt_exist_like_course_should_fail(dummy_authorized_client, dummy_courses):
    response = dummy_authorized_client.post("/ratings/", json={
        "course_id": dummy_courses[1].id,
        "choice": 0
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "You haven't rated the course yet!"


def test_like_course_doesnt_exist_should_fail(dummy_authorized_client, dummy_courses):
    response = dummy_authorized_client.post("/ratings/", json={
        "course_id": 1000000,
        "choice": 0
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Course with id '1000000' doesn't exist"


def test_unauthorized_user_like_course_should_fail(dummy_client, dummy_courses):
    response = dummy_client.post("/ratings/", json={
        "course_id": dummy_courses[1].id,
        "choice": 1
    })
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"
