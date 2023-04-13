build:
	docker-compose build

run:
	docker-compose up -d

# Остановка Docker-контейнера
stop:
	docker stop $(docker ps -q --filter ancestor=myapp)

# Запуск линтера Flake8
lint:
	flake8 .

# Запуск тестов
test:
	pytest -v tests/
