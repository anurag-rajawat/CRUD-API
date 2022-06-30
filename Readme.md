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
* It supports user registration and authentication.
* It requires authentication to perform certain operations (create, update & delete).
* It supports rating like, dislike and like a specific course by a user.

## Getting started

### Clone repository
```shell
$ git@github.com:/anurag-rajawat/CRUD-API.git
```
## Prerequisites
* **[Docker](https://docs.docker.com/get-docker/)** install the latest stable version and add it to the PATH.
 
* **[Docker Compose](https://docs.docker.com/compose/install/)** install the latest stable version and add it to the PATH.

* A `.env` file in the root directory containing the following entries, you can override these values if you want.
```text
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_PASSWORD=postgres
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=5e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Docker-based development environment

### After cloning repository, start application
```shell
$ docker compose -f docker-compose.yaml up -d
```

### Head over to http://localhost:8000/docs

## Local Virtual Environment (virtualenv)
* Create a virtual environment
```shell
$ python3.10 -m venv venv 
```

* Install the required dependencies
```shell
$ pip install -r requirements.txt
```

* Start the application
```shell
$ uvicorn finalversion.main:app --host=0.0.0.0 --port=8000
```

### Head over to http://localhost:8000/docs
