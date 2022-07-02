from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .Config import Settings
from .database import engine
from .routers import user, course, auth, rating

settings = Settings()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(rating.router)


@app.get("/", status_code=status.HTTP_200_OK)
def greet():
    return "Welcome to Giganoto!"
