# restful-api-django

A RESTful API server included...

1. Framework: Django
2. OpenAPI: Swagger
3. Database: MongoDB
4. ORM: MongoEngine
5. Test: Pytest

## Usage

### Start

```shell
python manage.py runserver
```

[Swagger](https://localhost:8000/swagger)

### Test

```shell
python manage.py test
```

### Coverage

```shell
coverage run --source='.' manage.py test
coverage report
```
