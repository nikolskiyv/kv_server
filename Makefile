.PHONY: build
build:
	docker-compose -f docker-compose.yml build

.PHONY: run
run_all_docker:
	docker-compose -f docker-compose.yml build && \
	docker-compose -f docker-compose.yml up -d

.PHONY: lint
lint:
	flake8 src

.PHONY: test
test:
	docker-compose -f docker-compose.yml up --build --exit-code-from tests

