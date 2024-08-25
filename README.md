# Cryptowallet

## Установка и развертка
- __Через основную машину(желательно дистр Linux)__
  - Замените `.env.example` на `.env` и настройте
  - `pip3 install poetry` - установка поетри, нужна 3.11 версия питона
  - `poetry install`
  - `poetry shell`
  - `python -m app.main`

- __Через Docker__
  - `docker-compose build`
  - `docker-compose up -d`

## Документация
Переходите по ссылке запущенного сервера на директорию `/docs` (ex. `http://127.0.0.1:8000/docs`)

## Миграции с Базой Данных
* __Через Linux__
  - `make migration message=WHAT_MIGRATION_DOES` - Создание версии миграции
  - `make migrate` - Сама миграция

* __Через Windows__
  - `alembic revision --autogenerate --message=WHAT_MIGRATION_DOES` - Создание версии миграции
  - `alembic upgrade head` - Сама миграция

## Тестирование
`pytest tests`

## Deployment via Uvicorn
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Used Technologies
<div>
  <img src="https://img.shields.io/badge/fastapi-black?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/redis-black?style=for-the-badge&logo=redis"/>
  <img src="https://img.shields.io/badge/celery-black?style=for-the-badge&logo=celery">
  <img src="https://img.shields.io/badge/postgresql-black?style=for-the-badge&logo=postgresql"/>
  <img src="https://img.shields.io/badge/openapi-yellow?style=for-the-badge&logo=openapi"/>
  <img src="https://img.shields.io/badge/sqlalchemy-black?style=for-the-badge&logo=sqlalchemy"/>
  <img src="https://img.shields.io/badge/pytest-black?style=for-the-badge&logo=pytest"/>
</div>
