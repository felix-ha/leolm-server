.PHONY: build
build:
	nvidia-docker compose build python-server

.PHONY: run
run:
	docker compose up -d python-server

.PHONY: stop
stop:
	docker compose down

.PHONY generate_settings
generate_settings:
	datamodel-codegen --input config.yaml --input-file-type yaml --output model_config.py
	