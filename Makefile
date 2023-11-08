.PHONY: build
build:
	nvidia-docker compose build python-server

.PHONY: run
run:
	docker compose up -d python-server

.PHONY: stop
stop:
	docker compose down
	