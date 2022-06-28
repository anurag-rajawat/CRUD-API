from typing import List

from fastapi import Response, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..utils import get_db

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ResponseBase])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ResponseBase)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id '{id}' doesn't exist!")
    return course


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseBase)
def add_course(course: schemas.CourseBase, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    new_course = models.Course(user_id=current_user.id, name=course.name, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id '{id}' doesn't exist!")
    # Don't know why the current_user.id is string?
    if course.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UpdateResponseBase)
def update_course(id: int, course: schemas.CourseBase, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Course).filter(models.Course.id == id)
    updated_course = query.first()
    if updated_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id '{id}' doesn't exist!")
    if updated_course.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    query.update(course.dict(), synchronize_session=False)
    db.commit()
    return updated_course
