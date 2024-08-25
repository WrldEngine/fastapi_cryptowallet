FROM python:3.11

RUN pip install poetry --no-cache-dir

WORKDIR /project

COPY . /project

RUN poetry install --no-dev --no-cache

EXPOSE 8000