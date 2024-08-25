.PHONY: migration
migration:
	alembic revision \
	  --autogenerate \
	  --message $(message)

.PHONY: migrate
migrate:
	alembic upgrade head