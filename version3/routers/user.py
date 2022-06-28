from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..utils import hash_password, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CreateUserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' doesn't exist!")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserResponse)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user
