.PHONY: up down build restart logs migrate makemigrations shell createsuperuser collectstatic

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

restart:
	docker compose restart

logs:
	docker compose logs -f

logs-web:
	docker compose logs -f web

logs-celery:
	docker compose logs -f celery

logs-beat:
	docker compose logs -f celery-beat

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

createsuperuser:
	docker compose exec web python manage.py createsuperuser

shell:
	docker compose exec web python manage.py shell

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

setup:
	docker compose up -d --build
	docker compose exec web python manage.py migrate
	docker compose exec web python manage.py setup_periodic_tasks

ps:
	docker compose ps