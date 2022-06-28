from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
