MANAGE = python3 manage.py


run:
	$(MANAGE) runserver

new-migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

lint:
	flake8 .
