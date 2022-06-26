from typing import Optional

from pydantic import BaseModel


class Course(BaseModel):
    name: str
    description: str
    length: Optional[str] = None
    is_published: Optional[bool] = False
