![Build](https://github.com/anurag-rajawat/CRUD-API/actions/workflows/workflow.yaml/badge.svg)

## About

Simple **CRUD API** which persists data in the Postgres database.

### Objective

* Learn about API, build projects.
* Enhance Python skills and learnings by building project.

### [Version1](https://github.com/anurag-rajawat/CRUD-API/tree/master/version1)

* This is a very basic CRUD API which didn't persist data in the database.

### [Version2](https://github.com/anurag-rajawat/CRUD-API/tree/master/version2)

* In this version, the API persists data in the Postgres database.
* It doesn't support user registration and authentication to perform operations.

### [Version3](https://github.com/anurag-rajawat/CRUD-API/tree/master/version3)

* It supports user registration and authentication.
* It requires authentication to perform certain operations (create, update & delete).

### [Final Version](https://github.com/anurag-rajawat/CRUD-API/tree/master/finalversion)

* The API persists data in the Postgres database.
* It uses [OAuth2](oauth.net/2/) for authorization.
* It supports user registration and authorization.
* It Uses a Bearer token for authentication.
* It supports rating like, dislike and like a specific course by a user.
* It requires authentication to perform certain operations (create, update, delete & rate a course).

## Getting started

### Clone repository

```shell
$ git@github.com:/anurag-rajawat/CRUD-API.git
```

## Docker-based development environment

### Prerequisites

* **[Docker](https://docs.docker.com/get-docker/)** install the latest stable version and add it to the PATH.

* **[Docker Compose](https://docs.docker.com/compose/install/)** install the latest stable version and add it to the
  PATH.

* A `.env` file in the root directory containing the following entries, you can override these values if you want.

```text
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_PASSWORD=postgres
DATABASE_NAME=postgres
DATABASE_USERNAME=postgres
SECRET_KEY=5e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### After cloning repository, start application

```shell
$ docker compose -f docker-compose.yaml up -d
```

### Head over to http://localhost:8000/docs

## Local Virtual Environment

## Prerequisites

* A `.env` file in the root directory, with the same entries as in docker environment.
* **[Postgres DB](https://www.postgresql.org/download/)** install the latest stable version and create a database with
  name `DATABASE_NAME` of `.env` file.

### Create a virtual environment.

```shell
$ python3.10 -m venv venv 
```

### Install the required dependencies

```shell
$ pip install -r requirements.txt
```

### Start the application

```shell
$ uvicorn finalversion.main:app --host=0.0.0.0 --port=8000
```

### Head over to http://localhost:8000/docs

## Request & Response Examples

#### User Endpoints

- [POST /users/](#create-a-new-user-users)
- [POST /users/](#login-login)
- [GET /users/[id]](#get-a-user-users3)

#### Course Endpoints

- [GET /](#get-)
- [GET /courses/](#get-courses)
- [GET /courses/[id]](#get-courses4)
- [GET /courses/?[limit]](#get-courseslimit2)
- [GET /courses/?[limit]&[skip]](#get-courseslimit3skip3)
- [GET /courses/?[search]](#get-coursessearchto20flask)
- [POST /courses/](#post-courses)
- [PUT /courses/5](#update-course-course5)
- [DELETE /courses/5](#delete-course-course5)

#### Rating Endpoints

`1` for like and `0` for dislike

- [POST /ratings/](#like-a-course-ratings)
- [POST /ratings/](#removing-like-from--a-course-ratings)

### Create a new user `/users/`

Request body:

    {
        "email": "testuser@gmail.com",
        "password": "password123"
    }

Response body:

    {
        "id": 3,
        "email": "testuser@gmail.com"
    }

### Get a user `/users/3`

Response body:

    {
        "id": 3,
        "email": "testuser@gmail.com"
    }

### Login `/login`

Request body:

```text
        username = anurag@gmail.com
        password = password123
```

Response body:

    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NTY3NTQyOTF9.3s12tcfuSwHpPMiwLaHzBPctrR85rSyLWt-GFtTT55c",
        "token_type": "bearer"
    }

### Get `/`

Response body:

    {
        "Welcome to Giganoto!"
    }

### GET `/courses`

Response body:

    {
        [
            {
                "Course": {
                    "name": "Introduction to Go language",
                    "description": "This is an intermediate Go course",
                    "user_id": 2,
                    "id": 4,
                    "uploaded_at": "2022-06-29T12:24:14.039478+05:30"
                },
                "Ratings": 0
            },
            {
                "Course": {
                    "name": "Introduction to Database",
                    "description": "This is a beginner friendly Database course",
                    "user_id": 1,
                    "id": 2,
                    "uploaded_at": "2022-06-29T12:23:17.506769+05:30"
                },
                "Ratings": 2
            },
            {
                "Course": {
                    "name": "Introduction to Python",
                    "description": "This is a beginner friendly Python course",
                    "user_id": 1,
                    "id": 3,
                    "uploaded_at": "2022-06-29T12:23:34.392123+05:30"
                },
                "Ratings": 0
            },
            {
                "Course": {
                    "name": "Introduction to flask",
                    "description": "This is a beginner flask course",
                    "user_id": 1,
                    "id": 1,
                    "uploaded_at": "2022-06-29T11:41:23.035566+05:30"
                },
                "Ratings": 2
            }
        ]
    }

### GET `/courses/4`

Response body:

    {
        "Course": {
            "name": "Introduction to Go language",
            "description": "This is an intermediate Go course",
            "user_id": 2,
            "id": 4,
            "uploaded_at": "2022-06-29T12:24:14.039478+05:30"
        },
        "Ratings": 0
    }

### GET `/courses/?limit=2`

Response body:

    {
        {
            "Course": {
                "name": "Introduction to flask",
                "description": "This is a beginner flask course",
                "user_id": 1,
                "id": 1,
                "uploaded_at": "2022-06-29T11:41:23.035566+05:30"
            },
            "Ratings": 2
        },
        {
            "Course": {
                "name": "Introduction to Database",
                "description": "This is a beginner friendly Dataabase course",
                "user_id": 1,
                "id": 2,
                "uploaded_at": "2022-06-29T12:23:17.506769+05:30"
            },
            "Ratings": 2
        }
    }

### GET `/courses/?limit=3&skip=3`

Response body:

    {
        "Course": {
            "name": "Introduction to flask",
            "description": "This is a beginner flask course",
            "user_id": 1,
            "id": 1,
            "uploaded_at": "2022-06-29T11:41:23.035566+05:30"
        },
        "Ratings": 2
    }

### GET `/courses/?search=to%20flask`

Response body:

    {
        "Course": {
            "name": "Introduction to flask",
            "description": "This is a beginner flask course",
            "user_id": 1,
            "id": 1,
            "uploaded_at": "2022-06-29T11:41:23.035566+05:30"
        },
        "Ratings": 2
    }

### POST `/courses/`

**You need to log in to perform this action**

Request body:

    {
        "name": "Database Design",
        "description": "This is an intermediate database design course"
    }

Response body:

    {
        "id": 5,
        "name": "Database Design",
        "user_id": 1,
        "owner": {
            "id": 1,
            "email": "anurag@gmail.com"
        }
    }

### Update Course `/course/5`

**You need to log in to perform this action**

Request body:

    {
        "name": "Introduction to Database Designing.",
        "description": "This is an intermediate database design course."
    }

Response body:

    {
        "id": 5,
        "name": "Introduction to Database Designing.",
        "user_id": 1,
        "owner": {
            "id": 1,
            "email": "anurag@gmail.com"
        },
        "description": "This is an intermediate database design course."
    }

### Delete Course `/course/5`

**You need to log in to perform this action**

### Like a course `/ratings/`

Request body:

    {
        "course_id": 1,
        "choice" : 1
    }

Response body:

    {
        "Successfully rated the course!"
    }

### Removing like from  a course `/ratings/`

Request body:

    {
        "course_id": 1,
        "choice" : 0
    }

Response body:

    {
        "Successfully removed the rating"
    }