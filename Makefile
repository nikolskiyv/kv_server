.PHONY: build run lint test

build:
	docker-compose build

run:
	docker-compose build && docker-compose up -d

lint:
	flake8 src

test:
	docker-compose up --build tests

