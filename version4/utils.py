from .database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    hashed_passwd = pwd_context.hash(password)
    return hashed_passwd


def verify(raw_passwd, hashed_passwd):
    return pwd_context.verify(raw_passwd, hashed_passwd)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
