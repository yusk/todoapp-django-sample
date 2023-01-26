# README

## env

* python 3.8.x
  * poetry

### all

```bash
cp .env.sample .env
poetry run poetry install
poetry run python manage.py migrate
```

## run

```bash
poetry run python manage.py runserver
```

## create user

```bash
poetry run python manage.py createsuperuser
```

## check api schema

```bash
# after run server
open localhost:8000/schema/ # need session login
```

## httpie

```bash
http post http://localhost:8000/api/register/dummy/
http post http://localhost:8000/api/auth/user/ email=test@test.com password=testuser

http post http://localhost:8000/api/auth/refresh/ token=$TOKEN
http post http://localhost:8000/api/auth/verify/ token=$TOKEN

http http://localhost:8000/api/user/ Authorization:"JWT $TOKEN"
```
