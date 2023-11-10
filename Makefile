.PHONY: build
build:
	nvidia-docker compose build transformers-playground-server

.PHONY: run
run:
	docker compose up -d transformers-playground-server

.PHONY: stop
stop:
	docker compose down
