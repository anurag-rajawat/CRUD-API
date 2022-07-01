import pytest

from finalversion import schemas


def test_get_all_courses(dummy_authorized_client, dummy_courses):
    response = dummy_authorized_client.get("/courses/")
    assert response.status_code == 200
    assert len(response.json()) == len(dummy_courses)


def test_get_course_by_id(dummy_client, dummy_courses):
    response = dummy_client.get(f"/courses/{dummy_courses[0].id}")
    assert response.json().get("Course").get("id") == dummy_courses[0].id
    assert response.json().get("Course").get("user_id") == dummy_courses[0].user_id
    assert response.json().get("Course").get("name") == dummy_courses[0].name
    assert response.json().get("Course").get("description") == dummy_courses[0].description
    assert response.status_code == 200


def test_unauthorized_user_create_courses_should_fail(dummy_client, dummy_courses):
    response = dummy_client.post("/courses/")
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"


@pytest.mark.parametrize("name, description", [
    ("First Course", "Description of first course"),
    ("Second course", "Description of second course"),
    ("Missing course", "Missing description"),
    ("Missing semester", "Description of missing semester course"),
    ("First Course", "Description of first course"),
])
def test_authorized_user_create_courses_should_pass(dummy_authorized_client, name, description):
    response = dummy_authorized_client.post("/courses/", json={
        "name": name
    })
    courses = schemas.ResponseBase(**response.json())
    assert response.status_code == 201
    assert courses.name == name
    assert response.json().get("owner").get("id") == courses.owner.id
    assert response.json().get("id") == courses.id


def test_unauthorized_user_delete_course_should_fail(dummy_client, dummy_courses, first_dummy_user):
    response = dummy_client.delete(f"/courses/{dummy_courses[0].id}")
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"
    response = dummy_client.get("/courses/")
    assert response.status_code == 200
    assert len(response.json()) == len(dummy_courses)


def test_authorized_user_delete_course_should_pass(dummy_authorized_client, dummy_courses, first_dummy_user):
    response = dummy_authorized_client.delete(f"/courses/{dummy_courses[0].id}")
    assert response.status_code == 204


def test_authorized_user_delete_course_doesnt_exist_should_fail(dummy_authorized_client, dummy_courses,
                                                                first_dummy_user):
    response = dummy_authorized_client.delete("/courses/1000000")
    assert response.status_code == 404
    assert response.json().get("detail") == f"Course with id '{1000000}' doesn't exist!"


def test_authorized_user_delete_someone_course_should_fail(dummy_authorized_client, dummy_courses):
    response = dummy_authorized_client.delete(f"/courses/{dummy_courses[3].id}")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform requested action"


def test_authorized_user_update_course_should_pass(dummy_authorized_client, dummy_courses):
    course = {"name": "Introduction to Database design",
              "description": "This is an intermediate database design course",
              "id": dummy_courses[1].id}
    response = dummy_authorized_client.put(f"/courses/{dummy_courses[1].id}",
                                           json=course)
    updated_course = schemas.UpdateResponseBase(**response.json())
    assert response.status_code == 200
    assert response.json().get("id") == updated_course.id
    assert response.json().get("user_id") == updated_course.user_id
    assert response.json().get("name") == updated_course.name
    assert response.json().get("description") == updated_course.description
    assert response.json().get("owner") == updated_course.owner


def test_authorized_user_update_another_user_course_should_fail(dummy_authorized_client, dummy_courses):
    course = {"name": "Introduction to Database design",
              "description": "This is an intermediate database design course",
              "id": dummy_courses[3].id}
    response = dummy_authorized_client.put(f"/courses/{dummy_courses[3].id}",
                                           json=course)
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform requested action"


def test_authorized_user_update_course_doesnt_exist_should_fail(dummy_authorized_client, first_dummy_user,
                                                                dummy_courses):
    course = {
        "name": "Introduction to Database design",
        "description": "This is an intermediate database design course",
        "id": dummy_courses[3].id
    }
    response = dummy_authorized_client.put("/courses/1000000", json=course)
    assert response.status_code == 404
    assert response.json().get("detail") == f"Course with id '{1000000}' doesn't exist!"


def test_unauthorized_user_update_another_user_course_should_fail(dummy_client, dummy_courses):
    course = {"name": "Introduction to Database design",
              "description": "This is an intermediate database design course",
              "id": dummy_courses[3].id}
    response = dummy_client.put(f"/courses/{dummy_courses[3].id}",
                                json=course)
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"
