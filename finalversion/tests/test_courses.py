import pytest

from finalversion import schemas


def test_get_all_courses(authorized_client, create_dummy_courses):
    response = authorized_client.get("/courses/")
    assert response.status_code == 200
    assert len(response.json()) == len(create_dummy_courses)


def test_get_course_by_id(client, create_dummy_courses):
    response = client.get(f"/courses/{create_dummy_courses[0].id}")
    assert response.json().get("Course").get("id") == create_dummy_courses[0].id
    assert response.json().get("Course").get("user_id") == create_dummy_courses[0].user_id
    assert response.json().get("Course").get("name") == create_dummy_courses[0].name
    assert response.json().get("Course").get("description") == create_dummy_courses[0].description
    assert response.status_code == 200


def test_unauthorized_user_create_courses_should_fail(client, create_dummy_courses):
    response = client.post("/courses/")
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"


@pytest.mark.parametrize("name, description", [
    ("First Course", "Description of first course"),
    ("Second course", "Description of second course"),
    ("Missing course", "Missing description"),
    ("Missing semester", "Description of missing semester course"),
    ("First Course", "Description of first course"),
])
def test_authorized_user_create_courses_should_pass(authorized_client, name, description):
    response = authorized_client.post("/courses/", json={
        "name": name
    })
    courses = schemas.ResponseBase(**response.json())
    assert response.status_code == 201
    assert courses.name == name
    assert response.json().get("owner").get("id") == courses.owner.id
    assert response.json().get("id") == courses.id


def test_unauthorized_user_delete_course_should_fail(client, create_dummy_courses, create_dummy_user):
    response = client.delete(f"/courses/{create_dummy_courses[0].id}")
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"
    response = client.get("/courses/")
    assert response.status_code == 200
    assert len(response.json()) == len(create_dummy_courses)


def test_authorized_user_delete_course_should_pass(authorized_client, create_dummy_courses, create_dummy_user):
    response = authorized_client.delete(f"/courses/{create_dummy_courses[0].id}")
    assert response.status_code == 204


def test_authorized_user_delete_course_doesnt_exist_should_fail(authorized_client, create_dummy_courses,
                                                                create_dummy_user):
    response = authorized_client.delete("/courses/1000000")
    assert response.status_code == 404
    assert response.json().get("detail") == f"Course with id '{1000000}' doesn't exist!"


def test_authorized_user_delete_someone_course_should_fail(authorized_client, create_dummy_courses):
    response = authorized_client.delete(f"/courses/{create_dummy_courses[3].id}")
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform requested action"


def test_authorized_user_update_course_should_pass(authorized_client, create_dummy_courses):
    course = {"name": "Introduction to Database design",
              "description": "This is an intermediate database design course",
              "id": create_dummy_courses[1].id}
    response = authorized_client.put(f"/courses/{create_dummy_courses[1].id}",
                                     json=course)
    updated_course = schemas.UpdateResponseBase(**response.json())
    assert response.status_code == 200
    assert response.json().get("id") == updated_course.id
    assert response.json().get("user_id") == updated_course.user_id
    assert response.json().get("name") == updated_course.name
    assert response.json().get("description") == updated_course.description
    assert response.json().get("owner") == updated_course.owner


def test_authorized_user_update_another_user_course_should_fail(authorized_client, create_dummy_courses):
    course = {"name": "Introduction to Database design",
              "description": "This is an intermediate database design course",
              "id": create_dummy_courses[3].id}
    response = authorized_client.put(f"/courses/{create_dummy_courses[3].id}",
                                     json=course)
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform requested action"


def test_authorized_user_update_course_doesnt_exist_should_fail(authorized_client, create_dummy_user,
                                                                create_dummy_courses):
    course = {
        "name": "Introduction to Database design",
        "description": "This is an intermediate database design course",
        "id": create_dummy_courses[3].id
    }
    response = authorized_client.put("/courses/1000000", json=course)
    assert response.status_code == 404
    assert response.json().get("detail") == f"Course with id '{1000000}' doesn't exist!"


def test_unauthorized_user_update_another_user_course_should_fail(client, create_dummy_courses):
    course = {"name": "Introduction to Database design",
              "description": "This is an intermediate database design course",
              "id": create_dummy_courses[3].id}
    response = client.put(f"/courses/{create_dummy_courses[3].id}",
                          json=course)
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"
