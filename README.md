<h1 align="center"> Проект: приложение для Благотворительного фонда 
поддержки котиков QRKot </h1>

___
<h4>Автор:</h4>

**Сластухин Александр** - студент Яндекс.Практикума Когорта 17+
https://github.com/last-ui

<h2>Краткое описание проекта</h2>

Фонд собирает пожертвования на различные целевые проекты: на медицинское 
обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в 
подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные
с поддержкой кошачьей популяции.

<h2>Подготовка проекта к запуску</h2>
- Установить и активировать виртуальное окружение

```
python3 -m venv venv
```
* Если у вас Linux/macOS
    ```
    source venv/bin/activate
    ```
* Если у вас windows
    ```
    source venv/scripts/activate
    ```
- Установить зависимости из файла requirements.txt
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
- Заполнить .env-файл в корневой парке проекта, вариант заполнения указан в файле
example.env.

<h2>Запуск проекта</h2>

**1. Выполнить не примененные миграции командой:**
```shell
alembic upgrade head
```

**2. Выполнить команду запуска приложения:**
```shell
uvicorn app.main:app
```

<h2>Примеры запросов</h2>
- POST-запрос регистрации пользователя:
```
localhost:8000/donation/
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "string" 
}
```
- Пример ответа от сервера:
```
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

- POST-запрос на создание пожертвования:
```
localhost:8000/donation/
Content-Type: application/json
{
  "full_amount": 10,
  "comment": "string"
}
```
- Пример ответа от сервера:
```
{
  "full_amount": 10,
  "comment": "string",
  "id": 0,
  "create_date": "2022-08-10T05:51:20.143Z"
}
```
-  GET-запрос на получение списка своих пожертвований:
```
localhost:8000/donation/my
```

- Пример ответа от сервера:
```
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2022-08-10T06:00:07.584Z"
  }
]
```

<h2>Техническая документация</h2>

Доступ к документации Swagger, c описанием эндпоинтов, примерами запросов и 
образцами ответов по ссылке:

http://localhost/docs


<h2>Используемые технологии</h2>

- [Python 3.10](https://www.python.org/downloads/release/python-3100/)
- [FastAPI 0.78](https://fastapi.tiangolo.com/release-notes/#0780)
- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/)
- [Alembic 1.7](https://docs.pydantic.dev/latest/changelog/#highlights_2)
