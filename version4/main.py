from fastapi import FastAPI, status

from . import models
from .database import engine
from .routers import user, course, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/", status_code=status.HTTP_200_OK)
def greet():
    return "Welcome to Giganoto!"
