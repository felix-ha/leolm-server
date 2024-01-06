.PHONY: build
build:
	nvidia-docker compose build transformers-playground-server

.PHONY: run
run:
	docker compose up -d transformers-playground-server

.PHONY: stop
stop:
	docker compose down

.PHONY: docker_build
docker_build:
	docker build . -t transformers-playground -f Dockerfile.streamlit
