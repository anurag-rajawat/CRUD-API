from pydantic import BaseModel


# To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the
# SQLAlchemy models, and the file schemas.py with the Pydantic models. These Pydantic models define more or less a
# "schema" (a valid data shape). So this will help us to avoid confusion while using both.
class CourseBase(BaseModel):
    name: str
    description: str | None = None


class ResponseBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UpdateResponseBase(ResponseBase):
    description: str

