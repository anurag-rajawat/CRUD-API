from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, course, auth, rating

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# If this api is configured for a specific webapp than narrow down the origins
# If it is public api then leave it
# origin = ["https://www.google.com"]
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
