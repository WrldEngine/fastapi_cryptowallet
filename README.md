# Cryptowallet (暗号ウォレット)

## 著者: カムランプラトフ【Kamran　Pulatov】

## インストールとセットアップ
- __メインマシン（Linuxディストリビューションが推奨）から__
  - `.env.example` を `.env` に名前変更し、設定します。
  - `pip3 install poetry` - Poetry をインストールします。Python 3.11 バージョンが必要です。
  - `poetry install`
  - `poetry shell`
  - `python -m app.main`

- __Docker 経由で__
  - `docker-compose build`
  - `docker-compose up -d`

## ドキュメント
起動したサーバーの `/docs` ディレクトリにアクセスしてください（例: `http://127.0.0.1:8000/docs`）

## データベースマイグレーション
* __Linux 経由で__
  - `make migration message=WHAT_MIGRATION_DOES` - マイグレーションのバージョンを作成します。
  - `make migrate` - 実際のマイグレーションを実行します。

* __Windows 経由で__
  - `alembic revision --autogenerate --message=WHAT_MIGRATION_DOES` - マイグレーションのバージョンを作成します。
  - `alembic upgrade head` - 実際のマイグレーションを実行します。

## テスト
`pytest tests`

## Uvicorn 経由でのデプロイメント
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 使用技術
<div>
  <img src="https://img.shields.io/badge/fastapi-black?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/redis-black?style=for-the-badge&logo=redis"/>
  <img src="https://img.shields.io/badge/celery-black?style=for-the-badge&logo=celery">
  <img src="https://img.shields.io/badge/postgresql-black?style=for-the-badge&logo=postgresql"/>
  <img src="https://img.shields.io/badge/openapi-yellow?style=for-the-badge&logo=openapi"/>
  <img src="https://img.shields.io/badge/sqlalchemy-black?style=for-the-badge&logo=sqlalchemy"/>
  <img src="https://img.shields.io/badge/pytest-black?style=for-the-badge&logo=pytest"/>
</div>
