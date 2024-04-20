# restful-api-django &middot; ![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)

A RESTful API server includes

* Framework: Django
* OpenAPI: Swagger
* Database: MongoDB
* ORM: MongoEngine
* Test: Pytest
* Environment: Docker
* Deployment: Docker Compose

## Usage

### Build Database

```shell
docker-compose up -d mongo mongo-express
```

[Mongo Express](http://localhost:8081)

* username: root
* password: pass

### Develop

```shell
python manage.py runserver
```

[Swagger](http://localhost:8000/swagger)

### Test

```shell
python manage.py test
```

### Coverage

```shell
coverage run --source='.' manage.py test
coverage report -m
```

### Deploy

```shell
docker build . -t restful-api-django
docker-compose up -d
```
