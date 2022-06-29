from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models, oauth2
from ..utils import get_db

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def rate_course(rating: schemas.RateCourseBase, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == rating.course_id).first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id '{rating.course_id}' doesn't exist")

    rating_query = db.query(models.Rating).filter(models.Rating.course_id == rating.course_id,
                                                  models.Rating.user_id == current_user.id)
    found_rating = rating_query.first()
    if rating.choice == 1:
        if found_rating:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User with id {current_user.id} has already rated the course with id {rating.course_id}")
        new_rating = models.Rating(course_id=rating.course_id, user_id=current_user.id)
        db.add(new_rating)
        db.commit()
        return "Successfully rated the course!"
    else:
        if not found_rating:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You haven't rated the course yet!")
        rating_query.delete(synchronize_session=False)
        db.commit()
        return "Successfully removed the rating"
