from typing import List

from fastapi import FastAPI, Response, Depends, status, HTTPException
from . import models, schemas
from .database import engine
from sqlalchemy.orm import Session

from .utils import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def greet():
    return "Welcome to Giganoto!"


@app.get("/courses", status_code=status.HTTP_200_OK, response_model=List[schemas.ResponseBase])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@app.get("/courses/{id}", status_code=status.HTTP_200_OK)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id '{id}' doesn't exist!")
    return course


@app.post("/courses", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseBase)
def add_course(course: schemas.CourseBase, db: Session = Depends(get_db)):
    new_course = models.Course(name=course.name, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.delete("/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id '{id}' doesn't exist!")
    course.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/courses/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UpdateResponseBase)
def update_course(id: int, course: schemas.CourseBase, db: Session = Depends(get_db)):
    query = db.query(models.Course).filter(models.Course.id == id)
    updated_course = query.first()
    if updated_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id '{id}' doesn't exist!")
    query.update(course.dict(), synchronize_session=False)
    db.commit()
    return updated_course
