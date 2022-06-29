from typing import Optional

from pydantic import BaseModel, EmailStr, conint


# To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the
# SQLAlchemy models, and the file schemas.py with the Pydantic models. These Pydantic models define more or less a
# "schema" (a valid data shape). So this will help us to avoid confusion while using both.
class CourseBase(BaseModel):
    name: str
    description: str | None = None


class UserBase(BaseModel):
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLoginBase(UserBase):
    pass


class ResponseBase(BaseModel):
    id: int
    name: str
    user_id: int
    owner: CreateUserResponse

    class Config:
        orm_mode = True


class UpdateResponseBase(ResponseBase):
    description: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


# 1 for like and less than it for dislike
class RateCourseBase(BaseModel):
    course_id: int
    choice: conint(le=1)
