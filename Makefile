ARG := $(word 2, $(MAKECMDGOALS) )

clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete


build:
	docker build --tag geninfo .

up: down build
	docker-compose up -d
	docker-compose logs -f

down:
	docker-compose down

stop:
	docker-compose stop

logs:
	docker-compose logs -f

migrations:
	docker-compose exec web python manage.py makemigrations

missing_migrations:
	docker-compose exec web python manage.py makemigrations --check --dry-run


migrate:
	docker-compose exec web python manage.py migrate

prune:
	docker volume rm $(shell docker volume ls -qf dangling=true)
	docker build prune -f
	docker system prune -a

load:
	docker-compose exec web python3 manage.py loaddata geninfo/info/fixtures/services.json --app info.Service

user:
	docker-compose exec web python3 manage.py createsuperuser

shell:
	docker-compose exec web python3 manage.py shell

bash:
	docker-compose exec web /bin/bash

tox:
	docker-compose exec web tox .

test:
	docker-compose exec web python3 manage.py test $(ARG) --keepdb

lint:
	docker-compose exec web prospector

format:
	docker-compose exec web black geninfo

collect:
	docker-compose exec web python3 manage.py collectstatic