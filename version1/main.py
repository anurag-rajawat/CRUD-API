from fastapi import FastAPI, HTTPException, Response
from starlette import status
from starlette.status import HTTP_204_NO_CONTENT

from .schema import Course
from .utils import courses, find_course, ID, find_course_idx

app = FastAPI()


@app.get("/")
def greet():
    return "Welcome to Giganoto!"


@app.get("/courses", status_code=status.HTTP_200_OK)
def get_courses():
    return {"Courses": courses}


@app.get("/courses/{id}", status_code=status.HTTP_200_OK)
def get_course(id: int):
    course = find_course(id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {id} not found")
    return {"Course": course}


@app.post("/courses", status_code=status.HTTP_201_CREATED)
def add_course(course: Course):
    # Save the course to DB
    # Do something to save it
    global ID
    course_dict = course.dict()
    course_dict['id'] = ID
    ID += 1
    courses.append(course_dict)
    return {"Successfully added the course": f"Course ID is {course_dict['id']} and name is {course_dict['name']}"}


@app.delete("/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int):
    # Authenticate user before doing so in next version
    idx = find_course_idx(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {id} not found")
    courses.pop(idx)
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.put("/courses/{id}", status_code=status.HTTP_200_OK)
def update_course(id: int, course: Course):
    idx = find_course_idx(id)
    print(idx)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {id} not found")
    course_dict = course.dict()
    course_dict['id'] = id
    courses[idx] = course_dict
    return {"Successfully updated the course details": course_dict}
